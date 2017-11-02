# ~*~ coding: utf-8 ~*~

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import choose_cashbox


def save_posting(driver):
    return close_dialog(driver, ".js-save-btn", ".b-dialog_type_warehouse")


def save_pay_post(driver, cashbox_sel, cashbox_idx):
    open_dialog(driver, ".js-save-btn", ".b-dialog .js-cashboxes")
    choose_cashbox(driver, cashbox_sel, cashbox_idx)

    return close_dialog(
        driver, ".js-submit-dialog", ".b-dialog .js-cashboxes"
    )

