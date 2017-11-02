# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import wait_selector_to_disappear
from src.lib.errors import raise_error

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import ( test_caret, autocomplete_add,
    autocomplete_client_fast_widget
)
from src.scaffolds.grid import remove_item_from_grid

from src.tests.warehouse.lib import (
    open_posting_dialog, close_posting_dialog, close_posting_dialog
)
from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.checkers import assert_added_to_table, TABLE_ERROR_MSG
from src.tests.warehouse.lib.set_data import (
    set_new_good, set_instock_good,
)

GRID_SEL = ".b-dialog_type_warehouse .js-grid"

NEW_GOOD_DATA = {
    u'supplier' : {
    'name': u"Evan's Supplies",
    'supplier' : True,
    },
    u'title' : u"Auto Pineapple 37",
    u'quantity' : u"2",
    u'price' : u"180",
}
ADD_REMOVE_DATA = {
    u'supplier' : {'name': u"Gregory Do Sup."},
    u'title' : u"Blue Guacamole",
    u'quantity' : u"30",
    u'price' : u"13",
}


class PostingAutocomplete(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/warehouse/posting")

    def test_0_preconditions(self):
        return create_posting(self.driver, NEW_GOOD_DATA)

    def test_1_supplier(self):
        open_posting_dialog(self.driver)

        test_caret(self.driver, '[data-opts-relate=js-wh-supplier]')
        autocomplete_client_fast_widget(
            self.driver, self, "#js-wh-supplier", NEW_GOOD_DATA['supplier']['name']
        )

        return close_posting_dialog(self.driver)

    # def test_2_goods(self):
    #     open_posting_dialog(self.driver)
    #     test_caret(self.driver, '[data-opts-relate=js-wh-title]')
    #     autocomplete_add(self.driver, self, "#js-wh-title", NEW_GOOD_DATA['title'])

    #     return close_posting_dialog(self.driver)


class PostingAddRemoveGoods(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_precondition(self):
        navigate(self.driver, "/app#!/warehouse/posting")
        return create_posting(self.driver, ADD_REMOVE_DATA)

    def test_1_add_item(self):
        open_posting_dialog(self.driver)

        set_instock_good(self.driver, ADD_REMOVE_DATA)

        posting_table = ".b-dialog_type_warehouse"
        item_cell = 1

        table_result = assert_added_to_table(
            self.driver, posting_table, item_cell, ADD_REMOVE_DATA['title']
        )
        return raise_error(table_result, TABLE_ERROR_MSG)

    def test_2_remove_item(self):
        remove_item_from_grid(self.driver, GRID_SEL)
        wait_selector_to_disappear(
            self.driver, ".b-dialog_type_warehouse .js-grid tbody"
        )
        close_posting_dialog(self.driver)
        return True



