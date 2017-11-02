# ~*~ coding: utf-8 ~*~
import unittest
from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear


'''
data_template = {
        u'name' : name,
        u'login' : login,
        u'pass' : pass,
        u'email' : mail,
    }
    or can use data_f_worker from src.tests.orders.spare_parts_and_works.lib.data
'''
def add_worker(driver, data):
    wait_to_see_selector(driver, ".js-employee-widget .js-add-button")
    find_element_by_selector(driver, ".js-employee-widget .js-add-button").click()
    wait_to_see_selector(driver, ".b-dialog")
    set_value(driver, ".form-control[id='l-e-name']", data['name'])
    set_value(driver, ".form-control[id='l-e-login']", data['login'])
    set_value(driver, ".form-control[id='l-e-password']", data['pass'])
    set_value(driver, ".form-control[id='l-e-email']", data['email'])
    find_element_by_selector(driver, ".b-dialog .js-submit-dialog").click()
    return wait_selector_to_disappear(driver, ".b-dialog", 10)
