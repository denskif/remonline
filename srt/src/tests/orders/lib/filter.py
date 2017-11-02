# ~*~ coding: utf-8 ~*~

import time

from selenium.webdriver.common.action_chains import ActionChains

from src.lib.dom import find_element_by_selector, make_selector
from src.lib.wait import (
    wait_for_selector, wait_to_see_selector, wait_selector_to_disappear
)


FILTER_BTN = "#ls-f-caller"
FILTERS_W_SEL = ".js-filters"
F_CHECK_BOX_SEL = ".b-popup__body .h-checkbox"

C_HEAD_SEL = "thead"


def open_filter(driver):
    wait_for_selector(driver, FILTER_BTN)
    find_element_by_selector(driver, FILTER_BTN).click()
    return wait_to_see_selector(driver, FILTERS_W_SEL)

def close_filter(driver):
    find_element_by_selector(driver, FILTER_BTN).click()
    return wait_selector_to_disappear(driver, FILTERS_W_SEL)

def submit_filter(driver):
    find_element_by_selector(driver, ".js-apply").click()
    time.sleep(1)
    return wait_to_see_selector(driver, "[data-order-id]")

def reset_filter(driver):
    find_element_by_selector(driver, ".js-reset").click()
    time.sleep(1)
    return wait_to_see_selector(driver, "tbody tr td")

def click_filter_btn(driver, f_btn_idx):
    return find_element_by_selector(
        driver, ".b-popup__button", f_btn_idx
    ).click()

def enable_all_checkboxes(driver):
    return find_element_by_selector(driver, ".js-on").click()

def disable_all_checkboxes(driver):
    return find_element_by_selector(driver, ".js-off").click()

def add_column(driver, column_name_sel):
    wait_to_see_selector(driver, C_HEAD_SEL)
    find_element_by_selector(driver, ".k-header-column-menu").click()
    menu = find_element_by_selector(driver, ".k-menu-vertical")

    actions = ActionChains(driver)
    actions.move_to_element(menu)
    actions.click()
    actions.perform()

    time.sleep(0.5)
    wait_to_see_selector(driver, ".k-animation-container")
    find_element_by_selector(
        driver, make_selector(".k-link", column_name_sel)
    ).click()

    return wait_to_see_selector(
        driver, make_selector(C_HEAD_SEL, column_name_sel)
    )
