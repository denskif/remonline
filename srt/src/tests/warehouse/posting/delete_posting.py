# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.dom import find_element_by_selector
from src.lib.wait import (
    wait_for_selector, wait_to_click_selector, wait_selector_to_disappear
)

from src.scaffolds.grid import remove_item_from_grid
from src.scaffolds.dialog import confirm_delete

from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.clean_up import delete_trans


class DeletePosting(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/posting")

    def test_1_delete_posting(self):
        create_posting(self.driver)
        delete_trans(self.driver)
        return True

    def test_2_confirmation_dialog(self):
        create_posting(self.driver)

        # Close confirmation dialog by "close" link
        remove_item_from_grid(self.driver, ".js-grid tbody")
        wait_to_click_selector(self.driver, ".b-modal_type_confirm .js-close")
        find_element_by_selector(
            self.driver, ".b-modal_type_confirm .js-close"
        ).click()
        wait_selector_to_disappear(self.driver, ".b-modal_type_confirm")

        # Close confirmation dialog by "X" button
        remove_item_from_grid(self.driver, ".js-grid tbody")
        wait_to_click_selector(
            self.driver, ".b-modal_type_confirm .b-modal__close"
        )
        find_element_by_selector(
            self.driver, ".b-modal_type_confirm .b-modal__close"
        ).click()
        wait_selector_to_disappear(self.driver, ".b-modal_type_confirm")

        return True

