#~*~ coding: utf-8 ~*~
import unittest

from src.tests.invoices.lib import wait_invoice_grid
from src.lib.dom import find_element_by_selector
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_see_selector
)

def select_invoice_with_checkbox(driver, sel, idx=None):
    wait_to_see_selector(driver, sel)
    find_element_by_selector(driver, sel, idx).click()
    return driver.find_element_by_css_selector(sel).is_selected()


def click_to_button(driver, sel):
    wait_to_see_selector(driver, sel)
    return find_element_by_selector(driver, sel).click()


def select_menu_option(driver, idx):
    wait_to_see_selector(driver, ".b-mass .dropdown-menu")
    find_element_by_selector(driver, ".js-action", idx).click()
    wait_to_see_selector(driver, ".b-modal")


def dialog_action(driver, sel):
    find_element_by_selector(driver, sel).click()
    return wait_selector_to_disappear(driver, sel)

