# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import (
    open_order, open_tab, TAB_WORKS, TAB_PAYMENTS, close_order
)
from src.tests.orders.spare_parts_and_works.lib.part import manual_add_new_part
from src.tests.orders.lib.status import (
    change_status_in_order, change_status_from_table, close_and_pay_from_table,
    close_and_pay_from_order
)
from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.payments import create_order_income

from src.scaffolds.dialog import close_dialog


WORK1 = {'name':'Cool work', 'quantity':'3', 'price':'555.2'}
WORK2 = {'name':'Cool work', 'quantity':'3', 'price':'350'}
DATA = {'price': "500",}

CLOSED_STATUS_INDEX = -1
MAIN_CASHBOX_INDEX = 1


class StatusClosedFromOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)


    def setUp(self):
        create_order(self.driver)
        open_order(self.driver)


    def test_1_close_order_with_zero_price(self):
        change_status_in_order(self.driver, CLOSED_STATUS_INDEX)
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")


    def test_2_close_order_with_payment(self):
        open_tab(self.driver, TAB_WORKS)
        manual_add_new_part(self.driver)
        close_and_pay_from_order(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")


    def test_3_close_order_with_overpayment(self):
        open_tab(self.driver, TAB_PAYMENTS)
        create_order_income(self.driver, DATA)

        open_tab(self.driver, TAB_WORKS)
        manual_add_new_part(self.driver)

        close_and_pay_from_order(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")


class StatusClosedFromTableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)


    def setUp(self):
        create_order(self.driver)


    def test_1_close_order_with_zero_price(self):
        return change_status_from_table(self.driver, CLOSED_STATUS_INDEX)


    def test_2_close_with_payment(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        manual_add_new_part(self.driver)
        save_order(self.driver)
        return close_and_pay_from_table(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )


    def test_3_close_with_overpayment(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_PAYMENTS)
        create_order_income(self.driver, DATA)

        open_tab(self.driver, TAB_WORKS)
        manual_add_new_part(self.driver)
        close_order(self.driver)

        close_and_pay_from_table(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )
        return True
