# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src import settings
from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import wait_for_selector, wait_selector_to_disappear
from src.lib.driver import get_driver
from src.lib.errors import assert_selector_is_visible
from src.lib.randomizer import make_login, make_email

from src.tests.auth.lib import (
    click_submit, click_sign_up, log_out,
    EMAIL_SEL, PASS_SEL, LOGIN_SEL, NAME_SEL, LAST_NAME_SEL, COMPANY_SEL,
    CITY_SEL, PHONE_SEL, SIGN_UP_BTN,
)


class Login(TestCase):

    @classmethod
    def setUpClass(cls):
        # Open login dialog window.
        cls.driver = get_driver()

        button = find_element_by_selector(cls.driver, ".js-auth-signin")
        assert_selector_is_visible(cls.driver, ".js-auth-signin")
        button.click()

    def test_login_to_account(self):
        self.driver.find_element_by_id(
            "l-auth-login",
        ).send_keys(settings.LOGIN)

        self.driver.find_element_by_id(
            "l-auth-pass",
        ).send_keys(settings.PASSWORD)

        find_element_by_selector(self.driver, ".js-submit").click()

        # Wait until desired element is present on page.
        wait_for_selector(self.driver, ".b-page__content")
        assert_selector_is_visible(self.driver, ".b-page__content")


class Signup(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_register_new_account(self):
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
