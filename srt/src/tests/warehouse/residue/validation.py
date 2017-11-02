# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.dom import (
    find_element_by_selector, find_elements_by_selector, find_input_by_selector
)
from src.lib.errors import assert_has_error_tooltip
from src.lib.wait import wait_to_see_selector

from src.scaffolds.grid import wait_grid_changed_rows_num, wait_grid_updated
from src.scaffolds.dialog import open_dialog, close_dialog

from src.tests.warehouse.lib.select import search_and_select
from src.tests.warehouse.lib.create import create_posting


V_RESIDUE_DATA = {
    u'supplier' : {'name':u"Kortic Supplies"},
    u'title' : u"Bong",
    u'quantity' : u"4",
    u'price' : u"13.99",
}

SUBMIT_BTN = ".js-submit-dialog"
GRID_SEL = ".js-grid"


class ValidateResidue(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/residue")

    def test_0_create_residue(self):
        navigate(self.driver, "/app#!/warehouse/posting")
        create_posting(self.driver, V_RESIDUE_DATA)
        return True

    def test_1_no_name(self):
        search_and_select(self.driver, V_RESIDUE_DATA['title'])

        open_dialog(self.driver, ".js-edit-button", ".b-dialog_type_warehouse")

        wait_to_see_selector(self.driver, "#l-wh-title")
        title = find_input_by_selector(self.driver, "#l-wh-title")
        title.clear()

        find_element_by_selector(self.driver, SUBMIT_BTN).click()

        assert_has_error_tooltip(self.driver, title)
        return close_dialog(self.driver, ".js-close-dialog", ".b-dialog_type_warehouse")


    def test_2_validate_prices(self):
        search_and_select(self.driver, V_RESIDUE_DATA['title'])

        open_dialog(self.driver, ".js-edit-button", ".b-dialog_type_warehouse")

        wrong_data = [u"test", "   ", "", "-37"]

        price_input = ".h-price-field input"

        wait_to_see_selector(self.driver, price_input)
        price_list = find_elements_by_selector(self.driver, price_input)

        for price in price_list:
            for data in wrong_data:
                price.clear()
                price.send_keys(data)

                find_element_by_selector(self.driver, SUBMIT_BTN).click()
                assert_has_error_tooltip(self.driver, price)

        return close_dialog(self.driver, ".js-close-dialog", ".b-dialog_type_warehouse")


