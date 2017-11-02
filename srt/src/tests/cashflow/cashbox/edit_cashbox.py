# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.dom import (
    make_selector, find_element_by_selector, set_value, find_input_by_selector
)
from src.lib.wait import wait_to_see_selector

from src.scaffolds.dialog import open_dialog

from src.tests.cashflow.lib import (
    open_cashbox_settings, DIALOG_SEL, NAME_INPUT_SEL, submit_cashbox_dialog,
    ACTIVE_BOX_SEL, close_cashbox_dialog
)
from src.tests.cashflow.lib.select import select_cashbox_by_name
from src.tests.cashflow.lib.cashbox import (
    create_local_cashbox, clean_up_cashboxes
)



class UpdateCashbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_change_name(self):
        cashbox = create_local_cashbox(self.driver)
        select_cashbox_by_name(self.driver, cashbox)
        open_cashbox_settings(self.driver)

        """
        Using upper case to prevent dismatch
        caused probably by selenium .text function
        """
        new_name = "TEST_BOX"
        set_value(self.driver, NAME_INPUT_SEL, new_name)
        submit_cashbox_dialog(self.driver)

        renamed_cashbox = find_element_by_selector(
            self.driver, make_selector(ACTIVE_BOX_SEL, ".b-cashbox__name")
        ).text

        return self.assertEqual(new_name, renamed_cashbox)

    def test_2_change_type(self):
        cashbox = create_local_cashbox(self.driver)
        select_cashbox_by_name(self.driver, cashbox)
        open_cashbox_settings(self.driver)

        find_element_by_selector(self.driver, "[for=l-cb-type-global]").click()
        submit_cashbox_dialog(self.driver)

        select_cashbox_by_name(self.driver, cashbox)
        open_cashbox_settings(self.driver)

        global_type = find_input_by_selector(self.driver, "#l-cb-type-global")

        return self.assertTrue(global_type.is_selected())

    @classmethod
    def tearDownClass(cls):
        close_cashbox_dialog(cls.driver)
        clean_up_cashboxes(cls.driver)

