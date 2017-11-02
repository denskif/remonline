# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib import STOCK_ID
from src.tests.api.lib.queries import (
    new_token, q_get, q_status, q_post, get_json
)
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import WAREHOUSE_URL, W_CATEGORY_URL, W_GOODS_URL
from src.tests.api.lib.schemas import (
    assert_response, STOCK_JSON, CATEGORIES_JSON, GOODS_JSON
)



class ApiWarehouseTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stocks = q_get(WAREHOUSE_URL, new_token())
        cls.categories = q_get(W_CATEGORY_URL, new_token())
        cls.goods = q_get(W_GOODS_URL.format(STOCK_ID), new_token())

    def test_1_get_warehouses(self):
        return self.assertEqual(q_status(self.stocks), SUCCESS)

    def test_2_check_warehouse_answer(self):
        return assert_response(get_json(self.stocks), STOCK_JSON)

    def test_3_get_categories(self):
        return self.assertEqual(q_status(self.categories), SUCCESS)

    def test_4_check_categories_answer(self):
        return assert_response(get_json(self.stocks), CATEGORIES_JSON)

    def test_5_get_goods(self):
        return self.assertEqual(q_status(self.goods), SUCCESS)

    def test_6_check_goods_answer(self):
        return assert_response(get_json(self.stocks), GOODS_JSON)
