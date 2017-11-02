# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, INVENTORY_URL
from src.lib.dom import set_value, find_element_by_selector
from src.lib.errors import assert_has_error_tooltip

from src.scaffolds.dialog import open_dialog, close_dialog

from src.tests.warehouse.lib.create import (
    create_global_stock, create_local_stock, make_stock_name
)

STOCK_SEL = ".js-warehouses [name=warehouse]"


class EditStock(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_0_edit_dialog(self):
        # Close by clicking away
        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")
        close_dialog(self.driver, ".h-dialog-mask", ".b-dialog")

        # Close by clicking "close" button
        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog")
        return True

    def test_1_no_name(self):
        create_local_stock(self.driver)

        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")

        stock_name = find_element_by_selector(self.driver, "#l-wh-title")
        stock_name.clear()

        find_element_by_selector(self.driver, ".js-submit-dialog").click()

        return assert_has_error_tooltip(self.driver, stock_name)

    def test_2_change_name(self):
        create_local_stock(self.driver)
        new_name = make_stock_name()

        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")
        set_value(self.driver, "#l-wh-title", new_name)

        close_dialog(self.driver, ".js-submit-dialog", ".js-submit-dialog")
        stock_name = find_element_by_selector(self.driver, STOCK_SEL).text

        return self.assertTrue(new_name in stock_name)

    def test_3_edit_stock_local(self):
        stock_name = make_stock_name()

        create_global_stock(self.driver, stock_name)
        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")

        find_element_by_selector(
            self.driver, "[for=l-wh-type-local] span"
        ).click()

        close_dialog(self.driver, ".js-submit-dialog", ".js-submit-dialog")

        edited_stock = find_element_by_selector(self.driver, STOCK_SEL).text

        self.assertTrue(stock_name in edited_stock)
        return self.assertEqual(len(edited_stock.split()) > 1, True)

    def test_4_edit_stock_global(self):
        stock_name = make_stock_name()

        create_local_stock(self.driver, stock_name)
        open_dialog(self.driver, ".js-wh-edit", ".b-dialog #l-wh-title")

        find_element_by_selector(
            self.driver, "[for=l-wh-type-global] span"
        ).click()

        close_dialog(self.driver, ".js-submit-dialog", ".js-submit-dialog")

        edited_stock = find_element_by_selector(self.driver, STOCK_SEL).text

        self.assertTrue(stock_name in edited_stock)
        return self.assertEqual(len(edited_stock.split()) > 1, True)
