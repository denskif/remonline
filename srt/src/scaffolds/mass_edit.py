# ~*~ coding: utf-8 ~*~

import time

from src.lib.dom import find_element_by_selector
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_see_selector
)


MAIN_CHECKBOX_SEL = ".k-grid-header .h-checkbox"
MAIN_SELECTED_SEL = ".js-selected-h"
ALL_CHECKBOXES_SEL = ".js-selected"
MASS_EDIT_MENU_SEL = ".b-mass .js-mass-text"
CLOSE_MASS_MENU_SEL = ".b-mass .b-mass__close"

def select_all_mass(driver):
    find_element_by_selector(driver, MAIN_CHECKBOX_SEL).click()
    return driver.find_element_by_css_selector(
        MAIN_SELECTED_SEL
    ).is_selected()

def check_all_mass_selected(driver):
    for check in driver.find_elements_by_css_selector(ALL_CHECKBOXES_SEL):
        if check.is_selected():
            return True
        else:
            return None

def check_all_mass_deselected(driver):
    for check in driver.find_elements_by_css_selector(ALL_CHECKBOXES_SEL):
        if check.is_selected() != True:
            return True
        else:
            return None

def test_mass_edit(driver):
    wait_for_selector(driver, MAIN_CHECKBOX_SEL)
    select_all_mass(driver)
    wait_for_selector(driver, MASS_EDIT_MENU_SEL)
    check_all_mass_selected(driver)

    # Avoiding the too slow rendering of the footer for selenium
    time.sleep(1)

    find_element_by_selector(driver, MAIN_CHECKBOX_SEL).click()
    wait_selector_to_disappear(driver, MASS_EDIT_MENU_SEL)
    check_all_mass_deselected(driver)

    select_all_mass(driver)
    wait_for_selector(driver, MASS_EDIT_MENU_SEL)
    check_all_mass_selected(driver)

    # Using sleep constrainedly (selenium being naughty)
    wait_to_see_selector(driver, MASS_EDIT_MENU_SEL)
    time.sleep(2)
    find_element_by_selector(driver, CLOSE_MASS_MENU_SEL).click()
    wait_selector_to_disappear(driver, MASS_EDIT_MENU_SEL)
    return check_all_mass_deselected(driver)

