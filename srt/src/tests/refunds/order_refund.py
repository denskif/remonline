# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.lib.driver import get_driver
from src.lib.url import (
	navigate, POSTING_URL, ORDERS_URL, REFUND_URL, CASHBOX_URL
)
from src.lib.dom import find_element_by_selector, make_selector
from src.lib.wait import wait_for_selector
from src.lib.notify import wait_error_notify, wait_info_notify

from src.scaffolds.dialog import open_additional_menu

from src.tests.orders.lib.open import open_order, close_order
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.status import close_and_pay_from_order
from src.tests.orders.lib.delete import delete_order

from src.tests.orders.spare_parts_and_works.lib.part import add_part_by_title

from src.tests.warehouse.lib.create import create_posting

from src.tests.refunds.lib import (
	REFUND_OPTION_SEL, REFUND_FIRST_ROW_CELL_SEL, REFUND_LINK_SEL,
	REFUND_ATTRIBUTE,
)
from src.tests.refunds.lib.refund import make_order_refund

from src.tests.cashflow.lib import CASHBOX_FIRST_ROW_SEL



CASHBOX_IDX = 1
CLOSED_STATUS_IDX = -1


class OrderRefund(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.driver = get_driver()

		# Post new item
		navigate(cls.driver, POSTING_URL)
		cls.item = create_posting(cls.driver)

		# Cteate new order and add item
		navigate(cls.driver, ORDERS_URL)
		create_order(cls.driver)
		open_order(cls.driver)
		add_part_by_title(cls.driver, cls.item)

		# Change status to closed with payment
		close_and_pay_from_order(cls.driver, CLOSED_STATUS_IDX, CASHBOX_IDX)
		close_order(cls.driver)

	def tearDown(self):
		order_dialog = find_element_by_selector(self.driver, ".b-order")

		if order_dialog and order_dialog.is_displayed():
			close_order(self.driver)

		navigate(self.driver, ORDERS_URL)

	def test_1_create_refund(self):
		make_order_refund(self.driver)

		# Get order label
		order_label = find_element_by_selector(
			self.driver, ".js-orders-grid tbody [href]"
		).text

		second_cell_idx = 1

		# Get refund description
		navigate(self.driver, REFUND_URL)
		wait_for_selector(self.driver, REFUND_FIRST_ROW_CELL_SEL)
		refund_description = find_element_by_selector(
			self.driver, REFUND_FIRST_ROW_CELL_SEL, idx=second_cell_idx
		).text

		self.assertIn(order_label, refund_description)

	def test_2_cant_delete_order_with_refund(self):
		open_order(self.driver)
		delete_order(self.driver)
		return wait_error_notify(self.driver)

	def test_3_all_items_refunded(self):
		open_order(self.driver)
		open_additional_menu(self.driver)
		find_element_by_selector(self.driver, REFUND_OPTION_SEL).click()
		return wait_info_notify(self.driver)


class OrderRefundPayment(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.driver = get_driver()

		# Post new item
		navigate(cls.driver, POSTING_URL)
		cls.item = create_posting(cls.driver)

		# Cteate new order and add item
		navigate(cls.driver, ORDERS_URL)
		create_order(cls.driver)
		open_order(cls.driver)
		add_part_by_title(cls.driver, cls.item)

		# Change status to closed with payment
		close_and_pay_from_order(cls.driver, CLOSED_STATUS_IDX, CASHBOX_IDX)
		close_order(cls.driver)

	def test1_check_refund_in_cashbox(self):
		make_order_refund(self.driver)

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
