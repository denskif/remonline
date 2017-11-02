# ~*~ coding: utf-8 ~*~
from src.lib.dom import find_element_by_selector, find_element_by_xpath
from src.lib.wait import (
    wait_for_selector, wait_to_click_selector, wait_selector_to_disappear,
    wait_to_see_selector,
)
from selenium.webdriver.common.action_chains import ActionChains

SUBMIT_DELETE_SEL = ".b-modal_type_confirm .b-modal__content .js-submit"
SUBMIT_REMOVAL_SEL = ".b-litebox .js-remove-confirm"
SUBMIT_NEW_DELETE_DIALOG = ".b-litebox .js-submit"
LEFT_MENU = ".b-sidebar.pull-left"
ADDITIONAL_MENU_BTN = ".js-additional .b-btn"
ADDITIONAL_MENU_SEL = ".js-additional .dropdown-menu"


def open_dialog(driver, selector, check_selector, selector_idx=None):
    wait_to_click_selector(driver, selector)
    find_element_by_selector(driver, selector, selector_idx).click()
    return wait_for_selector(driver, check_selector)


def close_dialog(driver, selector, check_selector):
    wait_to_click_selector(driver, selector)
    find_element_by_selector(driver, selector).click()
    return wait_selector_to_disappear(driver, check_selector)

def close_dialog_via_mask(driver, check_selector, check_disappear_sel):
    wait_to_see_selector(driver, check_selector)
    bar = driver.find_element_by_css_selector(LEFT_MENU)
    ac = ActionChains(driver)
    ac.move_to_element(bar).move_by_offset(50, 50).click().perform()
    return wait_selector_to_disappear(driver, check_disappear_sel)

def confirm_delete(driver):
    wait_to_click_selector(driver, SUBMIT_DELETE_SEL)
    find_element_by_selector(driver, SUBMIT_DELETE_SEL,).click()
    return wait_selector_to_disappear(driver, SUBMIT_DELETE_SEL)

# New Method for UI-kit-like frontend. Service widget remove method.
def confirm_removal(driver):
    wait_to_click_selector(driver, SUBMIT_REMOVAL_SEL)
    find_element_by_selector(driver, SUBMIT_REMOVAL_SEL).click()
    return wait_selector_to_disappear(driver, SUBMIT_REMOVAL_SEL)

def confirm_new_delete_dialog(driver):
    wait_to_click_selector(driver, SUBMIT_NEW_DELETE_DIALOG)
    find_element_by_selector(driver, SUBMIT_NEW_DELETE_DIALOG).click()
    return wait_selector_to_disappear(driver, SUBMIT_NEW_DELETE_DIALOG)

# Options menu contains refund, delete and other check methods
def open_additional_menu(driver):
    wait_for_selector(driver, ADDITIONAL_MENU_BTN)
    find_element_by_selector(driver, ADDITIONAL_MENU_BTN).click()
    return wait_to_see_selector(driver, ADDITIONAL_MENU_SEL)
