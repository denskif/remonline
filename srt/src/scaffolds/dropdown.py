# ~*~ coding: utf-8 ~*~

from selenium.webdriver.support.select import Select

from src.lib.wait import (
    wait_to_click_selector, wait_for_selector, wait_selector_to_disappear,
    wait_to_see_selector
)
from src.lib.dom import (
    find_element_by_selector, get_value, set_value, hover_and_click,
    make_selector,
)

from src.scaffolds.grid import wait_grid_updated


DROPDOWN_ACTIVE_ITEM_SEL = ".b-dropdown__item_state_active"
CATEGORY_DROPDOWN_SEL = ".js-c-categories"
STOCK_DROPDOWN_SEL = ".js-warehouses [name=warehouse]"


def choose_from_select(driver, selector, idx=None):
    node = driver.find_element_by_css_selector(selector)
    select = Select(node)

    # In this case we should take first value but not current.
    if idx == None:
        values = map(get_value, select.options)
        # Get first non equal value from the dropdown.
        idx = 1 if values[0] == get_value(node) else 0

    return select.select_by_index(idx)

# Select from dropdown by text
def choose_select_by_text(driver, selector, text):
    node = driver.find_element_by_css_selector(selector)
    select = Select(node)

    return select.select_by_visible_text(text)

def switch_location(driver, branch_idx):
    find_element_by_selector(driver, ".js-branch-picker").click()
    return find_element_by_selector(
        driver, ".b-branch-picker__item", idx=branch_idx,
    ).click()

def select_checkboxes(driver, checkbox_sel, idx_list):
    for num in idx_list:
        find_element_by_selector(driver, checkbox_sel, idx=num).click()
    return True

# Each cashbox dropdown has its own selector
def choose_cashbox(driver, cashbox_sel, cashbox_num):
    wait_to_click_selector(driver, cashbox_sel)

    return choose_from_select(driver, cashbox_sel, cashbox_num)

# Each cashbox dropdown has its own selector
def choose_cashbox_by_id(driver, cashbox_sel, cashbox_id):
    wait_to_click_selector(driver, cashbox_sel)

    find_element_by_selector(driver, cashbox_sel).click()
    box_sel = ".js-cb-id [value='{0}']".format(cashbox_id)

    driver.find_element_by_css_selector(box_sel).click()
    return wait_selector_to_disappear(driver, ".js-cashboxes .is-visible")

def choose_category(driver, category_num):
    wait_to_click_selector(driver, CATEGORY_DROPDOWN_SEL)

    find_element_by_selector(driver, CATEGORY_DROPDOWN_SEL).click()

    find_element_by_selector(
        driver, ".b-tree__node", idx=category_num
    ).click()

    return wait_selector_to_disappear(driver, ".b-popup__body")

# Requires unique sel like "data-node-title" or "data-node-id"
def choose_category_by_name(driver, name_sel, wrapper=None):
    if wrapper == None:
        category_sel = CATEGORY_DROPDOWN_SEL
    else:
        category_sel = make_selector(wrapper, CATEGORY_DROPDOWN_SEL)

    wait_to_click_selector(driver, category_sel)

    find_element_by_selector(driver, category_sel).click()

    find_element_by_selector(
        driver, name_sel
    ).click()

    return wait_selector_to_disappear(driver, ".b-popup__body")

def choose_stock(driver, stock_idx):
    wait_to_click_selector(driver, STOCK_DROPDOWN_SEL)
    return choose_from_select(driver, STOCK_DROPDOWN_SEL, stock_idx)

# Requires unique sel like "data-wh-title" or "data-wh-id"
def choose_stock_by_name(driver, name_sel):
    return choose_select_by_text(driver, STOCK_DROPDOWN_SEL,name_sel)

def choose_doc_to_print(driver, doc_checkbox_sel, idx_list):
    btn =  find_element_by_selector(driver, ".js-mp .b-mp")
    btn.click()
    select_checkboxes(driver, doc_checkbox_sel, idx_list)
    btn.click()
    wait_selector_to_disappear(driver, ".js-mp .b-mp .b-mp__list")
    return True

# test dropdown caret - if it's present and active
def test_caret(driver, caret_sel):
    find_element_by_selector(driver, caret_sel).click()
    wait_to_see_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    find_element_by_selector(driver, caret_sel).click()
    return wait_selector_to_disappear(driver, DROPDOWN_ACTIVE_ITEM_SEL)

def autocomplete_add(driver, test_self, input_sel, data):
    set_value(driver, input_sel, data[0:3])
    wait_to_see_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    find_element_by_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL).click()
    wait_selector_to_disappear(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    auto_data = get_value(
        driver.find_element_by_css_selector(input_sel)
    )

    return test_self.assertEqual(auto_data, data)

def autocomplete_client_fast_widget(driver, test_self, input_sel, data):
    set_value(driver, input_sel, data[0:3])
    wait_to_see_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    find_element_by_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL).click()
    wait_selector_to_disappear(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    auto_data = driver.find_element_by_css_selector(".js-edit-client").text

    return test_self.assertEqual(auto_data, data)
