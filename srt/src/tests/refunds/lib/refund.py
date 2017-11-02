# ~*~ coding: utf-8 ~*~

from src.scaffolds.dialog import open_dialog, close_dialog, open_additional_menu
from src.scaffolds.dropdown import choose_cashbox

from src.tests.refunds.lib import open_make_refund_dialog
from src.tests.shop.lib import open_last_sale, close_sale_dialog
from src.tests.orders.spare_parts_and_works.lib.edit import edit_with_double_click
from src.tests.orders.lib.open import open_order, close_order

from src.widget.client import fast_add_new_client


FISRT_CASHBOX_IDX = 1
REFUND_CLIENT_SEL = '[name=refund_client]'
REFUND_CASHBOX_DIALOG = ".b-dialog_type_cashbox"
ORDER_REFUND_DIALOG_SEL = ".js-create-refund-root"

QUANTITY =  {"quantity" : "1"} # By default refund quantity is 1

def pay_refund(driver):
    open_dialog(driver, ".js-submit", REFUND_CASHBOX_DIALOG)
    choose_cashbox(driver, '[name=cashbox]', FISRT_CASHBOX_IDX)
    close_dialog(driver, ".js-cbp-submit", REFUND_CASHBOX_DIALOG)

def make_sale_refund(driver, value=None):

    if value:
        quantity = {"quantity" : "{0}".format(value)}
    else:
        quantity = QUANTITY

    open_last_sale(driver)
    open_additional_menu(driver)
    open_make_refund_dialog(driver)
    fast_add_new_client(driver, REFUND_CLIENT_SEL)
    edit_with_double_click(driver, quantity)
    pay_refund(driver)
    return close_sale_dialog(driver)

def make_order_refund(driver, value=None):

    if value:
        quantity = {"quantity" : "{0}".format(value)}
    else:
        quantity = QUANTITY

    open_order(driver)
    open_additional_menu(driver)
    open_make_refund_dialog(driver)
    edit_with_double_click(driver, QUANTITY, wrapper=ORDER_REFUND_DIALOG_SEL)
    pay_refund(driver)
    return close_order(driver)
