#~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver
from src.lib.randomizer import random_z
from src.lib.url import navigate, POSTING_URL, INVENTORY_URL, WRITE_OFF_URL
from src.lib.dom import find_element_by_selector, double_click
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_see_selector,
    wait_to_click_selector,
)
from src.scaffolds.grid import wait_grid_updated, wait_grid_changed_rows_num
from src.scaffolds.dropdown import choose_from_select
from src.scaffolds.search import search_for

from src.tests.warehouse.lib import close_residue_dialog
from src.tests.warehouse.lib.create import (
    create_posting, make_write_off, post_existing_item,
    )
from src.tests.warehouse.lib.select import search_and_select, search_and_open
from src.tests.warehouse.lib.set_data import add_min_residue
from src.tests.warehouse.lib.clean_up import delete_residue




ALWAYS_FIRST_IN_LIST = "Anchor"

# Create posting with one quantity unit for make write off
def create_unique_item_data():
    return {
        u'title' : "{0} {1}".format(ALWAYS_FIRST_IN_LIST, random_z()),
        u'supplier' : {'name': u"Evan's Supplies"},
        u'quantity' : u"1",
        u'price' : u"100",
    }

# This residue control for PART_IN_STOCK
RESIDUE_CONTROL = {
    'min' : 11,
    'max' : 11,
}

# This data for write off part
ZERO_RESIDUE = u'0'

PART_IN_STOCK_SEL = ".k-grid-content tr td:nth-child(4)"
PART_NOT_IN_STOCK_SEL = ".k-grid-content tr td:nth-child(4) .h-c-muted"

BATCHES_IN_STOCK_SEL = ".js-batches-grid [data-uid] td:nth-child(6)"
BATCHES_NOT_INSTOCK_SEL = ".js-batches-grid [data-uid] .h-c-muted"

FILTER_SEL = ".js-wh-availability .b-sel"
BATCHES_FILTER_SEL = ".js-batches-availability .b-sel"

WAREHOUSE_DD_SEL = ".js-wh-id"
WAREHOUSE_IDX = 1

ALL_IDX = 0
ONLY_IN_STOCK_IDX = 1
NOT_IN_STOCK_IDX = 2
LOW_RESIDUE_IDX = 3

FIRST_STR_IDX = 0
SECOND_STR_IDX = 1
ACTIVE_STR = ".k-state-selected"
BATCHES_GRID_SEL = ".js-batches-grid tr"


class FilterTestsForResidueGrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        # create posting
        navigate(cls.driver, POSTING_URL)
        cls.part_for_zero_residue = create_unique_item_data()
        cls.part_in_stock = create_unique_item_data()
        cls.part_residue_control = create_unique_item_data()
        create_posting(cls.driver, cls.part_for_zero_residue)
        create_posting(cls.driver, cls.part_in_stock)
        create_posting(cls.driver, cls.part_residue_control)

        # make write off, part is not available
        navigate(cls.driver, WRITE_OFF_URL)
        make_write_off(cls.driver, cls.part_for_zero_residue)

        #add residue control
        navigate(cls.driver, INVENTORY_URL)
        search_and_select(cls.driver, cls.part_in_stock['title'])
        double_click(cls.driver, find_element_by_selector(
            cls.driver, ACTIVE_STR
            )
        )
        add_min_residue(cls.driver, RESIDUE_CONTROL)

    def setUp(self):
        navigate(self.driver, INVENTORY_URL)
        wait_to_see_selector(self.driver, FILTER_SEL)
        search_for(self.driver, ALWAYS_FIRST_IN_LIST)

    def test1_all_in_stock(self):
        choose_from_select(self.driver, WAREHOUSE_DD_SEL, WAREHOUSE_IDX)
        wait_to_see_selector(self.driver, ".k-grid-content tr")

        choose_from_select(self.driver, FILTER_SEL, ALL_IDX)
        wait_to_see_selector(self.driver, WAREHOUSE_DD_SEL)

        first = find_element_by_selector(
            self.driver, PART_IN_STOCK_SEL, FIRST_STR_IDX
        ).text
        second = find_element_by_selector(
            self.driver, PART_IN_STOCK_SEL, SECOND_STR_IDX
        ).text
        self.assertEqual(
            first, second and
            self.part_for_zero_residue['title'], self.part_in_stock['title']
        )

    def test2_only_in_stock(self):
        wait_to_see_selector(self.driver, FILTER_SEL)
        choose_from_select(self.driver, FILTER_SEL, ONLY_IN_STOCK_IDX)
        wait_selector_to_disappear(self.driver, PART_NOT_IN_STOCK_SEL)

        text_in_str = find_element_by_selector(
            self.driver, PART_IN_STOCK_SEL, FIRST_STR_IDX
        ).text

        self.assertEqual(text_in_str, self.part_in_stock['title'])

    def test3_not_in_stock(self):
        wait_to_see_selector(self.driver, FILTER_SEL)
        choose_from_select(self.driver, FILTER_SEL, NOT_IN_STOCK_IDX)
        wait_to_see_selector(self.driver, PART_NOT_IN_STOCK_SEL)

        text_in_str = find_element_by_selector(
            self.driver, PART_NOT_IN_STOCK_SEL, FIRST_STR_IDX
        ).text

        self.assertEqual(text_in_str, self.part_for_zero_residue['title'])

    def test4_low_residue(self):
        wait_to_see_selector(self.driver, FILTER_SEL)
        choose_from_select(self.driver, FILTER_SEL, LOW_RESIDUE_IDX)
        wait_selector_to_disappear(self.driver, PART_NOT_IN_STOCK_SEL)

        find_element_by_selector(
            self.driver,
            ".i-low-price-residue-icon",
        )

        text_in_str = find_element_by_selector(
            self.driver, PART_IN_STOCK_SEL, FIRST_STR_IDX
        ).text

        self.assertEqual(text_in_str, self.part_in_stock['title'])



class FilterTestsForBatches(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.driver = get_driver()
        cls.data_for_part = create_unique_item_data()
        # create posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.data_for_part)

        # make write off, part is not available
        navigate(cls.driver, WRITE_OFF_URL)
        make_write_off(cls.driver, cls.data_for_part)

        # make new batches for PART_NOT_AVAILABLE
        navigate(cls.driver, POSTING_URL)
        post_existing_item(cls.driver, cls.data_for_part)
        navigate(cls.driver, INVENTORY_URL)

        # select filter for residue grid
        wait_to_see_selector(cls.driver, FILTER_SEL)
        choose_from_select(cls.driver, FILTER_SEL, ALL_IDX)
        search_and_open(cls.driver, cls.data_for_part['title'])

    def setUp(self):
        wait_to_see_selector(self.driver, BATCHES_FILTER_SEL)

    def test1_all_in_stock(self):
        choose_from_select(self.driver, BATCHES_FILTER_SEL, ALL_IDX)
        wait_to_see_selector(self.driver, BATCHES_GRID_SEL)

        first = find_element_by_selector(
            self.driver, BATCHES_IN_STOCK_SEL, FIRST_STR_IDX
        ).text
        second = find_element_by_selector(
            self.driver, BATCHES_IN_STOCK_SEL, SECOND_STR_IDX
        ).text

        self.assertEqual(
            first, second and
            self.data_for_part['quantity'], ZERO_RESIDUE
        )

    def test2_only_in_stock(self):
        wait_to_see_selector(self.driver, BATCHES_GRID_SEL)
        choose_from_select(self.driver, BATCHES_FILTER_SEL, ONLY_IN_STOCK_IDX)
        wait_selector_to_disappear(self.driver, BATCHES_NOT_INSTOCK_SEL)

        quantity_in_str = find_element_by_selector(
            self.driver, BATCHES_IN_STOCK_SEL, FIRST_STR_IDX
        ).text

        self.assertEqual(quantity_in_str, self.data_for_part['quantity'])

    def test3_not_in_stock(self):
        wait_to_see_selector(self.driver, BATCHES_GRID_SEL)
        choose_from_select(self.driver, BATCHES_FILTER_SEL, NOT_IN_STOCK_IDX)
        wait_to_see_selector(self.driver, BATCHES_NOT_INSTOCK_SEL)

        quantity_in_str = find_element_by_selector(
            self.driver, BATCHES_IN_STOCK_SEL, FIRST_STR_IDX
        ).text

        self.assertEqual(quantity_in_str, ZERO_RESIDUE)

    @classmethod
    def tearDownClass(cls):
        # Set filter for all instock items and close card
        choose_from_select(cls.driver, BATCHES_FILTER_SEL, ALL_IDX)
        close_residue_dialog(cls.driver)