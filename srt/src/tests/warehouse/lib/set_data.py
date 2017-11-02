# ~*~ coding: utf-8 ~*~

from src.lib.dom import set_value, find_element_by_selector, make_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear, wait_to_click_selector

from src.scaffolds.dropdown import choose_category
from src.scaffolds.search import search_for
from src.scaffolds.grid import add_to_stack

from src.tests.warehouse.lib.checkers import assert_added_to_table
from src.tests.warehouse.lib import DIALOG_SEL


WO_TITLE_CELL = 2  # write-off title cell selector

ADD_ITEM_BTN = ".b-dialog__content .b-btn"
STACK_SEL = ".js-fletcher"

MIN_INPUT_SEL = ".input-small[name='min_residue']"
MAX_INPUT_SEL = ".input-small[name='max_residue']"
ADD_RESIDUE_BUTTON_SEL = ".js-min-residue-widget .js-add-button"

# wraps with dialog selector
def wrap_sel(sel):
    return make_selector(DIALOG_SEL, sel)

# Clicks "Add" button - adds goods to posting table in the form
def add_to_posting(driver):
    return find_element_by_selector(driver, ADD_ITEM_BTN).click()

def set_new_good(driver, item_data, category_num):
    set_value(driver, "#js-wh-title", item_data['title'])
    # Move focus for category block to open
    find_element_by_selector(driver, "#l-wh-quantity").click()

    choose_category(driver, category_num)

    set_value(driver, "#l-wh-quantity", item_data['quantity'])
    set_value(driver, "#js-wh-price", item_data['price'])

    add_to_posting(driver)
    wait_selector_to_disappear(driver, ".js-c-categories")
    return wait_to_see_selector(driver, wrap_sel(".js-grid tbody"))

def set_instock_good(driver, item_data):
    set_value(driver, "#js-wh-title", item_data['title'])
    set_value(driver, "#l-wh-quantity", item_data['quantity'])
    set_value(driver, "#js-wh-price", item_data['price'])

    add_to_posting(driver)
    return wait_to_see_selector(driver, wrap_sel(".js-grid tbody"))

# Use raise_error with this func in case assertion returns None
def add_to_outcome(driver, data):
    add_to_stack(driver, data)

    return assert_added_to_table(
        driver, STACK_SEL, WO_TITLE_CELL, data
    )

def add_min_residue(driver, data):
    '''
    Add rule for min refund
    data = {
        'min' : number,
        'max' : number,
    }
    '''
    wait_to_click_selector(driver, ADD_RESIDUE_BUTTON_SEL)
    find_element_by_selector(driver, ADD_RESIDUE_BUTTON_SEL).click()
    wait_to_see_selector(driver, ".b-winbox")
    set_value(driver, MIN_INPUT_SEL, data['min'])
    set_value(driver, MAX_INPUT_SEL, data['max'])
    find_element_by_selector(driver, ".b-winbox .js-submit").click()
    wait_selector_to_disappear(driver, ".b-winbox")
    find_element_by_selector(driver, ".js-submit-dialog").click()
    return wait_selector_to_disappear(driver, ".js-submit-dialog")
