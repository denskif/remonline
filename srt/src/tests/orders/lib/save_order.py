# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector
from src.lib.wait import (
    wait_selector_to_disappear, wait_for_selector, wait_to_click_selector
)

from src.scaffolds.dropdown import choose_cashbox
from src.scaffolds.dialog import close_dialog


CASHBOX_SEL = ".js-cashboxes [name=cashbox]"


def save_order(driver, seconds=None):
    wait_to_click_selector(
        driver, ".b-order .b-order__footer .js-save"
    )
    find_element_by_selector(
        driver, ".b-order .b-order__footer .js-save"
    ).click()
    return wait_selector_to_disappear(driver, ".b-order", time=seconds)

def save_and_prepay(driver, cashbox_index):
    wait_to_click_selector(
        driver, ".b-order .b-order__footer .js-save"
    )

    find_element_by_selector(
        driver, ".b-order .b-order__footer .js-save"
    ).click()

    choose_cashbox(driver, CASHBOX_SEL, cashbox_index)
    close_dialog(driver, ".js-submit-dialog", ".b-dialog")

    return wait_selector_to_disappear(driver, ".b-order")
