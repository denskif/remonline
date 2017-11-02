# ~*~ coding: utf-8 ~*~

from unittest import TestCase


from src.tests.api.lib.queries import new_token, q_get, q_status, get_json
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import BRANCH_URL
from src.tests.api.lib.schemas import BRANCH_JSON, assert_response



class ApiBranchTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.branch = q_get(BRANCH_URL, new_token())

    def test_1_get_all_branches(self):
        return self.assertEqual(q_status(self.branch), SUCCESS)

    def test_2_check_branch_answer(self):
        return assert_response(get_json(self.branch), BRANCH_JSON)
