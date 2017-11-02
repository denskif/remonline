# ~*~ coding: utf-8 ~*~

from src.lib.dom import (
    find_element_by_selector, find_elements_by_selector, hover_and_click, get_value
)
from src.lib.wait import (
    wait_selector_to_disappear, wait_for_selector, wait_to_click_selector,
    wait_condition, wait_to_see_selector
)
from src.lib.formatting import make_text_xpath

from src.scaffolds.dialog import confirm_delete
from src.scaffolds.grid import remove_item_from_grid
from src.scaffolds.search import reset_search
from src.scaffolds.dropdown import choose_select_by_text

from src.tests.warehouse.lib import BARCODE_DIALOG_SEL
from src.tests.warehouse.lib.create import DEFAULT_STOCK_NAME
from src.tests.warehouse.lib.select import search_and_select


TRASH_BTN_SEL = ".h-trash-button"


def delete_stock(driver):
    stock_to_delete = get_value(find_element_by_selector(
            driver, ".js-warehouses [name=warehouse]"
        ))

    find_element_by_selector(driver, ".js-wh-remove").click()
    confirm_delete(driver)

    def _delete_checker(driver):
        return stock_to_delete != get_value(find_element_by_selector(
            driver, ".js-warehouses [name=warehouse]"
        ))

    return wait_condition(driver, _delete_checker)


# Removes all the stocks made by tests (with default stock prefix)
def clean_up_stock(driver):
    wait_to_click_selector(driver, ".js-warehouses")

    clean_list = []

    for i in find_elements_by_selector(driver, ".js-warehouses option"):

        if DEFAULT_STOCK_NAME in i.text:
            clean_list.append(i.text)

    for i in clean_list:
        choose_select_by_text(driver, ".js-warehouses [name=warehouse]", i)

        delete_stock(driver)


# Stands for posting, write-off, movement transactions
def delete_trans(driver):
    num_cell = 1
    wait_for_selector(driver, ".js-grid")

    trans_num = find_element_by_selector(
        driver, ".js-grid tbody tr td", idx=num_cell
    ).text

    remove_item_from_grid(driver, ".js-grid tbody")
    confirm_delete(driver)
    first_row_num = find_element_by_selector(
        driver, ".js-grid tbody tr td", idx=num_cell
    ).text

    if trans_num == first_row_num:
        return None
    else:
        return True

def delete_residue(driver, data):
    search_and_select(driver, data['title'])
    hover_and_click(driver, ".js-remove-button")
    confirm_delete(driver)
    wait_selector_to_disappear(driver, ".js-grid tbody")

    return reset_search(driver)

def delete_barcode(driver, idx=None):
    idx = idx or 0

    wait_to_click_selector(driver, TRASH_BTN_SEL)
    find_element_by_selector(driver, TRASH_BTN_SEL, idx).click()
    return wait_selector_to_disappear(driver, BARCODE_DIALOG_SEL)


# Delete first string in grid
def delete_write_off(driver):
    wait_to_see_selector(driver, ".js-grid .k-grid-content .k-master-row")
    remove_item_from_grid(driver, ".js-grid tbody")
    wait_to_see_selector(driver, ".b-modal_type_confirm")
    return confirm_delete(driver)
