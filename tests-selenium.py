from selenium import webdriver
import unittest
from server import app
from model import connect_to_db, db, User
from seed import load_dummy_data
from flask import session
import server

class TestHomepage(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'PTSD Project')

# class TestSignUp(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/signup')
#         self.assertEqual(self.browser.title, 'Sign Up') 

# class TestLogIn(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/login')
#         self.assertEqual(self.browser.title, 'Log In')  

# class TestPrograms(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/programs')
#         self.assertEqual(self.browser.title, 'Programs')

# class TestRecordings(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/recordings')
#         self.assertEqual(self.browser.title, 'Recordings')

# class TestMessages(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/messages')
#         self.assertEqual(self.browser.title, 'Messages')

# class TestEmailMessage(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/email_message')
#         self.assertEqual(self.browser.title, 'Email Message')

# class TestTextMessage(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/text_message')
#         self.assertEqual(self.browser.title, 'Text Message')



if __name__ == '__main__':
    unittest.main()