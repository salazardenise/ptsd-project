""" Run this module to perform all Selenium integration tests."""

# standard python imports
import unittest

# third party imports
# from flask import session

# The selenium.webdriver module provides all the WebDriver implementations.
from selenium import webdriver

# The expected_conditions module contains a set of predefined conditions to use with WebDriverWait.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select

# The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions i mport NoSuchElementException

# import server
# from server import app
# from model import connect_to_db, db, User
# from seed import load_dummy_data


class TestHomepage(unittest.TestCase):
    """ This class tests clicking on signup/login/logout links at homapge. """

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
        self.assertIn('Signing up allows you to send message templates and favorite different features of this site.',
                      result.text)

    def test_click_login(self):
        """ Check that clicking on Log In redirects to correct route. """

        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_link_text('Log In').click()
        result = self.browser.find_element_by_id('logInForm')
        self.assertIn('Enter username:', result.text)
        self.assertIn('Enter password:', result.text)

    def test_click_programs(self):
        """ Check that clicking on Programs redirects to correct route. """

        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_link_text('Programs').click()
        result = self.browser.find_element_by_id('programsTitle')
        self.assertIn('Programs', result.text)

    def test_click_logout(self):
        """ Check that after logging in, user can click logout. """
    
        # first go to login
        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        # wait till users gets redirected to homepage
        WebDriverWait(self.browser, 5).until(EC.title_is('PTSD Project'))

        # click on logout
        self.browser.find_element_by_link_text('Log Out').click()

        # check that now login and singup links are displayed
        signup_link = self.browser.find_element_by_link_text('Sign Up')
        self.assertEqual(signup_link.is_displayed(), True)
        login_link = self.browser.find_element_by_link_text('Log In')
        self.assertEqual(login_link.is_displayed(), True)

        # check we are still at homepage
        self.assertEqual(self.browser.title, 'PTSD Project')


class TestSignUp(unittest.TestCase):
    """ This class tests user using SignUp page, filling out form. """

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
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()
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
        email_input = self.browser.find_element_by_name('email')
        email = 'denise@codes.com'
        email_input.send_keys(email)

        username_input = self.browser.find_element_by_name('username')
        username = 'BobCodes101'
        username_input.send_keys(username)

        password1_input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1_input.send_keys(password1)

        password2_input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2_input.send_keys(password2)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        WebDriverWait(self.browser, 3).until(EC.title_is('PTSD Project'))

    def test_should_be_able_to_enter_text_into_required_fields(self):
        """ Test entering text into fields. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        email_input = self.browser.find_element_by_name('email')
        email = 'bob@codes.com'
        email_input.send_keys(email)
        self.assertEqual(email_input.get_attribute('value'), email)

        username_input = self.browser.find_element_by_name('username')
        username = 'BobCodes101'
        username_input.send_keys(username)
        self.assertEqual(username_input.get_attribute('value'), username)

        password1_input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1_input.send_keys(password1)
        self.assertEqual(password1_input.get_attribute('value'), password1)

        password2_input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2_input.send_keys(password2)
        self.assertEqual(password2_input.get_attribute('value'), password2)

    def test_should_not_submit_form_if_username_taken(self):
        """ Test that form does not submit if username already exists in database. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        email_input = self.browser.find_element_by_name('email')
        email = 'denise@codes.com'
        email_input.send_keys(email)

        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password1_input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1_input.send_keys(password1)

        password2_input = self.browser.find_element_by_name('password2')
        password2 = 'Python101'
        password2_input.send_keys(password2)

        # attempt to submit form
        password2_input.submit()

        signup_error_message = self.browser.find_element_by_id('signUpErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(signup_error_message))
        result = self.browser.find_element_by_id('signUpErrorMessage')
        self.assertEqual('Error: Username is already taken. Please enter a different one.',
                         result.text)

    def test_should_not_submit_form_if_passwords_do_not_match(self):
        """ Test that form does not submit if two passwords entered do not match. """

        self.browser.get('http://localhost:5000/signup')

        # fill required fields in form
        email_input = self.browser.find_element_by_name('email')
        email = 'bill@codes.com'
        email_input.send_keys(email)

        username_input = self.browser.find_element_by_name('username')
        username = 'BillCodes101'
        username_input.send_keys(username)

        password1_input = self.browser.find_element_by_name('password1')
        password1 = 'Python101'
        password1_input.send_keys(password1)

        password2_input = self.browser.find_element_by_name('password2')
        password2 = 'Python102'
        password2_input.send_keys(password2)

        # attempt to submit form
        password2_input.submit()

        signup_error_message = self.browser.find_element_by_id('signUpErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(signup_error_message))
        result = self.browser.find_element_by_id('signUpErrorMessage')
        self.assertEqual('Error: Re-entered password does not match password. Please check this.',
                         result.text)

    def test_should_enter_data_into_form_fields(self):
        """ Test that you can enter data into form fields.  """

        self.browser.get('http://localhost:5000/signup')
        element = self.browser.find_element_by_name('first_name')
        original_value = element.get_attribute('value')
        self.assertEqual(original_value, '')

        element.clear()
        element.send_keys('Denise')

        element = self.browser.find_element_by_name('first_name')
        new_form_value = element.get_attribute('value')
        self.assertEqual(new_form_value, 'Denise')

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
    """ This class tests user using login page, filling out form. """

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to login shows correct title. """

        self.browser.get('http://localhost:5000/login')
        self.assertEqual(self.browser.title, 'Log In')

    def test_should_not_leave_page_unless_required_fields_filled_in(self):
        """ Test that user stays on page if all required fields not filled in. """

        self.browser.get('http://localhost:5000/login')
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()
        WebDriverWait(self.browser, 3).until(EC.title_is('Log In'))

    def test_clicking_on_unclickable_elements_does_nothing(self):
        """ Test that clicking on something unclickable does nothing. """

        self.browser.get('http://localhost:5000/login')
        self.browser.find_element_by_xpath("//body").click()

    def test_should_be_able_to_submit_form(self):
        """ Test that a user can log in. """

        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        WebDriverWait(self.browser, 5).until(EC.title_is('PTSD Project'))

    def test_should_be_able_to_enter_text_into_required_fields(self):
        """ Test entering text into fields. """

        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)
        self.assertEqual(username_input.get_attribute('value'), username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)
        self.assertEqual(password_input.get_attribute('value'), password)

    def test_should_not_submit_form_if_username_not_found(self):
        """ Test that form does not submit if username not found in database. """

        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'KatrinaCodes101'
        username_input.send_keys(username)
        self.assertEqual(username_input.get_attribute('value'), username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)
        self.assertEqual(password_input.get_attribute('value'), password)

        # attempt to submit form
        password_input.submit()

        login_error_message = self.browser.find_element_by_id('logInErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(login_error_message))
        result = self.browser.find_element_by_id('logInErrorMessage')
        self.assertEqual('Error: Username not recognized.', result.text)

    def test_should_not_submit_form_if_username_and_password_do_not_match(self):
        """ Test that form does not submit if username and password do not match to database. """

        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)
        self.assertEqual(username_input.get_attribute('value'), username)

        password_input = self.browser.find_element_by_name('password')
        password = 'NinjaEngineer101'
        password_input.send_keys(password)
        self.assertEqual(password_input.get_attribute('value'), password)

        # attempt to submit form
        password_input.submit()

        login_error_message = self.browser.find_element_by_id('logInErrorMessage')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(login_error_message))
        result = self.browser.find_element_by_id('logInErrorMessage')
        self.assertEqual('Error: Username and password do not match', result.text)

    def test_should_enter_data_into_form_fields(self):
        """ Test that you can enter data into form fields.  """

        self.browser.get('http://localhost:5000/login')
        element = self.browser.find_element_by_name('username')
        original_value = element.get_attribute('value')
        self.assertEqual(original_value, '')

        element.clear()
        element.send_keys('DeniseCodes101')

        element = self.browser.find_element_by_name('username')
        new_form_value = element.get_attribute('value')
        self.assertEqual(new_form_value, 'DeniseCodes101')

    def test_sending_keyboard_events_should_append_text_in_inputs(self):
        """ Test that you can append text to a field. """

        self.browser.get('http://localhost:5000/login')
        element = self.browser.find_element_by_name('username')
        element.send_keys('Denise')
        value = element.get_attribute('value')
        self.assertEqual(value, 'Denise')

        element.send_keys('Codes101')
        value = element.get_attribute('value')
        self.assertEqual(value, 'DeniseCodes101')

    def test_should_be_able_to_clear_text_from_input_elements(self):
        """ Test that text can be cleared from a field.  """
        self.browser.get('http://localhost:5000/login')
        element = self.browser.find_element_by_name('username')
        element.send_keys('DeniseCodes101')
        value = element.get_attribute('value')
        self.assertGreater(len(value), 0)

        element.clear()
        value = element.get_attribute('value')
        self.assertEqual(len(value), 0)

class TestPrograms(unittest.TestCase):
    """ This class tests user using programs page. """

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to programs shows correct title. """

        self.browser.get('http://localhost:5000/programs')
        self.assertEqual(self.browser.title, 'Programs')

    def test_clicking_on_unclickable_elements_does_nothing(self):
        """ Test that clicking on something unclickable does nothing. """

        self.browser.get('http://localhost:5000/programs')
        self.browser.find_element_by_xpath("//body").click()

    def test_should_be_able_to_submit_search_form_and_stay_on_same_page(self):
        """ Test search can be done. """

        self.browser.get('http://localhost:5000/programs')

        # fill required fields in form
        search_text_input = self.browser.find_element_by_name('search_text')
        search_text = 'CA'
        search_text_input.send_keys(search_text)

        # single_select_search_type_values = {'name': 'search_type', 'values': ['fac_name', 'city', 'state', 'zipcode']}
        select = Select(self.browser.find_element(By.NAME, 'search_type'))
        select.select_by_visible_text('state')

        # send form
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # assert table and map are now visible
        programs_table = self.browser.find_element_by_id('programsResults')
        self.assertEqual(programs_table.is_displayed(), True)
        programs_map = self.browser.find_element_by_id('programsMap')
        self.assertEqual(programs_map.is_displayed(), True)

        # stays on same page even if sending form
        WebDriverWait(self.browser, 3).until(EC.title_is('Programs'))

    def test_should_not_perform_search_unless_required_fields_filled_in(self):
        """ Test that search is not performed unless search_text value is entered. """

        self.browser.get('http://localhost:5000/programs')

        # send form
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # assert table and map are still hidden
        programs_table = self.browser.find_element_by_id('programsResults')
        self.assertEqual(programs_table.is_displayed(), False)
        programs_map = self.browser.find_element_by_id('programsMap')
        self.assertEqual(programs_map.is_displayed(), False)

        # should still be on same page
        WebDriverWait(self.browser, 3).until(EC.title_is('Programs'))

    def test_submit_search_form_and_no_results(self):
        """ Test that searching for something that restuns no results does just that. """

        self.browser.get('http://localhost:5000/programs')

        # fill required fields in form
        search_text_input = self.browser.find_element_by_name('search_text')
        # assume this does not exist anywhere in facilities table
        search_text = 'LionsTigersBears'
        search_text_input.send_keys(search_text)

        # send form
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # show error message
        programs_results = self.browser.find_element_by_id('programsResults')
        WebDriverWait(self.browser, 5).until(EC.visibility_of(programs_results))
        result = self.browser.find_element_by_id('programsResults')
        self.assertEqual('No results found. Try again with a different search.', result.text)

        # assert map is still hidden
        programs_map = self.browser.find_element_by_id('programsMap')
        self.assertEqual(programs_map.is_displayed(), False)

        # should still be on same page
        WebDriverWait(self.browser, 3).until(EC.title_is('Programs'))

    def test_submit_search_click_on_facility_cause_programs_to_display(self):
        """ Test that clicking on a facility shows its programs. """

        self.browser.get('http://localhost:5000/programs')

        # fill required fields in form
        search_text_input = self.browser.find_element_by_name('search_text')
        search_text = 'CA'
        search_text_input.send_keys(search_text)

        #single_select_search_type_values = {'name': 'search_type', 'values': ['fac_name', 'city', 'state', 'zipcode']}
        select = Select(self.browser.find_element(By.NAME, 'search_type'))
        select.select_by_visible_text('state')

        # send form
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # this causes map and table to show
        # try clicking on a facility name which triggers showing its programs
        wait = WebDriverWait(self.browser, 10)
        first_facility = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'facility-name')))
        first_facility.click()

        programs_list = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'programsList')))
        self.assertEqual(programs_list.is_displayed(), True)

        # since no user is logged in, there should be no solid favorite star
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fas')))
            not_found = False
        except:
            not_found = True

        assert not_found

    def test_logged_in_user_perform_search_solid_star_displayed(self):
        """ Test that a logged in user can perform a search and see their favorite facilities """

        # first go to login
        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        # wait till users gets redirected to homepage
        WebDriverWait(self.browser, 5).until(EC.title_is('PTSD Project'))

        # now go to programs page
        self.browser.get('http://localhost:5000/programs')

        # fill required fields in form
        search_text_input = self.browser.find_element_by_name('search_text')
        search_text = 'CA'
        search_text_input.send_keys(search_text)

        #single_select_search_type_values = {'name': 'search_type', 'values': ['fac_name', 'city', 'state', 'zipcode']}
        select = Select(self.browser.find_element(By.NAME, 'search_type'))
        select.select_by_visible_text('state')

        # send form
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # this causes map and table to show
        # check that one of the stars is solid (favorited already)
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'fas')))
        first_favorite_star = self.browser.find_element_by_tag_name('i')
        self.assertEqual(first_favorite_star.is_displayed(), True)

class TestRecordings(unittest.TestCase):
    """ this class tests user using recordings page. """

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to recordings shows correct title. """

        self.browser.get('http://localhost:5000/recordings')
        self.assertEqual(self.browser.title, 'Recordings')

    def test_no_user_logged_in_no_solid_stars(self):
        """ Test that a user (not logged in) sees no solid stars & cannot favoite recordings. """

        self.browser.get('http://localhost:5000/recordings')
        first_not_favorite_star = self.browser.find_element_by_class_name('far')
        self.assertEqual(first_not_favorite_star.is_displayed(), True)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fas')))
            not_found = False
        except:
            not_found = True

        assert not_found

    def test_no_user_logged_in_clicks_on_star_see_error_message(self):
        """ Test that a user (not logged in) clicks on a star, then sees an error message. """

        self.browser.get('http://localhost:5000/recordings')
        first_star = self.browser.find_element_by_class_name('recording-star')
        first_star.click()

        # no star becomes solid
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fas')))
            not_found = False
        except:
            not_found = True

        assert not_found

        # check that error message pops up
        programs_error_message = self.browser.find_element_by_id('recordingsErrorMessage')
        self.assertEqual(programs_error_message.is_displayed(), True)


    def test_user_logged_in_yes_solid_stars(self):
        """ Test that a user that is logged in sees their favortie recordings as solid stars. """

        # first go to login
        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        # wait till users gets redirected to homepage
        WebDriverWait(self.browser, 5).until(EC.title_is('PTSD Project'))

        # now go to recordings page
        self.browser.get('http://localhost:5000/recordings')

        first_favorite_star = self.browser.find_element_by_class_name('fas')
        self.assertEqual(first_favorite_star.is_displayed(), True)

class TestMessages(unittest.TestCase):
    """ This class tests user using messages page. """

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """ Check that going to messages shows correct title. """

        self.browser.get('http://localhost:5000/messages')
        self.assertEqual(self.browser.title, 'Messages')

    def test_no_user_logged_in_no_solid_stars(self):
        """ Test that a user that is not logged in sees no solid stars and cannot favoite a recording. """

        self.browser.get('http://localhost:5000/messages')
        first_not_favorite_star = self.browser.find_element_by_class_name('far')
        self.assertEqual(first_not_favorite_star.is_displayed(), True)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fas')))
            not_found = False
        except:
            not_found = True

        assert not_found

    def test_user_logged_in_yes_solid_stars(self):
        """ Test that a user that is logged in sees their favortie recordings as solid stars. """

        # first go to login
        self.browser.get('http://localhost:5000/login')

        # fill required fields in form
        username_input = self.browser.find_element_by_name('username')
        username = 'DeniseCodes101'
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_name('password')
        password = 'Python101'
        password_input.send_keys(password)

        # send form
        submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')
        submit_button.click()

        # wait till users gets redirected to homepage
        WebDriverWait(self.browser, 5).until(EC.title_is('PTSD Project'))

        # now go to recordings page
        self.browser.get('http://localhost:5000/messages')

        first_favorite_star = self.browser.find_element_by_class_name('fas')
        self.assertEqual(first_favorite_star.is_displayed(), True)

# class TestEmailMessage(unittest.TestCase):
#     """ This class tests user using email message page. """

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/email_message')
#         self.assertEqual(self.browser.title, 'Email Message')

# class TestTextMessage(unittest.TestCase):
#     """ This class tests user using text message page. """

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def tearDown(self):
#         self.browser.quit()

#     def test_title(self):
#         self.browser.get('http://localhost:5000/text_message')
#         self.assertEqual(self.browser.title, 'Text Message')

if __name__ == '__main__':
    unittest.main()
