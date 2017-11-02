# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.wait import wait_selector_to_disappear

from src.scaffolds.dialog import close_dialog

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order
from src.tests.orders.lib.status import (
    change_status_in_order, change_status_from_table
)

STATUS_IN_WORK_INDEX = 1


class StatusChangeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/orders")

    def test_1_change_status_from_order(self):
        create_order(self.driver)
        open_order(self.driver)
        change_status_in_order(self.driver, STATUS_IN_WORK_INDEX)
        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True

    def test_2_change_status_from_table(self):
        create_order(self.driver)
        change_status_from_table(self.driver, STATUS_IN_WORK_INDEX)
        return True
