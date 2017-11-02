# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector
from src.lib.wait import (
    wait_to_see_selector, wait_selector_to_disappear, wait_to_click_selector
)

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.grid import add_to_stack

from src.tests.orders.spare_parts_and_works.lib import CARET_SEL
from src.tests.orders.spare_parts_and_works.lib.create import create_part_dd
from src.tests.orders.spare_parts_and_works.lib.winbox import (
    set_text, input_checkbox, WINBOX_D_INPUT_SEL, WINBOX_W_INPUT_SEL,
    WINBOX_SEL,
)
from src.tests.orders.spare_parts_and_works.lib.select import (
    select_checkbox, select_discount_btn, select_warranty_btn, BTN_1, BTN_2,
)
from src.tests.orders.spare_parts_and_works.lib.save import save_part
from src.tests.warehouse.lib.select import set_active_residue

NAME_SEL = "part_title"
QUANTITY_SEL = "part_qty"
PRICE_SEL = "part_price"
COST_PRICE_SEL = "part_cost"
COMMENT_SEL = "part_comment"

ADD_FROM_WH_SEL = ".b-order__content .js-add-from-wh"
WH_DIALOG_SEL = ".b-dialog_type_warehouse"
SUBMIT_WRITE_OFF_SEL = ".b-dialog__content .js-submit-dialog"


IDX_D_CHBX = 0
IDX_W_CHBX = 1


DATA = {
    'name' : u"It's manual add part",
    'quantity' : u"10",
    'price' : u"100",
    'cost' : u"50",
    'discount_currency' :  u"10",
    'discount_rate' : u"50",
    'warranty_day' : u"14",
    'warranty_month' : u"6",
}


def manual_add_new_part(driver, data = None):
    data = data or DATA.copy()
    find_element_by_selector(driver, CARET_SEL).click()
    create_part_dd(driver)
    wait_to_see_selector(driver, WINBOX_SEL)

    if data['name']:
        set_text(driver, NAME_SEL, data['name'])
    else:
        raise ValueError("Service input should contain name.")

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

    save_part(driver)
    return wait_selector_to_disappear(driver, ".b-winbox")


def add_part_from_warehouse(driver, idx=None):

    ADD_FROM_WH_SEL = ".b-order__content .js-add-from-wh"
    WH_DIALOG_SEL = ".b-dialog_type_warehouse"

    wait_to_click_selector(driver, ADD_FROM_WH_SEL)
    find_element_by_selector(driver, ADD_FROM_WH_SEL).click()
    wait_to_see_selector(driver, WH_DIALOG_SEL)
    set_active_residue(driver, idx)
    find_element_by_selector(driver, ".b-dialog__content .js-wh-add").click()
    wait_to_see_selector(driver, ".b-dialog_type_warehouse .js-good-row")
    find_element_by_selector(driver, SUBMIT_WRITE_OFF_SEL).click()
    return wait_selector_to_disappear(driver, WH_DIALOG_SEL)


def add_part_by_title(driver, part_title):
    open_dialog(driver, ADD_FROM_WH_SEL, WH_DIALOG_SEL)
    add_to_stack(driver, part_title)
    return close_dialog(driver, SUBMIT_WRITE_OFF_SEL, WH_DIALOG_SEL)
