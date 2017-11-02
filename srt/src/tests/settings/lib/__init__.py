# ~*~ coding: utf-8 ~*~

import unittest
from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear
from src.lib.url import navigate

PRICE_AND_DISCOUNT = {
    "SEL": 'a[href="#!/settings/prices"]',
    "SEL_CHECK": ".js-posting-prices-round"
}

# Navigate to sections of settings
def chose_section(driver, section):
    find_element_by_selector(driver, section["SEL"]).click()
    return wait_to_see_selector(driver, section["SEL_CHECK"])
