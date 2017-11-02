# ~*~ coding: utf-8 ~*~

from src.lib.dom import make_selector

from src.scaffolds.dialog import open_dialog, close_dialog


ADD_CLEINT_SEL = ".js-add-button"
C_DIALOG_SEL = ".b-dialog"
SUBMIT_SEL = ".js-submit-dialog"
CLOSE_SEL = ".js-close-dialog"
JURIDICAL_SEL = ".js-client-juridical"
CLIENT_NAME_SEL = "#l-c-name"
CLIENT_ID_SEL = "[data-client-id]"
CLIENT_ID_SEL_N = "[data-client-id={0}]"
PHONE_SEL = ".js-phone"


def open_create_client_dialog(driver):
    return open_dialog(
        driver, ADD_CLEINT_SEL, make_selector(C_DIALOG_SEL, PHONE_SEL)
    )

def submit_client_dialog(driver):
    return close_dialog(driver, SUBMIT_SEL, C_DIALOG_SEL)

def close_client_dialog(driver):
    return close_dialog(driver, CLOSE_SEL, C_DIALOG_SEL)
