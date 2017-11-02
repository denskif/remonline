# ~*~ coding: utf-8 ~*~


import unittest, time

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value
from src.tests.orders.spare_parts_and_works.lib.save import save_srvc
from src.lib.errors import assert_has_error_tooltip
from src.lib.wait import wait_selector_to_disappear

WINBOX_SEL = ".js-winbox .b-winbox"


WINBOX_CHBX_SEL = ".b-checkbox__label"
WINBOX_D_INPUT_SEL = ".js-discount-holder [name=discount_value]"
WINBOX_W_INPUT_SEL = ".js-warranty-holder [name=warranty_value]"
TYPE_DISCOUNT = ".js-discount-sponsor .js-item-label"
SAVE_BTN = ".js-submit-good"


def _make_input_sel(attr_val):
    return ".b-winbox [name='{0}']".format(attr_val)

# --------
def input_tests(driver, lis, attr_val):
    input_sel = _make_input_sel(attr_val)

    for value in lis:
        find_element_by_selector(driver, input_sel).click()
        find_element_by_selector(driver, input_sel).clear()
        set_value(driver, input_sel, value)
        save_srvc(driver)
        error = find_element_by_selector(driver, input_sel)
        assert_has_error_tooltip(driver, error)

# --------
def checkbox_input_test(driver, lis, sel):
    for value in lis:
        find_element_by_selector(driver, sel).click()
        find_element_by_selector(driver, sel).clear()
        set_value(driver, sel, value)
        save_srvc(driver)
        error = find_element_by_selector(driver, sel)
        assert_has_error_tooltip(driver, error)

# ----------
def input_checkbox(driver, sel, val):
    find_element_by_selector(driver, sel).click()
    find_element_by_selector(driver, sel).clear()
    return set_value(driver, sel, val)


def set_text(driver, attr_val, val):
    input_sel = _make_input_sel(attr_val)
    return set_value(driver, input_sel, val)


def clear_text_input(driver, attr_val):
    input_sel = _make_input_sel(attr_val)
    find_element_by_selector(driver, input_sel).click()
    return find_element_by_selector(driver, input_sel).clear()


def text_input_assert(driver, attr_val):
    input_sel = _make_input_sel(attr_val)
    error = find_element_by_selector(driver, input_sel)
    return assert_has_error_tooltip(driver, error)


def close_winbox(driver):
    CLOSE_WINBOX_SEL = ".b-winbox .b-winbox__header .b-close"
    time.sleep(2)
    find_element_by_selector(driver, CLOSE_WINBOX_SEL).click()
    return wait_selector_to_disappear(driver, CLOSE_WINBOX_SEL)

# ------
def close_litebox(driver):
    CLOSE_LITEBOX_SEL = ".b-litebox .js-remove-dismiss"
    find_element_by_selector(driver, CLOSE_LITEBOX_SEL).click()
    return wait_selector_to_disappear(driver, CLOSE_LITEBOX_SEL)

def save_change(driver):
    find_element_by_selector(driver, SAVE_BTN).click()
    return wait_selector_to_disappear(driver, WINBOX_SEL)

def get_type_discount(driver):
    discount = find_element_by_selector(driver, TYPE_DISCOUNT)
    return discount.text