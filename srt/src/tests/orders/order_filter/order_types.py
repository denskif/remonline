# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.dom import (
    find_element_by_selector, make_selector, find_elements_by_selector
)
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.filter import (
    open_filter, close_filter, reset_filter, click_filter_btn,
    enable_all_checkboxes, disable_all_checkboxes, add_column, F_CHECK_BOX_SEL
)


FIRST_ROW_CELL_SEL = "tbody td"

ORDER_TYPE_F_IDX = 1
ORDER_TYPE_CLN_SEL = "[data-field=order_type]"
ORDER_TYPE_FIRST_BOX = ".b-popup__body span:nth-child(3)"

#    Grid has stale position for each column
#    it just doesn't display some columns on its private configuration
#    thats why we use nth-child(18) - stale index for order_type column
ORDER_TYPE_CELL_SEL = "tbody tr td:nth-child(19)"



class FilterOrderTypeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        open_filter(cls.driver)

    def test_1_on_off_types(self):
        click_filter_btn(self.driver, ORDER_TYPE_F_IDX)
        disable_all_checkboxes(self.driver)
        wait_selector_to_disappear(self.driver, FIRST_ROW_CELL_SEL)
        enable_all_checkboxes(self.driver)
        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        return True

    def test_2_type_filters(self):
        # Add order type column to the grid
        add_column(self.driver, ORDER_TYPE_CLN_SEL)

        # Filter by order type
        click_filter_btn(self.driver, ORDER_TYPE_F_IDX)
        disable_all_checkboxes(self.driver)
        find_element_by_selector(self.driver, F_CHECK_BOX_SEL).click()

        # Collect filtering order type
        type_enabled = find_element_by_selector(
            self.driver, ORDER_TYPE_FIRST_BOX
        ).text

        # Collect order type from grid
        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        rows = find_elements_by_selector(
            self.driver, ORDER_TYPE_CELL_SEL
        )
        order_types = []
        [order_types.append(row.text) for row in rows]
        return [self.assertEqual(type_enabled, elem) for elem in order_types]

    @classmethod
    def tearDownClass(cls):
        reset_filter(cls.driver)
        close_filter(cls.driver)
