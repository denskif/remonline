# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, INVENTORY_URL
from src.lib.dom import (
    find_element_by_selector, find_input_by_selector, get_value, make_selector,
    find_elements_by_selector,
)
from src.lib.errors import assert_has_error_tooltip
from src.lib.wait import wait_for_selector

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import choose_stock_by_name

from src.tests.warehouse.lib.create import (
    create_local_stock, create_global_stock, make_stock_name
)


class CreateStock(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_0_stock_dialog(self):
        # Close by clicking away
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #l-wh-title")
        close_dialog(self.driver, ".h-dialog-mask", ".b-dialog")

        # Close by clicking "close" button
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #l-wh-title")
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog")
        return True

    def test_1_no_name(self):
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #l-wh-title")

        stock_name = find_element_by_selector(self.driver, "#l-wh-title")
        stock_name.clear()

        find_element_by_selector(self.driver, ".js-submit-dialog").click()

        return assert_has_error_tooltip(self.driver, stock_name)

    def test_2_switch_stock_type(self):
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #l-wh-title")

        find_element_by_selector(
            self.driver, "[for=l-wh-type-global] span"
        ).click()

        global_radio_btn = find_input_by_selector(
            self.driver, "#l-wh-type-global"
        )

        self.assertTrue(global_radio_btn.is_selected())

        find_element_by_selector(
            self.driver, "[for=l-wh-type-local] span"
        ).click()

        local_radio_btn = find_input_by_selector(
            self.driver, "#l-wh-type-local"
        )

        return self.assertTrue(local_radio_btn.is_selected())

    def test_3_create_local_stock(self):
        create_local_stock(self.driver)
        return True

    def test_4_create_global_stock(self):
        create_global_stock(self.driver)
        return True

    def test_5_choose_stock_from_dropdown(self):
        stock_name = make_stock_name()

        create_local_stock(self.driver, stock_name)
        create_local_stock(self.driver)

        choose_stock_by_name(self.driver, stock_name)

        chosen_stock = get_value(find_element_by_selector(
            self.driver, ".js-warehouses [name=warehouse]"
        ))

        result = []
        Success = 1
        Fail = 0
        for i in find_elements_by_selector(self.driver, ".js-warehouses option"):
            if get_value(i) ==  chosen_stock:
                result.append(Success)
            else:
                result.append(Fail)

        return self.assertTrue(Success in result)
