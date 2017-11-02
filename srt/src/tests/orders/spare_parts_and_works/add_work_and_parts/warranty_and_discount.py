# ~*~ coding: utf-8 ~*~
import unittest
from selenium.webdriver.common.keys import Keys

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector
from src.lib.url import navigate, ORDERS_URL
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, close_order
from src.tests.orders.spare_parts_and_works.lib import TAB_SEL
from src.tests.orders.spare_parts_and_works.lib.service import (
    manual_add_new_srvc,
)
from src.tests.orders.spare_parts_and_works.lib.part import manual_add_new_part
from src.tests.orders.spare_parts_and_works.lib.edit import edit_final_discount
from src.tests.orders.spare_parts_and_works.lib.data import (
    data_f_srvc, data_f_part, data_f_edit_discount, RelationFromDiscountType,
    RelationFromFinalDiscount
)

rate = True
currency = False

class DiscauntTypeRateTests(unittest.TestCase):
    data_srvc = data_f_srvc(True, rate)
    rel = RelationFromDiscountType(data_srvc)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_srvc)

    def test1_check_price(self):
        STR_PRICE_SEL = ".js-price"
        in_grid = find_element_by_selector(self.driver, STR_PRICE_SEL).text
        must_be = self.rel.price()
        self.assertEqual(str(must_be), in_grid)

    def test2_check_amount(self):
        STR_AMOUNT_SEL = ".js-result"
        in_grid = find_element_by_selector(self.driver, STR_AMOUNT_SEL).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test3_check_final_price(self):
        FINAL_PRICE_SEL = ".js-total-sum"
        in_grid = find_element_by_selector(self.driver, FINAL_PRICE_SEL).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test4_check_final_discount(self):
        FINAL_DISCOUNT_RATE = ".js-total-discount"
        in_grid = find_element_by_selector(self.driver, FINAL_DISCOUNT_RATE).text
        must_be = self.rel.final_discount_rate()
        self.assertEqual(str(must_be), in_grid)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class DiscauntTypeCurrencyTests(unittest.TestCase):
    data_srvc = data_f_srvc(True, currency)
    rel = RelationFromDiscountType(data_srvc)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_srvc)

    def test1_check_price(self):
        str_price_sel = ".js-price"
        in_grid = find_element_by_selector(self.driver, str_price_sel).text
        must_be = self.rel.price()
        self.assertEqual(str(must_be), in_grid)

    def test2_check_amount(self):
        str_amount_sel = ".js-result"
        in_grid = find_element_by_selector(self.driver, str_amount_sel).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test3_check_final_price(self):
        final_price_sel = ".js-total-sum"
        in_grid = find_element_by_selector(self.driver, final_price_sel).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test4_check_final_discount(self):
        final_discount_rate = ".js-total-discount"
        in_grid = find_element_by_selector(self.driver, final_discount_rate).text
        must_be = self.rel.final_discount_rate()
        self.assertEqual(str(must_be), in_grid)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class FinalDiscauntTypeRateTests(unittest.TestCase):

    data_srvc = data_f_srvc()
    data_discount = data_f_edit_discount(rate, value=20)
    rel = RelationFromFinalDiscount(data_srvc,data_discount)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_srvc)
        edit_final_discount(cls.driver, cls.data_discount)

    def test1_check_price(self):
        str_price_sel = ".js-price"
        in_grid = find_element_by_selector(self.driver, str_price_sel).text
        must_be = self.rel.price()
        self.assertEqual(str(must_be), in_grid)

    def test2_check_amount(self):
        str_amount_sel = ".js-result"
        in_grid = find_element_by_selector(self.driver, str_amount_sel).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test3_check_final_price(self):
        final_price_sel = ".js-total-sum"
        in_grid = find_element_by_selector(self.driver, final_price_sel).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test4_check_final_discount(self):
        final_discount_rate = ".js-total-discount"
        in_grid = find_element_by_selector(self.driver, final_discount_rate).text
        must_be = self.rel.final_discount_rate()
        self.assertEqual(str(must_be), in_grid)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class FinalDiscauntTypeCurrencyTests(unittest.TestCase):
    data_srvc = data_f_srvc()
    data_discount = data_f_edit_discount(currency, value=20)
    rel = RelationFromFinalDiscount(data_srvc,data_discount)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_srvc)
        edit_final_discount(cls.driver, cls.data_discount)

    def test1_check_price(self):
        str_price_sel = ".js-price"
        in_grid = find_element_by_selector(self.driver, str_price_sel).text
        must_be = self.rel.price()
        self.assertEqual(str(must_be), in_grid)

    def test2_check_amount(self):
        str_amount_sel = ".js-result"
        in_grid = find_element_by_selector(self.driver, str_amount_sel).text
        must_be = self.rel.amount()
        self.assertEqual(str(must_be), in_grid)

    def test3_check_final_price(self):
        final_price_sel = ".js-total-sum"
        in_grid = find_element_by_selector(self.driver, final_price_sel).text
        must_be = self.rel.final_price()
        self.assertEqual(str(must_be), in_grid)

    def test4_check_final_discount(self):
        final_discount_rate = ".js-total-discount"
        in_grid = find_element_by_selector(self.driver, final_discount_rate).text
        must_be = self.rel.final_discount_rate()
        self.assertEqual(str(must_be), in_grid)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class TestForSomeStrWithDiscount(unittest.TestCase):

    data_srvc = data_f_srvc(True, rate)
    data_part = data_f_part(True, currency)
    rel_srvc = RelationFromDiscountType(data_srvc)
    rel_part = RelationFromDiscountType(data_part)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_srvc)
        manual_add_new_part(cls.driver, cls.data_part)

    def test1_check_final_price(self):
        final_price_sel = ".js-total-sum"
        in_grid = find_element_by_selector(self.driver, final_price_sel).text
        srvc_must_be = self.rel_srvc.final_price()
        part_must_be = self.rel_part.final_price()
        must_be = int(srvc_must_be)+int(part_must_be)
        self.assertEqual(str(must_be),in_grid.replace(' ',''))

    def test2_check_final_discount(self):
        final_discount_rate = ".js-total-discount"
        in_grid = find_element_by_selector(self.driver, final_discount_rate).text
        srvc_must_be = self.rel_srvc.final_discount_rate()
        part_must_be = self.rel_part.final_discount_rate()
        must_be = int(srvc_must_be) + int(float(part_must_be))
        self.assertEqual(str(must_be), in_grid)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)






