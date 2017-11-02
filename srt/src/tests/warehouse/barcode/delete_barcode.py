# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, INVENTORY_URL
from src.lib.dom import find_element_by_xpath, find_element_by_selector
from src.lib.formatting import make_text_xpath
from src.lib.wait import wait_selector_to_disappear

from src.tests.warehouse.lib import (
    open_residue_dialog, open_edit_barcode, BARCODE_TYPE_SEL, BARCODE_DIALOG_SEL,
    close_residue_dialog,
)
from src.tests.warehouse.lib.create import create_posting, create_barcode
from src.tests.warehouse.lib.select import search_and_select
from src.tests.warehouse.lib.clean_up import delete_barcode


ITEM_FOR_BARCODE = {
    u'supplier' : {'name': u"Barracuda Supplies"},
    u'title' : u"riba Kloun",
    u'quantity' : u"10",
    u'price' : u"850",
}

BARCODE_BTN_IDX = 1

EAN_13_TEXT = "EAN-13"
EAN_8_TEXT = "EAN-8"

BARCODE_SEL = ".js-edit-barcode"


class RemoveBarcode(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_1_create_item(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, ITEM_FOR_BARCODE)
        return True

    def test_2_remove_ean_13_barcode(self):
        search_and_select(self.driver, ITEM_FOR_BARCODE['title'])
        open_residue_dialog(self.driver)

        code = create_barcode(self.driver, EAN_13_TEXT, BARCODE_BTN_IDX)

        open_edit_barcode(self.driver, code)
        delete_barcode(self.driver, BARCODE_BTN_IDX)

        wait_selector_to_disappear(self.driver, BARCODE_SEL)

        return close_residue_dialog(self.driver)

    def test_3_remove_ean_8_barcode(self):
        search_and_select(self.driver, ITEM_FOR_BARCODE['title'])
        open_residue_dialog(self.driver)

        code = create_barcode(self.driver, EAN_8_TEXT, BARCODE_BTN_IDX)

        open_edit_barcode(self.driver, code)
        delete_barcode(self.driver, BARCODE_BTN_IDX)

        wait_selector_to_disappear(self.driver, BARCODE_SEL)

        return close_residue_dialog(self.driver)
