# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.dom import find_element_by_selector, find_elements_by_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.status import change_status_from_table
from src.tests.orders.lib.filter import (
    open_filter, close_filter, reset_filter, click_filter_btn,
    enable_all_checkboxes, disable_all_checkboxes, F_CHECK_BOX_SEL,
)


FIRST_ROW_CELL_SEL = "tbody td"

F_BTN_IDX = 0
CLOSED_STATUS_IDX = -1

STATUS_CELL_SEL = "tbody tr td:nth-child(3)"
STATUS_BOX = ".b-popup__body span:nth-child(3)"



class FilterStatusTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        open_filter(cls.driver)

    def test_1_on_off_statuses(self):
        click_filter_btn(self.driver, F_BTN_IDX)
        disable_all_checkboxes(self.driver)
        wait_selector_to_disappear(self.driver, FIRST_ROW_CELL_SEL)
        enable_all_checkboxes(self.driver)
        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        return True

    def test_2_status_filters(self):
        create_order(self.driver)
        change_status_from_table(self.driver, CLOSED_STATUS_IDX)

        click_filter_btn(self.driver, F_BTN_IDX)
        disable_all_checkboxes(self.driver)

        find_element_by_selector(
            self.driver, F_CHECK_BOX_SEL, CLOSED_STATUS_IDX
        ).click()
        status = find_element_by_selector(
            self.driver, STATUS_BOX, CLOSED_STATUS_IDX
        ).text

        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        rows = find_elements_by_selector(self.driver, STATUS_CELL_SEL)

        statuses = []
        [statuses.append(row.text) for row in rows]
        return [self.assertEqual(status, elem) for elem in statuses]

    @classmethod
    def tearDownClass(cls):
        reset_filter(cls.driver)
        close_filter(cls.driver)
