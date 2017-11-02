# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.dom import set_value, make_selector, find_element_by_selector
from src.lib.notify import wait_notify_worked
from src.lib.errors import assert_has_error_tooltip
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_see_selector
)

from src.scaffolds.dialog import open_dialog, close_dialog

from src.tests.warehouse.lib.create import (
    set_cat_active, create_category, make_category, make_cat_sel
)


CATEGORY_NAME = make_category()
CATEGORY_SEL = make_cat_sel(CATEGORY_NAME)

SUB_NAME = "SUB_{0}".format(make_category())
SUB_SEL = make_cat_sel(SUB_NAME)


class CreateCategory(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/categories")

    def test_1_category_dialog(self):
        # Close dialog b-dialog by clicking away
        set_cat_active(self.driver)
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #js-wh-title")
        close_dialog(self.driver, ".h-dialog-mask", ".b-dialog")

        # Close dialog by clicking "close button"
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #js-wh-title")
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog")
        return True

    def test_2_main_parent_node(self):
        set_cat_active(self.driver)
        edit_btn = find_element_by_selector(self.driver, ".js-edit-button")
        remove_btn = find_element_by_selector(self.driver, ".js-remove-button")

        self.assertEqual(edit_btn.is_enabled(), False)
        self.assertEqual(remove_btn.is_enabled(), False)
        return True

    def test_3_create_category(self):
        create_category(self.driver)
        return True

    def test_4_category_already_exist(self):
        cat_title = make_category()

        create_category(self.driver, cat_title)

        set_cat_active(self.driver)
        open_dialog(self.driver, ".js-wh-add", ".b-dialog #js-wh-title")
        set_value(self.driver, "#js-wh-title", cat_title)
        find_element_by_selector(self.driver, ".js-submit-dialog").click()

        return wait_notify_worked(self.driver)

    def test_5_no_name(self):
        set_cat_active(self.driver)

        open_dialog(self.driver, ".js-wh-add", ".b-dialog #js-wh-title")
        title = find_element_by_selector(self.driver, "#js-wh-title")
        title.clear()
        find_element_by_selector(self.driver, ".js-submit-dialog").click()
        wait_for_selector(self.driver, ".h-errors-tooltip")
        return assert_has_error_tooltip(self.driver, title)

    def test_6_category_collapser(self):
        wait_for_selector(self.driver, ".b-tree__collapser")
        find_element_by_selector(self.driver, ".b-tree__collapser").click()
        wait_for_selector(self.driver, ".b-tree__leaf_state_collapsed")

        find_element_by_selector(self.driver, ".b-tree__collapser").click()
        wait_selector_to_disappear(
            self.driver, ".b-tree__leaf_state_collapsed"
        )
        return wait_to_see_selector(self.driver, ".b-tree__foliage")


class SubCategory(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/categories")

    def test_1_create_sub_category(self):
        create_category(self.driver, CATEGORY_NAME)
        set_cat_active(self.driver, CATEGORY_SEL)

        open_dialog(self.driver, ".js-wh-add", ".b-dialog #js-wh-title")
        set_value(self.driver, "#js-wh-title", SUB_NAME)
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        return wait_for_selector(
            self.driver, make_selector(".b-tree__foliage", SUB_SEL)
        )

    def test_2_cant_remove_with_subcategory(self):
        set_cat_active(self.driver, CATEGORY_SEL)
        find_element_by_selector(
            self.driver, ".js-remove-button"
        ).click()

        wait_notify_worked(self.driver)
        return wait_to_see_selector(self.driver, CATEGORY_SEL)

    def test_3_remove_subcategory(self):
        set_cat_active(self.driver, SUB_SEL)
        find_element_by_selector(
            self.driver, ".js-remove-button"
        ).click()

        return wait_selector_to_disappear(self.driver, SUB_SEL)
