# ~*~ coding: utf-8 ~*~


import unittest
from decimal import Decimal
import time

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.dom import find_element_by_selector, find_input_by_selector
from src.lib.formatting import format_cash_amount
from src.lib.randomizer import random_x
from src.lib.wait import wait_for_selector, wait_selector_to_disappear

from src.scaffolds.grid import remove_item_from_grid
from src.scaffolds.dialog import confirm_delete

from src.tests.cashflow.lib import make_box_sel
from src.tests.cashflow.lib.transactions import make_income



AMOUNT = "555.55"
COMMENT = u"The unique -{0} money affair: {1}".format(AMOUNT, random_x())
REMOVE_BTN_SEL = "tbody td:nth-child(6) div"

TRANS = {
    'amount' : AMOUNT,
    'comment' : COMMENT,
}
RESTORE = ".h-restore-link"


class RemoveTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_remove_transaction(self):
        make_income(self.driver, TRANS)

        before_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        remove_item_from_grid(self.driver, ".js-report-grid")
        confirm_delete(self.driver)

        current_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        return self.assertEqual(
            Decimal(format_cash_amount(current_cf_value)),
            Decimal(
                format_cash_amount(before_cf_value)
            ) - Decimal(TRANS['amount'])
        )

    def test_2_check_removed(self):
        restore = find_input_by_selector(self.driver, REMOVE_BTN_SEL)
        return self.assertTrue(RESTORE[1:] in restore.get_attribute('class'))

    def test_3_restore_transaction(self):
        before_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        find_input_by_selector(self.driver, RESTORE).click()
        time.sleep(1)

        current_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        return self.assertEqual(
            Decimal(format_cash_amount(current_cf_value)),
            Decimal(TRANS['amount']) + Decimal(
                format_cash_amount(before_cf_value)
            )
        )

    def test_4_check_restored(self):
        remove = find_input_by_selector(self.driver, REMOVE_BTN_SEL)
        return self.assertTrue("h-remove-link" in remove.get_attribute('class'))
