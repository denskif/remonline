# ~*~ coding: utf-8 ~*~

import time
from unittest import TestCase

from src import settings

from src.lib.driver import get_driver, refresh
from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import wait_for_selector, wait_to_see_selector
from src.lib.errors import assert_has_error_tooltip, assert_class_is_visible

from src.tests.auth.lib import (
    click_submit, SIGN_IN_SEL, SUBMIT_SEL, LOGIN_SEL, PASS_SEL, log_out
)


INVALID_LOGIN = [
    u"Привет",
    u"Досвиданья",
    u"?><!@#$%^&*",
    u"",
]

INVALID_PASSWORD = [
    u"Досвиданья",
]


class LoginValidationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        # Open login dialog window.
        cls.driver = get_driver()
        wait_for_selector(cls.driver, SIGN_IN_SEL)
        find_element_by_selector(cls.driver, SIGN_IN_SEL).click()
        wait_to_see_selector(cls.driver, LOGIN_SEL)
        cls.login = find_element_by_selector(cls.driver, LOGIN_SEL)
        cls.password = find_element_by_selector(cls.driver, PASS_SEL)

    def test_1_invalid_login(self):
        # Negative test
        for bad_login in INVALID_LOGIN:
            set_value(self.driver, LOGIN_SEL, bad_login)
            click_submit(self.driver)
            assert_has_error_tooltip(self.driver, self.login)

    def test_2_invalid_password(self):
        # Negative test
        for bad_password in INVALID_PASSWORD:
            set_value(self.driver, LOGIN_SEL, "test") # proper login
            set_value(self.driver, PASS_SEL, bad_password)
            click_submit(self.driver)

            time.sleep(0.5) # Waiting for back-end answer - unable to use waits
            assert_has_error_tooltip(self.driver, self.password)

    @classmethod
    def tearDownClass(cls):
        refresh()


class LoginToAccountTests(TestCase):

    @classmethod
    def setUpClass(cls):
        # Open login dialog window.
        cls.driver = get_driver()
        wait_for_selector(cls.driver, SIGN_IN_SEL)
        find_element_by_selector(cls.driver, SIGN_IN_SEL).click()
        wait_to_see_selector(cls.driver, LOGIN_SEL)
        cls.login = find_element_by_selector(cls.driver, LOGIN_SEL)
        cls.password = find_element_by_selector(cls.driver, PASS_SEL)

    def test_1_login_to_account(self):
        set_value(self.driver, LOGIN_SEL, settings.LOGIN)
        set_value(self.driver, PASS_SEL, settings.PASSWORD)
        click_submit(self.driver)

        wait_to_see_selector(self.driver, ".b-page__content")
        wait_to_see_selector(self.driver, ".b-sidebar")
        wait_to_see_selector(self.driver, ".js-orders-grid")

    # Log-out from current account
    @classmethod
    def tearDownClass(cls):
        log_out(cls.driver)
