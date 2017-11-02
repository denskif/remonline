# ~*~ coding: utf-8 ~*~

from src.lib.dom import set_value, find_element_by_selector
from src.lib.wait import wait_for_selector
from src.lib.randomizer import random_z

from src.scaffolds.dialog import close_dialog


CREATE_CLIENT_BTN = ".js-create-client"
JURIDICAL_SEL = ".js-client-juridical"
CLIENT_NAME_SEL = "#l-c-name"
PHONE_SEL = "#l-c-phone"
EMAIL_SEL = "#l-c-email"
ADDRESS_SEL = "#l-c-address"
NOTE_SEL = "#l-c-notes"
SUPPLIER_CB_SEL = "[for=l-client-supplier] .h-checkbox"
CONFLICT_CB_SEL = "[for=l-client-conflicted] .h-checkbox"
NATURAL_E_SEL = ".js-client-juridical [data-value=false]"
LEGAL_E_SEL = ".js-client-juridical [data-value=true]"

DATA = {
    'name' : "Mr. {0}".format(random_z()),
}

def fast_add_new_client(driver, sel, client_data=None):
    data = client_data or DATA.copy()

    wait_for_selector(driver, sel)
    set_value(driver, sel, data['name'])
    wait_for_selector(driver, CREATE_CLIENT_BTN)
    find_element_by_selector(driver, CREATE_CLIENT_BTN).click()
    wait_for_selector(driver, JURIDICAL_SEL)

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

    return close_dialog(driver, ".js-submit-dialog", JURIDICAL_SEL)

