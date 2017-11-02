#~*~ coding: utf-8 ~*~
import unittest
import time
from selenium.common.exceptions import WebDriverException

from src.lib.driver import get_driver
from src.lib.url import navigate, INVOICES_URL
from src.lib.randomizer import random_z
from src.lib.wait import (
    wait_for_selector, wait_to_see_selector, wait_selector_to_disappear,
    wait_to_click_selector,
)
from src.lib.dom import find_element_by_selector
from src.lib.notify import wait_notify_worked


from src.tests.invoices.lib import (
    close_invoice_dialog, wait_invoice_grid, open_first_invoice, delete_invoice,
    select_invoice_in_grid,
)
from src.tests.invoices.lib.create import create_invoice_with_data
from src.tests.invoices.lib.status import get_status_idx, select_status


def client_data1():
    return {
        'name' : "Mr. {0}".format(random_z()),
        }

client_data = {
    'name' : "Mr. {0}".format(random_z()),
    }

STATUSES = [0, 1, 2, 3]

STATUS_LIST = [3, 0, 1, 2]


STATUS_IDX = 3
STATUS_SEL = ".js-status-{0} .b-statuses__item".format(STATUS_IDX)
STATUS_IN_GRID_SEL = ".js-status-label"
DD_STATUS_SEL = ".js-status-ddown"
STATUS_IN_DIALOG_SEL = ".b-invoice__header .js-invoice-status"


class ChangeOfStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)

    def setUp(self):
        wait_to_see_selector(self.driver,".js-add-invoice", 10)
        create_invoice_with_data(self.driver, client_data)
        wait_to_see_selector(self.driver, ".k-grid-content [data-uid]", 10)


    def test1_change_from_table(self):
        default_idx = get_status_idx(self.driver, STATUS_IN_GRID_SEL)
        default_idx_sel = ".js-status-label[data-status='{0}']".format(
            default_idx
        )
        wait_to_see_selector(self.driver, STATUS_IN_GRID_SEL)
        find_element_by_selector(self.driver, STATUS_IN_GRID_SEL).click()
        wait_to_see_selector(self.driver, DD_STATUS_SEL)

        select_status(self.driver, STATUS_SEL)
        wait_selector_to_disappear(self.driver, DD_STATUS_SEL)
        wait_selector_to_disappear(self.driver, default_idx_sel, 10)

        new_status_idx = get_status_idx(self.driver, STATUS_IN_GRID_SEL)
        self.assertEqual(STATUSES[STATUS_IDX], new_status_idx)


    def test2_change_from_dialog(self):
        open_first_invoice(self.driver)
        default_idx = get_status_idx(self.driver, STATUS_IN_DIALOG_SEL)
        default_idx_sel = ".js-invoice-status[data-status='{0}']".format(
            default_idx
        )
        wait_to_see_selector(self.driver, STATUS_IN_DIALOG_SEL)
        wait_notify_worked(self.driver)
        find_element_by_selector(self.driver, STATUS_IN_DIALOG_SEL).click()
        wait_to_see_selector(self.driver, DD_STATUS_SEL, 10)
        select_status(self.driver, STATUS_SEL)
        wait_selector_to_disappear(self.driver, ".b-invoice .b-statuses__list")
        wait_selector_to_disappear(self.driver, default_idx_sel)
        new_status_idx_in_dialog = get_status_idx(
            self.driver, STATUS_IN_DIALOG_SEL
        )
        close_invoice_dialog(self.driver)
        wait_to_see_selector(self.driver, ".k-grid-content")
        self.assertEqual(STATUSES[STATUS_IDX], new_status_idx_in_dialog)


    def test3_change_in_table_check_in_dialog(self):
        default_idx = get_status_idx(self.driver, STATUS_IN_GRID_SEL)
        default_idx_sel = ".js-status-label[data-status='{0}']".format(
            default_idx
        )
        find_element_by_selector(self.driver, STATUS_IN_GRID_SEL).click()
        wait_to_see_selector(self.driver, DD_STATUS_SEL)
        select_status(self.driver, STATUS_SEL)
        wait_selector_to_disappear(self.driver, DD_STATUS_SEL)
        wait_selector_to_disappear(self.driver, default_idx_sel,10)

        new_status_idx = get_status_idx(self.driver, STATUS_IN_GRID_SEL)
        open_first_invoice(self.driver)
        status_idx_dialog = get_status_idx(self.driver, STATUS_IN_DIALOG_SEL)
        close_invoice_dialog(self.driver)
        self.assertEqual(status_idx_dialog, new_status_idx)


    def test4_change_in_dialog_check_in_table(self):
        open_first_invoice(self.driver)

        wait_to_click_selector(self.driver, STATUS_IN_DIALOG_SEL, 10)

        default_idx = get_status_idx(self.driver, STATUS_IN_DIALOG_SEL)
        default_idx_sel = ".js-invoice-status[data-status='{0}']".format(
            default_idx
        )
        wait_notify_worked(self.driver)
        find_element_by_selector(self.driver, STATUS_IN_DIALOG_SEL).click()
        wait_to_see_selector(self.driver, DD_STATUS_SEL)
        select_status(self.driver, STATUS_SEL)

        wait_selector_to_disappear(self.driver, ".b-invoice .b-statuses__list")
        wait_selector_to_disappear(self.driver, default_idx_sel)

        new_status_idx_dialog = get_status_idx(
            self.driver, STATUS_IN_DIALOG_SEL
        )
        close_invoice_dialog(self.driver)
        wait_invoice_grid(self.driver)
        status_idx_grid = get_status_idx(self.driver, STATUS_IN_GRID_SEL)
        self.assertEqual(new_status_idx_dialog, status_idx_grid)

    def tearDown(self):
        select_invoice_in_grid(self.driver)
        delete_invoice(self.driver)


class ChangeStatusWithSelectedStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c_data = client_data1()
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)


    def test1_change_any_not_specific_status(self):
        create_invoice_with_data(self.driver, self.c_data)
        wait_invoice_grid(self.driver)
        def _status_change(idx):
            wait_to_see_selector(self.driver, STATUS_IN_GRID_SEL)
            find_element_by_selector(
                self.driver, STATUS_IN_GRID_SEL
                ).click()
            wait_to_see_selector(self.driver, DD_STATUS_SEL)
            find_element_by_selector(
                self.driver, ".js-status-{0} .b-statuses__item".format(idx)
                ).click()
            wait_selector_to_disappear(
                self.driver, ".b-invoice .b-statuses__list"
                )
            wait_selector_to_disappear(
                self.driver, ".js-status-{0} .b-statuses__item".format(idx)
                )
        map(_status_change, STATUS_LIST)

    def tearDown(self):
        select_invoice_in_grid(self.driver)
        delete_invoice(self.driver)


class ChangeInvoiceWithSelectedStatus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c_data = client_data1()
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)


    def test1_change_invoice_with_any_not_specific_status(self):
        create_invoice_with_data(self.driver, self.c_data)
        wait_notify_worked(self.driver)
        open_first_invoice(self.driver)

        def _status_change(idx):
            wait_to_see_selector(self.driver, STATUS_IN_DIALOG_SEL)
            find_element_by_selector(
                self.driver, STATUS_IN_DIALOG_SEL
            ).click()
            wait_to_see_selector(
                self.driver, ".js-invoice-wrapper .b-statuses__list", time=10
            )
            find_element_by_selector(
                self.driver, ".js-status-{0} .b-statuses__item".format(idx)
            ).click()
            wait_selector_to_disappear(
                self.driver, ".b-invoice .b-statuses__list"
            )
            wait_to_see_selector(self.driver,".b-invoice .js-dialog-submit")
        map(_status_change, STATUS_LIST)
        close_invoice_dialog(self.driver)

    def tearDown(self):
        select_invoice_in_grid(self.driver)
        delete_invoice(self.driver)
