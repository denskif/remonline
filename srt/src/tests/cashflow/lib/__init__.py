# ~*~ coding: utf-8 ~*~


from src.lib.dom import make_selector

from src.scaffolds.dialog import open_dialog, close_dialog



""" Helpers """

DIALOG_SEL = ".b-dialog"
CREATE_CASHBOX_SEL = ".js-create"
SUBMIT_SEL = ".js-submit-dialog"
CLOSE_SEL = ".js-close-dialog"
SETTING_SEL = ".b-cashbox__settings"
ACTIVE_BOX_SEL = ".b-cashbox_state_active"
NAME_INPUT_SEL = "#l-cb-name"
INCOME_DIALOG_SEL = ".js-income"
OUTCOME_DIALOG_SEL = ".js-outcome"
MOVE_DIALOG_SEL = ".js-move"
CASHBOX_FIRST_ROW_SEL = ".js-report-grid tbody tr"
TRASH_BTN_SEL = ".i-trash"

OUTCOME_TRANSACTION_SEL = ".h-cashbox-report .k-grid-content tr[data-uid] .h-c-red"
INCOME_TRANSACTION_SEL = ".h-cashbox-report .k-grid-content tr[data-uid] .h-c-green"

# Cells in cashflow grid
COMMENT_CELL = 1
INCOME_CELL = 2
EXPENSE_CELL = 3
TOTAL_CELL = 4

def make_box_sel(selector):
    return make_selector(ACTIVE_BOX_SEL, selector)


# Open dialogs
def open_create_cashbox_dialog(driver):
    return open_dialog(driver, CREATE_CASHBOX_SEL, DIALOG_SEL)


def open_cashbox_settings(driver):
    return open_dialog(
        driver, make_box_sel(SETTING_SEL), NAME_INPUT_SEL
    )


def open_income_dialog(driver):
    return open_dialog(
        driver, make_box_sel(INCOME_DIALOG_SEL), SUBMIT_SEL
    )


def open_expense_dialog(driver):
    return open_dialog(
        driver, make_box_sel(OUTCOME_DIALOG_SEL), SUBMIT_SEL
    )


def open_transfer_dialog(driver):
    return open_dialog(
        driver, make_box_sel(MOVE_DIALOG_SEL), SUBMIT_SEL
    )


# submit dilaog
def submit_cashbox_dialog(driver):
    return close_dialog(driver, SUBMIT_SEL, DIALOG_SEL)


# close dialogs
def close_cashbox_dialog(driver):
    return close_dialog(driver, CLOSE_SEL, DIALOG_SEL)
