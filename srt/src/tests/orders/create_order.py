# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.wait import wait_selector_to_disappear, wait_for_selector
from src.lib.dom import find_element_by_selector
from src.lib.formatting import format_phone_ua

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order
from src.tests.orders.lib.delete import delete_order

from src.scaffolds.dialog import open_dialog, close_dialog


CUSTOMER_DATA = {
    'name': u"Mr Psycho",
    'email': u"psy@co.com",
    'address': u"Mallholand Drive 15",
    'model': u"bombaster device",
    'malfunction': u"actually not working",
}
PHONE_SEL = "tbody td:nth-child(10) .h-c-muted"


class CreateOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")
        wait_selector_to_disappear(cls.driver, ".reveal-modal-bg")

    def test_1_open_close_order(self):
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")
        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True

    def test_2_create_order(self):
        phone_number = create_order(self.driver, CUSTOMER_DATA)
        new_phone = format_phone_ua(phone_number)
        client_phone = find_element_by_selector(self.driver, PHONE_SEL).text
        return self.assertEqual(new_phone, client_phone)


    def test_3_delete_order(self):
        order_id = find_element_by_selector(
            self.driver, "tbody tr [data-order-id]"
        ).get_attribute("data-order-id")
        open_order(self.driver)
        delete_order(self.driver)

        def _make_sel(data):
            return "[data-order-id=%s]" % (data)

        return wait_selector_to_disappear(self.driver, _make_sel(order_id))

