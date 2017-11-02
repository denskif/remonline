# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.driver import get_driver
from src.lib.dom import (
    find_element_by_selector, set_value, get_value
)
from src.lib.wait import (
    wait_for_selector, wait_to_click_selector, wait_selector_to_disappear
)
from src.lib.formatting import make_text_xpath
from src.lib.url import navigate, ORDERS_URL


from src.scaffolds.dialog import open_dialog

from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.client import add_new_client, assert_client
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, TAB_INFO
from src.tests.orders.lib.status import change_status_from_table



DEVICE_DATA = {
    'model': u"second device",
    'malfunction': u"second problem",
}
CLIENT_DATA1 = {
    'name': u"David Passaro",
    'phone': u"7771117711",
    'email': u"paden@afi.com",
    'address': u"13880 Dulles Corner Lane",
}
CLIENT_DATA2 = {
    'name': u"William Hince",
    'email': u"James@kills.com",
    'address': u"75 Midnight Lane",
}
CLIENT_DATA3 = {
    'name': u"Eric Reed",
    'email': u"biafra@dk.com",
    'address': u"13 Police Road",
}
CLIENT_DATA4 = {
    'name': u"Rainn Wilson",
    'email': u"Dietrich@office.com",
    'address': u"19 Bishop Road",
}
CLIENT_DATA5 = {
    'name': u"Robert Diggs",
    'email': u"tung@wu.com",
    'address': u"275 Mandarine Sqr Plaza",
}

CLOSED_STATUS_INDEX = -1

def click_create_more(driver, sel_idx=None):
    find_element_by_selector(driver, ".b-order__footer .b-btn_type_ico").click()
    return find_element_by_selector(driver, ".h-c-black", idx=sel_idx).click()

def assert_no_phone_client(driver, test_self, client):
    name = get_value(driver.find_element_by_css_selector("#js-o-name"))
    email = get_value(driver.find_element_by_css_selector("#js-o-email"))
    address = get_value(driver.find_element_by_css_selector("#js-o-address"))

    test_self.assertEqual(name, client['name'])
    test_self.assertEqual(email, client['email'])
    return test_self.assertEqual(address, client['address'])


class CreateOrderAndOneMore(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_create_and_one_more(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")

        add_new_client(self.driver, CLIENT_DATA1)
        set_value(self.driver, "#js-o-model", "first device")
        set_value(self.driver, "#js-o-malfunction", "first problem")

        # Click to open one more order from client and click it
        click_create_more(self.driver)

        # Wait for new order form to appear / sleep as a hack ;)
        time.sleep(1)
        wait_for_selector(self.driver, ".js-change-order-type")

        assert_client(self.driver, self, CLIENT_DATA1)

        set_value(self.driver, "#js-o-model", DEVICE_DATA['model'])
        set_value(self.driver, "#js-o-malfunction", DEVICE_DATA['malfunction'])

        save_order(self.driver)

        client_orders = self.driver.find_elements_by_xpath(
            make_text_xpath("span", CLIENT_DATA1['name'])
        )
        return self.assertEqual(len(client_orders), 2)


class CreateFromExistingOrder(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_create_more_orders(self):
        create_order(self.driver, CLIENT_DATA2)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_no_phone_client(self.driver, self, CLIENT_DATA2)


        # Click to create one more order
        click_create_more(self.driver)

        # Wait for new order form to appear / sleep as a hack ;)
        time.sleep(1)
        wait_for_selector(self.driver, ".js-change-order-type")

        assert_no_phone_client(self.driver, self, CLIENT_DATA2)

        set_value(self.driver, "#js-o-model", DEVICE_DATA['model'])
        set_value(self.driver, "#js-o-malfunction", DEVICE_DATA['malfunction'])

        save_order(self.driver)

        client_orders = self.driver.find_elements_by_xpath(
            make_text_xpath("span", CLIENT_DATA2['name'])
        )
        return self.assertEqual(len(client_orders), 2)


class CreateFromClosedOrder(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_create_one_more(self):
        create_order(self.driver, CLIENT_DATA3)
        change_status_from_table(self.driver, CLOSED_STATUS_INDEX)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_no_phone_client(self.driver, self, CLIENT_DATA3)

        # Click to create one more order
        create_one_more = 2
        click_create_more(self.driver, create_one_more)

        # Wait for new order form to appear / sleep as a hack ;)
        time.sleep(1)
        wait_for_selector(self.driver, ".js-change-order-type")

        assert_no_phone_client(self.driver, self, CLIENT_DATA3)

        set_value(self.driver, "#js-o-model", DEVICE_DATA['model'])
        set_value(self.driver, "#js-o-malfunction", DEVICE_DATA['malfunction'])

        save_order(self.driver)

        client_orders = self.driver.find_elements_by_xpath(
            make_text_xpath("span", CLIENT_DATA3['name'])
        )
        return self.assertEqual(len(client_orders), 2)

    def test_2_create_fee_order(self):
        create_order(self.driver, CLIENT_DATA4)
        change_status_from_table(self.driver, CLOSED_STATUS_INDEX)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_no_phone_client(self.driver, self, CLIENT_DATA4)

        # Click to create one more order
        click_create_more(self.driver)

        # Wait for new order form to appear / sleep as a hack ;)
        time.sleep(1)
        wait_for_selector(self.driver, ".js-change-order-type")

        assert_no_phone_client(self.driver, self, CLIENT_DATA4)

        set_value(self.driver, "#js-o-model", DEVICE_DATA['model'])
        set_value(self.driver, "#js-o-malfunction", DEVICE_DATA['malfunction'])

        save_order(self.driver)

        client_orders = self.driver.find_elements_by_xpath(
            make_text_xpath("span", CLIENT_DATA4['name'])
        )
        return self.assertEqual(len(client_orders), 2)

    def test_3_create_warranty_order(self):
        create_order(self.driver, CLIENT_DATA5)
        change_status_from_table(self.driver, CLOSED_STATUS_INDEX)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        assert_no_phone_client(self.driver, self, CLIENT_DATA5)

        # Click to create one more order
        warranty_order = 1
        click_create_more(self.driver, warranty_order)

        # Wait for new order form to appear / sleep as a hack ;)
        time.sleep(1)
        wait_for_selector(self.driver, ".js-change-order-type")

        assert_no_phone_client(self.driver, self, CLIENT_DATA5)

        set_value(self.driver, "#js-o-model", DEVICE_DATA['model'])
        set_value(self.driver, "#js-o-malfunction", DEVICE_DATA['malfunction'])

        save_order(self.driver)

        client_orders = self.driver.find_elements_by_xpath(
            make_text_xpath("span", CLIENT_DATA5['name'])
        )
        return self.assertEqual(len(client_orders), 2)
