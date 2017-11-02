# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_to_click_selector
from src.scaffolds.dialog import close_dialog


def transfer_order(driver, branch_selector):
    wait_to_click_selector(driver, ".i-tab")
    find_element_by_selector(driver, ".i-tab").click()
    return close_dialog(driver, branch_selector, ".b-order")
