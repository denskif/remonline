# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector, make_selector, set_value
from src.lib.errors import assert_xpath_is_visible
from src.lib.wait import wait_for_selector
from src.lib.formatting import make_text_xpath


GRID_DELETE_BTN = ".k-grid-delete"
ADD_WORK_BTN = ".js-work .b-btn"
ADD_PART_BTN = ".js-parts .b-btn"

#TODO: All tests are dipricated. They should be disconected. Module should be refactored or killed.


"""
    Operand "work" is a dictionary containing details of work:
    name, quantity, price.
"""

def add_work(driver, work):
    set_value(driver, ".js-work [name='title']", work['name'])
    set_value(driver, ".js-work [name='quantity']", work['quantity'])
    set_value(driver, ".js-work [name='price']", work['price'])

    find_element_by_selector(driver, ADD_WORK_BTN).click()

    return assert_xpath_is_visible(driver, make_text_xpath("td", work['name']))

def edit_work(driver, work_details):
    set_value(driver, ".js-work [name='quantity']", work_details['quantity'])
    set_value(driver, ".js-work [name='price']", work_details['price'])

    return  find_element_by_selector(driver, ADD_WORK_BTN).click()

"""
    Operand "spare" is a dictionary containing details of spare part:
    name, quantity, cost, price, etc.
"""

def add_spare_manually(driver, spare):
    set_value(driver, ".js-parts [name='title']", spare['name'])
    set_value(driver, ".js-parts [name='quantity']", spare['quantity'])
    set_value(driver, ".js-parts [name='cost']", spare['cost'])
    set_value(driver, ".js-parts [name='price']", spare['price'])

    find_element_by_selector(driver, ADD_PART_BTN).click()
    spare_added = make_text_xpath("td", spare['name'])
    return assert_xpath_is_visible(driver, spare_added)

def edit_manual_spare(driver, spare):
    set_value(driver, ".js-parts [name='quantity']", spare['quantity'])
    set_value(driver, ".js-parts [name='cost']", spare['cost'])
    set_value(driver, ".js-parts [name='price']", spare['price'])

    return find_element_by_selector(driver, ADD_PART_BTN).click()
