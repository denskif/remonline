# ~*~ coding: utf-8 ~*~

import unittest, time

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL, BRANCH_URL, PRICE_AND_DISCOUNT
from src.lib.wait import wait_for_selector
from src.tests.orders.lib.status import change_status_in_order_new
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_tab, open_order, TAB_PAYMENTS, open_position_in_order, open_widget_discont
from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc
from src.tests.orders.spare_parts_and_works.lib.data import (
    data_f_srvc
)
from src.tests.orders.spare_parts_and_works.lib.winbox import get_type_discount, close_winbox, save_change
from src.tests.settings.lib import chose_section, PRICE_AND_DISCOUNT
from src.tests.settings.lib.price_and_discount import get_value_discount



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


class ChangeDiscount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, BRANCH_URL)
        chose_section(cls.driver, PRICE_AND_DISCOUNT)
        time.sleep(1)

    def test_1_value_discount(self):
        discountSet = get_value_discount(self.driver)
        print discountSet
        navigate(self.driver, ORDERS_URL)
        create_order(self.driver, CUSTOMER_DATA)
        open_order(self.driver)
        data = data_f_srvc()
        manual_add_new_srvc(self.driver, data)
        time.sleep(2)
        open_position_in_order(self.driver)
        time.sleep(1)
        discountOrd = get_type_discount(self.driver)
        print discountOrd
        time.sleep(1)
        save_change(self.driver)
        #close_winbox(self.driver)
        time.sleep(1)
        open_widget_discont(self.driver)
        time.sleep(1)
        discountWid = get_type_discount(self.driver)
        print discountWid
        time.sleep(1)
        close_winbox(self.driver)
        time.sleep(1)































