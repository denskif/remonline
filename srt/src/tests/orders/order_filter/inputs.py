# ~*~ coding: utf-8 ~*~

import unittest

from selenium.webdriver.common.action_chains import ActionChains

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.dom import set_value, find_element_by_selector, make_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.filter import (
    open_filter, close_filter, submit_filter, reset_filter
)


CUSTOMER = {
    'name' : "MR Tucklberry",
    'phone' : "some data",
    'email' : "tuck@berry.us",
    'address' : "Whale driver 56",
    'device_type' : "Groove box",
    'brand' : "CY Borg",
    'model' : "T-1000",
    'malfunction' : "sho-to ne rode",
}

DEVICE_TYPE_SEL = "#js-f-kindof_good"
BRAND_SEL = "#js-f-brand"
MODEL_SEL = "#js-f-model"
CUSTOMER_SEL  = "#js-f-client__name"

FIRST_ROW_CELL_SEL = "tbody td"

D_TYPE_CELL_IDX = 5
BRAND_CELL_IDX = 6
MODEL_CELL_IDX = 7
CUSTOMER_CELL_IDX = 9

ORDER_TYPE_F_SEL = 1
ORDER_TYPE_CLN_SEL = "[data-field=order_type]"

C_HEAD_SEL = "thead"


def click_filter_btn(driver, f_btn_idx):
    return find_element_by_selector(
        driver, ".b-popup__button", f_btn_idx
    ).click()

def enable_all_checkboxes(driver):
    return find_element_by_selector(driver, ".js-on").click()

def disable_all_checkboxes(driver):
    return find_element_by_selector(driver, ".js-off").click()

def add_column(driver, column_name):
    find_element_by_selector(driver, ".k-header-column-menu").click()
    menu = find_element_by_selector(driver, ".k-menu-vertical")
    ch_box = find_element_by_selector(driver, column_name)
    ActionChains(
        driver,
    ).move_to_element(
        menu,
    ).move_to_element(
        ch_box,
    ).click(
        ch_box,
    ).perform()
    return wait_to_see_selector(driver, make_selector(C_HEAD_SEL, column_name))


class OpenCloseFilterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_open_close_filter(self):
        open_filter(self.driver)
        return close_filter(self.driver)


# Filter's tests for simple inputs with autocomplete
class FilterSimpleInputsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver, CUSTOMER)
        open_filter(cls.driver)

    def test_1_device_type(self):
        set_value(self.driver, DEVICE_TYPE_SEL, CUSTOMER['device_type'])
        submit_filter(self.driver)

        wait_to_see_selector(self.driver, FIRST_ROW_CELL_SEL)
        device_type = find_element_by_selector(
            self.driver, FIRST_ROW_CELL_SEL, D_TYPE_CELL_IDX
        ).text

        return self.assertEqual(device_type, CUSTOMER['device_type'])

    def test_2_brand(self):
        set_value(self.driver, BRAND_SEL, CUSTOMER['brand'])
        submit_filter(self.driver)

        brand = find_element_by_selector(
            self.driver, FIRST_ROW_CELL_SEL, BRAND_CELL_IDX
        ).text

        return self.assertEqual(brand, CUSTOMER['brand'])

    def test_3_model(self):
        set_value(self.driver, MODEL_SEL, CUSTOMER['model'])
        submit_filter(self.driver)

        model = find_element_by_selector(
            self.driver, FIRST_ROW_CELL_SEL, MODEL_CELL_IDX
        ).text

        return self.assertTrue(CUSTOMER['model'] in model)

    def test_4_customer(self):
        set_value(self.driver, CUSTOMER_SEL, CUSTOMER['name'])
        submit_filter(self.driver)

        customer = find_element_by_selector(
            self.driver, FIRST_ROW_CELL_SEL, CUSTOMER_CELL_IDX
        ).text

        return self.assertTrue(CUSTOMER['name'] in customer)

    def tearDown(self):
        reset_filter(self.driver)

    @classmethod
    def tearDownClass(cls):
        close_filter(cls.driver)
