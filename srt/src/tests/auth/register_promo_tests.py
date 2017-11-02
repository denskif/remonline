# ~*~ coding: utf-8 ~*~

import unittest

from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException

from src.lib.dom import find_element_by_class_name
from src.lib.wait import wait_for_id, wait_to_disappear
from src.lib.randomizer import make_login, make_email
from src.lib.errors import assert_class_is_visible
from src import settings



# This test is closed - promocodes are not in regular use

class RegisterWithPomoCodeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get(settings.HOST)

        # Open registration form
        button_cls = "js-auth-signup"

        button = find_element_by_class_name(cls.driver, button_cls)
        assert_class_is_visible(cls.driver, button_cls)
        button.click()


    def test_1_register_account_with_promo_code(self):
        # Click promo code link
        self.driver.find_element_by_class_name("js-set-promocode").click()

        # Filling in the first form
        email = self.driver.find_element_by_id("l-auth-email")
        login = self.driver.find_element_by_id("l-auth-login")
        password = self.driver.find_element_by_id("l-auth-pass")
        promo = self.driver.find_element_by_id("l-auth-promocode")


        new_email = make_email()
        email.send_keys(new_email)
        login.send_keys(make_login())
        password.send_keys("test")
        promo.send_keys("204")

        start_account = self.driver.find_element_by_class_name("js-submit")
        start_account.click()

        wait_for_id(self.driver, "l-auth-name")

        # Filling in the second form
        name = self.driver.find_element_by_id("l-auth-name")
        surname = self.driver.find_element_by_id("l-auth-lname")
        company = self.driver.find_element_by_id("l-auth-company")
        city = self.driver.find_element_by_id("l-auth-city")
        phone = self.driver.find_element_by_id("l-auth-phone")

        name.send_keys("John")
        surname.send_keys("Smith")
        company.send_keys("Test Company")
        city.send_keys("Test city")
        phone.click()
        phone.send_keys("0000000000")

        # Submit the second form and go to account
        enter_account = self.driver.find_element_by_class_name("js-submit")
        enter_account.click()

        # Ensure that second form is closed
        wait_to_disappear(self.driver, "b-modal_type_registration")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
