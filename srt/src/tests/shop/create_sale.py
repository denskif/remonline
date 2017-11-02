# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, SHOP_URL
from src.lib.dom import (
    find_element_by_selector, find_elements_by_selector, set_value, get_value,
)
from src.lib.errors import assert_has_error_tooltip
from src.lib.wait import wait_for_selector, wait_selector_to_disappear, wait_to_click_selector
from src.lib.randomizer import random_x

from src.tests.warehouse.lib.create import create_posting

from src.tests.shop.lib import (
    open_new_sale, close_sale_dialog, close_sale_dialog_via_mask, MAKE_SALE_SEL, SALE_CODE_SEL, NEW_SALE_BUTTON
)
from src.tests.shop.lib.sale import (
    prepare_sale, pay_for_sale, delete_sale, open_last_sale, make_sale
)

STACK_SEL = ".js-fletcher"
ROW_SEL = ".js-shop-grid tr"

description_text = u"This is special comment {0}".format(random_x())

GOODS_FOR_SALE = {
    u'title' : u"Mahichnuy Chobit",
    u'supplier' : {'name': u"Magic Supplies"},
    u'quantity' : u"25",
    u'price' : u"768.34",
    u'description' : description_text,
}


class ValidateSale(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, SHOP_URL)

    def setUp(self):
        wait_to_click_selector(self.driver, NEW_SALE_BUTTON)
        open_new_sale(self.driver)

    def test_1_open_close_sale(self):
        close_sale_dialog(self.driver)

    def test_2_close_sale_via_mask(self):
        close_sale_dialog_via_mask(self.driver)

    def test_3_no_goods_added(self):
        wait_for_selector(self.driver, MAKE_SALE_SEL)
        find_element_by_selector(self.driver, MAKE_SALE_SEL).click()

        return assert_has_error_tooltip(
            self.driver, find_element_by_selector(self.driver, STACK_SEL)
        )

    @classmethod
    def tearDownClass(cls):
        close_sale_dialog(cls.driver)


# Create tests should run as a suit (only for tests class installs goods)
class CreateSale(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, POSTING_URL)
        create_posting(cls.driver, GOODS_FOR_SALE)

    def test_1_make_sale(self):
        navigate(self.driver, SHOP_URL)

        wait_for_selector(self.driver, ROW_SEL)
        old_num_of_sales = len(find_elements_by_selector(
            self.driver, ROW_SEL
        ))

        prepare_sale(self.driver, GOODS_FOR_SALE['title'])
        pay_for_sale(self.driver)

        new_num_of_sales = len(find_elements_by_selector(
            self.driver, ROW_SEL
        ))

        return self.assertTrue(old_num_of_sales < new_num_of_sales)

    def test_2_check_sale(self):
        open_last_sale(self.driver)
        title_cell_sel = ".b-dialog .b-table__td"
        wait_for_selector(self.driver, title_cell_sel)
        title_cell_idx = 0
        sold = find_element_by_selector(
            self.driver, title_cell_sel, title_cell_idx
        ).text

        return self.assertEqual(sold, GOODS_FOR_SALE['title'])

    @classmethod
    def tearDownClass(cls):
        close_sale_dialog(cls.driver)


class CreateDescribedSale(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, SHOP_URL)

    def test_1_make_sale_with_description(self):
        prepare_sale(self.driver, GOODS_FOR_SALE['title'])

        set_value(
            self.driver, "[name=description]", GOODS_FOR_SALE['description']
        )

        pay_for_sale(self.driver)

        desc_cell_idx = 5
        return self.assertEqual(
            find_element_by_selector(
                self.driver, ".js-shop-grid tbody td", desc_cell_idx
            ).text, description_text
        )

    def test_2_check_described_sale(self):
        open_last_sale(self.driver)

        view_sale_desc_sel = ".js-sale-desc"

        wait_for_selector(self.driver, view_sale_desc_sel)
        descripton = get_value(
            find_element_by_selector(self.driver, view_sale_desc_sel)
        )

        return self.assertEqual(descripton, GOODS_FOR_SALE['description'])

    @classmethod
    def tearDownClass(cls):
        close_sale_dialog(cls.driver)


class DeleteSale(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, SHOP_URL)

    def test_1_remove_sale(self):
        make_sale(self.driver, GOODS_FOR_SALE['title'])

        wait_for_selector(self.driver, ROW_SEL)
        old_num_of_sales = len(find_elements_by_selector(
            self.driver, ROW_SEL
        ))

        sale_code = find_element_by_selector(
            self.driver, SALE_CODE_SEL
        ).get_attribute('href')
        first_sale_sel = "{0}='{1}']".format(SALE_CODE_SEL[:-1], sale_code)

        delete_sale(self.driver)
        wait_selector_to_disappear(self.driver, first_sale_sel)

        new_num_of_sales = len(find_elements_by_selector(
            self.driver, ROW_SEL
        ))
        deleted_sale = 1
        return self.assertEqual(
            old_num_of_sales, new_num_of_sales + deleted_sale
        )
