# ~*~ coding: utf-8 ~*~

from src.lib.wait import wait_for_selector
from src.lib.dom import set_value, find_element_by_selector

from src.scaffolds.dialog import confirm_delete, open_additional_menu
from src.scaffolds.grid import add_to_stack
from src.scaffolds.dropdown import choose_cashbox
from src.scaffolds.dialog import close_dialog

from src.tests.shop.lib import (
    open_new_sale, submit_sale, submit_sale_payment, open_last_sale,
)

FIRST_CASHBOX = 1
CASHBOX_DROPDOWN_SEL = ".js-cbp-cbpicker [name=cashbox]"

def prepare_sale(driver, title):
    open_new_sale(driver)
    return add_to_stack(driver, title)

def pay_for_sale(driver):
    submit_sale(driver)
    choose_cashbox(driver, CASHBOX_DROPDOWN_SEL, FIRST_CASHBOX)
    return submit_sale_payment(driver)

# removes top sale in the shop table
def delete_sale(driver):
    open_last_sale(driver)
    open_additional_menu(driver)
    find_element_by_selector(driver, ".js-remove-sale").click()
    return confirm_delete(driver)

def make_sale(driver, item_title):
    prepare_sale(driver, item_title)
    return pay_for_sale(driver)

def set_sale_discount(driver, discount):
    find_element_by_selector(driver, ".js-start").click()
    wait_for_selector(driver, ".js-discount-holder")
    set_value(driver, "[name=discount_value]", discount)
    return close_dialog(driver, ".js-submit-good", ".b-winbox")