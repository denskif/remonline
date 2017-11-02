# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.dom import find_element_by_selector, find_elements_by_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.scaffolds.dropdown import choose_from_select

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.open import open_order, open_tab, TAB_INFO
from src.tests.orders.lib.filter import (
    open_filter, close_filter, reset_filter, click_filter_btn,
    enable_all_checkboxes, disable_all_checkboxes, add_column, F_CHECK_BOX_SEL,
)


FIRST_ROW_CELL_SEL = "tbody td"

F_BTN_IDX = 3
ENGINEER_CLN_SEL = "[data-field=engineer]"
ENGINEER_CELL_SEL = "tbody tr td:nth-child(12)"
ENGINEER_FIRST_BOX = ".b-popup__body span:nth-child(3)"
ENGINEER_SEL = ".js-engineer"
ENGINEER_IDX = 1


class FilterEngineerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        open_filter(cls.driver)

    def test_1_on_off_engineer(self):
        click_filter_btn(self.driver, F_BTN_IDX)
        disable_all_checkboxes(self.driver)
        wait_selector_to_disappear(self.driver, FIRST_ROW_CELL_SEL)
        enable_all_checkboxes(self.driver)
        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        return True

    def test_2_engineer_filters(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        choose_from_select(self.driver, ENGINEER_SEL, ENGINEER_IDX)
        save_order(self.driver)

        add_column(self.driver, ENGINEER_CLN_SEL)
        click_filter_btn(self.driver, F_BTN_IDX)
        disable_all_checkboxes(self.driver)

        find_element_by_selector(
            self.driver, F_CHECK_BOX_SEL, ENGINEER_IDX
        ).click()
        engineer = find_element_by_selector(
            self.driver, ENGINEER_FIRST_BOX, ENGINEER_IDX
        ).text

        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        rows = find_elements_by_selector(self.driver, ENGINEER_CELL_SEL)

        engineers = []
        [engineers.append(row.text) for row in rows]
        return [self.assertEqual(engineer, elem) for elem in engineers]

    @classmethod
    def tearDownClass(cls):
        reset_filter(cls.driver)
        close_filter(cls.driver)
