# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector
from src.scaffolds.dialog import confirm_delete


def delete_order(driver):
    find_element_by_selector(
        driver, ".b-order__footer .js-additional"
    ).click()
    find_element_by_selector(driver, ".js-remove").click()
    return confirm_delete(driver)
