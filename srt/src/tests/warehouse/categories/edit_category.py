# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import wait_to_see_selector, wait_for_selector
from src.lib.notify import wait_notify_worked
from src.lib.errors import assert_has_error_tooltip

from src.scaffolds.dialog import open_dialog, close_dialog

from src.tests.warehouse.lib.create import (
    set_cat_active, create_category, make_category, make_cat_sel
)


class EditCategory(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/categories")

    def test_1_edit_category_name(self):
        cat_title = make_category()

        create_category(self.driver, cat_title)
        set_cat_active(self.driver, make_cat_sel(cat_title))

        new_cat_name = make_category()

        open_dialog(self.driver, ".js-edit-button", ".b-dialog #js-wh-title")
        set_value(self.driver, "#js-wh-title", new_cat_name)
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        return wait_to_see_selector(self.driver, make_cat_sel(new_cat_name))

    def test_2_set_no_name(self):
        cat_title = make_category()

        create_category(self.driver, cat_title)
        set_cat_active(self.driver, make_cat_sel(cat_title))

        open_dialog(self.driver, ".js-edit-button", ".b-dialog #js-wh-title")

        title = find_element_by_selector(self.driver, "#js-wh-title")
        title.clear()
        find_element_by_selector(self.driver, ".js-submit-dialog").click()
        wait_for_selector(self.driver, ".h-errors-tooltip")

        assert_has_error_tooltip(self.driver, title)

        close_dialog(self.driver, ".js-close-dialog", ".b-dialog")
        return True


