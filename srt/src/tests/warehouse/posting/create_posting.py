# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL
from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import (
    wait_to_see_selector, wait_to_click_selector, wait_selector_to_disappear
)

from src.tests.warehouse.lib import open_posting_dialog, close_posting_dialog
from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.save_trans import save_posting, save_pay_post
from src.tests.warehouse.lib.checkers import (
    check_item_in_table, assert_items_in_table
)
from src.tests.warehouse.lib.set_data import (
    set_new_good, set_instock_good, ADD_ITEM_BTN
)

from src.scaffolds.dialog import close_dialog
from src.scaffolds.dropdown import choose_category

from src.widget.client import fast_add_new_client


SPARES_CATEGORY = 1
CASHBOX_INDEX = 1
CASHBOX_SEL = ".js-cashboxes [name=cashbox]"


FIRST_POSTING_DATA = {
    u'supplier' : {'name': u"Evan's Supplies"},
    u'title' : u"Party chicken",
    u'quantity' : u"6",
    u'price' : u"100",
}
ITEM_DATA = {
    u'supplier' : {'name': u"Evan's Supplies"},
    u'title' : u"Rubber ducker",
    u'quantity' : u"15",
    u'price' : u"34.6",
}
ITEM_DATA_2 = {
    u'supplier' : {'name': u"Ricko Supplies"},
    u'title' : u"Wooden stuck",
    u'quantity' : u"7",
    u'price' : u"99.6",
}
GOOD1 = {
    u'supplier' : {'name': u"Scardo Supplies"},
    u'title' : u"Mega boots",
    u'quantity' : u"4",
    u'price' : u"77.77",
}
GOOD2 = {
    u'supplier' : {'name': u"Scardo Supplies"},
    u'title' : u"Wizard hat",
    u'quantity' : u"2",
    u'price' : u"300",
}


class CreatePosting(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)

    def test_1_open_close_dialog(self):
        # Posting doesn't close upon clicking on mask
        open_posting_dialog(self.driver)
        find_element_by_selector(self.driver, ".h-dialog-mask").click()

        time.sleep(1)
        wait_to_see_selector(self.driver, ".b-dialog_type_warehouse")

        # Close by clicking "close" button
        close_posting_dialog(self.driver)
        return True

    def test_2_post_new_item(self):
        create_posting(self.driver, FIRST_POSTING_DATA)
        return self.assertEqual(
            check_item_in_table(self.driver), FIRST_POSTING_DATA['title']
        )

    def test_3_post_existing_item(self):
        # Create new item
        create_posting(self.driver, ITEM_DATA)

        # Post this item again
        open_posting_dialog(self.driver)

        fast_add_new_client(self.driver, "#js-wh-supplier", ITEM_DATA['supplier'])
        set_instock_good(self.driver, ITEM_DATA)
        save_posting(self.driver)
        return self.assertEqual(
            check_item_in_table(self.driver), ITEM_DATA['title']
        )

    def test_4_post_few_items(self):
        open_posting_dialog(self.driver)
        fast_add_new_client(self.driver, "#js-wh-supplier", GOOD1['supplier'])
        set_new_good(self.driver, GOOD1, SPARES_CATEGORY)
        set_new_good(self.driver, GOOD2, SPARES_CATEGORY)

        save_posting(self.driver)

        item_list = [GOOD1['title'], GOOD2['title']]

        return assert_items_in_table(self.driver, item_list)


    def test_5_post_and_pay(self):
        open_posting_dialog(self.driver)
        fast_add_new_client(self.driver, "#js-wh-supplier", ITEM_DATA_2['supplier'])

        set_new_good(self.driver, ITEM_DATA_2, SPARES_CATEGORY)
        wait_to_click_selector(self.driver, "[for=ls-whcr-autocash] .h-checkbox")
        find_element_by_selector(
            self.driver, "[for=ls-whcr-autocash] .h-checkbox"
        ).click()

        save_pay_post(self.driver, CASHBOX_SEL, CASHBOX_INDEX)

        return self.assertEqual(
            check_item_in_table(self.driver), ITEM_DATA_2['title']
        )

        # turns off autosaved checkbox for payment in posting form
    def test_6_cleanup(self):
        open_posting_dialog(self.driver)
        wait_to_click_selector(self.driver, "[for=ls-whcr-autocash] .h-checkbox")
        find_element_by_selector(
            self.driver, "[for=ls-whcr-autocash] .h-checkbox"
        ).click()

        return close_posting_dialog(self.driver)


