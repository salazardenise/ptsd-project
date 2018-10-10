from server import app
from model import connect_to_db, db, User
from seed import load_dummy_data
import unittest

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

class TestRoutesWithDatabase(unittest.TestCase):

    def setUp(self):
        """ Set up before every test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # create tables and add sample data
        db.create_all()
        load_dummy_data()

        # # go to signup page
        # self.client.get('/signup')

    def tearDown(self):
        """ Tear down after every test. """

        db.session.close()
        db.drop_all()

    def test_successful_signup(self):
        """ Test when a new user does not enter the same password twice. """

        email = 'bob@codes.com'
        username = 'BobCodes1'
        password1 = 'Python101'
        password2 = 'Python102'

        data = {'email': email,
                'username': username, 
                'password1': password1,
                'password2': password2}

        result = self.client.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>You are not alone.</h2>', result.data)
        self.assertIn(b'BobCodes1 successfully signed up.', result.data)

    def test_successful_login(self):
        """ Test when a new user does not enter the same password twice. """

        username = 'denisecodes'
        password = 'Python'

        data = {'username': username, 
                'password': password}

        result = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>You are not alone.</h2>', result.data)
        self.assertIn(b'denisecodes successfully logged in.', result.data)

    def test_user_exists_found(self):

        username = 'denisecodes'

        data = {'username': username}

        result = self.client.get('/user_exists', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'found', result.data)

    def test_user_exists_not_found(self):

        username = 'fabiocodes'

        data = {'username': username}

        result = self.client.get('/user_exists', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'not found', result.data)

    def test_validate_login_valid(self):
        
        username = 'denisecodes'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/validate_login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'valid', result.data)

    def test_validate_login_not_valid(self):
        
        username = 'fabiocodes'
        password = 'Python'

        data = {'username': username, 'password': password}

        result = self.client.post('/validate_login', data=data, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'not valid', result.data)

if __name__ == '__main__':
    unittest.main()