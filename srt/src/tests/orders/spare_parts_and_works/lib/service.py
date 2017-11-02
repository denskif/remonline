# ~*~ coding: utf-8 ~*~
import unittest
from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value, double_click
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear
from src.lib.url import navigate, BOOK_URL
from src.tests.orders.spare_parts_and_works.lib import TAB_SEL, CARET_SEL
from src.tests.orders.spare_parts_and_works.lib.create import click_create_srvc_dd
from src.tests.orders.spare_parts_and_works.lib.winbox import (
    set_text, input_checkbox, WINBOX_D_INPUT_SEL, WINBOX_W_INPUT_SEL, WINBOX_SEL
)
from src.tests.orders.spare_parts_and_works.lib.select import (
    select_checkbox, select_discount_btn, select_warranty_btn, BTN_1, BTN_2,
)
from src.tests.orders.spare_parts_and_works.lib.save import save_srvc

NAME_SEL = "srvc_title"
QUANTITY_SEL = "srvc_qty"
PRICE_SEL = "srvc_price"
COST_PRICE_SEL = "srvc_cost"
COMMENT_SEL = "srvc_comment"

IDX_ADD_CHBX = 0
IDX_D_CHBX = 1
IDX_W_CHBX = 2

SAVE_SRVC_SEL = ""

DATA = {
    'name' : u"0It's manual add service",
    'add_to_book' : True,
    'quantity' : u"10",
    'price' : u"100",
    'cost' : u"50",
    'discount' : False,
    'discount_currency' : u'10',
    'warranty' : False,
    'warranty_month' : u"14",
    }


def manual_add_new_srvc(driver, data=None):
    data = data or DATA.copy()
    find_element_by_selector(driver, CARET_SEL).click()
    click_create_srvc_dd(driver)
    wait_to_see_selector(driver, WINBOX_SEL)

    if data['name']:
        set_text(driver, NAME_SEL, data['name'])
    else:
        raise ValueError("Service input should contain name.")

    if data.get('add_to_book'):
        select_checkbox(driver, IDX_ADD_CHBX)

    if data.get('quantity'):
        set_text(driver, QUANTITY_SEL, data['quantity'])

    if data.get('price'):
        set_text(driver, PRICE_SEL, data['price'])

    if data.get('cost'):
        set_text(driver, COST_PRICE_SEL, data['cost'])

    if data.get('discount'):
        if data.get('discount_type'):
            select_discount_btn(driver, BTN_1)

        input_checkbox(driver, WINBOX_D_INPUT_SEL, data['discount_value'])

    if data.get('warranty'):
        if not data.get('warranty_type'):
            select_warranty_btn(driver, BTN_2)

        input_checkbox(driver, WINBOX_W_INPUT_SEL, data['warranty_value'])

    save_srvc(driver)
    return wait_selector_to_disappear(driver, ".b-winbox")


# ---------
def new_autocomplete_add(driver, input, data):
    DROPDOWN_ACTIVE_ITEM_SEL = ".b-dropdown__item_state_active"
    INPUT_SEL = ".b-in-holder .js-srvc-input"

    set_value(driver, INPUT_SEL, data[0:3])
    wait_to_see_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL)
    find_element_by_selector(driver, DROPDOWN_ACTIVE_ITEM_SEL).click()
    return wait_selector_to_disappear(driver, DROPDOWN_ACTIVE_ITEM_SEL)


def go_to_book(driver):
    navigate(driver, BOOK_URL)
    return wait_to_see_selector(driver, ".b-page__content")


#data it's serveces name or price, idx_td its idx td name or price
def info_from_srvc_book(driver, idx_td):
    BOOK_SEL = ".js-operation-widget"
    BOOK_TABLE_SEL = ".js-operation-widget .js-grid .b-table__td"

    find_element_by_selector(driver, BOOK_SEL)
    wait_to_see_selector(driver, BOOK_TABLE_SEL, idx_td)
    srvc_data = find_element_by_selector(driver, BOOK_TABLE_SEL, idx_td).text
    return srvc_data

def add_new_srvc_to_book(driver, data):

    INPUT_NAME_SEL = ".form-control[id = 'l-operation-title']"
    INPUT_PRICE_SEL = ".form-control[id = 'l-operation-price']"
    ADD_SEL = ".js-operation-widget .js-add-button"
    wait_to_see_selector(driver, ADD_SEL)
    find_element_by_selector(driver, ADD_SEL).click()
    wait_to_see_selector(driver, ".b-dialog", 10)
    find_element_by_selector(driver, INPUT_NAME_SEL).click()
    set_value(driver, INPUT_NAME_SEL, data['name'])
    find_element_by_selector(driver, INPUT_PRICE_SEL).click()
    set_value(driver, INPUT_PRICE_SEL, data['price'])
    find_element_by_selector(driver, ".js-submit-dialog").click()
    return wait_selector_to_disappear(driver, ".b-dialog")







