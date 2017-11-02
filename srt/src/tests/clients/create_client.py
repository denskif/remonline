# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CLIENT_URL
from src.lib.dom import (
    find_elements_by_selector, find_element_by_selector, set_value, get_value
)
from src.lib.errors import assert_has_error_tooltip
from src.lib.randomizer import random_x, make_phone_number
from src.lib.wait import wait_to_see_selector
from src.lib.formatting import format_phone_ua

from src.scaffolds.dialog import close_dialog
from src.scaffolds.search import search_for, reset_search

from src.tests.clients.lib import (
    open_create_client_dialog, SUBMIT_SEL, CLIENT_NAME_SEL, close_client_dialog,
    CLIENT_ID_SEL, submit_client_dialog
)
from src.tests.clients.lib.client import (
    create_client, find_open_client, open_client, PHONE_SEL
)

CLIENT = {
    'name' : "King Kong",
    'phone' : make_phone_number(),
    'email' : "testt",
    'address' : "dg dg90",
    'note' : "Beware of beawers",
}
CLIENT_WITH_ATTRIBUTES = {
    'name' : "MRS {0}".format(random_x()),
    'supplier' : True,
    'conflicted' : True,
}
CLIENT_WITH_PHONES = {'name' : "C_W_P {0}".format(random_x())}
JURI_BTN = ".js-client-juridical .b-btn"


def set_up_phones(driver, phone_list):
    def _set_phone(input_idx, phone):
        set_value(driver, PHONE_SEL, phone, input_idx)
        return find_element_by_selector(driver, ".js-phone-add").click()
    return map(_set_phone, range(len(phone_list)), phone_list)


class ValidateClientTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_validate_client(self):
        open_create_client_dialog(self.driver)
        find_element_by_selector(self.driver, SUBMIT_SEL).click()
        return assert_has_error_tooltip(
            self.driver, find_element_by_selector(self.driver, CLIENT_NAME_SEL)
        )

    @classmethod
    def tearDownClass(cls):
        close_client_dialog(cls.driver)


class CreateClientTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_open_close_dialog(self):
        open_create_client_dialog(self.driver)
        close_client_dialog(self.driver)

        open_create_client_dialog(self.driver)
        close_dialog(self.driver, ".h-dialog-mask", ".b-dialog")
        return

    def test_2_simple_client(self):
        client = {'name' : "Tony {0}".format(random_x())}

        create_client(self.driver, client)

        search_for(self.driver, client['name'])
        added_client = find_element_by_selector(self.driver, CLIENT_ID_SEL).text

        return self.assertEqual(added_client, client['name'])


class ClientAttributesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_set_client_attributes(self):
        create_client(self.driver, CLIENT_WITH_ATTRIBUTES)

        search_for(self.driver, CLIENT_WITH_ATTRIBUTES['name'])
        wait_to_see_selector(self.driver, ".h-supplier")
        wait_to_see_selector(self.driver, ".h-conflicted")

        reset_search(self.driver)
        return True

    def test_2_set_client_type(self):
        physical_person = 0
        legal_entity = 1

        find_open_client(self.driver, CLIENT_WITH_ATTRIBUTES['name'])
        find_element_by_selector(
            self.driver, JURI_BTN, legal_entity
        ).click()
        submit_client_dialog(self.driver)
        wait_to_see_selector(self.driver, ".i-company")

        open_client(self.driver)
        find_element_by_selector(
            self.driver, JURI_BTN, physical_person
        ).click()

        submit_client_dialog(self.driver)
        wait_to_see_selector(self.driver, ".i-user")
        return reset_search(self.driver)


class ClientPhoneNumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_add_client_with_few_phones(self):
        open_create_client_dialog(self.driver)
        set_value(self.driver, CLIENT_NAME_SEL, CLIENT_WITH_PHONES['name'])

        phones = 5
        phones_to_set = [make_phone_number() for phone in range(phones)]
        set_up_phones(self.driver, phones_to_set)
        submit_client_dialog(self.driver)

        find_open_client(self.driver, CLIENT_WITH_PHONES['name'])
        client_phones = find_elements_by_selector(self.driver, PHONE_SEL)
        phones_to_check = map(get_value, client_phones)

        return self.assertEqual(
            map(format_phone_ua, phones_to_set), phones_to_check
        )

    @classmethod
    def tearDownClass(cls):
        close_client_dialog(cls.driver)
        reset_search(cls.driver)
