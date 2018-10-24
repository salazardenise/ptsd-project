# The selenium.webdriver module provides all the WebDriver implementations. 
from selenium import webdriver
# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys
# The expected_conditions module contains a set of predefined conditions to use with WebDriverWait.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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
        """ Check that going to homepage shows correct title. """

        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'PTSD Project')

    def test_click_signup(self):
        """ Check that clicking on Sign Up redirects to correct route. """

        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_link_text('Sign Up').click()
        result = self.browser.find_element_by_tag_name('p')
        self.assertEqual('Signing up allows you to favorite different features of this site. Fill out the form to proceed.', result.text)

    def test_click_login(self):
        """ Check that clicking on Log In redirects to correct route. """

        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_link_text('Log In').click()
        result = self.browser.find_element_by_id('logInForm')
        self.assertIn('Enter username:', result.text)
        self.assertIn('Enter password:', result.text)

class TestSignUp(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to signup shows correct title. """

        self.browser.get('http://localhost:5000/signup')
        self.assertEqual(self.browser.title, 'Sign Up') 

    def test_should_not_leave_page_unless_required_fields_filled_in(self):
        """ Test that user stays on page if all required fields not filled in. """

        self.browser.get('http://localhost:5000/signup')
        submitButton = self.browser.find_element_by_css_selector('input[type="submit"]')
        submitButton.click()
        WebDriverWait(self.browser, 3).until(EC.title_is('Sign Up'))

    def test_clicking_on_unclickable_elements_does_nothing(self):
        """ Test that clicking on something unclickable does nothing. """

        self.browser.get('http://localhost:5000/signup')
        self.browser.find_element_by_xpath("//body").click()

    def test_should_be_able_to_submit_form(self):
        """ Test that a new user can sign up.

        This test will fail if BobCodes101 exists in the database.
        Make sure to remove this user before running this test."""
        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        emailInput = self.browser.find_element_by_name('email')
        email = 'denise@codes.com'
        emailInput.send_keys(email)

        usernameInput = self.browser.find_element_by_name('username')
        username = 'BobCodes101'
        usernameInput.send_keys(username)

        password1Input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1Input.send_keys(password1)

        password2Input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2Input.send_keys(password2)

        # send form
        submitButton = self.browser.find_element_by_css_selector('input[type="submit"]')
        print(submitButton)
        submitButton.click()

        WebDriverWait(self.browser, 3).until(EC.title_is('PTSD Project'))

    def test_should_be_able_to_enter_text_into_required_fields(self):
        """ Test entering text into fields. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        emailInput = self.browser.find_element_by_name('email')
        email = 'bob@codes.com'
        emailInput.send_keys(email)
        self.assertEqual(emailInput.get_attribute('value'), email)

        usernameInput = self.browser.find_element_by_name('username')
        username = 'BobCodes101'
        usernameInput.send_keys(username)
        self.assertEqual(usernameInput.get_attribute('value'), username)

        password1Input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1Input.send_keys(password1)
        self.assertEqual(password1Input.get_attribute('value'), password1)

        password2Input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2Input.send_keys(password2)
        self.assertEqual(password2Input.get_attribute('value'), password2)

    def test_should_not_submit_form_if_username_taken(self):
        """ Test that form does not submit if username already exists in database. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        emailInput = self.browser.find_element_by_name('email')
        email = 'denise@codes.com'
        emailInput.send_keys(email)

        usernameInput = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        usernameInput.send_keys(username)

        password1Input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1Input.send_keys(password1)

        password2Input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2Input.send_keys(password2)

        # attempt to submit form
        password2Input.submit()

        signupErrorMessage = self.browser.find_element_by_id('signUpErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(signupErrorMessage))
        result = self.browser.find_element_by_id('signUpErrorMessage')
        self.assertEqual('Error: Username is already taken. Please enter a different one.', result.text)

    def test_should_not_submit_form_if_passwords_do_not_match(self):
        """ Test that form does not submit if two passwords entered do not match. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        emailInput = self.browser.find_element_by_name('email')
        email = 'bill@codes.com'
        emailInput.send_keys(email)

        usernameInput = self.browser.find_element_by_name('username')
        username = 'BillCodes101'
        usernameInput.send_keys(username)

        password1Input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1Input.send_keys(password1)

        password2Input = self.browser.find_element_by_name('password2')
        password2 = 'Python102'
        password2Input.send_keys(password2)

        # attempt to submit form
        password2Input.submit()

        signupErrorMessage = self.browser.find_element_by_id('signUpErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(signupErrorMessage))
        result = self.browser.find_element_by_id('signUpErrorMessage')
        self.assertEqual('Error: Re-entered password does not match password. Please check this.', result.text)

    def test_should_enter_data_into_form_fields(self):
        """ Test that you can enter data into form fields.  """
        self.browser.get('http://localhost:5000/signup')
        element = self.browser.find_element_by_name('first_name')
        originalValue = element.get_attribute('value')
        self.assertEqual(originalValue, '')

        element.clear()
        element.send_keys('Denise')

        element =  self.browser.find_element_by_name('first_name')
        newFormValue = element.get_attribute('value')
        self.assertEqual(newFormValue, 'Denise')

    def test_sending_keyboard_events_should_append_text_in_inputs(self):
        """ Test that you can append text to a field. """

        self.browser.get('http://localhost:5000/signup')
        element = self.browser.find_element_by_name('first_name')
        element.send_keys('Den')
        value = element.get_attribute('value')
        self.assertEqual(value, 'Den')

        element.send_keys('ise')
        value = element.get_attribute('value')
        self.assertEqual(value, 'Denise')

    def test_should_be_able_to_clear_text_from_input_elements(self):
        """ Test that text can be cleared from a field.  """
        self.browser.get('http://localhost:5000/signup')
        element = self.browser.find_element_by_name('first_name')
        element.send_keys('Denise')
        value = element.get_attribute('value')
        self.assertGreater(len(value), 0)

        element.clear()
        value = element.get_attribute('value')
        self.assertEqual(len(value), 0)

class TestLogIn(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to login shows correct title. """

        self.browser.get('http://localhost:5000/login')
        self.assertEqual(self.browser.title, 'Log In')  

class TestPrograms(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to programs shows correct title. """

        self.browser.get('http://localhost:5000/programs')
        self.assertEqual(self.browser.title, 'Programs')

class TestRecordings(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to recordings shows correct title. """

        self.browser.get('http://localhost:5000/recordings')
        self.assertEqual(self.browser.title, 'Recordings')

class TestMessages(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to messages shows correct title. """

        self.browser.get('http://localhost:5000/messages')
        self.assertEqual(self.browser.title, 'Messages')

# class TestEmailMessage(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/email_message')
#         self.assertEqual(self.browser.title, 'Email Message')

# class TestTextMessage(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/text_message')
#         self.assertEqual(self.browser.title, 'Text Message')

if __name__ == '__main__':
    unittest.main()