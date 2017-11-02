# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.wait import (
    wait_selector_to_disappear, wait_to_see_selector, wait_for_selector
)
from src.lib.dom import (
    find_element_by_selector, set_value, double_click, hover_and_click,
    make_selector,
)

from src.tests.orders.spare_parts_and_works.lib.save import save_srvc_edit
from src.tests.orders.spare_parts_and_works.lib.winbox import (
    set_text, input_checkbox, WINBOX_D_INPUT_SEL, WINBOX_W_INPUT_SEL,
)
from src.tests.orders.spare_parts_and_works.lib.select import (
    select_checkbox, select_discount_btn, select_warranty_btn, BTN_1, BTN_2,
)
from src.tests.orders.spare_parts_and_works.lib import YELLOW_SEL

IDX_D_CHBX = 0
IDX_W_CHBX = 1

NAME_SEL = "good_title"
QUANTITY_SEL = "good_qty"
PRICE_SEL = "good_price"
COST_PRICE_SEL = "good_cost"
COMMENT_SEL = "good_comment"

FIRST_ROW_SEL = ".b-table__tr_mode_selectable .b-table__td"

FIN_DICSOUNT_INPUT_SEL = ".b-in_type_money"


def edit_with_double_click(driver, data, idx = None, wrapper=None):
    """ data templete = {
        'quantity' : "2",
        'price' : "234",
        'cost' : "126",
        'discount' : "3",
        'discount_type' : True, -- rate=True, currency=False
        'quantity' : True,      -- day=True, month=False
    }
    """

    idx = idx or 0

    if wrapper:
        first_row_sel = make_selector(wrapper, FIRST_ROW_SEL)
    else:
        first_row_sel = FIRST_ROW_SEL

    double_click(driver, find_element_by_selector(driver, first_row_sel, idx))
    wait_to_see_selector(driver, ".b-winbox")

    if data.get('quantity'):
        set_text(driver, QUANTITY_SEL, data['quantity'])

    if data.get('price'):
        set_text(driver, PRICE_SEL, data['price'])

    if data.get('cost'):
        set_text(driver, COST_PRICE_SEL, data['cost'])

    if data.get('discount'):
        wait_to_see_selector(driver, ".b-in_type_money")

        if not data.get('discount_type'):
            select_discount_btn(driver, BTN_2)
        if data.get('discount_type'):
            select_discount_btn(driver,BTN_1)

        input_checkbox(driver, WINBOX_D_INPUT_SEL, data['discount_value'])

    if data.get('warranty'):
        wait_to_see_selector(driver, ".b-in_type_num-sm")

        if not data.get('warranty_type'):
            select_warranty_btn(driver, BTN_2)
        if data.get('warranty_type'):
            select_warranty_btn(driver, BTN_1)

        input_checkbox(driver, WINBOX_W_INPUT_SEL, data['warranty_value'])

    save_srvc_edit(driver)
    wait_selector_to_disappear(driver, ".b-winbox")
    wait_to_see_selector(driver, ".js-good-row")
	# TODO: check tests using this method and remove it from here
    return True #wait_selector_to_disappear(driver, YELLOW_SEL, 10)


def add_comment_for_first_in_grid(driver, data_f_comment):
    wait_to_see_selector(driver, ".b-table__tr_mode_selectable")
    hover_and_click(driver, ".js-comment")
    set_text(driver, COMMENT_SEL, data_f_comment)
    find_element_by_selector(driver, ".js-submit-text").click()
    return wait_selector_to_disappear(driver, ".b-winbox")


'''
    Data for edit_final_discount:

    rate = True or
    currency = False

    data = {
        'discount_type' : rate or currency,
        'discount_value' : value,
    }
'''
def edit_final_discount(driver, data):
    find_element_by_selector(driver, ".js-total-discount-label").click()
    wait_to_see_selector(driver, ".b-winbox")
    if data.get('discount_type'):
        select_discount_btn(driver, BTN_1)

    set_value(driver, ".b-in_type_money", data['discount_value'])
    find_element_by_selector(driver, ".js-apply-changes").click()
    return wait_selector_to_disappear(driver, ".b-winbox")
