# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CATEGORIES_URL, POSTING_URL
from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import (
    wait_selector_to_disappear, wait_to_see_selector, wait_to_click_selector
)
from src.lib.notify import wait_notify_worked

from src.scaffolds.dialog import open_dialog, confirm_delete
from src.scaffolds.dropdown import choose_category_by_name, choose_stock

from src.widget.client import fast_add_new_client

from src.tests.warehouse.lib import open_posting_dialog
from src.tests.warehouse.lib.save_trans import save_posting
from src.tests.warehouse.lib.checkers import check_item_in_table
from src.tests.warehouse.lib.set_data import add_to_posting

from src.tests.warehouse.lib.create import (
    set_cat_active, create_category, make_category, make_cat_sel
)


DELETE_CAT_DATA = {
    u'supplier' : {'name': u"Surgion Sups"},
    u'title' : u"Armour vest 45 FF-T",
    u'quantity' : u"2",
    u'price' : u"550",
}

CATEGORY_NAME_1 = make_category()
CATEGORY_SEL_1 = make_cat_sel(CATEGORY_NAME_1)
STOCK_IDX = 1


class DeleteCategory(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CATEGORIES_URL)

    def test_1_remove_from_page(self):
        category_name = make_category()
        category_sel = make_cat_sel(category_name)

        create_category(self.driver, category_name)
        set_cat_active(self.driver, category_sel)
        find_element_by_selector(
            self.driver, ".js-remove-button"
        ).click()
        return wait_selector_to_disappear(self.driver, category_sel)

    def test_2_remove_from_dialog(self):
        category_name = make_category()
        category_sel = make_cat_sel(category_name)

        create_category(self.driver, category_name)
        find_element_by_selector(
            self.driver, category_sel
        ).click()
        open_dialog(self.driver, ".js-edit-button", ".b-dialog #js-wh-title")

        find_element_by_selector(
            self.driver, ".h-trash-button"
        ).click()
        confirm_delete(self.driver)
        return wait_selector_to_disappear(self.driver, category_sel)


class DeleteCategoryWithGood(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CATEGORIES_URL)

    def test_1_create_new_cat(self):
        create_category(self.driver, CATEGORY_NAME_1)
        return True

    def test_2_post_item_with_cat(self):
        navigate(self.driver, POSTING_URL)

        open_posting_dialog(self.driver)

        choose_stock(self.driver, STOCK_IDX)
        set_value(self.driver, "#js-wh-title", DELETE_CAT_DATA['title'])
        fast_add_new_client(self.driver, "#js-wh-supplier", DELETE_CAT_DATA['supplier'])

        choose_category_by_name(self.driver, CATEGORY_SEL_1)

        set_value(self.driver, "#l-wh-quantity", DELETE_CAT_DATA['quantity'])
        set_value(self.driver, "#js-wh-price", DELETE_CAT_DATA['price'])

        add_to_posting(self.driver)
        wait_selector_to_disappear(self.driver, ".js-c-categories")
        wait_to_see_selector(self.driver, ".b-dialog_type_warehouse .js-grid tbody")
        save_posting(self.driver)

        wait_notify_worked(self.driver)

        return self.assertEqual(
            check_item_in_table(self.driver), DELETE_CAT_DATA['title']
        )

    def test_3_check_category_not_removed(self):
        set_cat_active(self.driver, CATEGORY_SEL_1)
        find_element_by_selector(
            self.driver, ".js-remove-button"
        ).click()

        wait_notify_worked(self.driver)

        return wait_to_see_selector(self.driver, CATEGORY_SEL_1)
