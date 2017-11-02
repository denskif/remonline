#~*~ coding: utf-8 ~*~
import unittest
import time
from selenium.webdriver.common.keys import Keys

from src.lib.driver import get_driver
from src.lib.url import navigate, INVOICES_URL, ORDERS_URL
from src.lib.wait import wait_for_selector, wait_to_see_selector, wait_selector_to_disappear
from src.lib.dom import find_element_by_selector, get_value, set_value

from src.tests.invoices.lib import (
    save_invoice, all_invoices_in_grid, wait_invoice_grid,
    NON_EXISTED_ORDER_N, ORDER_N, COMMENT, open_invoice_dialog, close_invoice_dialog,
    add_order, delete_invoice, open_first_invoice, add_comment, ALL_INVOICE_CHECKBOX_SEL
)
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order
from src.tests.orders.lib.save_order import save_order
from src.tests.invoices.lib.select import select_invoice_with_checkbox
from src.tests.invoices.lib.create import delete_all_invoices
from src.scaffolds.dialog import close_dialog
from src.widget.client import fast_add_new_client
from src.widget.services_and_spare_parts import fast_add_new_service
from src.lib.randomizer import random_x
from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc

CLIENT_SEL = ".js-client-picker [name=client_id]"
DATA = {'name' : "Service #. {0}".format(random_x())}
INPUT_FIELD_SEL = ".b-in-holder .js-prod-search-input"
GRID_SEL = ".b-table .js-goods-group"
GRID_ELEMENTS_SEL = ".js-goods-group tr"
LAST_SERVICE_STRING_INDEX = -1
SERVICE_NAME = ".js-group-undefined .b-table__tr"
ERROR_SEL = ".h-errors-tooltip .js-order-input"


class CreateInvoice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)

    def test1_create_empty_invoice(self):
        wait_to_see_selector(self.driver, ".k-grid-content")
        open_invoice_dialog(self.driver)
        fast_add_new_client(self.driver, CLIENT_SEL)
        save_invoice(self.driver)
        wait_to_see_selector(self.driver, ".k-grid-content tr")

    def test2_invalid_order_input(self):
        open_invoice_dialog(self.driver)
        fast_add_new_client(self.driver, CLIENT_SEL)
        add_order(self.driver, NON_EXISTED_ORDER_N)
        wait_for_selector(self.driver, ERROR_SEL)
        close_invoice_dialog(self.driver)

    @classmethod
    def tearDownClass(cls):
        delete_all_invoices(cls.driver)


class CreateInvoiceWithData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        manual_add_new_srvc(cls.driver)
        save_order(cls.driver)

        cls.order_number = find_element_by_selector(
            cls.driver,
            ".k-grid-content [data-order-id]", idx=0
        ).text
        navigate(cls.driver, INVOICES_URL)
        open_invoice_dialog(cls.driver)
        fast_add_new_client(cls.driver, CLIENT_SEL)
        add_order(cls.driver, cls.order_number)
        wait_to_see_selector(cls.driver, ".b-dialog .js-goods-group")
        add_comment(cls.driver, COMMENT)

        fast_add_new_service(cls.driver, INPUT_FIELD_SEL, DATA)
        save_invoice(cls.driver)
        wait_selector_to_disappear(cls.driver, ".h-blink-yellow-1")
        wait_invoice_grid(cls.driver)
        cls.old_list_invoice = len(all_invoices_in_grid(cls.driver))
        open_first_invoice(cls.driver)

    def test1_check_comment(self):
        comment = get_value(
            find_element_by_selector(
                self.driver, ".b-invoice__content .js-invoice-comment"
            )
        )
        self.assertEqual(COMMENT, comment)

    def test2_check_true_order_number(self):
        order = find_element_by_selector(self.driver, ".js-group-header").text
        self.assertIn(self.order_number, order)


    def test3_check_work(self):
        service_name = find_element_by_selector(
            self.driver,
            SERVICE_NAME,
            idx=1
        ).text
        self.assertIn(DATA['name'], service_name)


    def test4_check_comment_in_table(self):
        close_invoice_dialog(self.driver)
        comment_in_grid = find_element_by_selector(
            self.driver, ".k-grid-content [data-uid] td:nth-child(7)"
        ).text
        self.assertEqual(comment_in_grid, COMMENT)

    def test5_delete_invoice(self):
        open_first_invoice(self.driver)
        delete_invoice(self.driver)
        wait_selector_to_disappear(self.driver, ".k-grid .kl-selectable td")
