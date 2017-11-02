# ~*~ coding: utf-8 ~*~

from src.lib.dom import set_value

from src.scaffolds.dropdown import choose_cashbox_by_id

from src.tests.cashflow.lib import (
    open_income_dialog, submit_cashbox_dialog, open_expense_dialog,
    open_transfer_dialog
)

from src.lib.dom import (
    find_element_by_selector, find_elements_by_selector, hover_and_click, hover,
    double_click,
    )
from src.lib.wait import wait_selector_to_disappear, wait_to_see_selector

SUM_SEL = "#l-cb-payment"
COMMENT_SEL = "#l-cb-description"
CASHBOX_SEL = ".js-cb-id"

DATA = {
    'amount' : "1000",
    'comment' : "This is a test comment",
}

# Takes in dictionary
def make_income(driver, data):
    data = data or DATA

    open_income_dialog(driver)

    set_value(driver, SUM_SEL, data['amount'])
    set_value(driver, COMMENT_SEL, data['comment'])

    return submit_cashbox_dialog(driver)

def make_expense(driver, data):
    data = data or DATA

    open_expense_dialog(driver)

    set_value(driver, SUM_SEL, data['amount'])
    set_value(driver, COMMENT_SEL, data['comment'])

    return submit_cashbox_dialog(driver)

def make_transfer(driver, box_idx, data=None):
    data = data or DATA

    open_transfer_dialog(driver)

    choose_cashbox_by_id(driver, CASHBOX_SEL, box_idx)

    set_value(driver, SUM_SEL, data['amount'])
    set_value(driver, COMMENT_SEL, data['comment'])

    return submit_cashbox_dialog(driver)



def find_transaction_in_cashbox_grid(driver, data):
    wait_to_see_selector(driver, ".h-cashbox-report .k-grid-content")
    list_outcome = find_elements_by_selector(driver, ".h-cashbox-report .k-grid-content tr[data-uid]")
    elem = find_element_by_selector(driver,".h-cashbox-report .k-grid-content tr[data-uid] .h-c-green")
# def delete_transaction(driver, data):



def delete_transaction_from_cashbox(driver, idx = None):
    # import ipdb; ipdb.set_trace()
    wait_to_see_selector(driver, ".h-cashbox-report .k-grid-content")
    hover(driver, ".h-cashbox-report .k-grid-content tr[data-uid] .h-remove-link").click()
    wait_to_see_selector(driver, ".b-modal_type_confirm")
    find_element_by_selector(driver, ".js-submit").click()
    return wait_selector_to_disappear(driver, ".js-submit")

