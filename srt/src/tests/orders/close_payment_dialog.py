# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.wait import wait_for_selector
from src.tests.orders.lib.status import change_status_in_order_new
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_tab, open_order, TAB_PAYMENTS
from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc
from src.tests.orders.spare_parts_and_works.lib.data import (
    data_f_srvc
)
from src.scaffolds.dialog import close_dialog, close_dialog_via_mask

CUSTOMER_DATA = {
    'name': u"Mr Psycho",
    'email': u"psy@co.com",
    'address': u"Mallholand Drive 15",
    'model': u"bombaster device",
    'malfunction': u"actually not working",
}

PAYMENT_DIALOG = ".b-dialog_type_cashbox"
ORDER_DIALOG = ".b-order__wrapper"
CLOSE_PAYMENT_BUTTON = '.js-cbp-cancel'
CLOSE_ORDER_BUTTON = '.js-close-dialog'
STATUS_IN_CLOSE_INDEX = 4


class ClosePaymentDialog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver, CUSTOMER_DATA)
        open_order(cls.driver)
        data = data_f_srvc()
        manual_add_new_srvc(cls.driver, data)
        open_tab(cls.driver, TAB_PAYMENTS)

    def setUp(self):
        change_status_in_order_new(self.driver, STATUS_IN_CLOSE_INDEX)

    def test_1_close_dialog_via_button(self):
        close_dialog(self.driver, CLOSE_PAYMENT_BUTTON, PAYMENT_DIALOG)
        return True

    def test_2_close_dialog_via_mask(self):
        close_dialog_via_mask(self.driver, CLOSE_PAYMENT_BUTTON)
        return wait_for_selector(self.driver, PAYMENT_DIALOG)

    @classmethod
    def tearDownClass(cls):
        close_dialog(cls.driver, CLOSE_PAYMENT_BUTTON, PAYMENT_DIALOG)
        close_dialog(cls.driver, CLOSE_ORDER_BUTTON, ORDER_DIALOG)