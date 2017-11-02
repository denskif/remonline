# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.dom import get_value, find_element_by_selector, set_value
from src.lib.errors import assert_has_error_tooltip
from src.lib.randomizer import random_x
from src.lib.wait import wait_for_selector

from src.tests.cashflow.lib import (
    make_box_sel, ACTIVE_BOX_SEL, open_transfer_dialog, SUBMIT_SEL,
    close_cashbox_dialog, COMMENT_CELL, EXPENSE_CELL, INCOME_CELL,
)
from src.tests.cashflow.lib.cashbox import (
    create_local_cashbox, clean_up_cashboxes
)
from src.tests.cashflow.lib.select import select_cashbox_by_name
from src.tests.cashflow.lib.transactions import (
    make_transfer, SUM_SEL, COMMENT_SEL,
)

from src.lib import tail


BAD_DATA = ["0", "-999", "0.001", "text", " ", "45 45" ]

AMOUNT = "777.77"
COMMENT = u"The unique -{0} money expense: {1}".format(AMOUNT, random_x())

MOVE_SUM = {
    'amount' : AMOUNT,
    'comment' : COMMENT,
}



class ValidateTransfer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)
        """
            This test needs two more cashboxes,
        so that cashbox dropdown will show - "not selected"
        1 box - Money transfer not available
        2 boxes - casbox dropdown selected by default
        3 boxes - dropdown not selected
        """
        create_local_cashbox(cls.driver)
        create_local_cashbox(cls.driver)

    def test_1_no_input(self):
        open_transfer_dialog(self.driver)
        find_element_by_selector(self.driver, SUBMIT_SEL).click()

        box_dropdown = find_element_by_selector(
            self.driver, ".b-dialog__content .js-cashboxes"
        )
        sum_input = find_element_by_selector(self.driver, SUM_SEL)
        comment_input = find_element_by_selector(self.driver, COMMENT_SEL)

        assert_has_error_tooltip(self.driver, box_dropdown)
        assert_has_error_tooltip(self.driver, sum_input)
        assert_has_error_tooltip(self.driver, comment_input)
        return True

    def test_2_bad_input_for_sum(self):
        sum_input = find_element_by_selector(self.driver, SUM_SEL)

        for data in BAD_DATA:
            set_value(self.driver, SUM_SEL, data)
            find_element_by_selector(self.driver, SUBMIT_SEL).click()
            assert_has_error_tooltip(self.driver, sum_input)

        return True

    @classmethod
    def tearDownClass(cls):
        close_cashbox_dialog(cls.driver)
        clean_up_cashboxes(cls.driver)


class MoneyTransfer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)
        # Create boxes to move money between
        cls.box1 = create_local_cashbox(cls.driver)
        select_cashbox_by_name(cls.driver, cls.box1)

        cls.box1_id = find_element_by_selector(
            cls.driver, ACTIVE_BOX_SEL
        ).get_attribute("data-cashbox-id")

        select_cashbox_by_name(cls.driver, create_local_cashbox(cls.driver))

    def test_1_move_transaction(self):
        # Move money
        make_transfer(self.driver, self.box1_id, MOVE_SUM)
        # Check transaction data in sender box
        table_comment = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", COMMENT_CELL
        ).text
        table_expense = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", EXPENSE_CELL
        ).text
        # Check transaction data in destiantion box
        select_cashbox_by_name(self.driver, self.box1)
        wait_for_selector(self.driver, ".h-cashbox-report tbody tr td")

        table_income = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", INCOME_CELL
        ).text
        # Check results
        self.assertEqual(tail(table_comment.split(". ")), COMMENT)
        self.assertEqual(table_expense, "-" + AMOUNT)
        return self.assertEqual(table_income, AMOUNT)

    @classmethod
    def tearDownClass(cls):
        clean_up_cashboxes(cls.driver)
