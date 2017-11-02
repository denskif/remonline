# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib import BRANCH_ID
from src.tests.api.lib.queries import new_token, q_get, q_status, get_json
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import B_MODEL_URL, B_SERVICE_URL
from src.tests.api.lib.schemas import assert_response, MODELS_JSON, SERVICES_JSON





class ApiBookModelsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.models = q_get(B_MODEL_URL.format(BRANCH_ID), new_token())

    def test_1_get_models(self):
        return self.assertEqual(q_status(self.models), SUCCESS)

    def test_2_check_models_answer(self):
        return assert_response(get_json(self.models), MODELS_JSON)



class ApiBookServicesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.services = q_get(B_MODEL_URL.format(BRANCH_ID), new_token())

    def test_1_get_services(self):
        return self.assertEqual(q_status(self.services), SUCCESS)

    def test_2_check_services_answer(self):
        return assert_response(get_json(self.services), SERVICES_JSON)
