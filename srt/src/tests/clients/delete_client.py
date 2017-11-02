# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CLIENT_URL
from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_selector_to_disappear

from src.scaffolds.dialog import confirm_delete
from src.scaffolds.search import reset_search

from src.tests.clients.lib import CLIENT_ID_SEL
from src.tests.clients.lib.client import (
    create_client, find_open_client, open_client
)


CLIENT_TO_REMOVE = {
    'name' : "Porky Svyn",
    'phone' : '1111111111',
    'email' : "porky@svuniaky.com",
    'address' : "Koryto 35",
    'note' : "stutter and spluter",
}
TRASH_BTN = ".h-trash-button"

class RemoveClientTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_remove_client(self):
        create_client(self.driver, CLIENT_TO_REMOVE)

        find_open_client(self.driver, CLIENT_TO_REMOVE['name'])
        find_element_by_selector(self.driver, TRASH_BTN).click()
        confirm_delete(self.driver)

        return wait_selector_to_disappear(self.driver, CLIENT_ID_SEL)

    @classmethod
    def tearDown(cls):
        reset_search(cls.driver)
