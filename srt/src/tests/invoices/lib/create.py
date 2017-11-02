#~*~ coding: utf-8 ~*~
import unittest

from src.tests.invoices.lib import (
    open_invoice_dialog, save_invoice, ALL_INVOICE_CHECKBOX_SEL
)

from src.widget.client import fast_add_new_client
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.lib.dom import find_element_by_selector
from src.tests.invoices.lib.select import select_invoice_with_checkbox


def create_invoice_with_data(driver, client_data):

    CLIENT_SEL = ".js-client-picker [name=client_id]"
    open_invoice_dialog(driver)
    wait_to_see_selector(driver, ".b-dialog .b-invoice__header", 10)
    fast_add_new_client(driver, CLIENT_SEL, client_data)
    return save_invoice(driver)

def delete_all_invoices(driver):
    blue_btn = ".b-page__content .k-grid-pager .b-btn_color_blue"
    select_invoice_with_checkbox(driver, ALL_INVOICE_CHECKBOX_SEL)
    wait_to_see_selector(driver, blue_btn)
    find_element_by_selector(driver, blue_btn).click()
    wait_to_see_selector(driver, ".dropup")
    find_element_by_selector(driver, ".dropup .js-action", idx=1).click()
    wait_to_see_selector(driver, ".b-modal_type_confirm")
    find_element_by_selector(driver, ".b-modal_type_confirm .js-submit").click()
    return wait_selector_to_disappear(driver, ".b-modal_type_confirm")
