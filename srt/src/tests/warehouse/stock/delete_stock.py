# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, INVENTORY_URL, POSTING_URL
from src.lib.notify import wait_notify_worked
from src.lib.wait import wait_for_selector
from src.lib.dom import find_element_by_selector, set_value

from src.scaffolds.dialog import confirm_delete
from src.scaffolds.dropdown import choose_stock_by_name

from src.widget.client import fast_add_new_client

from src.tests.warehouse.lib import open_posting_dialog
from src.tests.warehouse.lib.create import (
    create_local_stock, create_global_stock, make_stock_name
)
from src.tests.warehouse.lib.clean_up import clean_up_stock, delete_stock
from src.tests.warehouse.lib.set_data import set_new_good
from src.tests.warehouse.lib.save_trans import save_posting
from src.tests.warehouse.lib.checkers import check_item_in_table


CUSTOM_STOCK = make_stock_name()
SPARES_CATEGORY = 1
STOCK_SEL = ".js-warehouses [name=warehouse]"

CUSTOM_ITEM = {
    u'supplier' : {'name': u"Magic Midgets Inc."},
    u'title' : u"Proctor Case",
    u'quantity' : u"2",
    u'price' : u"34.6",
}


class DeleteStock(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_1_remove_local_stock(self):
        create_local_stock(self.driver)
        return delete_stock(self.driver)

    def test_2_remove_global_stock(self):
        create_global_stock(self.driver)
        return delete_stock(self.driver)


class DeleteLastStock(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_0_clean_up(self):
        wait_for_selector(self.driver, STOCK_SEL)
        clean_up_stock(self.driver)
        return True

    def test_1_dont_remove_last_stock(self):
        wait_for_selector(self.driver, STOCK_SEL)

        find_element_by_selector(self.driver, ".js-wh-remove").click()
        confirm_delete(self.driver)

        wait_notify_worked(self.driver)
        return wait_for_selector(self.driver, STOCK_SEL)


class DeleteStockWithItem(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVENTORY_URL)

    def test_1_create_stock(self):
        create_local_stock(self.driver, CUSTOM_STOCK)
        return True

    def test_2_post_item_to_custom_stock(self):
        navigate(self.driver, POSTING_URL)

        open_posting_dialog(self.driver)

        choose_stock_by_name(self.driver, CUSTOM_STOCK)
        fast_add_new_client(self.driver, "#js-wh-supplier", CUSTOM_ITEM['supplier'])
        set_new_good(self.driver, CUSTOM_ITEM, SPARES_CATEGORY)

        save_posting(self.driver)
        wait_notify_worked(self.driver)
        return self.assertEqual(
            check_item_in_table(self.driver), CUSTOM_ITEM['title']
        )

    def test_3_delete_stock_with_residue(self):
        wait_for_selector(self.driver, STOCK_SEL)

        choose_stock_by_name(self.driver, CUSTOM_STOCK)

        find_element_by_selector(self.driver, ".js-wh-remove").click()
        confirm_delete(self.driver)

        wait_notify_worked(self.driver)
        return wait_for_selector(self.driver, STOCK_SEL)




