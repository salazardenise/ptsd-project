import unittest
from server import app
from model import connect_to_db, db, User
from seed import load_dummy_data
from flask import session

class TestRoutes(unittest.TestCase):

    def setUp(self):
        """ 
        Set up before every test. 

        The Flask app has a test_client() method on it.
        It is a mini browswer that can make requests.
        """

        self.client = app.test_client()
        app.config['Testing'] = True

    def test_hompage_flask_route(self):
        """ Test that homepage displays at root route. """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>You are not alone.</h2>', result.data)

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

        username = 'denisecodes'

        data = {'username': username}

        result = self.client.get(f'/validate_signup?username={username}')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)

    def test_validate_signup_username_not_found(self):
        """ Test when a username attempts to signup with a new username. """

        username = 'fabiocodes'

        data = {'username': username}

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
        self.assertIn(b'<h2>You are not alone.</h2>', result.data)
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

        username = 'denisecodes'
        password = 'Python101'

        data = {'username': username, 'password': password}

        result = self.client.post('/validate_login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)
        self.assertIn(b'"valid_login":false', result.data)

    def test_validate_login_valid_username_valid_password(self):
        """ Test when user attempts to login with valid username and password. """

        username = 'denisecodes'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/validate_login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":true', result.data)
        self.assertIn(b'"valid_login":true', result.data)

    def test_validate_login_invalid_username(self):
        """ Test when user attempts to login with invalid username. """
        
        username = 'fabiocodes'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/validate_login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"username_found":false', result.data)
        self.assertIn(b'"valid_login":null', result.data)

    def test_successful_login(self):
        """ Test when a new user signs up successfully. """

        username = 'denisecodes'
        password = 'Python'

        data = {'username': username, 
                'password': password}

        with self.client as c:
            result = c.post('/login', data=data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(session['user_id'], 1)
            self.assertIn(b'<h2>You are not alone.</h2>', result.data)
            self.assertIn(b'denisecodes successfully logged in.', result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b'denisecodes successfully logged out.', result.data)

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
        self.assertIn(b'<h1>Programs</h1>', result.data)

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

if __name__ == '__main__':
    unittest.main()