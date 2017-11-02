# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.lib.randomizer import make_phone_number, make_email, random_x
from src.lib.formatting import format_phone_ua

from src.tests.api.lib import MARKET_SOURCE_1, MARKET_SOURCE_2
from src.tests.api.lib.queries import (
    new_token, q_get, q_status, q_post, get_json, q_put
)
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import CLIENT_URL, CLIENT_SOURCE_URL
from src.tests.api.lib.schemas import (
    assert_response, CLIENT_SOURCE_JSON, CLIENT_LIST_JSON, NEW_CLIENT_JSON,
    make_load, unpack_count, unpack_data
)


UNIQUE = 1
JURI = 'juridical'
BAD = 'conflicted'
SUPPLIER = 'supplier'


CLIENT = {
    'name' : "MR_{0}".format(random_x()),
    'phone[]' : format_phone_ua(make_phone_number()),
    'email' : make_email(),
    'address' : "Downing street, {0}".format(random_x()),
    'marketing_source' : MARKET_SOURCE_1,
    JURI : True,
    SUPPLIER : True,
    BAD : True,
}
CLIENT_2_UPDATE = {
    'id' : None,
    'name' : "MR_{0}".format(random_x()),
    'phone[]' : format_phone_ua(make_phone_number()),
    'email' : make_email(),
    'address' : "Downing street, {0}".format(random_x()),
    'marketing_source' : MARKET_SOURCE_2,
    JURI : False,
    SUPPLIER : False,
    BAD : False,
}


def make_client(data):
    return q_post(CLIENT_URL, make_load(data))

def get_id(request):
    return unpack_data(request)['id']


class ApiGetClientsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clients = q_get(CLIENT_URL, new_token())
        cls.sources = q_get(CLIENT_SOURCE_URL, new_token())
        cls.client_data = CLIENT.copy()

    def test_1_get_clients(self):
        return self.assertEqual(q_status(self.clients), SUCCESS)

    def test_2_check_clients_answer(self):
        return assert_response(get_json(self.clients), CLIENT_LIST_JSON)

    def test_3_get_client_sources(self):
        return self.assertEqual(q_status(self.sources), SUCCESS)

    def test_4_check_client_source_answer(self):
        return assert_response(get_json(self.sources), CLIENT_SOURCE_JSON)


class ApiPostFilterClientsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_data = CLIENT.copy()

    def test_1_create_client(self):
        new_client = make_client(self.client_data)
        return self.assertEqual(q_status(new_client), SUCCESS)

    def test_2_filter_client_data(self):
        client_by_name = q_get(
            CLIENT_URL, make_load(
                {'names[]' : self.client_data['name']})
        )
        self.assertEqual(unpack_count(client_by_name), UNIQUE)
        self.assertEqual(q_status(client_by_name), SUCCESS)

    def test_3_filter_client_address(self):
        client_address = q_get(
            CLIENT_URL, make_load(
                {'addresses[]' : self.client_data['address']})
        )
        self.assertEqual(unpack_count(client_address), UNIQUE)
        return self.assertEqual(q_status(client_address), SUCCESS)

    def test_4_filter_client_phone(self):
        client_phone = q_get(
            CLIENT_URL, make_load(
                {'phones[]' : self.client_data['phone[]']})
        )
        self.assertEqual(unpack_count(client_phone), UNIQUE)
        return self.assertEqual(q_status(client_phone), SUCCESS)

    def test_5_filter_client_email(self):
        client_email = q_get(
            CLIENT_URL, make_load(
                {'emails[]' : self.client_data['email']})
        )
        self.assertEqual(unpack_count(client_email), UNIQUE)
        return self.assertEqual(q_status(client_email), SUCCESS)

    def test_6_filter_client_source(self):
        client_source = q_get(
            CLIENT_URL, make_load(
                {'marketing_sources[]' : self.client_data['marketing_source']})
        )

        for item in unpack_data(client_source):
            source = item['marketing_source']
            self.assertEqual(source['id'] , MARKET_SOURCE_1)

        return self.assertEqual(q_status(client_source), SUCCESS)

    def test_7_filter_client_juridical(self):
        client = q_get(
            CLIENT_URL, make_load(
                {JURI : self.client_data[JURI]})
        )

        map(lambda i: self.assertEqual(i[JURI], True), unpack_data(client))
        return self.assertEqual(q_status(client), SUCCESS)

    def test_8_filter_client_conflicted(self):
        client = q_get(
            CLIENT_URL, make_load(
                {BAD : self.client_data[BAD]})
        )

        map(lambda i: self.assertEqual(i[BAD], True), unpack_data(client))
        return self.assertEqual(q_status(client), SUCCESS)

    def test_9_filter_client_supplier(self):
        client = q_get(
            CLIENT_URL, make_load(
                {SUPPLIER : self.client_data[SUPPLIER]})
        )

        map(lambda i: self.assertEqual(i[SUPPLIER], True), unpack_data(client))
        return self.assertEqual(q_status(client), SUCCESS)


class ApiChangeClientsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = make_client(CLIENT.copy())

    def test_1_check_client_updated(self):
        new_client_data = CLIENT_2_UPDATE.copy()
        new_client_data['id'] = get_id(self.client)
        updated_client = q_put(CLIENT_URL, make_load(new_client_data))
        return self.assertEqual(q_status(updated_client), SUCCESS)
