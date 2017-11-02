# ~*~ coding: utf-8 ~*~

from src.lib.dom import make_selector, find_element_by_selector
from src.lib.wait import wait_for_selector


"""
    Change color in the color picker widget.

    `wrapper` - within this DOM node the widget should be placed.
    `idx` - the color with this index will be chosen.
"""
def change_color(driver, wrapper, idx=None):
    idx = idx or 0
    widget_sel = make_selector(wrapper, ".b-colorpicker")
    trigger_sel = make_selector(wrapper, ".js-colorpicker")
    widget_item_sel = make_selector(widget_sel, ".b-colorpicker__item")

    find_element_by_selector(driver, trigger_sel).click()

    wait_for_selector(driver, widget_sel)
    find_element_by_selector(driver, widget_item_sel, idx=idx).click()

    return idx
