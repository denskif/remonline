# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_to_see_selector
from src.lib.url import navigate, ORDERS_URL, go_to_cashbox

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, close_order
from src.tests.orders.spare_parts_and_works.lib import TAB_SEL
from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc
from src.tests.orders.spare_parts_and_works.lib.data import data_f_srvc
from src.tests.orders.lib.payments import (
    create_order_income, create_order_outcome
)

from src.tests.cashflow.lib.transactions import delete_transaction_from_cashbox

PRICE = {
    'price': u"100",
    }
PRICE_IN = {
    'price': u"20",
    }
PRICE_OUT = {
    'price': u"40",
    }

COMMENT_STR_SEL = ".js-order-payments .b-table__tr .h-m-0"
PAYMENTS_TAB = ".b-dialog .i-finance"
EMPTY_TABLE_SEL = ".b-table__sub"
ORDER_NUMBER_IN_GID = ".h-branch-1[data-order-id]"
PRICE_LABEL_SEL = ".b-table__td [data-bind~=priceLabel]"



class CreateOrderPaymentsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        cls.order_number = find_element_by_selector(
            cls.driver, ORDER_NUMBER_IN_GID, idx=0
        ).text
        open_order(cls.driver)
        wait_to_see_selector(cls.driver, TAB_SEL)

    def setUp(self):
        open_tab(self.driver, PAYMENTS_TAB)

    def test1_create_income(self):
        create_order_income(self.driver, PRICE)
        wait_to_see_selector(self.driver, ".js-table-row .h-c-green")

        find_element_by_selector(self.driver, ".b-table__body")
        payment_comment = find_element_by_selector(
            self.driver, COMMENT_STR_SEL
        ).text
        self.assertIn(self.order_number, payment_comment)

    def test2_create_outcome(self):
        create_order_outcome(self.driver, PRICE)
        wait_to_see_selector(self.driver, ".js-table-row .h-c-red")

        find_element_by_selector(self.driver, ".b-table__body ")
        payment_comment = find_element_by_selector(
            self.driver, COMMENT_STR_SEL
        ).text
        self.assertIn(self.order_number, payment_comment)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class DeleteOrderTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        cls.order_numer = find_element_by_selector(
            cls.driver, ORDER_NUMBER_IN_GID, idx=0
        ).text
        open_order(cls.driver)
        find_element_by_selector(cls.driver, PAYMENTS_TAB).click()
        create_order_income(cls.driver, PRICE)
        close_order(cls.driver)

    def test1_delete_transaction(self):
        go_to_cashbox(self.driver)
        wait_to_see_selector(self.driver, ".h-cashbox-report .k-grid-content")
        delete_transaction_from_cashbox(self.driver)
        navigate(self.driver, ORDERS_URL)
        open_order(self.driver)
        open_tab(self.driver, PAYMENTS_TAB)
        wait_to_see_selector(self.driver, EMPTY_TABLE_SEL)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class ValidateCalculationOrderPayments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.srvc_data = data_f_srvc()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        cls.order_numer = find_element_by_selector(
            cls.driver, ORDER_NUMBER_IN_GID, idx=0
        ).text
        open_order(cls.driver)
        wait_to_see_selector(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.srvc_data)
        cls.in_widget = find_element_by_selector(
            cls.driver, ".js-total-sum"
        ).text
        find_element_by_selector(cls.driver, PAYMENTS_TAB).click()
        create_order_income(cls.driver, PRICE_IN)
        create_order_outcome(cls.driver, PRICE_OUT)

    def test1_check_total_payments(self):
        payed_label_sel = ".b-table__td [data-bind~=payedLabel]"
        in_grid = find_element_by_selector(self.driver, payed_label_sel).text
        must_be = int(PRICE_IN['price']) - int(PRICE_OUT['price'])
        self.assertEqual(in_grid, str(must_be))

    def test2_check_order_sum(self):
        in_grid = find_element_by_selector(self.driver, PRICE_LABEL_SEL).text
        oprder_sum_in_footer = find_element_by_selector(
            self.driver,".js-order-payment-info .h-m-0"
        ).text
        self.assertIn(in_grid, oprder_sum_in_footer and self.in_widget)

    def test3_check_debt(self):
        order_sum = int(find_element_by_selector(
            self.driver, PRICE_LABEL_SEL
        ).text)
        in_grid = find_element_by_selector(self.driver, ".js-order-debt-wp").text
        must_be = order_sum + int(PRICE_OUT['price']) - int(PRICE_IN['price'])
        self.assertEqual(in_grid, str(must_be))

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)
