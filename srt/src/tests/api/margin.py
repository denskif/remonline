# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib.queries import new_token, q_get, q_status, get_json
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import MARGIN_URL
from src.tests.api.lib.schemas import MARGIN_JSON, assert_response



class ApiMarginTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.margin = q_get(MARGIN_URL, new_token())

    def test_1_get_margins(self):
        return self.assertEqual(q_status(self.margin), SUCCESS)

    def test_2_check_response(self):
        return assert_response(get_json(self.margin), MARGIN_JSON)
