# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, INVENTORY_URL, POSTING_URL, CATEGORIES_URL
from src.lib.dom import (
    click_nth_node, find_element_by_selector, get_value, make_selector,
    set_value
)
from src.lib.wait import wait_to_see_selector
from src.lib.randomizer import make_spare_part
from src.lib.errors import raise_error

from src.scaffolds.grid import wait_grid_updated, wait_grid_changed_rows_num
from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import choose_category_by_name
from src.scaffolds.search import reset_search

from src.tests.warehouse.lib.select import search_and_select, set_active_residue
from src.tests.warehouse.lib.create import (
    create_posting, create_category, make_category, make_cat_sel
)
from src.tests.warehouse.lib.checkers import assert_added_to_table, TABLE_ERROR_MSG


RESIDUE_DATA_1 = {
    u'supplier' : {'name':u"Supra Supplies"},
    u'title' : u"Liver",
    u'quantity' : u"2",
    u'price' : u"120",
}
RESIDUE_DATA_2 = {
    u'supplier' : {'name':u"Supra Supplies"},
    u'title' : u"Krovianka",
    u'quantity' : u"5",
    u'price' : u"77.14",
    u'article' : u"777",
    u'code' : u"878",
    u'description' : u"Stuff from villagers",
}

CATEGORY_NAME = make_category()
GRID_SEL = ".js-grid"
TITLE_CELL = 3
WH_DIALOG_SEL = ".b-dialog_type_warehouse"

RESIDUE_CAT_SEL = make_selector(WH_DIALOG_SEL, ".js-c-categories")


class EditResidue(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_0_residue_dialog(self):
        set_active_residue(self.driver)

        open_dialog(self.driver, ".js-edit-button", ".b-dialog_type_warehouse")
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog_type_warehouse")

        open_dialog(self.driver, ".js-edit-button", ".b-dialog_type_warehouse")
        close_dialog(self.driver, ".h-dialog-mask", ".b-dialog_type_warehouse")
        return True


class EditCategoryInResidue(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_residue(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, RESIDUE_DATA_1)
        return True

    def test_1_create_category(self):
        navigate(self.driver, CATEGORIES_URL)

        create_category(self.driver, CATEGORY_NAME)
        return True

    def test_2_edit_category_for_residue(self):
        navigate(self.driver, INVENTORY_URL)
        search_and_select(self.driver, RESIDUE_DATA_1['title'])

        open_dialog(self.driver, ".js-edit-button", WH_DIALOG_SEL)
        choose_category_by_name(
            self.driver, make_cat_sel(CATEGORY_NAME), WH_DIALOG_SEL
        )
        close_dialog(self.driver, ".js-submit-dialog", WH_DIALOG_SEL)

        set_active_residue(self.driver)
        open_dialog(self.driver, ".js-edit-button", WH_DIALOG_SEL)

        wait_to_see_selector(self.driver, RESIDUE_CAT_SEL)

        new_category = find_element_by_selector(
            self.driver, RESIDUE_CAT_SEL
        ).text

        self.assertEqual(new_category, CATEGORY_NAME)

        return close_dialog(self.driver, ".js-close-dialog", WH_DIALOG_SEL)


class EditItemDataInResidue(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_0_preconditions(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, RESIDUE_DATA_2)
        return

    def test_1_edit_item_data(self):
        search_and_select(self.driver, RESIDUE_DATA_2['title'])
        open_dialog(self.driver, ".js-edit-button", WH_DIALOG_SEL)

        wait_to_see_selector(self.driver, "#l-wh-description")
        set_value(self.driver, "#l-wh-description", RESIDUE_DATA_2['description'])
        set_value(self.driver, "#l-wh-code", RESIDUE_DATA_2['code'])
        set_value(self.driver, "#l-wh-article", RESIDUE_DATA_2['article'])

        close_dialog(self.driver, ".js-submit-dialog", WH_DIALOG_SEL)

        set_active_residue(self.driver)
        open_dialog(self.driver, ".js-edit-button", WH_DIALOG_SEL)

        wait_to_see_selector(self.driver, "#l-wh-code")

        code = get_value(find_element_by_selector(self.driver, "#l-wh-code"))
        article = get_value(
            find_element_by_selector(self.driver, "#l-wh-article")
        )
        description = get_value(
            find_element_by_selector(self.driver, "#l-wh-description")
        )
        self.assertEqual(code, RESIDUE_DATA_2['code'])
        self.assertEqual(article, RESIDUE_DATA_2['article'])
        self.assertEqual(description, RESIDUE_DATA_2['description'])

        return close_dialog(self.driver, ".js-close-dialog", WH_DIALOG_SEL)

    def test_2_edit_name(self):
        search_and_select(self.driver, RESIDUE_DATA_2['title'])
        open_dialog(self.driver, ".js-edit-button", WH_DIALOG_SEL)

        new_item = make_spare_part()

        wait_to_see_selector(self.driver, "#l-wh-title")
        set_value(self.driver, "#l-wh-title", new_item)
        close_dialog(self.driver, ".js-submit-dialog", WH_DIALOG_SEL)

        reset_search(self.driver)
        search_and_select(self.driver, new_item)

        assert_added_to_table(
            self.driver, GRID_SEL, TITLE_CELL, new_item)

        raise_error(
            assert_added_to_table(
                self.driver, GRID_SEL, TITLE_CELL, new_item
            ), TABLE_ERROR_MSG
        )

        return reset_search(self.driver)
