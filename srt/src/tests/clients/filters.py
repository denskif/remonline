# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CLIENT_URL
from src.lib.randomizer import make_phone_number
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_selector_to_disappear

from src.scaffolds.search import search_for, reset_search

from src.tests.clients.lib.client import create_client
from src.tests.clients.lib.filter import (
    filter_all_clients, filter_all_legals, filter_customers, filter_suppliers,
    filter_naturals, filter_legal_entities,
)


CUSTOMER = {
    'name' : "Mr Easy Customer",
    'phone' : make_phone_number(),
    'email' : "easy@nodomain.us",
    'address' : "buy 67",

}
SUPPLIER = {
    'name' : "Mr Best Supplies",
    'phone' : make_phone_number(),
    'email' : "suppy@nodomain.us",
    'address' : "supply 68",
    'supplier' : True,
}
NATURAL_E = {
    'name' : "Mr Natural Entity",
    'phone' : make_phone_number(),
    'email' : "easy@nodomain.us",
    'address' : "buy 67",
    'legal' : False,
}
LEGAL_E = {
    'name' : "Mr Legal Entity",
    'phone' : make_phone_number(),
    'email' : "suppy@nodomain.us",
    'address' : "supply 68",
    'legal' : True,
}
CLIENT_ID_SEL = "[data-client-id]"


class FilterClientTypesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_create_client_types(self):
        create_client(self.driver, CUSTOMER)
        create_client(self.driver, SUPPLIER)
        return True

    def test_2_filter_all(self):
        filter_all_clients(self.driver)
        client_list = [CUSTOMER['name'], SUPPLIER['name']]

        for client in client_list:
            search_for(self.driver, client)
            found_client = find_element_by_selector(
                self.driver, CLIENT_ID_SEL
            ).text
            self.assertEqual(found_client, client)
            reset_search(self.driver)
        return True

    def test_2_filter_suppliers(self):
        filter_suppliers(self.driver)
        supplier = SUPPLIER['name']
        customer = CUSTOMER['name']

        search_for(self.driver, supplier)
        found_client = find_element_by_selector(
            self.driver, CLIENT_ID_SEL
        ).text
        self.assertEqual(found_client, supplier)
        reset_search(self.driver)

        search_for(self.driver, customer)
        wait_selector_to_disappear(self.driver, CLIENT_ID_SEL)
        reset_search(self.driver)
        return True

    def test_3_filter_customers(self):
        filter_customers(self.driver)
        supplier = SUPPLIER['name']
        customer = CUSTOMER['name']

        search_for(self.driver, customer)
        found_client = find_element_by_selector(
            self.driver, CLIENT_ID_SEL
        ).text
        self.assertEqual(found_client, customer)
        reset_search(self.driver)

        search_for(self.driver, supplier)
        wait_selector_to_disappear(self.driver, CLIENT_ID_SEL)
        reset_search(self.driver)
        return True

    @classmethod
    def tearDownClass(cls):
        filter_all_clients(cls.driver)


class FilterClientKindsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_create_client_types(self):
        create_client(self.driver, NATURAL_E)
        create_client(self.driver, LEGAL_E)
        return True

    def test_2_filter_all(self):
        filter_all_legals(self.driver)
        client_list = [NATURAL_E['name'], LEGAL_E['name']]

        for client in client_list:
            search_for(self.driver, client)
            found_client = find_element_by_selector(
                self.driver, CLIENT_ID_SEL
            ).text
            self.assertEqual(found_client, client)
            reset_search(self.driver)
        return True

    def test_2_filter_naturals(self):
        filter_naturals(self.driver)
        natural = NATURAL_E['name']
        legal = LEGAL_E['name']

        search_for(self.driver, natural)
        found_client = find_element_by_selector(
            self.driver, CLIENT_ID_SEL
        ).text
        self.assertEqual(found_client, natural)
        reset_search(self.driver)

        search_for(self.driver, legal)
        wait_selector_to_disappear(self.driver, CLIENT_ID_SEL)
        reset_search(self.driver)
        return True

    def test_3_filter_legals(self):
        filter_legal_entities(self.driver)
        natural = NATURAL_E['name']
        legal = LEGAL_E['name']

        search_for(self.driver, legal)
        found_client = find_element_by_selector(
            self.driver, CLIENT_ID_SEL
        ).text
        self.assertEqual(found_client, legal)
        reset_search(self.driver)

        search_for(self.driver, natural)
        wait_selector_to_disappear(self.driver, CLIENT_ID_SEL)
        reset_search(self.driver)
        return True

    @classmethod
    def tearDownClass(cls):
        filter_all_legals(cls.driver)
