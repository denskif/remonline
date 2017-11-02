#~*~ coding: utf-8 ~*~
import unittest

from src.lib.dom import find_element_by_selector


def get_status_idx(driver, sel):
    return int(find_element_by_selector(driver, sel).get_attribute("data-status"))


def select_status(driver,sel):
    return find_element_by_selector(driver, sel).click()


def click_select_invoice(driver, sel):
    return find_element_by_selector(driver, sel).click()



