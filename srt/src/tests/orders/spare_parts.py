# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.randomizer import make_spare_part
from src.lib.dom import (
    find_element_by_selector, find_element_by_class_name, set_value
)
from src.lib.wait import (
    wait_for_xpath, wait_for_selector, wait_to_click_selector
)
from src.lib.formatting import (
    format_price, make_double_text_xpath, make_text_xpath
)
from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, ORDERS_URL
from src.lib.errors import assert_xpath_is_visible, assert_has_error_tooltip

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.open import open_tab, TAB_WORKS, open_order
from src.tests.orders.lib.work_and_parts import (
    add_spare_manually, edit_manual_spare, ADD_PART_BTN
)

from src.scaffolds.dropdown import choose_from_select
from src.scaffolds.dialog import close_dialog, open_dialog
from src.scaffolds.grid import remove_item_from_grid

from src.tests.warehouse.lib.create import create_posting



SPARE_PART1 = {
    'name': u'Super shield',
    'quantity': u'3',
    'cost': u'230.33',
    'price': u'340.50',
}
SPARE_PART2 = {
    'name': u'Mega antena',
    'quantity': u'2',
    'cost': u'250',
    'price': u'333.99',
    'sum': u'667.98'
}
SPARE_PART3 = {
    'title': u'Black Hawk',
    'quantity': u'100',
    'price': u'700',
    'supplier':{'name':"Mr. Smith's Shop"},
}
EDIT_SPARE_PART1 = {
    'name': u'Super shield',
    'quantity': u'1',
    'cost': u'333',
    'price': u'666',
}

TECHNICIAN_IDX = 1

#TODO: All tests are dipricated. They should be disconected. Module should be refactored or killed.

class SpareValidationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_no_data_set(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        title = find_element_by_selector(self.driver, ".js-parts [name='title']")
        quantity = find_element_by_selector(self.driver, ".js-parts [name='quantity']")
        cost = find_element_by_selector(self.driver, ".js-parts [name='cost']")
        price = find_element_by_selector(self.driver, ".js-parts [name='price']")
        cost.clear()
        quantity.clear()
        price.clear()

        find_element_by_selector(self.driver, ADD_PART_BTN).click()

        assert_has_error_tooltip(self.driver, quantity)
        assert_has_error_tooltip(self.driver, price)
        return assert_has_error_tooltip(self.driver, title)

    def test_2_text_input(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        set_value(self.driver, ".js-parts [name='title']", 'test')
        set_value(self.driver, ".js-parts [name='quantity']", 'test')
        set_value(self.driver, ".js-parts [name='cost']", 'test')
        set_value(self.driver, ".js-parts [name='price']", 'test')

        find_element_by_selector(self.driver, ADD_PART_BTN).click()

        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='quantity']")
        ))
        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='cost']")
        ))
        return assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='price']")
        ))

    def test_3_negative_num(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        set_value(self.driver, ".js-parts [name='title']", 'test')
        set_value(self.driver, ".js-parts [name='quantity']", '-1')
        set_value(self.driver, ".js-parts [name='cost']", '-1')
        set_value(self.driver, ".js-parts [name='price']", '-1')

        find_element_by_selector(self.driver, ADD_PART_BTN).click()

        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='quantity']")
        ))
        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='cost']")
        ))
        return assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-parts [name='price']")
        ))


class SpareAddManualyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_add_spare_manualy(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        add_spare_manually(self.driver, SPARE_PART1)
        return True

    def test_2_delete_spare(self):
        remove_item_from_grid(
            self.driver, ".js-parts"
        )
        return True

    # Count price of spares added manually
    def test_3_count_spare(self):
        add_spare_manually(self.driver, SPARE_PART2)
        spare_sum = find_element_by_selector(
            self.driver, ".js-parts .js-aggregate-sum"
        ).text
        self.assertTrue(format_price(spare_sum) == SPARE_PART2['sum'])
        save_order(self.driver)
        return True

    def test_4_edit_manual_spare(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        add_spare_manually(self.driver, SPARE_PART1)

        find_element_by_selector(
            self.driver, ".js-parts tbody tr:nth-child(2) td"
        ).click()
        edit_manual_spare(self.driver, EDIT_SPARE_PART1)
        save_order(self.driver)
        return True

    def test_5_add_spare_and_worker(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        choose_from_select(self.driver, ".js-parts select",  TECHNICIAN_IDX)
        technician = find_element_by_selector(
            self.driver, ".js-parts select option", TECHNICIAN_IDX
        ).text

        add_spare_manually(self.driver, SPARE_PART1)

        event = make_double_text_xpath("p", "@class, 'k-reset'", technician)
        assert_xpath_is_visible(self.driver, event)
        return save_order(self.driver)


class SpareAddFromWarehouseTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_precondition_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, SPARE_PART3)

        navigate(self.driver, ORDERS_URL)
        return True

    def test_1_add_spare_from_warehouse(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        open_dialog(
            self.driver, ".js-add-warehouse", ".b-dialog_type_warehouse .b-search__input"
        )

        find_element_by_selector(
            self.driver, ".b-dialog_type_warehouse .b-search__input"
        ).send_keys(SPARE_PART3['title'])
        wait_to_click_selector(
            self.driver, ".b-dialog_type_warehouse .b-search__reset"
        )

        find_element_by_selector(
            self.driver, ".js-grid-residue .k-grid-content tr td:nth-child(3)"
        ).click()
        find_element_by_selector(
            self.driver, ".b-dialog_type_warehouse .js-wh-add"
        ).click()
        close_dialog(
            self.driver, ".b-dialog_type_warehouse .js-submit-dialog", ".b-dialog_type_warehouse"
        )

        assert_xpath_is_visible(
            self.driver, make_text_xpath("td", SPARE_PART3['title'])
        )

        return save_order(self.driver)

    def test_2_add_from_warehouse_with_worker(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        open_dialog(
            self.driver, ".js-add-warehouse", ".b-dialog_type_warehouse .b-search__input"
        )

        find_element_by_selector(
            self.driver, ".b-dialog_type_warehouse .b-search__input"
        ).send_keys(SPARE_PART3['title'])
        wait_to_click_selector(
            self.driver, ".b-dialog_type_warehouse .b-search__reset"
        )
        find_element_by_selector(
            self.driver, ".js-grid-residue .k-grid-content tr td:nth-child(3)"
        ).click()
        find_element_by_selector(
            self.driver, ".b-dialog_type_warehouse .js-wh-add"
        ).click()

        choose_from_select(
            self.driver, ".b-dialog__content .h-mt-15 select",  TECHNICIAN_IDX
        )
        technician = find_element_by_selector(
            self.driver, ".b-dialog__content .h-mt-15 select option", TECHNICIAN_IDX
        ).text

        close_dialog(
            self.driver, ".b-dialog_type_warehouse .js-submit-dialog", ".b-dialog_type_warehouse"
        )

        assert_xpath_is_visible(
            self.driver, make_text_xpath("td", SPARE_PART3['title'])
        )
        event = make_double_text_xpath("p", "@class, 'k-reset'", technician)
        assert_xpath_is_visible(self.driver, event)

        return save_order(self.driver)
