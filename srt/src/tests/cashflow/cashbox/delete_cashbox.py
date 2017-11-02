# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CASHBOX_URL
from src.lib.dom import find_element_by_selector
from src.lib.formatting import make_double_text_xpath
from src.lib.wait import wait_xpath_to_disappear

from src.scaffolds.dialog import confirm_delete

from src.tests.cashflow.lib import open_cashbox_settings, TRASH_BTN_SEL
from src.tests.cashflow.lib.cashbox import create_local_cashbox
from src.tests.cashflow.lib.select import select_cashbox_by_name



class RemoveCashbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CASHBOX_URL)

    def test_1_remove_box(self):
        cashbox = create_local_cashbox(self.driver)
        select_cashbox_by_name(self.driver, cashbox)
        open_cashbox_settings(self.driver)

        find_element_by_selector(self.driver, TRASH_BTN_SEL).click()

        confirm_delete(self.driver)

        box_path = make_double_text_xpath(
            "p", "@class, 'b-cashbox__name'", cashbox
        )

        return wait_xpath_to_disappear(self.driver, box_path)
