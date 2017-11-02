# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value, get_attribute, find_elements_by_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear
from src.lib.url import navigate

ACTIVE_BTN = ".b-btn_state_active"

def get_value_discount(driver):
    discount = find_element_by_selector(driver, ACTIVE_BTN)
    return discount.text

