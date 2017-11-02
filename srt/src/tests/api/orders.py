# ~*~ coding: utf-8 ~*~

from time import time
from unittest import TestCase

from src.lib.randomizer import random_x, make_phone_number, make_email
from src.lib.formatting import format_phone_ua

from src.tests.api.lib import STUFF, BRANCH_ID
from src.tests.api.lib.queries import (
    new_token, q_get, q_status, get_json, q_post,
)
from src.tests.api.lib.s_codes import SUCCESS
from src.tests.api.lib.url import (
    ORDERS_URL, ORDER_TYPES_URL, ORDER_C_F_URL, ORDER_STATUS_URL, CLIENT_URL
)
from src.tests.api.lib.schemas import (
    assert_response, ORDER_C_F_JSON, ORDER_TYPES_JSON, ORDER_JSON, make_load,
    unpack_count, unpack_data,
)

# This is the difference bettwen time in tests and server time
TIME_DIFFERENCE = 60000
MILISECONDS = 1000

def get_timestamp():
    return int(time() * MILISECONDS - TIME_DIFFERENCE)

UNIQUE = 1
ORDER_TYPE_ID = 10760
CLIENT_ID = 2141769
ORDER_TYPE = 'order_type'
BRAND = 'brand'
BRANCH = 'branch_id'
STATUS_ID = 27920
MANAGER = 'manager'
ENGINEER = 'engineer'
STATUS_DONE = 27924
STATUS_CLOSED = 27925


ORDER = {
    BRANCH : BRANCH_ID,
    'client_id' : CLIENT_ID,
    ORDER_TYPE : ORDER_TYPE_ID,
    BRAND : "brand_{0}".format(random_x()),
    'model' : "model_{0}".format(random_x()),
    'serial' : "serial_{0}".format(random_x()),
    'urgent' : 1,
    'estimated_cost' : 250.6,
    'appearance' : "regular stuff",
    'packagelist' : "empty package",
    'malfunction' : "badly injured",
    'assigned_at' : get_timestamp(),
    'estimated_done_at' : get_timestamp(),
    MANAGER : STUFF,
    ENGINEER : STUFF,
    'manager_notes' : "Simon said okay",
    'warranty_date' : get_timestamp(),
    'kindof_good' : "Pots and pans",
    'custom_fields' : '{\"122457\": \"new stuff\", \"121632\": \"the stuff\"}',
}

CLIENT = {
    'name' : "MR_{0}".format(random_x()),
    'phone[]' : format_phone_ua(make_phone_number()),
    'email' : make_email(),
    'address' : "Downing street, {0}".format(random_x()),
}

"""
done_at: array -
modified_at: array - Фильтр по дате изменения заказа;
closed_at: array
"""
def get_id(request):
    return unpack_data(request)['id']

def get_order_lable(request):
    return map(lambda i: i['id_label'], unpack_data(request))

def array(elem):
    return [elem]

def create_order(data):
    return  q_post(ORDERS_URL, make_load(data))

def change_order_status(order_id, status):
    data = {
            'order_id' : order_id,
            'status_id' : status,
        }

    return q_post(ORDER_STATUS_URL, make_load(data))


class ApiGetOrdersTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.orders = q_get(ORDERS_URL, new_token())
        cls.types = q_get(ORDER_TYPES_URL, new_token())
        cls.fields = q_get(ORDER_C_F_URL, new_token())

    def test_1_get_orders(self):
        return self.assertEqual(q_status(self.orders), SUCCESS)

    def test_2_check_order_answer(self):
        return assert_response(get_json(self.orders), ORDER_JSON)

    def test_3_get_order_types(self):
        return self.assertEqual(q_status(self.types), SUCCESS)

    def test_4_check_types_answer(self):
        return assert_response(get_json(self.types), ORDER_TYPES_JSON)

    def test_5_get_custom_fields(self):
        return self.assertEqual(q_status(self.fields), SUCCESS)

    def test_6_check_fileds_answer(self):
        return assert_response(get_json(self.fields), ORDER_C_F_JSON)


class ApiPostFilterOrdersTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.order_data = ORDER.copy()

    def test_1_create_order(self):
        new_order = create_order(self.order_data)
        return self.assertEqual(q_status(new_order), SUCCESS)

    def test_2_filter_order_types(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'types[]' : self.order_data[ORDER_TYPE]})
        )

        for item in unpack_data(orders):
            t_type = item[ORDER_TYPE]
            self.assertEqual(t_type['id'] , ORDER_TYPE_ID)

        return self.assertEqual(q_status(orders), SUCCESS)

    def test_3_filter_order_branches(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'branches[]' : self.order_data[BRANCH]})
        )

        map(
            lambda i: self.assertEqual(i[BRANCH], BRANCH_ID),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_4_filter_order_brands(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'brands[]' : self.order_data[BRAND]})
        )

        self.assertEqual(unpack_count(orders), UNIQUE)
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_5_filter_order_statuses(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'statuses[]' : STATUS_ID})
        )

        for item in unpack_data(orders):
            t_type = item['status']
            self.assertEqual(t_type['id'] , STATUS_ID)

        return self.assertEqual(q_status(orders), SUCCESS)

    def test_6_filter_order_managers(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'managers[]' : self.order_data[MANAGER]})
        )

        map(
            lambda i: self.assertEqual(i['manager_id'], STUFF),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_7_filter_order_engineers(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'engineers[]' : self.order_data[ENGINEER]})
        )

        map(
            lambda i: self.assertEqual(i['engineer_id'], STUFF),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)


class ApiFilterClientInOrderTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = q_post(CLIENT_URL, make_load(CLIENT.copy()))
        data = ORDER.copy()
        data['client_id'] = get_id(cls.client)
        cls.orders = create_order(data)

    def test_1_filter_order_client_name(self):
        orders = q_get(
            ORDERS_URL, make_load({'client_names[]' : CLIENT['name']}))

        for item in unpack_data(orders):
            t_type = item['client']
            self.assertEqual(t_type['name'] , CLIENT['name'])

        return self.assertEqual(q_status(orders), SUCCESS)

    def test_2_filter_order_client_phone(self):
        orders = q_get(
            ORDERS_URL, make_load({'client_phones[]' : CLIENT['phone[]']}))

        for item in unpack_data(orders):
            t_type = item['client']
            self.assertEqual(t_type['phone'] , array(CLIENT['phone[]']))

        return self.assertEqual(q_status(orders), SUCCESS)


class ApiChangeOrderStatusTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.new_order = create_order(ORDER.copy())

    def test_1_change_order_status(self):
        new_status = change_order_status(get_id(self.new_order), STATUS_DONE)
        return self.assertEqual(q_status(new_status), SUCCESS)

    def test_2_check_new_order_status(self):
        orders = q_get(
            ORDERS_URL, make_load({'ids[]' : get_id(self.new_order)})
        )

        for item in unpack_data(orders):
            t_type = item['status']
            self.assertEqual(t_type['id'] , STATUS_DONE)

        return self.assertEqual(q_status(orders), SUCCESS)


class ApiFilterOrderIdsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.order_data = ORDER.copy()
        cls.order = create_order(cls.order_data)

    def test_1_filter_order_id(self):
        order_id = get_id(self.order)
        orders = q_get(
            ORDERS_URL, make_load(
                {'ids[]' : order_id})
        )

        map(
            lambda i: self.assertEqual(i['id'], order_id),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_2_filter_order_label(self):
        orders = q_get(
            ORDERS_URL, make_load(
                {'ids[]' : get_id(self.order)})
        )
        lable = get_order_lable(orders)

        order_labels = q_get(
            ORDERS_URL, make_load(
                {'id_labels[]' : lable})
        )

        map(
            lambda i: self.assertEqual(array(i['id_label']), lable),
            unpack_data(order_labels),
        )
        return self.assertEqual(q_status(order_labels), SUCCESS)


class ApiFilterOrderTimeAttributes(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.order_data = ORDER.copy()
        cls.time = get_timestamp()

    def test_1_filter_order_created_at(self):
        create_order(self.order_data)

        orders = q_get(
            ORDERS_URL, make_load({'created_at[]' : self.time})
        )

        map(
            lambda i: self.assertTrue(i['created_at'] > self.time),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_2_filter_order_modified_at(self):
        create_order(self.order_data)

        orders = q_get(
            ORDERS_URL, make_load({'modified_at[]' : self.time})
        )

        map(
            lambda i: self.assertTrue(i['modified_at'] > self.time),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_3_filter_order_done_at(self):
        order = get_id(create_order(self.order_data))
        change_order_status(order, STATUS_DONE)

        orders = q_get(
            ORDERS_URL, make_load({'done_at[]' : self.time})
        )

        map(
            lambda i: self.assertTrue(i['done_at'] > self.time),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)

    def test_4_filter_order_closed_at(self):
        order = get_id(create_order(self.order_data))
        change_order_status(order, STATUS_CLOSED)

        orders = q_get(
            ORDERS_URL, make_load({'closed_at[]' : self.time})
        )

        map(
            lambda i: self.assertTrue(i['closed_at'] > self.time),
            unpack_data(orders),
        )
        return self.assertEqual(q_status(orders), SUCCESS)
