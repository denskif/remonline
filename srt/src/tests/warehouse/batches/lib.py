# ~*~ coding: utf-8 ~*~
import unittest

from src.lib.randomizer import random_z
from src.lib.dom import find_element_by_selector
from src.lib.url import navigate, INVENTORY_URL
from src.lib.wait import wait_to_see_selector, wait_to_click_selector

from src.scaffolds.dialog import close_dialog
from src.scaffolds.grid import add_to_stack
from src.scaffolds.dropdown import choose_select_by_text

from src.tests.warehouse.lib.select import search_and_open, search_and_select
from src.tests.warehouse.lib import submit_move_dialog


BATCHES_SEL = ".js-batches-grid [data-uid] td:nth-child(6)"
BASE_ON_SEL = ".js-batches-grid [data-uid] td:nth-child(3)"
ADD_MOVE_BTN_SEL = ".js-wh-move"

DATA_FOR_BASE_ON = {
        'refund' : u"Возврат",
        'move' : u"Перемещение",
    }

def create_data_with_quantity(quantity):
    if not isinstance(quantity, int):
        quantity = 2 # positive amount for quantity
    return {
        u'title' : "Part with zero residue {0}".format(random_z()),
        u'supplier' : {'name': u"Evan's Supplies"},
        u'quantity' : quantity,
        u'price' : u"100",
    }

def open_batches(driver, item_name):
    navigate(driver, INVENTORY_URL)
    wait_to_see_selector(driver, ".js-wh-residue-search")
    search_and_open(driver, item_name)
    return wait_to_see_selector(driver, BATCHES_SEL)


# Get refund value from batches grid
def get_text_from_grid(driver, str_idx):
    return find_element_by_selector(driver, BATCHES_SEL, str_idx).text

def close_part_dialog(driver):
    return close_dialog(driver, ".js-close-dialog", ".js-close-dialog")

def create_movement(driver, title, stock):
    wait_to_see_selector(driver, ADD_MOVE_BTN_SEL)
    find_element_by_selector(driver, ADD_MOVE_BTN_SEL).click()
    wait_to_see_selector(driver, ".b-dialog_type_warehouse")
    add_to_stack(driver, title)
    choose_select_by_text(driver,".js-target-warehouses .js-wh-id", stock)
    return submit_move_dialog(driver)

def get_base_on_text(driver, str_idx):
    return find_element_by_selector(driver, BASE_ON_SEL, str_idx).text

