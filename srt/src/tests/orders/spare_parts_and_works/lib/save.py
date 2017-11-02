# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector



# save with winbox
def save_srvc(driver):
    SAVE_SRVC_SEL = ".b-winbox__body .js-srvc-submit"
    return find_element_by_selector(driver, SAVE_SRVC_SEL).click()

def save_srvc_edit(driver):
    SAVE_SRVC_SEL = ".b-winbox__body .js-submit-good"
    return find_element_by_selector(driver, SAVE_SRVC_SEL).click()


def save_part(driver):
    SAVE_PART_SEL = ".b-winbox__body .js-part-submit"
    return find_element_by_selector(driver, SAVE_PART_SEL).click()


