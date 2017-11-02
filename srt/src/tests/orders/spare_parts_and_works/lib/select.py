# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector
from src.lib.wait import  wait_to_see_selector
from src.tests.orders.spare_parts_and_works.lib import TAB_SEL, CARET_SEL


BTN_1 = 0
BTN_2 = 1


def select_checkbox(driver, idx):
    WINBOX_CHBX_SEL = ".b-checkbox__label"
    return find_element_by_selector(driver, WINBOX_CHBX_SEL, idx).click()


def select_discount_btn(driver, idx):
    WINBOX_D_BUTTON_SEL = ".js-discount-btns .b-btn[data-value='{0}']".format(idx)
    return find_element_by_selector(driver, WINBOX_D_BUTTON_SEL).click()


def select_warranty_btn(driver, idx):
    WINBOX_W_BUTTON_SEL = ".js-warranty-buttons .b-btn[data-value='{0}']".format(idx)
    return find_element_by_selector(driver, WINBOX_W_BUTTON_SEL).click()


def select_caret(driver):
    wait_to_see_selector(driver, TAB_SEL)
    return find_element_by_selector(driver, CARET_SEL).click()


