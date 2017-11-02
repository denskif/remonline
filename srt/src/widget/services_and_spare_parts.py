import unittest
from src.lib.driver import get_driver

from src.lib.wait import wait_for_selector, wait_to_click_selector
from src.lib.randomizer import random_x
from src.lib.dom import find_element_by_selector, set_value
from src.scaffolds.dialog import close_dialog


INPUT_WINBOX_SEL = ".b-winbox__body .b-in_type_char"
ADD_SERVICE_SEL = ".b-dropdown .js-create-srvc"
MODAL_WINBOX_SEL = ".b-winbox"
PRICE_SEL = ".b-winbox .js-prod-price"
QUANTITY_SEL = ".b-winbox .js-prod-quantity"
PROD_COST_SEL = ".b-winbox .js-prod-cost"
WARRANTY_SEL = ".js-warranty-yn .b-checkbox__box"
#DISCOUNT_SEL = ".js-discount-yn .b-checkbox__box"
SAVE_SERVICE_BUTTON_SEL = ".b-winbox .js-srvc-submit"
GRID_ELEMENTS_SEL = ".js-goods-group tr"
GRID_SEL = ".b-table .js-goods-group"

DATA = {
    'name' : "Service #. {0}".format(random_x()),
}


def fast_add_new_service(driver, sel, service_data=None):
    data = service_data or DATA.copy()
    wait_for_selector(driver, sel)
    set_value(driver, sel, data['name'])
    wait_to_click_selector(driver, ADD_SERVICE_SEL)
    find_element_by_selector(driver, ADD_SERVICE_SEL).click()
    wait_for_selector(driver, MODAL_WINBOX_SEL)

    if not data['name']:
        raise ValueError("Input field should contain name.")
    else:
        set_value(driver, INPUT_WINBOX_SEL, data['name'])

    if 'price' in data.keys():
        set_value(driver, PRICE_SEL, data['price'])

    if 'quantity' in data.keys():
        set_value(driver, QUANTITY_SEL, data['quantity'])

    if 'price_cost' in data.keys():
        set_value(driver, PROD_COST_SEL, data['price_cost'])

    close_dialog(driver, SAVE_SERVICE_BUTTON_SEL, ".b-dialog .js-srvc-submit")

