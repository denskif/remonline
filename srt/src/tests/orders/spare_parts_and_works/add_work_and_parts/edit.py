# ~*~ coding: utf-8 ~*~
import unittest
import re

from src.lib.driver import get_driver
from src.lib.dom import (
    find_element_by_selector, set_value, get_value, hover_and_click,
)
from src.lib.wait import wait_selector_to_disappear, wait_to_see_selector
from src.lib.url import navigate, ORDERS_URL, POSTING_URL
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, close_order
from src.tests.warehouse.lib.create import create_posting

from src.tests.orders.spare_parts_and_works.lib import TAB_SEL, YELLOW_SEL
from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc
from src.tests.orders.spare_parts_and_works.lib.part import (
    manual_add_new_part, add_part_from_warehouse,
    )
from src.tests.orders.spare_parts_and_works.lib.edit import (
    edit_with_double_click, add_comment_for_first_in_grid,
    )
from src.tests.orders.spare_parts_and_works.lib.create import delete_str
from src.tests.orders.spare_parts_and_works.lib.data import (
    data_f_srvc, data_f_edit_srvc, data_f_part, data_f_wharehouse, comment,
    data_for_edit_part, RelationFromDiscountType,
    )
from src.tests.orders.spare_parts_and_works.lib.tooltip import (
    get_tooltip_text, WARRANTY_TT_SEL,
    COST_TT_SEL, DISCOUNT_TT_SEL, FINAL_DISCONT_TT_SEL, FINAL_PRICE_TT_SEL,
    )


#We need use wait time 10, because standart settings time not work
WAIT_FOR_YELLOW = 10
STRING_SEL = ".b-table__tr"
FINAL_DISCOUNT_RATE = ".js-total-discount"


class EditCommentInTableStr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_f_wh = data_f_wharehouse()
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        wait_to_see_selector(cls.driver, ".js-wh-posting")
        create_posting(cls.driver, cls.data_f_wh)
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)

    def setUp(self):
        wait_to_see_selector(self.driver, TAB_SEL)


    def test1_srvc_str_comment(self):
        data = data_f_srvc()
        data_c = comment()
        manual_add_new_srvc(self.driver, data)
        add_comment_for_first_in_grid(self.driver, data_c['comment'])
        wait_selector_to_disappear(self.driver, YELLOW_SEL, 10)
        comment_in_grid = find_element_by_selector(self.driver, ".js-comment").text
        self.assertIn(data_c['comment'], comment_in_grid)

    def test2_manual_part_str_comment(self):
        data = data_f_part()
        data_c = comment()
        manual_add_new_part(self.driver, data)
        add_comment_for_first_in_grid(self.driver, data_c['comment'])
        wait_selector_to_disappear(self.driver, YELLOW_SEL, 10)
        comment_in_grid = find_element_by_selector(self.driver, ".js-comment").text
        self.assertIn(data_c['comment'], comment_in_grid)

    def test3_part_from_wharehouse_str_comment(self):
        data_c = comment()
        add_part_from_warehouse(self.driver)
        add_comment_for_first_in_grid(self.driver, data_c['comment'])
        wait_selector_to_disappear(self.driver, YELLOW_SEL, 10)
        comment_in_grid = find_element_by_selector(self.driver, ".js-comment").text
        self.assertIn(data_c['comment'], comment_in_grid)

    def tearDown(self):
        delete_str(self.driver)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class EditQuontityInTableStr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_f_wh = data_f_wharehouse()
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        wait_to_see_selector(cls.driver, ".js-wh-posting")
        create_posting(cls.driver, cls.data_f_wh)
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)

    def setUp(self):
        wait_to_see_selector(self.driver, TAB_SEL)


    def test1_srvc_quontity_str(self):
        data = data_f_srvc()
        data_p = data_f_edit_srvc()
        manual_add_new_srvc(self.driver, data)
        wait_to_see_selector(self.driver, ".b-table__tr_mode_selectable")
        find_element_by_selector(self.driver, ".js-qty").click()
        set_value(self.driver,".js-qty", data_p['quantity'])
        new = get_value(find_element_by_selector(self.driver, ".js-qty"))
        self.assertEqual(data_p['quantity'], new)


    def test2_manual_part_quontity_str(self):
        data = data_f_part()
        data_p = data_for_edit_part()
        manual_add_new_part(self.driver, data)
        wait_to_see_selector(self.driver, ".b-table__tr_mode_selectable")
        find_element_by_selector(self.driver, ".js-qty").click()
        set_value(self.driver,".js-qty", data_p['quantity'])
        new = get_value(find_element_by_selector(self.driver, ".js-qty"))
        self.assertEqual(data_p['quantity'], new)


    def test3_part_from_wharehouse_quontity_str(self):
        data_p = data_for_edit_part()
        add_part_from_warehouse(self.driver)
        wait_to_see_selector(self.driver, ".b-table__tr_mode_selectable")
        wait_selector_to_disappear(self.driver, ".js-qty:input")


    def tearDown(self):
        delete_str(self.driver)


    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class EditManualSrvcData(unittest.TestCase):

    #Data for this test must have True discount and warranty
    data_create = data_f_srvc()
    data_edit = data_f_edit_srvc()
    rel = RelationFromDiscountType(data_edit)

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.data_create)
        edit_with_double_click(cls.driver, cls.data_edit)

    def test1_check_change_quantity(self):
        STR_QUANTITY_SEL = ".js-qty"
        new = get_value(find_element_by_selector(self.driver, STR_QUANTITY_SEL))

        self.assertEqual(new, self.data_edit['quantity'])

    def test2_check_change_price(self):
        STR_PRICE_SEL = ".js-price"
        new = find_element_by_selector(self.driver, STR_PRICE_SEL).text
        edit_price = self.rel.price()

        self.assertEqual(str(new), edit_price)

    def test3_check_change_cost(self):
        hover_and_click(self.driver, STRING_SEL)
        text = get_tooltip_text(self.driver, COST_TT_SEL)
        new_cost = re.findall(r'\d+', text)

        self.assertEqual(new_cost[0], self.data_edit['cost'])

    def test4_check_change_discount(self):
        hover_and_click(self.driver, STRING_SEL)
        text = get_tooltip_text(self.driver, DISCOUNT_TT_SEL)
        new_discount_str = re.findall(r'(\d+).+\(([\d\.+]+).+\)', text)
        new_discount = self.rel.discount(new_discount_str)

        self.assertEqual(new_discount, self.data_edit['discount_value'])

    def test5_check_change_warranty(self):
        hover_and_click(self.driver, STRING_SEL)
        text = get_tooltip_text(self.driver, WARRANTY_TT_SEL)
        new_warranty = re.findall(r'\d+', text)

        self.assertEqual(new_warranty[0], self.data_edit['warranty_value'])

    def test6_check_change_final_discount_rate(self):
        new_discount_rate = find_element_by_selector(
            self.driver, FINAL_DISCOUNT_RATE
        ).text
        discount = self.rel.final_discount_rate()

        self.assertEqual(discount, new_discount_rate)

    def test7_check_change_final_discount_currency(self):
        text = get_tooltip_text(self.driver, FINAL_DISCONT_TT_SEL)
        new_discount_percent = re.findall(r'([\d\.+]+).+', text)
        discount = self.rel.final_discount_currency()

        self.assertEqual(discount, new_discount_percent[0])

    def test8_check_change_final_price(self):
        text = get_tooltip_text(self.driver, FINAL_PRICE_TT_SEL)
        final_price = self.rel.final_price()

        self.assertIn(str(final_price), text)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)
