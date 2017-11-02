# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, INVOICES_URL

from src.lib.dom import find_element_by_selector, find_elements_by_selector
from src.lib.randomizer import random_z
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_see_selector,
    wait_to_click_selector,
)
from src.tests.invoices.lib import (wait_invoice_grid, open_first_invoice,
    select_invoice_in_grid, delete_invoice, ALL_INVOICE_CHECKBOX_SEL
)
from src.tests.invoices.lib.create import create_invoice_with_data
from src.tests.invoices.lib.select import (select_invoice_with_checkbox,
    click_to_button, select_menu_option, dialog_action
)

client_data = {
    'name' : "Mr. {0}".format(random_z()),
}

ALL_SELECTED_SEL = ".k-grid-header .js-selected-h"
SELECTED_SEL = ".h-checkbox"
MASS_EDIT_BTN = ".b-mass .b-btn"
INVOICE_NUM = 1
GRID_CONTENT_SEL = ".k-grid-content tr"
MENU_PRINT_IDX = 0
MENU_DELETE_IDX = 1
DIALOG_CLOSE_SEL = ".b-modal .js-close"
DIALOG_CONFIRMATION_SEL = ".b-modal .js-submit"


class VisibilityMassEditButton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)

    def setUp(self):
        create_invoice_with_data(self.driver, client_data)
        wait_invoice_grid(self.driver)


    def test1_select_invoice(self):
        select_invoice_with_checkbox(self.driver, SELECTED_SEL, INVOICE_NUM)
        wait_invoice_grid(self.driver)
        wait_to_see_selector(self.driver, MASS_EDIT_BTN)


    def test2_select_all_invoice(self):
        select_invoice_with_checkbox(self.driver, ALL_INVOICE_CHECKBOX_SEL)
        wait_invoice_grid(self.driver)
        wait_to_see_selector(self.driver, MASS_EDIT_BTN)


    def test3_disappear_mass_edit_button(self):
        select_invoice_with_checkbox(self.driver, ALL_INVOICE_CHECKBOX_SEL)
        wait_invoice_grid(self.driver)
        wait_to_see_selector(self.driver, MASS_EDIT_BTN)
        wait_invoice_grid(self.driver)
        find_element_by_selector(self.driver, ALL_INVOICE_CHECKBOX_SEL).click()
        wait_selector_to_disappear(self.driver, MASS_EDIT_BTN)

    def tearDown(self):
        select_invoice_in_grid(self.driver)
        delete_invoice(self.driver)



class DeleteInvoiceWithMassEdit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)


    def test1_check_delete_dialog_one_selected(self):
        create_invoice_with_data(self.driver, client_data)
        select_invoice_with_checkbox(self.driver, SELECTED_SEL, INVOICE_NUM)
        click_to_button(self.driver, MASS_EDIT_BTN)
        wait_to_see_selector(self.driver, ".b-mass .dropdown-menu")
        select_menu_option(self.driver, MENU_DELETE_IDX)
        dialog_action(self.driver, DIALOG_CLOSE_SEL)


    def test2_check_delete_dialog_all_selected(self):
        create_invoice_with_data(self.driver, client_data)

        select_invoice_with_checkbox(self.driver, ALL_INVOICE_CHECKBOX_SEL)
        click_to_button(self.driver, MASS_EDIT_BTN)
        wait_to_click_selector(self.driver, ".b-mass .dropdown-menu")
        select_menu_option(self.driver, MENU_DELETE_IDX)
        dialog_action(self.driver, DIALOG_CLOSE_SEL)


    def test3_delete_invoice(self):
        client_data1 = {
            'name' : "Mr. {0}".format(random_z()),
        }

        create_invoice_with_data(self.driver, client_data1)

        select_invoice_with_checkbox(self.driver, SELECTED_SEL, INVOICE_NUM)
        click_to_button(self.driver, MASS_EDIT_BTN)
        select_menu_option(self.driver, MENU_DELETE_IDX)
        dialog_action(self.driver, DIALOG_CONFIRMATION_SEL)
        wait_to_see_selector(self.driver, GRID_CONTENT_SEL)
        invoice_data_in_grid = find_element_by_selector(
            self.driver, GRID_CONTENT_SEL, INVOICE_NUM
        ).text
        self.assertNotIn(client_data1['name'], invoice_data_in_grid)


    def test4_delete_more_then_one_invoice(self):
        client_data_list = []
        num_new_invoice = 4
        invoice_idx = 1
        invoice_idx_grid = 1
        for i in range(num_new_invoice):
            client_name = {
            'name' : "Mr. {0}".format(random_z()),
            }
            create_invoice_with_data(self.driver, client_name)
            client_data_list.append(client_name['name'])

        for i in range(num_new_invoice):
            select_invoice_with_checkbox(self.driver, SELECTED_SEL, invoice_idx)
            invoice_idx = invoice_idx + 1
        click_to_button(self.driver, MASS_EDIT_BTN)
        select_menu_option(self.driver, MENU_DELETE_IDX)
        dialog_action(self.driver, DIALOG_CONFIRMATION_SEL)
        client = find_element_by_selector(
            self.driver, ".k-grid-content td:nth-child(4)", idx=1
        ).text
        self.assertNotIn(client, client_data_list)


    def test5_check_unselected_if_close_mass_edit_menu(self):

        select_invoice_with_checkbox(self.driver, ALL_INVOICE_CHECKBOX_SEL)
        wait_to_see_selector(self.driver, MASS_EDIT_BTN)
        find_element_by_selector(self.driver, ".b-mass .b-mass__close").click()
        wait_selector_to_disappear(self.driver, MASS_EDIT_BTN)
        self.assertFalse(self.driver.find_element_by_css_selector(
            ALL_INVOICE_CHECKBOX_SEL
            ).is_selected()
        )


    @classmethod
    def tearDownClass(cls):
        navigate(cls.driver, INVOICES_URL)


class PrintInvoiceWithMassEdit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, INVOICES_URL)


    def test1_check_print_dialog_one_selected(self):
        wait_invoice_grid(self.driver)
        select_invoice_with_checkbox(self.driver, SELECTED_SEL, INVOICE_NUM)
        click_to_button(self.driver, MASS_EDIT_BTN)
        wait_to_see_selector(self.driver, ".b-mass .dropdown-menu")
        select_menu_option(self.driver, MENU_PRINT_IDX)
        wait_to_see_selector(self.driver, DIALOG_CONFIRMATION_SEL)
        dialog_action(self.driver, DIALOG_CLOSE_SEL)
        wait_selector_to_disappear(self.driver, DIALOG_CLOSE_SEL)

    def test2_check_print_dialog_all_selected(self):
        wait_invoice_grid(self.driver)
        select_invoice_with_checkbox(self.driver, ALL_INVOICE_CHECKBOX_SEL)
        click_to_button(self.driver, MASS_EDIT_BTN)
        wait_to_see_selector(self.driver, ".b-mass .dropdown-menu")
        select_menu_option(self.driver, MENU_PRINT_IDX)
        wait_to_see_selector(self.driver, DIALOG_CONFIRMATION_SEL)
        dialog_action(self.driver, DIALOG_CLOSE_SEL)
        wait_selector_to_disappear(self.driver, DIALOG_CLOSE_SEL)
