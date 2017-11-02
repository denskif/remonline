# ~*~ coding: utf-8 ~*~
import unittest
from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector, hover
from src.lib.wait import wait_to_see_selector

# TT for tooltip
COST_TT_SEL      = ".js-price"
DISCOUNT_TT_SEL  = ".js-discount"
WARRANTY_TT_SEL  = ".js-warranty"

FINAL_DISCONT_TT_SEL = ".js-discount-hint"
FINAL_PRICE_TT_SEL = ".js-sum-hint"



def _make_tooltip_sel(attr_val):
    return "{0}[aria-describedby]".format(attr_val)


#This method for get tooltip text from part and srvc grid
def get_tooltip_text(driver, selector):
    tooltip_sel = _make_tooltip_sel(selector)
    hover(driver, selector)
    wait_to_see_selector(driver, tooltip_sel)
    return find_element_by_selector(driver, tooltip_sel).get_attribute("data-original-title")
