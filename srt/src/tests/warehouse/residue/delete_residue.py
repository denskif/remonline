# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, INVENTORY_URL
from src.lib.dom import find_element_by_selector, hover_and_click
from src.lib.wait import (
    wait_selector_to_disappear, wait_for_selector, wait_to_click_selector
)
from src.lib.notify import wait_notify_worked

from src.scaffolds.grid import wait_grid_changed_rows_num, wait_grid_updated
from src.scaffolds.search import search_for
from src.scaffolds.dialog import confirm_delete, close_dialog

from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.clean_up import delete_trans, delete_residue
from src.tests.warehouse.lib.select import (
    search_and_select, TABLE_ROW_SEL, GRID_SEL
)
from src.tests.warehouse.lib.checkers import assert_residue_not_in_table


RESIDUE_A_DATA = {
    u'supplier' : {'name': u"Kortic Supplies"},
    u'title' : u"Roller coaster",
    u'quantity' : u"2",
    u'price' : u"153",
}
RESIDUE_T_DATA = {
    u'supplier' : {'name': u"Krasty Su."},
    u'title' : u"Torch",
    u'quantity' : u"2",
    u'price' : u"199",
}
RESIDUE_F_DATA = {
    u'supplier' : {'name': u"Krasty Su."},
    u'title' : u"Porch",
    u'quantity' : u"2",
    u'price' : u"217",
}



"""
For the test cases "DeleteResidueFromTable" and "DeleteResidueFromForm"
we need to post entity, then delete the posting so that residue will show 0,
and finally delete residue from stock.
"""
class DeleteResidueFromTable(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, RESIDUE_T_DATA)
        return True

    def test_1_delete_posting(self):
        return delete_trans(self.driver)

    def test_2_delete_residue(self):
        navigate(self.driver, INVENTORY_URL)
        delete_residue(self.driver, RESIDUE_T_DATA)
        return True


class DeleteResidueFromForm(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, RESIDUE_F_DATA)
        return True

    def test_1_delete_posting(self):
        return delete_trans(self.driver)

    def test_2_delete_residue(self):
        navigate(self.driver, INVENTORY_URL)

        search_and_select(self.driver, RESIDUE_F_DATA['title'])
        hover_and_click(self.driver, ".js-edit-button")

        wait_for_selector(
            self.driver, ".b-dialog_type_warehouse .h-trash-button"
        )

        wait_to_click_selector(self.driver, ".h-trash-button")
        find_element_by_selector(self.driver, ".h-trash-button").click()
        confirm_delete(self.driver)

        assert_residue_not_in_table(self.driver, RESIDUE_F_DATA)
        return True


class DeleteResidueHasAmount(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    # Create new residue with positive amount
    def test_0_create_new_residue(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, RESIDUE_A_DATA)
        return True

    def test_1_cannot_delete_from_table(self):
        search_and_select(self.driver, RESIDUE_A_DATA['title'])

        hover_and_click(self.driver, ".js-remove-button")
        confirm_delete(self.driver)

        wait_notify_worked(self.driver)
        return True

    def test_2_cannot_delete_from_form(self):
        search_and_select(self.driver, RESIDUE_A_DATA['title'])

        hover_and_click(self.driver, ".js-edit-button")

        wait_for_selector(
            self.driver, ".b-dialog_type_warehouse .h-trash-button"
        )

        wait_to_click_selector(self.driver, ".h-trash-button")
        find_element_by_selector(self.driver, ".h-trash-button").click()
        confirm_delete(self.driver)

        wait_notify_worked(self.driver)
        close_dialog(self.driver, ".js-close-dialog", ".b-dialog_type_warehouse")
        return True
