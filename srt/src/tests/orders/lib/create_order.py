# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import wait_for_selector, wait_selector_to_disappear
from src.lib.errors import assert_xpath_is_visible
from src.lib.randomizer import (
    make_phone_number, make_email, make_address, make_client_name
)

from src.tests.orders.lib import wait_orders_grid_updated
from src.tests.orders.lib.save_order import save_order

from src.scaffolds.dialog import open_dialog, confirm_delete


CUSTOMER_DATA = {
    'name': u"Roger Daltrey",
    'email': u"harry@who.com",
    'address': u"174 Motown Drive",
}


NAME_SEL = "#js-o-name"
PHONE_SEL = "#js-o-phone"
EMAIL_SEL = "#js-o-email"
ADDRESS_SEL = "#js-o-address"
MODEL_SEL = "#js-o-model"
MALFUNCTION_SEL = "#js-o-malfunction"
DEVICE_TYPE_SEL = "#js-o-kindof_good"
BRAND_SEL = "#js-o-brand"


"""
CLIENT WITH DEVICE TEMPLATE
{
    'name' : "some data",
    'phone' : "some data",
    'email' : "some data",
    'address' : "some data",
    'device_type' : "some data",
    'brand' : "some data",
    'model' : "some data",
    'malfunction' : "some data",
}
"""

def create_dummy_client():
    client_data = make_client_name()
    phone_data = make_phone_number()
    email_data = make_email()
    address_data = make_address()

    return {
        'name': client_data,
        'phone': phone_data,
        'email': email_data,
        'address': address_data,
    }


def create_order(driver, client_data=None):
    client_data = client_data or create_dummy_client()
    open_dialog(driver, ".js-orders-add", ".js-change-order-type")

    # Fill in all required fields

    if 'phone' in client_data.keys():
        phone_number = client_data['phone']
    else:
        phone_number = make_phone_number()

    set_value(driver, NAME_SEL, client_data['name'])
    set_value(driver, PHONE_SEL, phone_number)
    set_value(driver, EMAIL_SEL, client_data['email'])
    set_value(driver, ADDRESS_SEL, client_data['address'])

    if 'device_type' in client_data.keys():
        set_value(driver, DEVICE_TYPE_SEL, client_data['device_type'])

    if 'brand' in client_data.keys():
        set_value(driver, BRAND_SEL, client_data['brand'])

    if 'model' in client_data.keys():
        set_value(driver, MODEL_SEL, client_data['model'])

    if 'malfunction' in client_data.keys():
        set_value(driver, MALFUNCTION_SEL, client_data['malfunction'])

    save_order(driver, seconds=20)
    wait_orders_grid_updated(driver)

    return phone_number





