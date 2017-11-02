# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.errors import assert_has_error_tooltip
from src.lib.dom import (
    find_element_by_selector, make_selector, find_input_by_selector,
    find_element_by_xpath,
)
from src.lib.wait import wait_for_selector
from src.lib.formatting import make_double_text_xpath

from src.scaffolds.dialog import close_dialog

from src.tests.cashflow.lib import (
    open_create_cashbox_dialog, submit_cashbox_dialog, close_cashbox_dialog,
    SUBMIT_SEL, DIALOG_SEL, NAME_INPUT_SEL
)
from src.tests.cashflow.lib.cashbox import (
    create_local_cashbox, create_global_cashbox, clean_up_cashboxes
)


class ValidateCashbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_open_close_dialog(self):
        open_create_cashbox_dialog(self.driver)
        close_dialog(self.driver, ".h-dialog-mask", ".h-dialog-mask")

        open_create_cashbox_dialog(self.driver)
        close_cashbox_dialog(self.driver)
        return

    def test_2_no_name(self):
        open_create_cashbox_dialog(self.driver)
        submit_sel = make_selector(DIALOG_SEL, SUBMIT_SEL)

        wait_for_selector(self.driver, submit_sel)

        find_element_by_selector(self.driver, submit_sel).click()

        cashbox_name = find_element_by_selector(self.driver, NAME_INPUT_SEL)

        return assert_has_error_tooltip(self.driver, cashbox_name)

    def test_3_switch_type(self):
        find_element_by_selector(self.driver, "[for=l-cb-type-global]").click()
        global_type = find_input_by_selector(self.driver, "#l-cb-type-global")

        self.assertTrue(global_type.is_selected())

        find_element_by_selector(self.driver, "[for=l-cb-type-local]").click()
        local_type = find_input_by_selector(self.driver, "#l-cb-type-local")

        return self.assertTrue(local_type.is_selected())

    @classmethod
    def tearDownClass(cls):
        cls.driver = get_driver()
        close_cashbox_dialog(cls.driver)


class CreateCashbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_create_local(self):
        cashbox = create_local_cashbox(self.driver)

        box_path = make_double_text_xpath(
            "p", "@class, 'b-cashbox__name'", cashbox
        )
        cashbox_name = find_element_by_xpath(self.driver, box_path)

        return self.assertTrue(cashbox_name.is_displayed())

    def test_2_create_global(self):
        cashbox = create_global_cashbox(self.driver)

        box_path = make_double_text_xpath(
            "p", "@class, 'b-cashbox__name'", cashbox
        )
        cashbox_name = find_element_by_xpath(self.driver, box_path)

        return self.assertTrue(cashbox_name.is_displayed())

    @classmethod
    def tearDownClass(cls):
        clean_up_cashboxes(cls.driver)