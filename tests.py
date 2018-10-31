import unittest
from server import app
from model import connect_to_db, db, User
from seed import load_dummy_data
from flask import session
import server

class TestRoutes(unittest.TestCase):

    def setUp(self):
        """ 
        Set up before every test. 

        The Flask app has a test_client() method on it.
        It is a mini browswer that can make requests.
        """

        self.client = app.test_client()
        app.config['Testing'] = True

    def test_signup_flask_route(self):
        """ Test that signup displays signup page. """

        result = self.client.get('/signup')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Sign Up</h1>', result.data)

    def test_login_flask_route(self):
        """ Test that login displays login page. """

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Log In</h1>', result.data)

class TestHomepage(unittest.TestCase):
    def setUp(self):
        """ 
        Set up before every test. 

        The Flask app has a test_client() method on it.
        It is a mini browswer that can make requests.
        """

        self.client = app.test_client()
        app.config['Testing'] = True

        # Make mock
        def _get_random_quote():
            return {
                'media': 'http://healthruwords.com/wp-content/uploads/2016/09/Healthruwords.com_-_Inspirational_Images_-_Imagination-over-Knowledge-300x300.jpg',
                'author': 'Roxana Jones'
            }

        server.get_random_quote = _get_random_quote

    def test_hompage_flask_route(self):
        """ Test that homepage displays at root route. """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'You are not alone', result.data)
        self.assertIn(b'Author: Roxana Jones', result.data)
        self.assertIn(b'http://healtruwords.com', result.data)

class TestSignup(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_validate_signup_username_found(self):
        """ Test when new user attempts to signup with a username that is already taken. """

        username = 'DeniseCodes101'

        result = self.client.get(f'/validate_signup?username={username}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)

    def test_validate_signup_username_not_found(self):
        """ Test when a username attempts to signup with a new username. """

        username = 'fabiocodes'

        result = self.client.get(f'/validate_signup?username={username}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":false', result.data)

    def test_successful_signup(self):
        """ Test when a new user signs up with valid username and password. """

        email = 'bob@codes.com'
        username = 'BobCodes1'
        password1 = 'Python101'

        data = {'email': email,
                'username': username, 
                'password1': password1}

        result = self.client.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'You are not alone', result.data)
        self.assertIn(b'BobCodes1 successfully signed up.', result.data)

class TestLoginLogout(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_validate_login_valid_username_invalid_password(self):
        """ Test when user attempts to login and password does not match username. """

        username = 'DeniseCodes101'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)
        self.assertIn(b'"valid_login":false', result.data)

    def test_validate_login_valid_username_valid_password(self):
        """ Test when user attempts to login with valid username and password. """

        username = 'DeniseCodes101'
        password = 'Python101'

        data = {'username': username, 'password': password}

        result = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)
        self.assertIn(b'"valid_login":true', result.data)

    def test_validate_login_invalid_username(self):
        """ Test when user attempts to login with invalid username. """
        
        username = 'fabiocodes'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":false', result.data)
        self.assertIn(b'"valid_login":null', result.data)

    def test_successful_login(self):
        """ Test when a new user signs up successfully. """

        username = 'DeniseCodes101'
        password = 'Python101'

        data = {'username': username, 
                'password': password}

        with self.client as c:
            result = c.post('/login', data=data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(session['user_id'], 1)
            self.assertIn(b'"username_found":true', result.data)
            self.assertIn(b'"valid_login":true', result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b'DeniseCodes101 successfully logged out.', result.data)

class TestPrograms(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_programs_flask_route(self):
        """ Test that programs displays programs page. """

        result = self.client.get('/programs')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Programs', result.data)

    def test_facilities_search_fac_name_no_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Facilities 1, 2, and 3 start with a fac_name of 'fac_name_'."""

        search_type = 'fac_name'
        search_text = 'fac_name_'

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"fac_name":"fac_name_1"', result.data)
        self.assertIn(b'"fac_name":"fac_name_2"', result.data)
        self.assertIn(b'"fac_name":"fac_name_3"', result.data)
        self.assertNotIn(b'"favorite":1', result.data)
        self.assertIn(b'"favorite":0', result.data)

    def test_facilities_search_fac_name_yes_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Facilities 1, 2, and 3 start with a fac_name of 'fac_name_'."""

        search_type = 'fac_name'
        search_text = 'fac_name_'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"fac_name":"fac_name_1"', result.data)
        self.assertIn(b'"fac_name":"fac_name_2"', result.data)
        self.assertIn(b'"fac_name":"fac_name_3"', result.data)
        self.assertIn(b'"favorite":1', result.data)

    def test_facilities_search_city_no_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        All 3 facility cities in database start with 'City'. """

        search_type = 'city'
        search_text = 'City'

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"city":"CityOfAngels"', result.data)
        self.assertIn(b'"city":"CityOfDevils"', result.data)
        self.assertIn(b'"city":"CityOfWizards"', result.data)
        self.assertNotIn(b'"favorite":1', result.data)
        self.assertIn(b'"favorite":0', result.data)

    def test_facilities_search_city_yes_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        All 3 facility cities in database start with 'City'. """

        search_type = 'city'
        search_text = 'City'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"city":"CityOfAngels"', result.data)
        self.assertIn(b'"city":"CityOfDevils"', result.data)
        self.assertIn(b'"city":"CityOfWizards"', result.data)
        self.assertIn(b'"favorite":1', result.data)

    def test_facilities_search_state_no_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. """

        search_type = 'state'
        search_text = 'CA'

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"state":"CA"', result.data)
        self.assertNotIn(b'"favorite":1', result.data)
        self.assertIn(b'"favorite":0', result.data)

    def test_facilities_search_state_yes_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. """

        search_type = 'state'
        search_text = 'CA'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"state":"CA"', result.data)
        self.assertIn(b'"favorite":1', result.data)

    def test_facilities_search_zipcode_no_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Only program 1 has a zipcode of 10000."""

        search_type = 'zipcode'
        search_text = '10000'

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"zipcode":"10000"', result.data)
        self.assertNotIn(b'"favorite":1', result.data)
        self.assertIn(b'"favorite":0', result.data)

    def test_facilities_search_zipcode_yes_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Only program 1 has a zipcode of 10000."""

        search_type = 'zipcode'
        search_text = '10000'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"zipcode":"10000"', result.data)
        self.assertIn(b'"favorite":1', result.data)


    def test_facilities_search_nothing_no_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Test searching for not allowed type."""

        search_type = 'color'
        search_text = 'red'

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'[]', result.data)

    def test_facilities_search_nothing_yes_user_logged_in(self):
        """ Test that programs.json route returns facilities desired in JSON format. 

        Test searching for not allowed type."""

        search_type = 'color'
        search_text = 'red'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get(f'/programs.json?search_type={search_type}&search_text={search_text}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'[]', result.data)

    def test_get_programs_by_facility(self):
        """ Test that programs_by_facility.json route returns programs desired in JSON format. 

        fac_id of 2 has 2 programs 2 and 3 associated it."""

        fac_id = 2

        result = self.client.get(f'/programs_by_facility.json?fac_id={fac_id}')
        self.assertEqual(result.status_code, 200)
        self.assertNotIn(b'"program_id":1', result.data)
        self.assertIn(b'"program_id":2', result.data)
        self.assertIn(b'"program_id":3', result.data)

    def test_toggle_facility_to_favorite_user_logged_in(self):
        """ Test that logged in user can favorite a facility. 

        User 2's favorite facilities are 2 and 3.
        Let's test user 2 favoriting facility 1."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        fac_id = 1

        result = self.client.get(f'/toggle_favorite_facility?fac_id={fac_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":true', result.data)

    def test_toggle_facility_to_unfavorite_user_logged_in(self):
        """ Test that logged in user can unfavorite a facility. 

        User 2's favorite facilities are 2 and 3.
        Let's test user 2 unfavoriting facility 2."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        fac_id = 2

        result = self.client.get(f'/toggle_favorite_facility?fac_id={fac_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":false', result.data)

    def test_toggle_facility_user_not_logged_in(self):
        """ Test that user not logged in attempts to toggle favoriting program. """

        fac_id = 1

        result = self.client.get(f'/toggle_favorite_facility?fac_id={fac_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":false', result.data)
        self.assertIn(b'"favorite":null', result.data)

class TestRecordings(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_recordings_flask_route_user_not_logged_in(self):
        """ Test that recordings displays recordings page. """

        result = self.client.get('/recordings')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Recordings</h1>', result.data)
        self.assertIn(b'Ocean', result.data)
        self.assertIn(b'Park', result.data)
        self.assertIn(b'Wind', result.data)
        self.assertNotIn(b'fas fa-star', result.data)

    def test_recordings_flask_route_user_logged_in(self):
        """ Test that recordings displays recordings page. 

        User 2 has favorited recordings 2 and 3."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

        result = self.client.get('/recordings')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Recordings</h1>', result.data)
        self.assertIn(b'Ocean', result.data)
        self.assertIn(b'Park', result.data)
        self.assertIn(b'Wind', result.data)
        self.assertIn(b'fas fa-star', result.data)

    def test_toggle_recording_to_favorite_user_logged_in(self):
        """ Test that logged in user can favorite a recording. 

        User 2's favorite recordings are 2 and 3.
        Let's test user 2 favoriting recording 1."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        recording_id = 1

        result = self.client.get(f'/toggle_favorite_recording?recording_id={recording_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":true', result.data)

    def test_toggle_recording_to_unfavorite_user_logged_in(self):
        """ Test that logged in user can unfavorite a recording. 

        User 2's favorite recordings are 2 and 3.
        Let's test user 2 unfavoriting recording 2."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        recording_id = 2

        result = self.client.get(f'/toggle_favorite_recording?recording_id={recording_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":false', result.data)

    def test_toggle_recording_user_not_logged_in(self):
        """ Test that user not logged in attempts to toggle favoriting recording. """

        recording_id = 1

        result = self.client.get(f'/toggle_favorite_recording?recording_id={recording_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":false', result.data)
        self.assertIn(b'"favorite":null', result.data)

class TestMessages(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_messages_flask_route_user_not_logged_in(self):
        """ Test that messages displays messages page. """

        result = self.client.get('/messages')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Message Templates</h1>', result.data)
        self.assertNotIn(b'fas fa-star', result.data)

    def test_messages_flask_route_user_logged_in(self):
        """ Test that messages displays messages page. 

        User 2 has favorited messages 2 and 3."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

        result = self.client.get('/messages')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Message Templates</h1>', result.data)
        self.assertIn(b'fas fa-star', result.data)

    def test_toggle_message_to_favorite_user_logged_in(self):
        """ Test that logged in user can favorite a message. 

        User 2's favorite messages are 2 and 3.
        Let's test user 2 favoriting message 1."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        message_id = 1

        result = self.client.get(f'/toggle_favorite_message?message_id={message_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":true', result.data)

    def test_toggle_message_to_unfavorite_user_logged_in(self):
        """ Test that logged in user can unfavorite a message. 

        User 2's favorite messages are 2 and 3.
        Let's test user 2 unfavoriting message 2."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                
        message_id = 2

        result = self.client.get(f'/toggle_favorite_message?message_id={message_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)
        self.assertIn(b'"favorite":false', result.data)

    def test_toggle_message_user_not_logged_in(self):
        """ Test that user not logged in attempts to toggle favoriting message. """

        message_id = 1

        result = self.client.get(f'/toggle_favorite_message?message_id={message_id}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":false', result.data)
        self.assertIn(b'"favorite":null', result.data)

    def test_validate_logged_in_user_not_logged_in(self):
        """ Test the validate_logged_in route when user is not logged in. """

        result = self.client.get(f'/validate_logged_in')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":false', result.data)

    def test_validate_logged_in_user_yes_logged_in(self):
        """ Test the validate_logged_in route when user is logged in. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

        result = self.client.get(f'/validate_logged_in')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"user_logged_in":true', result.data)

class TestEmailMessage(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

        # Make mock
        def _load_message_and_send(_):
            message_status = {
                'labelIds': ['SENT']
            }
            return message_status

        server.load_message_and_send = _load_message_and_send

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_store_message_id_route(self):
        """ Test that message id is stored in session with this route. """

        message_id = 1

        result = self.client.get(f'/store_message_id?message_id={message_id}', follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        with self.client as c:
            with c.session_transaction() as sess:
                self.assertEqual(sess['message_id'], '1')

    def test_email_message_user_not_logged_in_redirect_home(self):
        """ Test route /email_message when user not logged in. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['message_id'] = 2

        result = self.client.get('/email_message', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        # route redirects to homepage if no user logged in and flashes the following
        self.assertIn(b'Sign Up or Log In to enable sending email message templates.', result.data)
        self.assertIn(b'You are not alone', result.data)

    def test_email_message_user_yes_logged_in_no_credentials_redirect_authorize(self):
        """ Test route /email_message when user logged in but no credentials. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['message_id'] = 2
                sess['user_id'] = 2

        result = self.client.get('/email_message')
        self.assertEqual(result.status_code, 302)
        # route redirects to /authorize when user_id but not credentials is in session

    def test_email_message_user_yes_logged_in_yes_credentials_render_email_message(self):
        """ Test route /email_message when user logged in and credentials in session. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2
                sess['message_id'] = 2
                sess['credentials'] = ''

        result = self.client.get('/email_message', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Email Message</h1>', result.data)

    def test_email_message_post(self):
        """ Test sending email message. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

        data = {
            'from_first_name': 'Denise',
            'from_last_name': 'Codes',
            'to_name': 'Roy Codes',
            'to_email': 'denise@codes.com',
            'subject': 'subject',
            'body_message': 'body_message'
        }

        result = self.client.post('/email_message', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        # this message gets flashed
        self.assertIn(b'email message was sent', result.data)
        self.assertIn(b'You are not alone', result.data)

class TestTextMessage(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

        # Make mock
        def _send_text_message(from_, body, to):
            pass

        server.send_text_message = _send_text_message

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_text_message_user_not_logged_in(self):
        """ Test get test_message route when user is not lgged in. """

        message_id = 1

        result = self.client.get(f'/text_message?message_id={message_id}', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        # this message gets flashed
        self.assertIn(b'Sign Up or Log In to enable sending text message templates.', result.data)
        self.assertIn(b'You are not alone', result.data)

    def test_text_message_user_logged_in(self):
        """ Test get test_message route when user is logged in. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

        message_id = 1

        result = self.client.get(f'/text_message?message_id={message_id}', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Text Message</h1>', result.data)

    def test_text_message_post(self):
        """ Test sending a text message. """

        data = {
            'from_first_name': 'Denise',
            'from_last_name': 'Codes',
            'to_name': 'Roy Codes',
            'body_message': 'body_message',
            'phone': '000-000-0000'
        }

        result = self.client.post('/text_message', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        # this message gets flashed
        self.assertIn(b'message sent to Roy Codes', result.data)
        self.assertIn(b'You are not alone', result.data)


if __name__ == '__main__':
    unittest.main()