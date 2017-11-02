# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver

from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import wait_selector_to_disappear, wait_to_see_selector
from src.scaffolds.dropdown import choose_cashbox, choose_select_by_text


CASHBOX_SEL = ".js-cashboxes"
INCOME_BTN_SEL = ".js-income"
OUTCOME_BTN_SEL = ".js-outcome"
INPUT_PRICE_SEL = ".b-dialog__content .h-price-field"
DEFAULT_CASHBOX_IDX = 1

'''
Template data for order_payment_income/outcome
    data = {
    'price' : price,
    'cashier' : cashier_name,
    }
'''


def select_cashbox(driver, data=None):
    choose_select_by_text

def select_cashier(driver, data=None):
    choose_select_by_text

def open_income_dialog(driver):
    find_element_by_selector(driver, INCOME_BTN_SEL).click()
    return wait_to_see_selector(driver, ".b-dialog")

def open_outcome_dialog(driver):
    find_element_by_selector(driver, OUTCOME_BTN_SEL).click()
    return wait_to_see_selector(driver, ".b-dialog")

def close_order_payment(driver):
    find_element_by_selector(driver, ".b-dialog__content .js-close-dialog").click()
    return wait_selector_to_disappear(driver, ".b-dialog__content .js-close-dialog")

def save_order_payment(driver):
    find_element_by_selector(driver, ".b-dialog__content .js-submit-dialog").click()
    return wait_selector_to_disappear(driver, ".b-dialog__content .js-submit-dialog")


# TODO: relocated this block to orders/lib/payments
def create_order_income(driver, data, idx=None):
    idx = idx or DEFAULT_CASHBOX_IDX

    open_income_dialog(driver)
    choose_cashbox(driver, ".b-sel-holder [name=cashbox]", idx)
    set_value(driver, ".h-price-field [name=payment]", data['price'])
    return save_order_payment(driver)

def create_order_outcome(driver, data, idx=None):
    idx = idx or DEFAULT_CASHBOX_IDX

    open_outcome_dialog(driver)
    choose_cashbox(driver, ".b-sel-holder [name=cashbox]", idx)
    set_value(driver, ".h-price-field [name=payment]", data['price'])
    return save_order_payment(driver)
