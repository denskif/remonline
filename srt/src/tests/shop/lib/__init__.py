# ~*~ coding: utf-8 ~*~

from src.lib.dom import make_selector

from src.scaffolds.dialog import open_dialog, close_dialog, close_dialog_via_mask


SALE_DIALOG_SEL = ".b-sale"
CLOSE_SEL = ".js-close-dialog"
MAKE_SALE_SEL = make_selector(SALE_DIALOG_SEL, ".b-sale__footer .b-btn")
CASHBOX_DIALOG_SEL = ".b-dialog_type_cashbox"
SUBMIT_SALE_SEL = ".js-cbp-submit"
SALE_CODE_SEL = ".js-shop-grid tbody [href]"
SELL_BUTTON = ".js-submit-dialog"
CLOSE_PAYMENT_BUTTON = ".js-cbp-cancel"
NEW_SALE_BUTTON = ".js-shop-sell"


def open_new_sale(driver):
    return open_dialog(driver, NEW_SALE_BUTTON, SALE_DIALOG_SEL)

def close_sale_dialog(driver):
    return close_dialog(driver, CLOSE_SEL, SALE_DIALOG_SEL)

def close_sale_dialog_via_mask(driver):
    return close_dialog_via_mask(driver, SALE_DIALOG_SEL, SALE_DIALOG_SEL)

def submit_sale(driver):
    return open_dialog(driver, MAKE_SALE_SEL, CASHBOX_DIALOG_SEL)

def submit_sale_payment(driver):
    return close_dialog(driver, SUBMIT_SALE_SEL, CASHBOX_DIALOG_SEL)

# opens top sale in the shop table
def open_last_sale(driver):
    return open_dialog(driver, SALE_CODE_SEL, ".b-dialog")

def open_sale_payment_dialog(driver):
    return open_dialog(driver, SELL_BUTTON, CASHBOX_DIALOG_SEL)

def close_sale_payment_dialog(driver):
    return close_dialog(driver, CLOSE_PAYMENT_BUTTON, CASHBOX_DIALOG_SEL)

def close_sale_payment_dialog_via_mask(driver):
    return close_dialog_via_mask(driver, SALE_DIALOG_SEL, CASHBOX_DIALOG_SEL)

