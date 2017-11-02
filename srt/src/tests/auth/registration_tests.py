# ~*~ coding: utf-8 ~*~

from unittest import TestCase
import time

from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import (
    wait_selector_to_disappear, wait_for_selector, wait_to_see_selector
)

from src.lib.randomizer import make_login, make_email
from src.lib.errors import assert_has_error_tooltip
from src.lib.driver import get_driver, refresh

from src.tests.auth.lib import (
    click_submit, click_sign_up, log_out,
    EMAIL_SEL, PASS_SEL, LOGIN_SEL, NAME_SEL, LAST_NAME_SEL, COMPANY_SEL,
    CITY_SEL, PHONE_SEL, PARTNERS_PAGE_LINK, PARTNER_BTN_SEL, SUBMIT_SEL,
    SIGN_UP_BTN,
)


BAD_EMAIL_LIST = [
    u"test@test",
    u"test.test",
    u"\"test\"@test.com",
    u"пример@test.com",
    u"test@test@test.com",
    u"?><!#$%{}|&^%&*@test.com",
]
BAD_LOGIN_LIST = [
    u"Доброе утро",
    u"?><!@#$%^&*(",
]
MINIMAL_CHARS_DATA = {
    'login' : "12", # 3 chars required
    'email' : "test@test.com", # this data is ok
    'pass' : "123", # 4 chars required
}


class ValidateRegistrationFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

        # Open registration form
        wait_for_selector(cls.driver, SIGN_UP_BTN)
        click_sign_up(cls.driver)

        cls.email = find_element_by_selector(cls.driver, EMAIL_SEL)
        cls.login = find_element_by_selector(cls.driver, LOGIN_SEL)
        cls.password = find_element_by_selector(cls.driver, PASS_SEL)

    def test_1_blank_fields_validation(self):
        # Negative test
        click_submit(self.driver)

        assert_has_error_tooltip(self.driver, self.email)
        assert_has_error_tooltip(self.driver, self.login)
        assert_has_error_tooltip(self.driver, self.password)

    def test_2_email_validation(self):
        # Negative test
        for bad_email in BAD_EMAIL_LIST:
            set_value(self.driver, EMAIL_SEL, bad_email)
            assert_has_error_tooltip(self.driver, self.email)

    def test_3_login_validation(self):
        # Negative test
        for bad_login in BAD_LOGIN_LIST:
            set_value(self.driver, LOGIN_SEL, bad_login)
            assert_has_error_tooltip(self.driver, self.login)

    # Following tests check the back-end data validations

    def test_4_minimal_chars_form_validation(self):
        # Negative test
        set_value(self.driver, EMAIL_SEL, MINIMAL_CHARS_DATA['email'])
        set_value(self.driver, LOGIN_SEL, MINIMAL_CHARS_DATA['login'])
        set_value(self.driver, PASS_SEL, MINIMAL_CHARS_DATA['pass'])

        click_submit(self.driver)
        time.sleep(0.5) # Waiting for back-end answer - unable to use waits

        assert_has_error_tooltip(self.driver, self.login)
        assert_has_error_tooltip(self.driver, self.password)

    def test_5_password_field_cyrillic_input(self):
        # Negative test
        set_value(self.driver, LOGIN_SEL, "test")
        set_value(self.driver, PASS_SEL, u"Привет")

        click_submit(self.driver)
        time.sleep(0.5) # Waiting for back-end answer - unable to use waits

        assert_has_error_tooltip(self.driver, self.password)

    def test_6_login_already_exist(self):
        # Negative test
        # This is a login of template company
        set_value(self.driver, LOGIN_SEL, "template")
        set_value(self.driver, PASS_SEL, "1234")

        click_submit(self.driver)
        time.sleep(0.5) # Waiting for back-end answer - unable to use waits

        assert_has_error_tooltip(self.driver, self.login)

    def test_7_email_already_exist(self):
        # Negative test
        # This is an email of template company
        set_value(self.driver, EMAIL_SEL, "test@test.test")
        set_value(self.driver, LOGIN_SEL, "template2")
        set_value(self.driver, PASS_SEL, u"1234")

        click_submit(self.driver)
        time.sleep(0.5) # Waiting for back-end answer - unable to use waits

        assert_has_error_tooltip(self.driver, self.email)

    @classmethod
    def tearDownClass(cls):
        refresh()


class RegisterNewAccountTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_1_register_new_account(self):
        wait_for_selector(self.driver, SIGN_UP_BTN)
        click_sign_up(self.driver)

        # Filling in the first form
        set_value(self.driver, EMAIL_SEL, make_email())
        set_value(self.driver, LOGIN_SEL, make_login())
        set_value(self.driver, PASS_SEL, "test")

        click_submit(self.driver)

        # Awaiting second registration form to appear
        wait_for_selector(self.driver, "#l-auth-name")

        # Filling in the second form
        set_value(self.driver, NAME_SEL, "John")
        set_value(self.driver, LAST_NAME_SEL, "Smith")
        set_value(self.driver, COMPANY_SEL, "Test Company")
        set_value(self.driver, CITY_SEL, "Test city")
        set_value(self.driver, PHONE_SEL, "0000000000")

        click_submit(self.driver)

        # Ensure that second form is closed
        wait_selector_to_disappear(self.driver, "#l-auth-name")


class RegisterPartnerAccountTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_1_register_a_partner(self):

        find_element_by_selector(self.driver, PARTNERS_PAGE_LINK).click()
        wait_for_selector(self.driver, PARTNER_BTN_SEL)

        find_element_by_selector(self.driver, PARTNER_BTN_SEL).click()
        wait_to_see_selector(self.driver, SUBMIT_SEL)

        set_value(self.driver, EMAIL_SEL, make_email())
        set_value(self.driver, PASS_SEL, "test")

        click_submit(self.driver)

        # Awaiting second registration form to appear
        wait_for_selector(self.driver, "#l-auth-name")

        # Filling in the second form
        set_value(self.driver, NAME_SEL, "John")
        set_value(self.driver, LAST_NAME_SEL, "Smith")
        set_value(self.driver, COMPANY_SEL, "Test Company")
        set_value(self.driver, CITY_SEL, "Test city")
        set_value(self.driver, PHONE_SEL, "0000000000")

        click_submit(self.driver)

        # Ensure that second form is closed
        wait_selector_to_disappear(self.driver, "#l-auth-name")
        wait_to_see_selector(self.driver, ".h-referral-link")

    @classmethod
    def tearDownClass(cls):
        log_out(cls.driver)

