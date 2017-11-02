# ~*~ coding: utf-8 ~*~

import unittest

from selenium.webdriver.common.action_chains import ActionChains

from src.lib.driver import get_driver
from src.lib.dom import set_value, get_value, find_element_by_selector
from src.lib.url import navigate
from src.lib.wait import wait_for_selector

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import test_caret, autocomplete_add

from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.open import open_order, open_tab, TAB_INFO
from src.tests.orders.lib.client import add_new_client, assert_client


CLIENT_DATA = {
    'name': u"Marshall Mathers",
    'phone': u"3335553355",
    'email': u"bruce@lll.com",
    'address': u"550 Madison Avenue",
}
CLIENT_DATA1 = {
    'name': u"Matthew Bellamy",
    'phone': u"2226662266",
    'email': u"james@esum.com",
    'address': u"5200 Blue Lagoon",
}
CLIENT_DATA2 = {
    'name': u"Jack Garrett",
    'phone': u"8883338833",
    'email': u"jackson@worry.com",
    'address': u"222 W. Merchandise Mart Plaza",
}
EDIT_CLIENT_DATA = {
    'name': u"Chris Martin",
    'phone': u"4447774477",
    'email': u"anthony@cold.com",
    'address': u"4000 Warner Blvd",
}
EMPTY_CLIENT_DATA = {
    'name': "",
    'phone': "",
    'email': "",
    'address': "",
}


def edit_client(driver, client):
    set_value(driver, "#l-c-name", client['name'])
    set_value(driver, ".js-phone", client['phone'])
    set_value(driver, "#l-c-email", client['email'])
    set_value(driver, "#l-c-address", client['address'])
    return True

def assert_client_reset(driver, test_self, client):
    name = get_value(driver.find_element_by_css_selector("#js-o-name"))
    phone = get_value(driver.find_element_by_css_selector("#js-o-phone"))
    email = get_value(driver.find_element_by_css_selector("#js-o-email"))
    address = get_value(driver.find_element_by_css_selector("#js-o-address"))

    test_self.assertEqual(name, client['name'])
    test_self.assertEqual(phone, client['phone'])
    test_self.assertEqual(email, client['email'])
    return test_self.assertEqual(address, client['address'])



class CreateClientTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")

    def test_1_create_client(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")
        add_new_client(self.driver, CLIENT_DATA)
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        return assert_client(self.driver, self, CLIENT_DATA)

    @classmethod
    def tearDownClass(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")


class EditClientTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")

    def test_1_edit_client(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")
        add_new_client(self.driver, CLIENT_DATA1)
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_client(self.driver, self, CLIENT_DATA1)

        # Edit client's info
        wait_for_selector(self.driver, ".js-edit-client")
        open_dialog(self.driver, ".js-edit-client .h-mr-5", "#l-c-name")
        edit_client(self.driver, EDIT_CLIENT_DATA)
        close_dialog(self.driver, ".js-submit-dialog", "#l-c-name")

        return assert_client(self.driver, self, EDIT_CLIENT_DATA)

    @classmethod
    def tearDownClass(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")


class ResetClientTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")

    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_reset_client(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")
        add_new_client(self.driver, CLIENT_DATA)
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_client(self.driver, self, CLIENT_DATA)

        client_block = self.driver.find_element_by_css_selector(
            ".b-client-choice"
        )
        reset_btn = self.driver.find_element_by_css_selector(
            ".b-client-choice__reset"
        )

        # Hover over the client block and client reset button
        ActionChains(
            self.driver,
        ).move_to_element(
            client_block,
        ).move_to_element(
            reset_btn,
        ).click(
            reset_btn,
        ).perform()

        return assert_client_reset(self.driver, self, EMPTY_CLIENT_DATA)


class ClientAutomcpleteTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")

    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_create_unique_client(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")
        add_new_client(self.driver, CLIENT_DATA2)
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        return assert_client(self.driver, self, CLIENT_DATA2)

    def test_2_check_autocomplete(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")

        test_caret(self.driver, "[data-opts-relate=js-o-name]")
        autocomplete_add(self.driver, self, "#js-o-name", CLIENT_DATA2['name'])
        return assert_client(self.driver, self, CLIENT_DATA2)
