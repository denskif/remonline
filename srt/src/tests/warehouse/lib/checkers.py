# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector, make_selector
from src.lib.wait import wait_for_selector, wait_selector_to_disappear
from src.lib.formatting import make_text_xpath
from src.lib.errors import assert_xpath_is_visible

from src.scaffolds.grid import wait_grid_updated
from src.scaffolds.search import search_for, reset_search


TITLE_CELL = 2
TABLE_ERROR_MSG = "Item is not in the table!"


# Returns item name
def check_item_in_table(driver):
    find_element_by_selector(driver, ".k-plus").click()
    wait_for_selector(driver, ".k-detail-cell tbody td")

    return find_element_by_selector(
        driver, ".k-detail-cell tbody td", idx=TITLE_CELL
    ).text

def assert_items_in_table(driver, list_of_items):
    find_element_by_selector(driver, ".k-plus").click()
    wait_for_selector(driver, ".k-detail-cell tbody td")

    for item in list_of_items:
        assert_xpath_is_visible(driver, make_text_xpath("td", item))

    # Cleanup
    find_element_by_selector(driver, ".k-minus").click()
    wait_selector_to_disappear(driver, ".k-detail-cell")

    return True

'''
checks if chosen item was added to stack table
argument cell_idx - stands for number of "td" element in row
argument checks the proper cell containing item title
'''
def assert_added_to_table(driver, table_sel, cell_idx, data):

    table = find_element_by_selector(
        driver, make_selector(table_sel, "tbody td"), idx=cell_idx
    )
    table_text = table.text

    if table_text == data:
        return True
    else:
        return None

# Residue checkers
def assert_residue_not_in_table(driver, data):
    search_for(driver, data['title'])
    wait_selector_to_disappear(driver, ".js-grid tbody")
    return reset_search(driver)

