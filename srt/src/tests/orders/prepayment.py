# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.dom import find_element_by_selector, set_value
from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL
from src.lib.errors import assert_xpath_is_visible
from src.lib.randomizer import make_phone_number
from src.lib.formatting import format_phone, make_text_xpath

from src.scaffolds.dialog import open_dialog

from src.tests.orders.lib import wait_orders_grid_updated
from src.tests.orders.lib.open import TAB_INFO, open_tab, open_order
from src.tests.orders.lib.save_order import save_and_prepay
from src.tests.orders.lib.create_order import create_order


MAIN_CASHBOX_INDEX = 1


class PrepaymentTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_prepay_while_creating(self):
    # Create new order with prepayment
        open_dialog(self.driver, ".js-orders-add", ".js-change-order-type")

        # Fill in all required fields
        self.driver.find_element_by_id("js-o-name").send_keys("Michael Jackson")

        phone_number = make_phone_number()
        phone = self.driver.find_element_by_id("js-o-phone")
        phone.click()
        phone.send_keys(phone_number)

        self.driver.find_element_by_id("js-o-model").send_keys("super device")
        self.driver.find_element_by_id("js-o-malfunction").send_keys("not working")
        self.driver.find_element_by_id("l-o-prepayment").send_keys("450")

        save_and_prepay(self.driver, MAIN_CASHBOX_INDEX)

        # Format phone number so it can be found in the table
        new_phone = format_phone(phone_number)

        #Check by phone number if new order was added
        assert_xpath_is_visible(
            self.driver, make_text_xpath('span', new_phone)
        )
        return wait_orders_grid_updated(self.driver)