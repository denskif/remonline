# ~*~ coding: utf-8 ~*~

from src.lib.dom import click_nth_node

from src.tests.warehouse.lib import open_residue_dialog
from src.scaffolds.grid import wait_grid_updated, wait_grid_changed_rows_num
from src.scaffolds.search import search_for


FIRST_ROW_IDX = 0
GRID_SEL = ".js-grid"
TABLE_ROW_SEL = ".js-grid tbody tr"

def set_active_residue(driver, idx=None):
    wait_grid_updated(driver, GRID_SEL)
    idx = idx or FIRST_ROW_IDX
    return click_nth_node(driver, TABLE_ROW_SEL, idx)

# Use only with residue table
# Finds item via search and selects it - ready to open/delete
def search_and_select(driver, item_name):
    wait_grid_updated(driver, GRID_SEL)
    search_for(driver, item_name)
    return set_active_residue(driver)

def search_and_open(driver, item_name):
    search_and_select(driver, item_name)
    return open_residue_dialog(driver)


