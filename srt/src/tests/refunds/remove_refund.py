# ~*~ coding: utf-8 ~*~

import time
from unittest import TestCase

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, SHOP_URL, REFUND_URL
from src.lib.dom import find_element_by_selector, make_selector, hover_and_click
from src.lib.wait import wait_for_selector, wait_selector_to_disappear

from src.scaffolds.dialog import confirm_new_delete_dialog, open_additional_menu

from src.tests.warehouse.lib.create import create_posting
from src.tests.shop.lib.sale import make_sale
from src.tests.refunds.lib.refund import make_sale_refund
from src.tests.refunds.lib import open_last_refund, REFUND_FIRST_ROW_CELL_SEL


REFUND_FIRST_ROW_SEL = ".js-refunds-app .b-table__tr"


class RemoveRefund(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.driver = get_driver()

		# Post new item to stock
		navigate(cls.driver, POSTING_URL)
		cls.item = create_posting(cls.driver)

		# Make two sales and refund them
		navigate(cls.driver, SHOP_URL)
		make_sale(cls.driver, cls.item)
		make_sale_refund(cls.driver)
		make_sale(cls.driver, cls.item)
		make_sale_refund(cls.driver)

		# Go to refunds page
		navigate(cls.driver, REFUND_URL)
		wait_for_selector(cls.driver, REFUND_FIRST_ROW_SEL)

	def tearDown(self):
		# Waiting for refund table to render
		# More agile solution not found
		time.sleep(0.5)

	def test_1_delete_from_table(self):
		# get id of latest refund
		refund_id = find_element_by_selector(
			self.driver, REFUND_FIRST_ROW_SEL
		).get_attribute("data-table-oid")

		# delete refund from table
		hover_and_click(
			self.driver, make_selector(REFUND_FIRST_ROW_CELL_SEL, ".i-trash")
		)
		confirm_new_delete_dialog(self.driver)

		# check refund disappeared from table
		return wait_selector_to_disappear(
			self.driver, "[data-table-oid={0}]".format(refund_id)
		)

	def test_2_delete_from_dialog(self):
		# get id of latest refund
		refund_id = find_element_by_selector(
			self.driver, REFUND_FIRST_ROW_SEL
		).get_attribute("data-table-oid")

		open_last_refund(self.driver)
		open_additional_menu(self.driver)

		# Delete refund with the dialog menu option
		find_element_by_selector(self.driver, ".js-delete").click()
		confirm_new_delete_dialog(self.driver)
		
		# check refund disappeared from table
		return wait_selector_to_disappear(
			self.driver, "[data-table-oid={0}]".format(refund_id)
		) 