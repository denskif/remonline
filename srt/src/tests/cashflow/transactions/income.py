# ~*~ coding: utf-8 ~*~

import unittest
from decimal import Decimal

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.errors import assert_has_error_tooltip
from src.lib.dom import find_element_by_selector, set_value, get_value
from src.lib.wait import wait_to_see_selector
from src.lib.formatting import format_cash_amount
from src.lib.randomizer import random_x

from src.tests.cashflow.lib import (
    open_income_dialog, SUBMIT_SEL, close_cashbox_dialog, make_box_sel,
    COMMENT_CELL, INCOME_CELL, TOTAL_CELL,
)
from src.tests.cashflow.lib.transactions import make_income

SUM_SEL = "#l-cb-payment"
COMMENT_SEL = "#l-cb-description"

BAD_DATA = ["0", "-999", "0.001", "text", " ", "45 45" ]

AMOUNT = "333.33"
COMMENT = "The unique {0} money income. {1}".format(AMOUNT, random_x())

INCOME = {
    'amount' : AMOUNT,
    'comment' : COMMENT,
}


class ValidateIncome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_no_input(self):
        open_income_dialog(self.driver)
        find_element_by_selector(self.driver, SUBMIT_SEL).click()

        sum_input = find_element_by_selector(self.driver, SUM_SEL)
        comment_input = find_element_by_selector(self.driver, COMMENT_SEL)

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


class CheckIncomeTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_create_transaction(self):
        wait_to_see_selector(self.driver, make_box_sel(".h-d-ib"))

        before_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        make_income(self.driver, INCOME)

        current_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        return self.assertEqual(
            Decimal(format_cash_amount(current_cf_value)),
            Decimal(INCOME['amount']) + Decimal(
                format_cash_amount(before_cf_value)
            )
        )

    def test_2_check_comment(self):
        table_comment = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", COMMENT_CELL
        ).text

        return self.assertEqual(table_comment, COMMENT)

    def test_3_check_amount(self):
        table_income = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", INCOME_CELL
        ).text

        return self.assertEqual(table_income, AMOUNT)

    def test_4_check_total(self):
        total = find_element_by_selector(
            self.driver, ".h-cashbox-report tbody tr td", TOTAL_CELL
        ).text

        current_cf_value = find_element_by_selector(
            self.driver, make_box_sel(".h-d-ib")
        ).text

        return self.assertEqual(
            format_cash_amount(total), format_cash_amount(current_cf_value)
        )
