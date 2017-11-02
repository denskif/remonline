# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver

from src.lib.url import (
    navigate, POSTING_URL, SHOP_URL, ORDERS_URL, REFUND_URL, WRITE_OFF_URL,
    INVENTORY_URL, MOVE_URL,
)
from src.lib.dom import make_selector, hover_and_click
from src.lib.wait import wait_to_see_selector, wait_to_click_selector

from src.scaffolds.dialog import confirm_new_delete_dialog

from src.tests.shop.lib.sale import delete_sale, make_sale

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.delete import delete_order
from src.tests.orders.lib.open import open_order, close_order
from src.tests.orders.lib.status import close_and_pay_from_order
from src.tests.orders.spare_parts_and_works.lib.part import add_part_by_title

from src.tests.refunds.lib import REFUND_FIRST_ROW_CELL_SEL
from src.tests.refunds.lib.refund import make_sale_refund, make_order_refund

from src.tests.warehouse.lib.create import (
    create_posting, make_write_off, make_stock_name, create_local_stock
)
from src.tests.warehouse.lib.clean_up import delete_write_off
from src.tests.warehouse.batches.lib import (
    create_data_with_quantity, open_batches, get_text_from_grid,
    close_part_dialog, create_movement, get_base_on_text, DATA_FOR_BASE_ON,
)


STR_IDX = 0
STR_IDX_REFUND = 1
CLOSED_STATUS_INDEX = -1
MAIN_CASHBOX_INDEX = 1

QUANTITY_REFUND = 1
QUANTITY_MOVE = 1

STR_IDX_FIRST_BATCH = 1
STR_IDX_SECOND_BATCH = 0


# It`s big testcase, testing sale, refund,  deleting refund, deleting sale
class MoveSaleBatchesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        quantity = 10
        cls.driver = get_driver()
        cls.item_data = create_data_with_quantity(quantity)

        # New posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.item_data)

    def test1_residue_before_refund(self):
        # Make sale
        navigate(self.driver, SHOP_URL)
        make_sale(self.driver, self.item_data['title'])

        # See residue after sale
        open_batches(self.driver, self.item_data['title'])
        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertNotEqual(int(residue), int(self.item_data['quantity']))

    def test2_residue_after_refund(self):

        # Make sale refund
        navigate(self.driver, SHOP_URL)
        make_sale_refund(self.driver, QUANTITY_REFUND)

        open_batches(self.driver, self.item_data['title'])
        residue = get_text_from_grid(self.driver, STR_IDX_REFUND)
        close_part_dialog(self.driver)
        self.assertEqual(
            int(residue), self.item_data['quantity']-QUANTITY_REFUND
        )

    def test3_residue_after_delete_refund(self):
        # Delete refund
        navigate(self.driver, REFUND_URL)
        wait_to_see_selector(self.driver, REFUND_FIRST_ROW_CELL_SEL)
        hover_and_click(
            self.driver, make_selector(REFUND_FIRST_ROW_CELL_SEL, ".i-trash")
        )
        confirm_new_delete_dialog(self.driver)

        # See residue after delete refund
        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertNotEqual(int(residue), self.item_data['quantity'])

    def test4_residue_after_delete_sale(self):
        #Delete sale
        navigate(self.driver, SHOP_URL)
        delete_sale(self.driver)

        #Check residue
        open_batches(self.driver, self.item_data['title'])
        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertEqual(int(residue), self.item_data['quantity'])


class MoveOrderBatchesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        quantity = 5
        cls.driver = get_driver()
        cls.item_data = create_data_with_quantity(quantity)

        # New posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.item_data)

    def test1_residue_before_refund(self):
        # Make order
        navigate(self.driver, ORDERS_URL)
        wait_to_click_selector(self.driver, ".js-orders-add")
        create_order(self.driver)
        open_order(self.driver)
        add_part_by_title(self.driver, self.item_data['title'])
        close_and_pay_from_order(
            self.driver, CLOSED_STATUS_INDEX, MAIN_CASHBOX_INDEX
        )
        close_order(self.driver)

        # See residue after outcome to order
        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertNotEqual(int(residue), self.item_data['quantity'])

    def test2_residue_after_refund(self):
        # Make order refund
        navigate(self.driver, ORDERS_URL)
        wait_to_see_selector(self.driver, ".js-orders-grid tr")
        make_order_refund(self.driver)

        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX_REFUND)
        close_part_dialog(self.driver)
        self.assertEqual(
            int(residue), self.item_data['quantity']-QUANTITY_REFUND
        )

    def test3_residue_after_delete_refund(self):
        # Delete refund
        navigate(self.driver, REFUND_URL)
        wait_to_see_selector(self.driver, REFUND_FIRST_ROW_CELL_SEL)
        hover_and_click(
            self.driver, make_selector(REFUND_FIRST_ROW_CELL_SEL, ".i-trash")
        )
        confirm_new_delete_dialog(self.driver)

        # See residue after delete refund
        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertNotEqual(int(residue), self.item_data['quantity'])

    def test4_residue_after_delete_order(self):
        #Delete sale
        navigate(self.driver, ORDERS_URL)
        wait_to_see_selector(self.driver, ".js-orders-grid tr")
        open_order(self.driver)
        delete_order(self.driver)

        #Check residue
        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertEqual(int(residue), self.item_data['quantity'])


class WriteOffBatchesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        quantity = 10
        cls.driver = get_driver()
        cls.item_data = create_data_with_quantity(quantity)

        # New posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.item_data)

    def test1_residue_after_write_off(self):
        quantity_write_off = 1
        # Make write_off
        navigate(self.driver, WRITE_OFF_URL)
        make_write_off(self.driver, self.item_data)

        # See residue after write_off
        open_batches(self.driver, self.item_data['title'])

        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertEqual(
            int(residue), self.item_data['quantity'] - quantity_write_off
        )

    def test2_residue_after_delete_write_off(self):
        # Delete write_off
        navigate(self.driver, WRITE_OFF_URL)
        delete_write_off(self.driver)

        # See residue after delete write_off
        open_batches(self.driver, self.item_data['title'])
        residue = get_text_from_grid(self.driver, STR_IDX)
        close_part_dialog(self.driver)
        self.assertEqual(int(residue), self.item_data['quantity'])


class WarehouseMoveBatchesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        quantity = 10
        cls.driver = get_driver()
        cls.item_data = create_data_with_quantity(quantity)
        cls.stock_name = "AAA Stock" # This stock should always be in the top

        # New posting
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.item_data)

        # New warehouse(stock)
        navigate(cls.driver, INVENTORY_URL)
        create_local_stock(cls.driver, cls.stock_name)

        # New move
        navigate(cls.driver, MOVE_URL)
        create_movement(cls.driver, cls.item_data['title'], cls.stock_name)

    def test1_residue_in_new_batch(self):
        # New batch is a movement batch
        navigate(self.driver, INVENTORY_URL)
        open_batches(self.driver, self.item_data['title'])
        residue = get_text_from_grid(self.driver, STR_IDX_SECOND_BATCH)
        base_on = get_base_on_text(self.driver, STR_IDX_SECOND_BATCH)
        self.assertEqual(
            base_on, int(residue) and DATA_FOR_BASE_ON['move'],QUANTITY_MOVE
        )

    def test2_residue_in_old_batches(self):
        # old batch is a posting batch
        residue = get_text_from_grid(self.driver, STR_IDX_FIRST_BATCH)
        self.assertEqual(
            int(residue), self.item_data['quantity'] - QUANTITY_MOVE
        )
