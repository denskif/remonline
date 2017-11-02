# ~*~ coding: utf-8 ~*~

import time
from unittest import TestCase

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, SHOP_URL, REFUND_URL, CASHBOX_URL
from src.lib.dom import find_element_by_selector, make_selector
from src.lib.wait import wait_for_selector
from src.lib.notify import wait_error_notify, wait_info_notify

from src.scaffolds.dialog import confirm_delete, open_additional_menu

from src.tests.warehouse.lib.create import create_posting
from src.tests.shop.lib.sale import make_sale
from src.tests.shop.lib import open_last_sale, close_sale_dialog
from src.tests.refunds.lib.refund import make_sale_refund
from src.tests.refunds.lib import (
	REFUND_FIRST_ROW_CELL_SEL, REFUND_LINK_SEL, REFUND_ATTRIBUTE,
)
from src.tests.cashflow.lib import CASHBOX_FIRST_ROW_SEL


REFUND_OPTION_SEL = ".js-refund"


class SaleRefund(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.driver = get_driver()
		navigate(cls.driver, POSTING_URL)
		cls.item = create_posting(cls.driver)
		navigate(cls.driver, SHOP_URL)
		make_sale(cls.driver, cls.item)

	def tearDown(self):
		sale_dialog = find_element_by_selector(self.driver, ".b-sale")
		
		if sale_dialog and sale_dialog.is_displayed():
			close_sale_dialog(self.driver)

		navigate(self.driver, SHOP_URL)

	def test1_create_refund(self):
		make_sale_refund(self.driver)
		# Get sale label
		sale_label = find_element_by_selector(
			self.driver, ".js-shop-grid [href]"
		).text
		
		second_cell_idx = 1

		# Get refund label
		navigate(self.driver, REFUND_URL)
		wait_for_selector(self.driver, REFUND_FIRST_ROW_CELL_SEL)
		refund_label = find_element_by_selector(
			self.driver, REFUND_FIRST_ROW_CELL_SEL, idx=second_cell_idx
		).text

		self.assertIn(sale_label, refund_label)

	def test2_cant_delete_sale_with_refund(self):
		open_last_sale(self.driver)
		open_additional_menu(self.driver)
		find_element_by_selector(self.driver, ".js-remove-sale").click()
		confirm_delete(self.driver)
		return wait_error_notify(self.driver)

	def test3_all_items_refunded(self):
		open_last_sale(self.driver)
		open_additional_menu(self.driver)
		find_element_by_selector(self.driver, REFUND_OPTION_SEL).click()
		return wait_info_notify(self.driver)


class ShopRefundPayment(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.driver = get_driver()
		navigate(cls.driver, POSTING_URL)
		cls.item = create_posting(cls.driver)
		navigate(cls.driver, SHOP_URL)
		make_sale(cls.driver, cls.item)

	def test1_check_refund_in_cashbox(self):
		make_sale_refund(self.driver)

		navigate(self.driver, REFUND_URL)
		wait_for_selector(self.driver, REFUND_FIRST_ROW_CELL_SEL)

		refund_label = find_element_by_selector(
			self.driver, 
			make_selector(REFUND_FIRST_ROW_CELL_SEL, "a")
		).text

		navigate(self.driver, CASHBOX_URL)
		wait_for_selector(self.driver, CASHBOX_FIRST_ROW_SEL)

		refund_transaction = find_element_by_selector(
			self.driver,
			make_selector(CASHBOX_FIRST_ROW_SEL, REFUND_LINK_SEL)
		).text
		return self.assertTrue(refund_label in refund_transaction)