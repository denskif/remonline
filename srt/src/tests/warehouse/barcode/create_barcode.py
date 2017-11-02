# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, INVENTORY_URL
from src.lib.errors import assert_has_error_tooltip
from src.lib.dom import (
    find_element_by_selector, get_value, find_element_by_xpath, set_value
)
from src.lib.formatting import make_text_xpath
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.scaffolds.dropdown import (
    choose_from_select, choose_select_by_text, choose_category, choose_stock,
)

from src.widget.client import fast_add_new_client

from src.tests.warehouse.lib import (
    open_residue_dialog, close_residue_dialog, open_barcode_dialog,
    close_barcode_dialog, BARCODE_TYPE_SEL, BARCODE_INPUT_SEL, GENERATE_BC_SEL,
    open_posting_dialog,
)
from src.tests.warehouse.lib.create import create_posting, create_barcode
from src.tests.warehouse.lib.select import search_and_select
from src.tests.warehouse.lib.set_data import add_to_posting
from src.tests.warehouse.lib.save_trans import save_posting


ITEM_FOR_BARCODE = {
    u'supplier' : {'name': u"Barracuda Supplies"},
    u'title' : u"Belaya Akula",
    u'quantity' : u"3",
    u'price' : u"17800",
}
ITEM_FOR_GENERATING_BARCODE = {
    u'supplier' : {'name': u"Octopus Supplies"},
    u'title' : u"Sevriuga",
    u'quantity' : u"3",
    u'price' : u"13800",
}
ITEM_FOR_CREATING_BARCODE = {
    u'supplier' : {'name': u"Dogfish Supplies"},
    u'title' : u"Beluga",
    u'quantity' : u"3",
    u'price' : u"14700",
}
POSTING_BARCODE_DATA = {
    u'supplier' : {'name': u"Barracuda Supplies"},
    u'title' : u"Vosminog",
    u'quantity' : u"6",
    u'price' : u"8999",
}


SUBMIT_BTN_IDX = 1
STOCK_IDX = 1
SPARES_CATEGORY = 1

EAN_13_TEXT = "EAN-13"
EAN_8_TEXT = "EAN-8"

BARCODE_SEL = ".js-edit-barcode"


class ValidateBarcode(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_item(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, ITEM_FOR_BARCODE)
        return True

    def test_1_no_data_set(self):
        navigate(self.driver, INVENTORY_URL)
        search_and_select(self.driver, ITEM_FOR_BARCODE['title'])

        open_residue_dialog(self.driver)
        open_barcode_dialog(self.driver)

        find_element_by_selector(
            self.driver, ".b-dialog .js-submit-dialog", idx=SUBMIT_BTN_IDX
        ).click()

        code = find_element_by_selector(self.driver, BARCODE_INPUT_SEL)
        assert_has_error_tooltip(self.driver, code)

        # Clean up
        close_barcode_dialog(self.driver, idx=SUBMIT_BTN_IDX)
        return close_residue_dialog(self.driver)


class GenerateBarcode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, ITEM_FOR_GENERATING_BARCODE)
        navigate(cls.driver, INVENTORY_URL)
        search_and_select(cls.driver, ITEM_FOR_GENERATING_BARCODE['title'])
        open_residue_dialog(cls.driver)
        open_barcode_dialog(cls.driver)

    def test_1_change_type(self):
        type_dropdown = find_element_by_selector(self.driver, BARCODE_TYPE_SEL)
        old_type = get_value(type_dropdown)
        choose_from_select(self.driver, BARCODE_TYPE_SEL)
        new_type = get_value(type_dropdown)

        return self.assertNotEqual(old_type, new_type)

    def test_2_generate_ean_13(self):
        choose_select_by_text(self.driver, BARCODE_TYPE_SEL, EAN_13_TEXT)

        find_element_by_selector(self.driver, GENERATE_BC_SEL).click()

        time.sleep(1)
        ean_13_code = get_value(
            find_element_by_selector(self.driver, BARCODE_INPUT_SEL)
        )
        ean_13_code_length = 13
        return self.assertEqual(len(ean_13_code), ean_13_code_length)

    def test_3_clean_input_by_type_change(self):
        choose_from_select(self.driver, BARCODE_TYPE_SEL)

        code_value = get_value(
            find_element_by_selector(self.driver, BARCODE_INPUT_SEL)
        )
        return self.assertEqual(len(code_value), 0)

    def test_4_generate_ean_8(self):
        choose_select_by_text(self.driver, BARCODE_TYPE_SEL, EAN_8_TEXT)

        find_element_by_selector(self.driver, GENERATE_BC_SEL).click()

        time.sleep(1)
        ean_8_code = get_value(
            find_element_by_selector(self.driver, BARCODE_INPUT_SEL)
        )
        ean_8_code_length = 8
        return self.assertEqual(len(ean_8_code), ean_8_code_length)

    @classmethod
    def tearDownClass(cls):
        close_barcode_dialog(cls.driver, idx=SUBMIT_BTN_IDX)
        close_residue_dialog(cls.driver)


class CreateBarcode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, ITEM_FOR_CREATING_BARCODE)
        navigate(cls.driver, INVENTORY_URL)
        search_and_select(cls.driver, ITEM_FOR_CREATING_BARCODE['title'])
        open_residue_dialog(cls.driver)

    def test_1_create_ean_13(self):
        ean_13_code = create_barcode(
            self.driver, EAN_13_TEXT, SUBMIT_BTN_IDX)

        ean_13_xpath = find_element_by_xpath(
            self.driver, make_text_xpath("div", ean_13_code)
        )

        return self.assertTrue(ean_13_xpath.is_displayed())

    def test_2_create_ean_8(self):
        ean_8_code = create_barcode(
            self.driver, EAN_8_TEXT, SUBMIT_BTN_IDX)

        ean_8_xpath = find_element_by_xpath(
            self.driver, make_text_xpath("div", ean_8_code)
        )

        return self.assertTrue(ean_8_xpath.is_displayed())

    @classmethod
    def tearDownClass(cls):
        close_residue_dialog(cls.driver)


class CreatePostingBarcode(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_1_create_item_with_ean_13(self):
        # Create Barcode while posting item
        navigate(self.driver, POSTING_URL)
        open_posting_dialog(self.driver)
        choose_stock(self.driver, STOCK_IDX)

        set_value(self.driver, "#js-wh-title", POSTING_BARCODE_DATA['title'])
        fast_add_new_client(
            self.driver,
            "#js-wh-supplier",
            POSTING_BARCODE_DATA['supplier']
        )

        choose_category(self.driver, SPARES_CATEGORY)

        set_value(self.driver, "#l-wh-quantity", POSTING_BARCODE_DATA['quantity'])
        set_value(self.driver, "#js-wh-price", POSTING_BARCODE_DATA['price'])

        ean_13_code = create_barcode(self.driver, EAN_13_TEXT)

        add_to_posting(self.driver)
        wait_selector_to_disappear(self.driver, ".js-c-categories")
        wait_to_see_selector(self.driver, ".b-dialog_type_warehouse .js-grid tbody")

        save_posting(self.driver)

        # Find barcode in the item card and assert the result
        navigate(self.driver, INVENTORY_URL)

        search_and_select(self.driver, POSTING_BARCODE_DATA['title'])
        open_residue_dialog(self.driver)

        wait_to_see_selector(self.driver, BARCODE_SEL)
        result_code = find_element_by_selector(self.driver, BARCODE_SEL).text

        return self.assertEqual(result_code, ean_13_code)

    @classmethod
    def tearDown(cls):
        close_residue_dialog(cls.driver)
