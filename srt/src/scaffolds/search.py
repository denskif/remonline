# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector, set_value, make_selector
from src.lib.wait import (
    wait_to_click_selector, wait_selector_to_disappear, wait_to_see_selector
)


RESET_SEARCH_SEL = ".b-search__reset"
SEARCH_SEL = ".b-search__input"

def search_for(driver, data, wrapper=None):
    if wrapper is None:
        search_sel = SEARCH_SEL
        reset_sel = RESET_SEARCH_SEL
    else:
        search_sel = make_selector(wrapper, SEARCH_SEL)
        reset_sel = make_selector(wrapper, RESET_SEARCH_SEL)

    wait_to_see_selector(driver, search_sel)
    find_element_by_selector(driver, search_sel)
    set_value(driver, search_sel, data)

    return wait_to_click_selector(driver, reset_sel)

def reset_search(driver):
    find_element_by_selector(driver, RESET_SEARCH_SEL).click()
    return wait_selector_to_disappear(driver, RESET_SEARCH_SEL)
