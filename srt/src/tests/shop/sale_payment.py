# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, SHOP_URL, CASHBOX_URL
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_for_selector, wait_selector_to_disappear, wait_to_click_selector

from src.tests.warehouse.lib.create import create_posting

from src.tests.shop.lib import (
    close_sale_payment_dialog_via_mask, close_sale_dialog, close_sale_payment_dialog, open_sale_payment_dialog,
    SALE_CODE_SEL, CASHBOX_DIALOG_SEL
)

from src.tests.shop.lib.sale import prepare_sale, pay_for_sale, set_sale_discount


GOODS = {
    u'title' : u"Topor Drovosek",
    u'supplier' : {'name': u"Magical Supplies"},
    u'quantity' : u"13",
    u'price' : u"756",
}

GOODS1 = {
    u'title' : u"Topor Drovoseka",
    u'supplier' : {'name': u"Magical Suppliess"},
    u'quantity' : u"12",
    u'price' : u"755",
}

DISCOUNT = "7" # percent
SHOP_FIRST_ROW_SEL = ".js-shop-grid tbody tr td"
BOX_FIRST_ROW_SEL = ".js-report-grid tbody td"
T_PRICE_CELL_IDX = 6
SALE_L_SEL = ".js-sale-link"
SELL_BUTTON = ".js-submit-dialog"
CLOSE_PAYMENT_BUTTON = ".js-cbp-cancel"
CLOSE_SELL_BUTTON = ".js-close-dialog"
INCOME_CELL = 2


class SalePayment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, GOODS)

    def setUp(self):
        navigate(self.driver, SHOP_URL)
        prepare_sale(self.driver, GOODS['title'])

    def test_1_sale_with_discount(self):
        set_sale_discount(self.driver, DISCOUNT)
        price = find_element_by_selector(self.driver, "tbody .js-price").text
        pay_for_sale(self.driver)
        price_in_table = find_element_by_selector(
            self.driver, SHOP_FIRST_ROW_SEL, T_PRICE_CELL_IDX
        ).text
        return self.assertEqual(price, price_in_table)

    def test_2_check_payment_in_cashbox(self):
        pay_for_sale(self.driver)
        sale_code = find_element_by_selector(self.driver, SALE_CODE_SEL).text
        sale_price = find_element_by_selector(
            self.driver, SHOP_FIRST_ROW_SEL, T_PRICE_CELL_IDX
        ).text
        navigate(self.driver, CASHBOX_URL)
        wait_for_selector(self.driver, BOX_FIRST_ROW_SEL)

        income = find_element_by_selector(
            self.driver, BOX_FIRST_ROW_SEL, INCOME_CELL
        ).text

        wait_for_selector(self.driver, SALE_L_SEL)
        sale_in_box = find_element_by_selector(
            self.driver, SALE_L_SEL
        ).text

        self.assertEqual(income, sale_price)
        return self.assertTrue(sale_code in sale_in_box)


class ClosePaymentDialog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, GOODS1)
        navigate(cls.driver, SHOP_URL)
        prepare_sale(cls.driver, GOODS['title'])

    def setUp(self):
        wait_to_click_selector(self.driver, SELL_BUTTON)
        open_sale_payment_dialog(self.driver)

    def test_1_close_dialog_via_mask(self):
        close_sale_payment_dialog_via_mask(self.driver)
        wait_selector_to_disappear(self.driver, CASHBOX_DIALOG_SEL)

    def test_2_close_dialog(self):
        close_sale_payment_dialog(self.driver)

    @classmethod
    def tearDownClass(cls):
        close_sale_dialog(cls.driver)

