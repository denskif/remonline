# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib.queries import new_token, q_get, q_status, get_json
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import STUFF_URL
from src.tests.api.lib.schemas import EMPLOYEES_JSON, assert_response



class ApiStuffTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stuff = q_get(STUFF_URL, new_token())

    def test_1_get_employees(self):
        return self.assertEqual(q_status(self.stuff), SUCCESS)

    def test_2_check_employee_answer(self):
        return assert_response(get_json(self.stuff), EMPLOYEES_JSON)
