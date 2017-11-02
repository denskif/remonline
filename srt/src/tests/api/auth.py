# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.tests.api.lib.queries import (
    q_token, q_status, q_post, get_json,
)
from src.tests.api.lib.s_codes import (
    SUCCESS, API_KEY_MISSED, INVALID_API_KEY, TOKEN_MISSED, INVALID_TOKEN,
)
from src.tests.api.lib.url import TOKEN_URL, ORDERS_URL


EMPTY_DICT = {}
BAD_API_KEY = {'api_key' : "11111111112222222222333333333344",}
BAD_TOKEN = {'token' : "1111111111222222222233333333334444444444",}

# Key for code value in response json
CODE_KEY = 'code'


class ApiTokenTests(TestCase):

    def test_1_make_new_token(self):
        return self.assertEqual(q_status(q_token()), SUCCESS)

    def test_2_no_apikey(self):
        answer =  get_json(q_post(TOKEN_URL, EMPTY_DICT))
        return self.assertEqual(
           answer[CODE_KEY], API_KEY_MISSED
        )

    def test_3_bad_apikey(self):
        answer =  get_json(q_post(TOKEN_URL, BAD_API_KEY))
        return self.assertEqual(
           answer[CODE_KEY], INVALID_API_KEY
        )

    def test_4_no_token(self):
        answer =  get_json(q_post(ORDERS_URL, EMPTY_DICT))
        return self.assertEqual(
           answer[CODE_KEY], TOKEN_MISSED
        )

    def test_5_bad_token(self):
        answer =  get_json(q_post(ORDERS_URL, BAD_TOKEN))
        return self.assertEqual(
           answer[CODE_KEY], INVALID_TOKEN
        )
