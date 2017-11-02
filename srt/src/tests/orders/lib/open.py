# ~*~ coding: utf-8 ~*~
import time

from src.lib.dom import find_element_by_selector, find_displayed, hover_and_click, hover
from src.lib.wait import (
    wait_for_selector, wait_to_click_selector, wait_to_see_selector
)

from src.tests.orders.lib import make_orders_grid_selector
from src.lib.dom import double_click
from src.scaffolds.dialog import close_dialog
from src.tests.orders.spare_parts_and_works.lib.winbox import WINBOX_SEL

TAB_INFO = ".i-info"
TAB_WORKS = ".i-wrench"
TAB_PAYMENTS = ".b-order__header .i-finance"
TAB_WORKS_IDX = 1
ORDER_CODE_SEL = "[data-order-id] a"
CLOSE_ORDER_SEL = ".b-order__footer .js-close-dialog"
POSITION_IN_ORDER = ".b-table__tr_mode_selectable"
WIDGET_SEL_BTN = ".js-total-discount-label"

def open_tab(driver, tab_selector):
    return find_element_by_selector(
        driver, tab_selector
    ).click()

def change_location(driver, location_selector):
    find_element_by_selector(driver, ".js-branch-picker").click()
    return find_element_by_selector(driver, location_selector).click()

def open_order(driver):
    wait_to_click_selector(driver, ORDER_CODE_SEL)
    find_element_by_selector(driver, ORDER_CODE_SEL).click()
    return wait_for_selector(driver, ".js-change-order-type")

def close_order(driver):
    CLOSE_ORDER_SEL = ".b-order__wrapper .b-order__footer .js-close-dialog"
    wait_to_see_selector(driver, CLOSE_ORDER_SEL)
    return close_dialog(driver, CLOSE_ORDER_SEL, CLOSE_ORDER_SEL)

def open_position_in_order(driver, idx=None):
    # Index of position begining to 2
    idx = idx or 2
    positions = find_displayed(
        driver.find_elements_by_css_selector(POSITION_IN_ORDER)
    )
    if not positions:
        return None

    element = ".b-table__tr_mode_selectable:nth-child({0})".format(idx)
    hover(driver, element)
    time.sleep(1)
    # Refact
    element1 = ".b-table__tr_mode_selectable:nth-child({0}) .i-edit ".format(idx)
    find_element_by_selector(driver, element1).click()
    #time.sleep(1)
    return wait_to_see_selector(driver, WINBOX_SEL)

def open_widget_discont(driver):
    find_element_by_selector(driver, WIDGET_SEL_BTN).click()
    return wait_to_see_selector(driver, WINBOX_SEL)
