# ~*~ coding: utf-8 ~*~

from selenium.webdriver.common.keys import Keys

from src.scaffolds.dialog import open_dialog, close_dialog, confirm_delete

from src.lib.dom import find_element_by_selector, find_elements_by_selector, set_value
from src.lib.wait import wait_for_selector, wait_to_see_selector, wait_to_click_selector
from src.lib.randomizer import random_x
from src.widget.client import fast_add_new_client


ALL_INVOICE_CHECKBOX_SEL = ".k-grid-header .h-checkbox"

INVOICE_DIALOG_SEL = ".b-invoice .js-client-picker"
GRID_ELEMENTS_SEL = ".k-grid-content tr"
DELETE_INVOICE = ".js-delete-invoice"
INVOICE_CLIENT_SEL = ".k-grid-content tbody tr td [href]"
INPUT_ORDER = ".js-order-input"
INPUT_COMMENT = ".js-invoice-comment"

ADD_INVOICE =".js-add-invoice"
CLOSE_SEL = ".js-dialog-cancel"
SAVE_SEL = ".js-dialog-submit"

ORDER_N = "D53"
NON_EXISTED_ORDER_N = "A{0}".format(random_x())
COMMENT = "It`s a nice comment for invoice{0}".format(random_x())


def open_invoice_dialog(driver):
    return open_dialog(driver, ADD_INVOICE, INVOICE_DIALOG_SEL)


def close_invoice_dialog(driver):
    return close_dialog(driver, CLOSE_SEL, INVOICE_DIALOG_SEL)


def save_invoice(driver):
    return close_dialog(driver, SAVE_SEL, SAVE_SEL)


def all_invoices_in_grid(driver):
    return find_elements_by_selector(driver, GRID_ELEMENTS_SEL)


def wait_invoice_grid(driver):
    return wait_for_selector(driver, GRID_ELEMENTS_SEL)


def add_order(driver, order_number):
    set_value(driver, INPUT_ORDER, order_number)
    return find_element_by_selector(driver, INPUT_ORDER).send_keys(Keys.ENTER)


def delete_invoice(driver):
    wait_to_see_selector(driver, DELETE_INVOICE)
    find_element_by_selector(driver, DELETE_INVOICE).click()
    return confirm_delete(driver)


def open_first_invoice(driver):
    find_element_by_selector(driver, INVOICE_CLIENT_SEL).click()
    return wait_to_see_selector(driver, INVOICE_DIALOG_SEL)


def add_comment(driver, data):
    return set_value(driver, INPUT_COMMENT, data)


def select_invoice_in_grid(driver, idx = None):
    sel = ".k-grid-content td:nth-child(2) [href]"
    wait_to_click_selector(driver, sel, 10)
    return find_element_by_selector(driver, sel, idx=None).click()


