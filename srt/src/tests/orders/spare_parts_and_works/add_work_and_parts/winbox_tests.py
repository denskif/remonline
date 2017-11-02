# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear
from src.lib.url import navigate, ORDERS_URL
from src.lib.errors import assert_has_error_tooltip
from src.lib.randomizer import random_x

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, close_order

from src.tests.orders.spare_parts_and_works.lib import TAB_SEL
from src.tests.orders.spare_parts_and_works.lib.winbox import (
    WINBOX_SEL, set_text, input_tests, checkbox_input_test, close_winbox,
    input_checkbox, WINBOX_D_INPUT_SEL, WINBOX_W_INPUT_SEL, clear_text_input,
    text_input_assert,
)
from src.tests.orders.spare_parts_and_works.lib.select import (
    select_caret, select_checkbox, select_discount_btn, select_warranty_btn,
    BTN_1, BTN_2,
)
from src.tests.orders.spare_parts_and_works.lib.create import (
    click_create_srvc_dd, create_part_dd
)
from src.tests.orders.spare_parts_and_works.lib.service import (
    info_from_srvc_book, IDX_D_CHBX, IDX_W_CHBX, IDX_ADD_CHBX, go_to_book,
    NAME_SEL, QUANTITY_SEL, PRICE_SEL, COST_PRICE_SEL, COMMENT_SEL,
)
from src.tests.orders.spare_parts_and_works.lib.save import save_srvc


NAME = {
    'srvc' : u"AAASome service name num {0}".format(random_x()),
    'part' : u"It's some part name num {0}".format(random_x()),
}
COMMENT = {
    'comment' : u"It's cool comment or not {0}".format(random_x())
}

good_data = {
    'quantity' : u"10",
    'price' : u"15",
    'cost' : u"10",
    'discount' : u"10",
    'warranty' : u"14",
}

BAD_DATA = ["abc", "-1", "0.001",]
BAD_DATA2 = ["abc", "-1",]
MAX_INPUT_CHARS_AMOUNT = COMMENT['comment']*4


class WinboxValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def setUp(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_SEL)
        select_caret(self.driver)

    def test1_srvc_winbox_validation(self):
        click_create_srvc_dd(self.driver)
        wait_to_see_selector(self.driver, WINBOX_SEL)
        find_element_by_selector(self.driver, ".b-winbox .b-close").click()

    def test2_part_winbox_validation(self):
        create_part_dd(self.driver)
        wait_to_see_selector(self.driver, WINBOX_SEL)
        find_element_by_selector(self.driver, ".b-winbox .b-close").click()

    def tearDown(self):
        close_order(self.driver)


class WinboxSrvcInputsValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def setUp(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_SEL)
        select_caret(self.driver)
        click_create_srvc_dd(self.driver)
        wait_to_see_selector(self.driver, WINBOX_SEL)

    def test1_text_input_validation(self):
        max_size = 100
        clear_text_input(self.driver, NAME_SEL)
        save_srvc(self.driver)
        text_input_assert(self.driver, NAME_SEL)
        set_text(self.driver, COMMENT_SEL, MAX_INPUT_CHARS_AMOUNT)
        text_in_comment = find_element_by_selector(
            self.driver, ".b-winbox [name='" + COMMENT_SEL + "']"
        ).get_attribute('value')
        self.assertEqual(len(text_in_comment), max_size)
        close_winbox(self.driver)

    def test2_input_bad_data_in_winbox(self):
        set_text(self.driver, NAME_SEL, NAME['srvc'])
        input_tests(self.driver, BAD_DATA, QUANTITY_SEL)

        input_tests(self.driver, BAD_DATA2, PRICE_SEL)
        input_tests(self.driver, BAD_DATA2, COST_PRICE_SEL)

        select_discount_btn(self.driver, BTN_1)
        checkbox_input_test(self.driver, BAD_DATA2, WINBOX_D_INPUT_SEL)
        select_discount_btn(self.driver, BTN_2)
        checkbox_input_test(self.driver, BAD_DATA2, WINBOX_D_INPUT_SEL)

        select_warranty_btn(self.driver, BTN_1)
        checkbox_input_test(self.driver, BAD_DATA2, WINBOX_W_INPUT_SEL)

        select_warranty_btn(self.driver, BTN_2)
        checkbox_input_test(self.driver, BAD_DATA2, WINBOX_W_INPUT_SEL)
        close_winbox(self.driver)

    def test3_input_good_data_in_winbox(self):
        set_text(self.driver, NAME_SEL, NAME['srvc'])
        set_text(self.driver, QUANTITY_SEL, good_data['quantity'])
        set_text(self.driver, PRICE_SEL, good_data['price'])
        set_text(self.driver, COST_PRICE_SEL, good_data['cost'])
        select_discount_btn(self.driver, BTN_1)
        input_checkbox(self.driver, WINBOX_D_INPUT_SEL, good_data['discount'])
        select_warranty_btn(self.driver, BTN_1)
        input_checkbox(self.driver, WINBOX_W_INPUT_SEL, good_data['warranty'])
        save_srvc(self.driver)
        wait_selector_to_disappear(self.driver, WINBOX_SEL)

    def test4_input_discount_more_price(self):
        set_text(self.driver, NAME_SEL, NAME['srvc'])
        set_text(self.driver, QUANTITY_SEL, good_data['quantity'])
        set_text(self.driver, PRICE_SEL, good_data['discount'])
        select_discount_btn(self.driver, BTN_1)
        input_checkbox(self.driver, WINBOX_D_INPUT_SEL, good_data['price'])
        save_srvc(self.driver)
        error = find_element_by_selector(self.driver, WINBOX_D_INPUT_SEL)
        assert_has_error_tooltip(self.driver, error)
        close_winbox(self.driver)

    def tearDown(self):
        close_order(self.driver)


class SrvcAddToBookList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def setUp(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_SEL)
        select_caret(self.driver)
        click_create_srvc_dd(self.driver)
        wait_to_see_selector(self.driver, WINBOX_SEL)

    def test1_select_checkbox_add_service(self):
        check_data = {
            'name' : u"01Check to add service name num1{0}".format(random_x()),
            'price' : u"15",
        }
        idx_name_td = 0
        idx_price_td = 2

        set_text(self.driver, NAME_SEL, check_data['name'])
        select_checkbox(self.driver, IDX_ADD_CHBX)
        set_text(self.driver, PRICE_SEL, check_data['price'])
        save_srvc(self.driver)
        close_order(self.driver)
        go_to_book(self.driver)

        name = info_from_srvc_book(self.driver, idx_name_td)
        price = info_from_srvc_book(self.driver, idx_price_td)
        data = "{0} {1}".format(check_data['name'], check_data['price'])
        new_data = name + " " + price
        self.assertEqual(data, new_data)

    @classmethod
    def tearDownClass(cls):
        navigate(cls.driver, ORDERS_URL)
