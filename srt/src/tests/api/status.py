# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib.queries import new_token, q_get, q_status, get_json
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import STATUS_URL
from src.tests.api.lib.schemas import STATUS_JSON, assert_response


class ApiStatusTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.status = q_get(STATUS_URL, new_token())

    def test_1_get_statuses(self):
        return self.assertEqual(q_status(self.status), SUCCESS)

    def test_2_check_status_response(self):
        return assert_response(get_json(self.status), STATUS_JSON)
