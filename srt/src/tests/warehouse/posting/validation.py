# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver, refresh
from src.lib.url import navigate, POSTING_URL, INVENTORY_URL
from src.lib.dom import find_element_by_selector, set_value, find_elements_by_selector
from src.lib.errors import assert_has_error_tooltip
from src.lib.randomizer import make_spare_part
from src.lib.wait import wait_for_selector, wait_to_click_selector

from src.scaffolds.dialog import open_dialog, close_dialog

from src.widget.client import fast_add_new_client

from src.tests.warehouse.lib import open_posting_dialog
from src.tests.warehouse.lib.create import create_local_stock
from src.tests.warehouse.lib.clean_up import clean_up_stock
from src.tests.warehouse.lib.set_data import add_to_posting, set_new_good


VALIDATION_DATA = {
    u'title' : u"Party Goose",
    u'quantity' : u"6",
    u'price' : u"100",}

SPARES_CATEGORY = 1
ADD_ITEM_BTN = ".b-dialog__content .btn-default"
SUPPLIER_SEL = "#js-wh-supplier"


class PostingValidationTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)

    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-dialog_type_warehouse")

    def test_1_no_text(self):
        # Validate Item block fields: title, quantity, cost
        open_posting_dialog(self.driver)

        title = find_element_by_selector(self.driver, "#js-wh-title")
        quantity = find_element_by_selector(self.driver, "#l-wh-quantity")
        cost = find_element_by_selector(self.driver, "#js-wh-price")
        quantity.clear()
        cost.clear()

        add_to_posting(self.driver)

        check_list = [title, quantity, cost]

        def assert_check_list(driver, check_list):
            for i in check_list:
                assert_has_error_tooltip(driver, i)

        return assert_check_list(self.driver, check_list)

    def test_2_no_category_chosen(self):
        open_posting_dialog(self.driver)
        set_value(self.driver, "#js-wh-title", make_spare_part())

        # click away for category block to appear
        find_element_by_selector(self.driver, "#l-wh-quantity").click()

        wait_to_click_selector(self.driver, ".js-barcodes")
        category = find_element_by_selector(self.driver, ".js-c-categories")
        add_to_posting(self.driver)

        return assert_has_error_tooltip(self.driver, category)

    def test_3_text_for_nums(self):
        open_posting_dialog(self.driver)
        quantity = find_element_by_selector(self.driver, "#l-wh-quantity")
        cost = find_element_by_selector(self.driver, "#js-wh-price")

        set_value(self.driver, "#l-wh-quantity", "test")
        set_value(self.driver, "#js-wh-price", "test")

        add_to_posting(self.driver)

        check_list = [quantity, cost]

        def assert_check_list(driver, check_list):
            for i in check_list:
                assert_has_error_tooltip(driver, i)

        return assert_check_list(self.driver, check_list)

    def test_4_negative_nums(self):
        open_posting_dialog(self.driver)
        cost = find_element_by_selector(self.driver, "#js-wh-price")
        quantity = find_element_by_selector(self.driver, "#l-wh-quantity")

        negative_num = "-56"
        set_value(self.driver, "#js-wh-price", negative_num)
        set_value(self.driver, "#l-wh-quantity", negative_num)

        add_to_posting(self.driver)
        assert_has_error_tooltip(self.driver, cost)
        assert_has_error_tooltip(self.driver, quantity)

    def test_5_no_supplier(self):
        open_posting_dialog(self.driver)

        find_element_by_selector(self.driver, ".js-save-btn").click()
        supplier = find_element_by_selector(self.driver, SUPPLIER_SEL)

        return assert_has_error_tooltip(self.driver, supplier)

    def test_6_no_items_added(self):
        open_posting_dialog(self.driver)

        fast_add_new_client(self.driver, SUPPLIER_SEL)
        find_element_by_selector(self.driver, ".js-save-btn").click()

        items = find_element_by_selector(self.driver, ".b-dialog__content table")
        return assert_has_error_tooltip(self.driver, items)

    def test_7_price_input_validation(self):
        open_posting_dialog(self.driver)

        wrong_data = [u"test", "   ", "", "-56"]

        price_input = ".h-price-field input"
        price_list = find_elements_by_selector(self.driver, price_input)

        for price in price_list:
            for data in wrong_data:
                price.clear()
                price.send_keys(data)

                add_to_posting(self.driver)
                assert_has_error_tooltip(self.driver, price)

        return True


class PostingChooseStockValidationTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_stock(self):
        navigate(self.driver, INVENTORY_URL)
        create_local_stock(self.driver)
        refresh()
        return True

    def test_1_no_stock_chosen(self):
        navigate(self.driver, POSTING_URL)

        open_posting_dialog(self.driver)
        fast_add_new_client(self.driver, SUPPLIER_SEL)
        set_new_good(self.driver, VALIDATION_DATA, SPARES_CATEGORY)

        find_element_by_selector(self.driver, ".js-save-btn").click()
        stock = find_element_by_selector(self.driver, ".js-warehouses")

        assert_has_error_tooltip(self.driver, stock)
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog_type_warehouse")
        return True

    def test_2_clean_up_stocks(self):
        navigate(self.driver, INVENTORY_URL)
        clean_up_stock(self.driver)
        return True
