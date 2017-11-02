# ~*~ coding: utf-8 ~*~

from selenium.common.exceptions import NoSuchElementException


from src.lib.dom import (
    click_nth_node, double_click, make_selector, find_element_by_selector,
    find_displayed, hover_and_click
)
from src.lib.wait import (
    wait_for_selector, wait_to_click_selector, wait_selector_to_disappear,
    wait_condition, wait_to_see_selector
)

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.search import search_for


ADD_SEL = ".js-add-button"
EDIT_SEL = ".js-edit-button"

SUBMIT_SEL = ".js-submit-dialog"

GRID_DELETE_BTN = ".h-remove-link"

DIALOG_SEL = ".b-dialog"

TITLE_CELL = 3 # idx of title cell in standart dialog table of goods

# Deprecated: to remove
def wait_grid_updated(driver, wrapper):
    return wait_for_selector(
        driver, make_selector(wrapper, ".k-grid-content tr")
    )

def wait_grid_changed_rows_num(driver, row_sel):
    grid_and_row_sel = make_selector(".js-grid", row_sel)

    count_before = len(find_displayed(
        driver.find_elements_by_css_selector(grid_and_row_sel),
    ))

    def _is_changed_count(driver):
        return count_before != len(find_displayed(
            driver.find_elements_by_css_selector(grid_and_row_sel),
        ))

    return wait_condition(driver, _is_changed_count)

"""
    Test standard grid by the next functionality:

        1. Open dialog by dblclicking;
        2. Close dialog (mask way);
        3. Open create dialog;
        3. Close dialog (button way);
        4. Open edit dialog;
        5. Close dialog by clicking on the save button.
"""
def test_grid_behaviour(driver, wrapper):
    add_sel = make_selector(wrapper, ADD_SEL)
    edit_sel = make_selector(wrapper, EDIT_SEL)
    dialog_check_sel = ".b-dialog .js-close-dialog"

    wait_to_see_selector(driver, make_selector(wrapper, ".js-grid"))

    # check if it's kendo grid or custom grid
    kendo_grid = find_element_by_selector(
        driver, make_selector(wrapper, ".k-grid")
    )

    if kendo_grid is None:
        row_sel = make_selector(wrapper, ".b-table__tr")
        first_row_idx = 1
    else:
        row_sel = make_selector(wrapper, "tbody tr")
        first_row_idx = 0

    # Test: open dialog by double clicking on the table row.
    wait_for_selector(driver, row_sel)
    first_row = find_element_by_selector(driver, row_sel, first_row_idx)
    double_click(driver, first_row)
    wait_for_selector(driver, dialog_check_sel)

    # Test: close dialog by clicking on the `close` button.
    close_dialog(driver, ".js-close-dialog", dialog_check_sel)

    # Test: open create dialog.
    open_dialog(driver, add_sel, dialog_check_sel)

    # Test: close dialog by clicking on the dialog mask.
    close_dialog(driver, ".h-dialog-mask", dialog_check_sel)

    # Test: open edit dialog.
    click_nth_node(driver, row_sel, first_row_idx)
    find_element_by_selector(driver, edit_sel).click()
    wait_for_selector(driver, dialog_check_sel)

    # Test: close dialog by clicking on the save button.
    close_dialog(driver, SUBMIT_SEL, dialog_check_sel)

def make_remove_btn_selector(selector):
    return make_selector(selector, GRID_DELETE_BTN)

def remove_item_from_grid(driver, grid_sel):
    driver.find_element_by_css_selector(
        make_remove_btn_selector(grid_sel)
    ).click()
    return True

def remove_item_from_product_stack(driver):
    wait_for_selector(driver, ".js-fletcher")
    find_element_by_selector(driver, ".js-start", 1).click()
    return True

# use for movement dialog
def add_to_stack(driver, title):
    search_for(driver, title, DIALOG_SEL)
    find_element_by_selector(
        driver,  make_selector(DIALOG_SEL, ".js-grid tbody tr td"), TITLE_CELL
    ).click()

    find_element_by_selector(driver, ".js-wh-add").click()
    return


#use for table in widget spare_and_works
def wait_table_changed_rows_num(driver, row_sel):
    grid_and_row_sel = make_selector(".b-table", row_sel)

    count_before = len(find_displayed(
        driver.find_elements_by_css_selector(grid_and_row_sel),
    ))

    def _is_changed_count(driver):
        return count_before != len(find_displayed(
            driver.find_elements_by_css_selector(grid_and_row_sel),
        ))

    return wait_condition(driver, _is_changed_count)
