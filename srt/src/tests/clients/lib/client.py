# ~*~ coding: utf-8 ~*~

from src.lib.randomizer import random_x
from src.lib.dom import set_value, make_selector, find_element_by_selector

from src.scaffolds.search import search_for
from src.scaffolds.dialog import open_dialog

from src.tests.clients.lib import (
    open_create_client_dialog, CLIENT_NAME_SEL, submit_client_dialog,
    CLIENT_ID_SEL, C_DIALOG_SEL, JURIDICAL_SEL
)


PHONE_SEL = ".js-phone"
EMAIL_SEL = "#l-c-email"
ADDRESS_SEL = "#l-c-address"
NOTE_SEL = "#l-c-notes"
SUPPLIER_CB_SEL = "[for=l-client-supplier] .h-checkbox"
CONFLICT_CB_SEL = "[for=l-client-conflicted] .h-checkbox"
NATURAL_E_SEL = ".js-client-juridical [data-value=false]"
LEGAL_E_SEL = ".js-client-juridical [data-value=true]"


DATA = {
    'name' : "Mr. {0}".format(random_x()),
}

"""
CLIENT TEMPLATE
{
    'name' : "some data",
    'legal' : True/False, -(False for natural entity, True for legal entity)
    'supplier' : True,
    'conflicted' True,
    'phone' : "some data",
    'email' : "some data",
    'address' : "some data",
    'note' : "some data",
}
"""


def create_client(driver, data=None):
    data = data or DATA

    open_create_client_dialog(driver)

    if not data['name']:
        raise ValueError("Client data should contain name.")
    else:
        set_value(driver, CLIENT_NAME_SEL, data['name'])

    if "legal" in data.keys() and data['legal'] == False:
        find_element_by_selector(driver, NATURAL_E_SEL).click()
    elif "legal" in data.keys() and data['legal'] == True:
        find_element_by_selector(driver, LEGAL_E_SEL).click()

    if 'supplier' in data.keys() and data['supplier'] == True:
        find_element_by_selector(driver, SUPPLIER_CB_SEL).click()

    if 'conflicted' in data.keys() and data['conflicted'] == True:
        find_element_by_selector(driver, CONFLICT_CB_SEL).click()

    if 'phone' in data.keys():
        set_value(driver, PHONE_SEL, data['phone'])

    if 'email' in data.keys():
        set_value(driver, EMAIL_SEL, data['email'])

    if 'address' in data.keys():
        set_value(driver, ADDRESS_SEL, data['address'])

    if 'note' in data.keys():
        set_value(driver, NOTE_SEL, data['note'])

    return submit_client_dialog(driver)

def open_client(driver):
    return open_dialog(
        driver, CLIENT_ID_SEL, make_selector(C_DIALOG_SEL, JURIDICAL_SEL)
    )

def find_open_client(driver, client_name):
    search_for(driver, client_name)
    return open_dialog(
        driver, CLIENT_ID_SEL, make_selector(C_DIALOG_SEL, JURIDICAL_SEL)
    )


