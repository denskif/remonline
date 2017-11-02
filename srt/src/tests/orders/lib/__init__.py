# ~*~ coding: utf-8 ~*~

from src.lib.dom import make_selector

from src.scaffolds.grid import wait_grid_updated


ORDERS_GRID_SEL = ".js-orders-grid"


def make_orders_grid_selector(selector):
    return make_selector(ORDERS_GRID_SEL, selector)

def wait_orders_grid_updated(driver):
    return wait_grid_updated(driver, ORDERS_GRID_SEL)
