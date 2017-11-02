# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver
from src.lib.randomizer import random_z

from src.lib.url import navigate, POSTING_URL, SHOP_URL, ORDERS_URL
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_to_see_selector, wait_to_click_selector


from src.scaffolds.dialog import close_dialog

from src.tests.shop.lib.sale import make_sale

from src.tests.refunds.lib.refund import make_sale_refund, make_order_refund

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, close_order
from src.tests.orders.lib.status import close_and_pay_from_order
from src.tests.orders.spare_parts_and_works.lib.part import add_part_by_title

from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.batches.lib import (
    create_data_with_quantity, open_batches, BATCHES_SEL, close_part_dialog,
    DATA_FOR_BASE_ON,
)


CREATED_AT_SEL = ".js-batches-grid [data-uid] td:nth-child(3)"



STR_IDX = 0
STR_IDX_REFUND = 1
CLOSED_STATUS_INDEX = -1
MAIN_CASHBOX_INDEX = 1
QUANTITY = 20


class CreateBatchesValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.item_data = create_data_with_quantity(QUANTITY)

        # New posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.item_data)

    def test1_posting(self):
        # Open part
        open_batches(self.driver, self.item_data['title'])

        quantity_in_grid = find_element_by_selector(
            self.driver, BATCHES_SEL, STR_IDX
        ).text
        close_part_dialog(self.driver)
        # close_order(self.driver)
        self.assertEqual(str(self.item_data['quantity']), quantity_in_grid)

    def test2_refund_with_sale(self):
        navigate(self.driver, SHOP_URL)
        make_sale(self.driver, self.item_data['title'])
        wait_to_see_selector(self.driver, ".k-grid-content")
        make_sale_refund(self.driver)

        open_batches(self.driver, self.item_data['title'])


        created_at_in_grid = find_element_by_selector(
            self.driver, CREATED_AT_SEL, STR_IDX
        ).text
        '''
        refund with sale we can identificated only with created at document
        in grid it hardcode value
        when we will be run localisation tests, we need create the mechanism,
        which will be use true data values
        '''
        close_part_dialog(self.driver)
        self.assertEqual(created_at_in_grid, DATA_FOR_BASE_ON['refund'])

    def test3_refund_with_order(self):
        navigate(self.driver, ORDERS_URL)
        wait_to_click_selector(self.driver, ".js-orders-add")
        create_order(self.driver)
        open_order(self.driver)
        add_part_by_title(self.driver, self.item_data['title'])

        close_and_pay_from_order(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )
        close_order(self.driver)
        wait_to_see_selector(self.driver, ".js-orders-grid")
        make_order_refund(self.driver)

        open_batches(self.driver, self.item_data['title'])
        created_at_in_grid = find_element_by_selector(
            self.driver, CREATED_AT_SEL, STR_IDX
        ).text
        self.assertEqual(created_at_in_grid, DATA_FOR_BASE_ON['refund'])


    @classmethod
    def tearDownClass(cls):
        close_part_dialog(cls.driver)
