# ~*~ coding: utf-8 ~*~

from src.lib.dom import make_selector, find_element_by_selector, find_element_by_xpath
from src.lib.wait import wait_selector_to_disappear, wait_for_selector
from src.lib.formatting import make_text_xpath

from src.scaffolds.dialog import open_dialog, close_dialog

""" -Helpers- """
DIALOG_SEL = ".b-dialog_type_warehouse"

# Contains of dialog sel and type dropdown sel
BARCODE_DIALOG_SEL = ".b-dialog .js-b-type"

CLOSE_BTN_SEL = ".js-close-dialog"

SUBMIT_BARCODE_DIALOG_SEL = ".js-submit-dialog"
SUBMIT_WRITEOFF_BTN_SEL = ".js-submit-dialog"
SUBMIT_MOVE_DIALOG_SEL = ".js-submit-dialog"

BARCODE_TYPE_SEL = ".js-b-type"
BARCODE_INPUT_SEL = "#l-b-code"
BARCODE_TAG_SEL = "div"
GENERATE_BC_SEL = ".js-generate"


def open_posting_dialog(driver):
    return open_dialog(
        driver, ".js-wh-posting", make_selector(DIALOG_SEL, ".js-warehouses [name=warehouse]"),
    )

def close_posting_dialog(driver):
    return close_dialog(driver, CLOSE_BTN_SEL, DIALOG_SEL)



def open_residue_dialog(driver):
    return open_dialog(driver, ".js-edit-button", DIALOG_SEL)

def close_residue_dialog(driver):
    return close_dialog(driver, CLOSE_BTN_SEL, DIALOG_SEL)



def open_write_off(driver):
    return open_dialog(driver, ".js-wh-outcome", DIALOG_SEL)

def close_write_off(driver):
    return close_dialog(driver, CLOSE_BTN_SEL, DIALOG_SEL)

def submit_write_off(driver):
    return close_dialog(driver, SUBMIT_WRITEOFF_BTN_SEL, DIALOG_SEL)


def submit_move_dialog(driver):
    return close_dialog(driver, SUBMIT_MOVE_DIALOG_SEL, SUBMIT_MOVE_DIALOG_SEL)



def open_barcode_dialog(driver):
    return open_dialog(driver, ".js-add-barcode", BARCODE_DIALOG_SEL)

"""
- Barcode's dialog openes over another dialog
- smtimes btn selectors can be the same for both dialogs
- use idx argument to find the exact sel you need to close or submint dialog
"""
def submit_barcode_dialog(driver, idx=None):
    idx = idx or 0

    find_element_by_selector(driver, SUBMIT_BARCODE_DIALOG_SEL, idx).click()
    return wait_selector_to_disappear(driver, BARCODE_DIALOG_SEL)

def close_barcode_dialog(driver, idx=None):
    idx = idx or 0

    find_element_by_selector(driver, CLOSE_BTN_SEL, idx).click()
    return wait_selector_to_disappear(driver, BARCODE_DIALOG_SEL)
"""========================================================================="""

def open_edit_barcode(driver, barcode):
    find_element_by_xpath(
            driver, make_text_xpath(BARCODE_TAG_SEL, barcode)
        ).click()
    return wait_for_selector(driver, BARCODE_TYPE_SEL)
