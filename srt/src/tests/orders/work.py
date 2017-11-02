# ~*~ coding: utf-8 ~*~

import unittest
import time

from selenium.webdriver.common.action_chains import ActionChains

from src.lib.dom import find_element_by_selector, set_value, get_value
from src.lib.wait import wait_for_selector, wait_to_see_selector
from src.lib.formatting import format_price, make_double_text_xpath
from src.lib.driver import get_driver
from src.lib.errors import assert_xpath_is_visible, assert_has_error_tooltip
from src.lib.url import navigate, BOOK_URL, ORDERS_URL

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.open import open_tab, TAB_WORKS, open_order
from src.tests.orders.lib.work_and_parts import add_work, edit_work, ADD_WORK_BTN

from src.scaffolds.dropdown import choose_from_select, autocomplete_add, test_caret
from src.scaffolds.dialog import close_dialog, open_dialog
from src.scaffolds.grid import remove_item_from_grid


WORK1 = {
    'name': u'Some work',
    'quantity': u'2',
    'price': u'450.5',
}
WORK2 = {
    'name': u'Videogame',
    'quantity': u'3',
    'price': u'77.7',
    'sum': u'233.10',
}
EDIT_WORK1 = {
    'name': u'Videogame',
    'quantity': u'5',
    'price': u'336',
}

WORK_LIST = ['diagnostics', '25']

#TODO: All tests are dipricated. They should be disconected. Module should be refactored or killed.

class WorkValidationTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_no_data_set(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        title = find_element_by_selector(self.driver, ".js-work [name='title']")
        quantity = find_element_by_selector(self.driver, ".js-work [name='quantity']")
        price = find_element_by_selector(self.driver, ".js-work [name='price']")
        quantity.clear()
        price.clear()

        find_element_by_selector(self.driver, ADD_WORK_BTN).click()

        assert_has_error_tooltip(self.driver, quantity)
        assert_has_error_tooltip(self.driver, price)
        return assert_has_error_tooltip(self.driver, title)

    def test_2_text_input(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        set_value(self.driver, ".js-work [name='title']", 'test')
        set_value(self.driver, ".js-work [name='quantity']", 'test')
        set_value(self.driver, ".js-work [name='price']", 'test')

        find_element_by_selector(self.driver, ADD_WORK_BTN).click()

        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-work [name='quantity']")
        ))
        return assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-work [name='price']")
        ))

    def test_3_negative_num(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        bad_inp = '-1'

        set_value(self.driver, ".js-work [name='title']", 'test')
        set_value(self.driver, ".js-work [name='quantity']", bad_inp)
        set_value(self.driver, ".js-work [name='price']", bad_inp)

        find_element_by_selector(self.driver, ADD_WORK_BTN).click()

        assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-work [name='quantity']")
        ))
        return assert_has_error_tooltip(self.driver, (
            find_element_by_selector(self.driver, ".js-work [name='price']")
        ))


class WorkTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_add_work(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        add_work(self.driver, WORK1)
        return True

    def test_2_delete_work(self):
        remove_item_from_grid(
            self.driver, ".js-work"
        )
        return True

    def test_3_count_work(self):
        add_work(self.driver, WORK2)
        work_sum = find_element_by_selector(
            self.driver, ".js-work .js-aggregate-sum"
        ).text

        self.assertTrue(format_price(work_sum) == WORK2['sum'])
        save_order(self.driver)
        return True

    def test_4_edit_work(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        add_work(self.driver, WORK1)
        find_element_by_selector(
            self.driver, ".js-work tbody tr:nth-child(2) td"
        ).click()
        edit_work(self.driver, EDIT_WORK1)
        save_order(self.driver)
        return True

    def test_5_add_work_and_worker(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        TECHNICIAN_IDX = 1
        choose_from_select(self.driver, ".js-work select",  idx=TECHNICIAN_IDX)
        technician = find_element_by_selector(
            self.driver, ".js-work select option", idx=TECHNICIAN_IDX
        ).text

        add_work(self.driver, WORK1)

        event = make_double_text_xpath("p", "@class, 'k-reset'",  technician)
        assert_xpath_is_visible(self.driver, event)
        return save_order(self.driver)


class WorkAutocompleteTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    # Should be replaced by test on proper dict
    def test_0_preconditions(self):
        navigate(self.driver, BOOK_URL)

        widget_btn = ".js-operation-widget .js-add-button"
        wait_to_see_selector(self.driver, widget_btn)

        time.sleep(1)
        open_dialog(
            self.driver, widget_btn, "#l-operation-title"
        )
        set_value(self.driver, "#l-operation-title", WORK_LIST[0])
        set_value(self.driver, "#l-operation-price", WORK_LIST[1])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        navigate(self.driver, ORDERS_URL)
        return True

    def test_1_caret(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        return test_caret(self.driver, "[data-opts-relate=js-ow-title]")

    def test_2_open_by_typein(self):
        autocomplete_add(self.driver, self, "#js-ow-title", WORK_LIST[0])

        work = get_value(
            find_element_by_selector(self.driver, "#js-ow-title")
        )

        self.assertEqual(work, WORK_LIST[0])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")


