# ~*~ coding: utf-8 ~*~

import unittest
import time

from src.lib.wait import wait_selector_to_disappear, wait_for_selector
from src.lib.errors import assert_selector_is_visible
from src.lib.dom import find_element_by_selector

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL, BRANCH_URL

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, change_location
from src.tests.orders.lib.move_order import transfer_order
from src.tests.orders.lib.delete import delete_order

from src.tests.settings.branch import create_branch
from src.scaffolds.dropdown import switch_location


BRANCH_DATA = {
    u'#l-b-name': u"Location Mars",
    u'#l-b-orders-prefix': u"C-I",
    u'#l-b-address': u"345 Bombay Bicycle Road, London",
}
LOCATION_IDX = 0


class TransferOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_0_precondition(self):
        navigate(self.driver, BRANCH_URL)
        create_branch(self.driver, BRANCH_DATA)
        navigate(self.driver, ORDERS_URL)

    def test_1_order_transfer(self):
        create_order(self.driver)
        open_order(self.driver)
        move_to_branch = ".b-order .b-order__sidebar .open ul li p"
        transfer_order(self.driver, move_to_branch)

        # Check that order is marked as transfered
        assert_selector_is_visible(self.driver, ".i-system")
        switch_location(self.driver, LOCATION_IDX)

        wait_selector_to_disappear(self.driver, ".k-loading-mask")
        wait_selector_to_disappear(self.driver, ".k-loading-color")
        wait_selector_to_disappear(self.driver, ".h-order-row_blink_yellow")
        return assert_selector_is_visible(self.driver, ".i-system")


    def test_2_delete_transfered(self):
        time.sleep(1)
        order_id = find_element_by_selector(
            self.driver, "tbody tr [data-order-id]"
        ).get_attribute("data-order-id")
        open_order(self.driver)
        delete_order(self.driver)

        def _make_sel(data):
            return "[data-order-id=%s]" % (data)

        return wait_selector_to_disappear(self.driver, _make_sel(order_id))
