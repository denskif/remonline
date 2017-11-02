# ~*~ coding: utf-8 ~*~

from src import settings
from src.lib.wait import wait_to_see_selector


ORDERS_URL = "/app#!/orders"
CASHBOX_URL = "/app#!/payments/cashbox"
SHOP_URL = "/app#!/shop"
INVOICES_URL = "/app#!/payments/invoices"
POSTING_URL = "/app#!/warehouse/posting"
INVENTORY_URL = "/app#!/warehouse/residue"
WRITE_OFF_URL = "/app#!/warehouse/outcome"
CATEGORIES_URL = "/app#!/warehouse/categories"
CLIENT_URL = "/app#!/clients"
BOOK_URL = "/app#!/settings/book"
WORKERS_URL = "/app#!/settings/employee"
BRANCH_URL = "/app#!/settings/branch"
REFUND_URL = "/app#!/payments/refunds"
MOVE_URL = "/app#!/warehouse/move"

PRICE_AND_DISCOUNT = "app#!/settings/prices"


def make_absolute_url(url):
    url = url if url.startswith("/") else "/" + url
    return settings.HOST + url

def navigate(driver, url):
    return driver.get(make_absolute_url(url))

def go_to_cashbox(driver):
    navigate(driver, CASHBOX_URL)
    return wait_to_see_selector(driver, ".h-cashbox-report")
