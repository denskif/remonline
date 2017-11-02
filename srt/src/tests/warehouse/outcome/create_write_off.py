# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, WRITE_OFF_URL, POSTING_URL
from src.lib.dom import (
    find_element_by_selector, make_selector, set_value, hover_and_click
)
from src.lib.errors import assert_has_error_tooltip, raise_error
from src.lib.wait import (
    wait_to_click_selector, wait_for_selector, wait_selector_to_disappear
)

from src.scaffolds.dialog import open_dialog, close_dialog, confirm_removal
from src.scaffolds.search import search_for
from src.scaffolds.grid import remove_item_from_grid

from src.tests.warehouse.lib import (
    open_write_off, submit_write_off, close_write_off, DIALOG_SEL,
    SUBMIT_WRITEOFF_BTN_SEL,
)
from src.tests.warehouse.lib.create import create_posting, make_write_off
from src.tests.warehouse.lib.checkers import (
    assert_added_to_table, TABLE_ERROR_MSG, check_item_in_table
)
from src.tests.warehouse.lib.set_data import add_to_outcome, STACK_SEL


WRITE_OFF_DATA = {
    u'supplier' : {'name':u"China Cu."},
    u'title' : u"Koren Zhenshenya",
    u'quantity' : u"5",
    u'price' : u"78",
}

WO_DATA_1 = {
    u'supplier' : {'name':u"China Cu."},
    u'title' : u"Morskoy Konek",
    u'quantity' : u"2",
    u'price' : u"99.99",
}

WO_COMMENT_DATA = {
    u'supplier' : {'name':u"China Cu."},
    u'title' : u"Zolotaya Palma",
    u'quantity' : u"2",
    u'price' : u"100",
}
MASK_SEL = ".h-dialog-mask"



class CreateWriteOff(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_open_close_dialog(self):
        navigate(self.driver, WRITE_OFF_URL)
        # Close by clicking "close" button
        open_write_off(self.driver)
        close_write_off(self.driver)

        # Close by clicking away
        open_write_off(self.driver)
        close_dialog(self.driver, MASK_SEL, MASK_SEL)
        return True

    def test_1_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, WRITE_OFF_DATA)
        return True

    def test_2_create_write_off(self):
        navigate(self.driver, WRITE_OFF_URL)
        make_write_off(self.driver, WRITE_OFF_DATA)
        return self.assertEqual(
            check_item_in_table(self.driver), WRITE_OFF_DATA['title']
        )


class CommentWriteOff(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, WRITE_OFF_URL)

    def test_0_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, WO_COMMENT_DATA)
        return True

    def test_1_set_comment(self):
        open_write_off(self.driver)

        comment = "This is comment."
        cell_idx = 5

        add_to_outcome(self.driver, WO_COMMENT_DATA['title'])
        set_value(self.driver, "[name=description]", comment)

        submit_write_off(self.driver)

        return raise_error(
            assert_added_to_table(
                self.driver, ".js-grid", cell_idx, comment
            ), TABLE_ERROR_MSG
        )


class ValidateWriteOff(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, WRITE_OFF_URL)

    @classmethod
    def tearDown(cls):
        close_write_off(cls.driver)

    def test_1_no_item_added(self):
        open_write_off(self.driver)

        wait_to_click_selector(self.driver, SUBMIT_WRITEOFF_BTN_SEL)
        find_element_by_selector(self.driver, SUBMIT_WRITEOFF_BTN_SEL).click()

        grid_sel = find_element_by_selector(
            self.driver, ".js-fletcher"
        )

        return assert_has_error_tooltip(self.driver, grid_sel)


class WriteOffAddRemoveGoods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_0_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, WO_DATA_1)
        return True

    def test_1_add_item(self):
        navigate(self.driver, WRITE_OFF_URL)
        open_write_off(self.driver)
        return add_to_outcome(self.driver, WO_DATA_1['title'])

    def test_2_remove_item(self):
        hover_and_click(self.driver, ".js-trasher")
        confirm_removal(self.driver)

        wait_selector_to_disappear(
            self.driver, make_selector(STACK_SEL, ".js-goods-group")
        )
        return close_write_off(self.driver)







