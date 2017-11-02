# ~*~ coding: utf-8 ~*~
import unittest
from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, set_value, hover_and_click, hover
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear, wait_for_selector



def click_create_srvc_dd(driver):
    CREATE_SRVC_SEL = ".b-in-holder .b-dropdown .js-create-srvc"
    wait_to_see_selector(driver, CREATE_SRVC_SEL)
    return find_element_by_selector(driver, CREATE_SRVC_SEL).click()



def create_part_dd(driver):
    CREATE_PART_SEL = ".b-in-holder .b-dropdown .js-create-part"
    wait_to_see_selector(driver, CREATE_PART_SEL)
    return find_element_by_selector(driver, CREATE_PART_SEL).click()


#delete part or srvc in parts and srvc grid
def delete_str(driver):
    hover(driver, ".b-table__tr_mode_selectable")
    wait_for_selector(driver, ".js-trasher")
    hover_and_click(driver, ".js-trasher")
    wait_to_see_selector(driver, ".b-litebox")
    find_element_by_selector(driver,".js-remove-confirm").click()
    return wait_selector_to_disappear(driver, ".b-litebox")


