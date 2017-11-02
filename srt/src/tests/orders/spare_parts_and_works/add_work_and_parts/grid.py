# ~*~ coding: utf-8 ~*~


import unittest

from src.lib.driver import get_driver
from src.lib.dom import (
    find_element_by_selector, find_elements_by_selector, hover_and_click, hover,
    double_click,
    )
from src.lib.wait import wait_selector_to_disappear, wait_to_see_selector
from src.lib.notify import wait_notify_to_appear
from src.lib.url import navigate, ORDERS_URL, WORKERS_URL, POSTING_URL

from src.scaffolds.dialog import close_dialog
from src.scaffolds.dropdown import choose_select_by_text

from src.tests.warehouse.lib.create import create_posting

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, close_order
from src.tests.orders.spare_parts_and_works.lib import TAB_SEL, YELLOW_SEL
from src.tests.orders.spare_parts_and_works.lib.create import delete_str
from src.tests.orders.spare_parts_and_works.lib.service import (
    manual_add_new_srvc, new_autocomplete_add, go_to_book, add_new_srvc_to_book,
    )
from src.tests.orders.spare_parts_and_works.lib.part import (
    manual_add_new_part, add_part_from_warehouse,
    )
from src.tests.orders.spare_parts_and_works.lib.winbox import (
     close_winbox, close_litebox,
    )
from src.tests.settings.lib.employee import add_worker

from src.tests.orders.spare_parts_and_works.lib.data import (
    data_f_srvc, data_f_part, data_f_wharehouse, data_f_book, data_f_worker,
    )
from src.tests.orders.spare_parts_and_works.lib.tooltip import (
    get_tooltip_text, COST_TT_SEL, DISCOUNT_TT_SEL, FINAL_DISCONT_TT_SEL,
    FINAL_PRICE_TT_SEL,
    )


data = data_f_srvc()

icon_text = {
    'part' : u"Запчасть / Материал",
    'srvc' : u"Работа",
}


WINBOX_SEL = ".b-winbox .b-winbox__header"
STRING_SEL = ".b-table__tr_mode_selectable"
TD_SEL = ".b-table__tr_mode_selectable td"


class AddItemsToTableValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.warehouse = data_f_wharehouse()
        cls.part = data_f_part()
        cls.book = data_f_book()
        go_to_book(cls.driver)
        add_new_srvc_to_book(cls.driver, cls.book)
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, cls.warehouse)
        navigate(cls.driver, ORDERS_URL)

    def setUp(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_SEL)
        wait_to_see_selector(self.driver, TAB_SEL)

    def test1_manual_add_srvc(self):
        service = data_f_srvc()
        manual_add_new_srvc(self.driver, service)
        wait_to_see_selector(self.driver, STRING_SEL)
        text = find_element_by_selector(self.driver, STRING_SEL, idx=0).text
        self.assertIn(service['name'], text)

    def test2_add_srvc_from_book(self):
        new_autocomplete_add(
            self.driver, ".b-in-holder .js-srvc-input", self.book['name']
        )
        wait_to_see_selector(self.driver, STRING_SEL)
        text = find_element_by_selector(self.driver, STRING_SEL, idx=0).text
        self.assertIn(self.book['name'], text)

    def test3_add_manual_part(self):
        manual_add_new_part(self.driver, self.part)
        wait_to_see_selector(self.driver, STRING_SEL)
        text = find_element_by_selector(self.driver, STRING_SEL, idx=0).text
        self.assertIn(self.part['name'], text)


    def test4_add_one_part_from_warehouse(self):
        add_part_from_warehouse(self.driver)
        wait_to_see_selector(self.driver, STRING_SEL)
        text = find_element_by_selector(self.driver, STRING_SEL, idx=0).text
        self.assertIn(self.warehouse['title'], text)

    def test5_add_same_part_from_warehouse(self):
        add_part_from_warehouse(self.driver)
        add_part_from_warehouse(self.driver)
        wait_notify_to_appear(self.driver)

    def tearDown(self):
        close_order(self.driver)


# ----------
class AddInOneOrderValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.warehouse = data_f_wharehouse()
        cls.part = data_f_part()
        cls.worker = data_f_worker()
        cls.book = data_f_book()
        cls.driver = get_driver()
        go_to_book(cls.driver)
        add_new_srvc_to_book(cls.driver, cls.book)
        navigate(cls.driver, WORKERS_URL)
        add_worker(cls.driver, cls.worker)
        navigate(cls.driver, POSTING_URL)
        wait_to_see_selector(cls.driver, ".js-wh-posting")
        create_posting(cls.driver, cls.warehouse)
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        wait_to_see_selector(cls.driver, TAB_SEL)

    def test1_add_all_in_table(self):
        service = data_f_srvc()
        str_num = 4
        manual_add_new_srvc(self.driver, service)
        new_autocomplete_add(
            self.driver, ".b-in-holder .js-srvc-input", self.book['name']
        )
        manual_add_new_part(self.driver, self.part)
        add_part_from_warehouse(self.driver)
        quontity_string = find_elements_by_selector(self.driver, STRING_SEL)
        self.assertEqual(len(quontity_string), str_num)

    def test2_add_engineer_in_table_validation(self):
        header_sel = ".js-group-header"
        service = data_f_srvc()
        choose_select_by_text(
            self.driver, ".js-ctx-engineer", self.worker['name']
        )
        manual_add_new_srvc(self.driver, service)
        wait_to_see_selector(self.driver, header_sel)
        text = find_element_by_selector(self.driver, header_sel, idx=1).text
        self.assertEqual(text, self.worker['name'])

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class StringActionsValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = data_f_srvc()
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        wait_to_see_selector(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, cls.service)

    def test1_edit_window_with_double_click(self):
        double_click(self.driver, find_element_by_selector(self.driver, TD_SEL))
        wait_to_see_selector(self.driver, WINBOX_SEL,time=10)
        close_winbox(self.driver)

    def test2_edit_window_with_edit_icon(self):
        edit_icon_sel = ".js-goods-group [data-app-name=GoodEditor]"

        find_element_by_selector(self.driver, edit_icon_sel).click()
        wait_to_see_selector(self.driver, WINBOX_SEL)
        close_winbox(self.driver)

    def test3_delete_window(self):
        delete_icon_sel = ".js-goods-group [data-app-name=Trasher]"

        hover_and_click(self.driver,delete_icon_sel)
        wait_to_see_selector(self.driver, ".b-litebox .b-litebox__header")
        close_litebox(self.driver)

    def test4_comment_window(self):
        find_element_by_selector(self.driver, TD_SEL).click()
        find_element_by_selector(self.driver, ".js-comment").click()
        wait_to_see_selector(self.driver, WINBOX_SEL)
        close_winbox(self.driver)

    def tearDown(self):
        wait_to_see_selector(self.driver, ".js-goods-group")

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)


class TooltipsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)
        create_order(cls.driver)
        open_order(cls.driver)
        open_tab(cls.driver, TAB_SEL)
        manual_add_new_srvc(cls.driver, data)
        wait_to_see_selector(cls.driver, ".js-good-row")
        wait_selector_to_disappear(cls.driver, YELLOW_SEL)

    def test1_tooltip_action_validation(self):
        tt_sel = ".js-tooltip[aria-describedby]"
        hover(self.driver, COST_TT_SEL)
        wait_to_see_selector(self.driver, tt_sel)


    def test2_tooltips_cost_validation(self):
        text = get_tooltip_text(self.driver, COST_TT_SEL)
        self.assertIn(data['cost'], text)


    def test3_tooltip_srvc_icon_validation(self):
        srvc_icon_tt_sel = ".b-table__td .i-wrench"
        text = get_tooltip_text(self.driver, srvc_icon_tt_sel)
        self.assertIn(icon_text['srvc'], text)


    def test4_tooltip_warranty_validation(self):
        warranty_icon_tt_sel = ".b-table__td .js-warranty"
        text = get_tooltip_text(self.driver, warranty_icon_tt_sel)
        self.assertIn(data['warranty_value'], text)


    def test5_tooltip_discount_validation(self):
        text = get_tooltip_text(self.driver, DISCOUNT_TT_SEL)
        self.assertIn(data['discount_value'], text)


    def test6_tooltip_final_discount(self):
        text = get_tooltip_text(self.driver, FINAL_DISCONT_TT_SEL)
        self.assertIn(data['discount_value'], text)


    def test7_tooltip_final_price(self):
        price = int(data['price'])
        discount = int(data['discount_value'])
        quantity = int(data['quantity'])
        final_price = quantity*(price-price*discount/100)
        text = get_tooltip_text(self.driver, FINAL_PRICE_TT_SEL)
        self.assertIn(str(final_price), text)


    def test8_tooltip_part_icon_validation(self):
        part_icon_tt_sel = ".b-table__td .i-puzzle"
        hover_and_click(self.driver, ".b-table__tr")
        delete_str(self.driver)
        manual_add_new_part(self.driver)
        hover_and_click(self.driver, ".b-table__td")
        text = get_tooltip_text(self.driver, part_icon_tt_sel)
        self.assertIn(icon_text['part'], text)

    @classmethod
    def tearDownClass(cls):
        close_order(cls.driver)
