# ~*~ coding: utf-8 ~*~

from src.lib.dom import set_value, make_selector, find_element_by_selector


CLIENT_F_SEL = ".js-supplier-filter"
LEGAL_F_SEL = ".js-juridical-filter"

SHOW_ALL_BTN = "[data-value=all]"
SHOW_CUSTOMERS_BTN = "[data-value=false]"
SHOW_SUPPLIERS_BTN = "[data-value=true]"
SHOW_NATURAL_BTN = "[data-value=false]"
SHOW_LEGAL_BTN = "[data-value=true]"


def wrap_client(btn_selector):
    return make_selector(CLIENT_F_SEL, btn_selector)

def wrap_legals(btn_selector):
    return make_selector(LEGAL_F_SEL, btn_selector)

def filter_all_clients(driver):
    return find_element_by_selector(driver, wrap_client(SHOW_ALL_BTN)).click()

def filter_all_legals(driver):
    return find_element_by_selector(driver, wrap_legals(SHOW_ALL_BTN)).click()

def filter_customers(driver):
    return find_element_by_selector(
        driver, wrap_client(SHOW_CUSTOMERS_BTN)
    ).click()

def filter_suppliers(driver):
    return find_element_by_selector(
        driver, wrap_client(SHOW_SUPPLIERS_BTN)
    ).click()

def filter_naturals(driver):
    return find_element_by_selector(
        driver, wrap_legals(SHOW_NATURAL_BTN)
    ).click()

def filter_legal_entities(driver):
    return find_element_by_selector(
        driver, wrap_legals(SHOW_LEGAL_BTN)
    ).click()
