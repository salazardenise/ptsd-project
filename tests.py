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

# class TestSignUp(unittest.TestCase):

#     def setUp(self):
#         """ Set up before every test. """

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # connect to test database
#         connect_to_db(app, 'postgresql:///testdb')

#         # create tables and add sample data
#         db.create_all()
#         load_dummy_data()

#         # # go to signup page
#         # self.client.get('/signup')

#     def tearDown(self):
#         """ Tear down after every test. """

#         db.session.close()
#         db.drop_all()

#     def test_passwords_do_not_match(self):
#         """ Test when a new user does not enter the same password twice. """

#         email = 'bob@codes.com'
#         username = 'BobCodes1'
#         password1 = 'Python101'
#         password2 = 'Python102'

#         data = {'email': email,
#                 'username': username, 
#                 'password1': password1,
#                 'password2': password2}

#         self.client.get('/signup')
#         # To complete later


#     def test_username_already_exists(self):
#         """ Test when a new user enters a username that is already taken. """

#         email = 'denise@codes.com'
#         username = 'denisecodes'
#         password1 = 'Python'
#         password2 = 'Python'

#         data = {'email': email,
#                 'username': username, 
#                 'password1': password1,
#                 'password2': password2}

#         self.client.get('/signup')
#         # To complete later

#     def test_successful_signup(self):

#         email = 'bob@codes.com'
#         username = 'BobCodes1'
#         password1 = 'Python101'
#         password2 = 'Python101'

#         data = {'email': email,
#                 'username': username, 
#                 'password1': password1,
#                 'password2': password2}

#         self.client.get('/signup')
#         # To complete later


if __name__ == '__main__':
    unittest.main()