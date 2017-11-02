# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, CLIENT_URL
from src.lib.dom import find_element_by_selector, get_value
from src.lib.wait import wait_selector_to_disappear, wait_to_see_selector

from src.scaffolds.dialog import confirm_delete
from src.scaffolds.mass_edit import test_mass_edit

from src.tests.clients.lib import CLIENT_ID_SEL_N, CLIENT_ID_SEL
from src.tests.clients.lib.client import create_client


CLIENT_TO_REMOVE = {
    'name' : "Porky Svyn",
    'phone' : '1111111111',
    'email' : "porky@svuniaky.com",
    'address' : "Koryto 35",
    'note' : "stutter and spluter",
}
TRASH_BTN = ".h-trash-button"
MASS_EDIT_BTN = ".b-mass .b-btn"
MASS_DELETE_SEL = ".b-mass [data-action-key]"
MASS_DELETE_SEL_IDX = 1


class MassDeleteClientTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, CLIENT_URL)

    def test_1_mass_edit_diagnostic(self):
        return test_mass_edit(self.driver)

    def test_remove_client(self):
        create_client(self.driver)

        find_element_by_selector(self.driver, "tbody .h-checkbox").click()
        client_id = find_element_by_selector(
            self.driver, CLIENT_ID_SEL
        ).get_attribute(CLIENT_ID_SEL)

        wait_to_see_selector(self.driver, MASS_EDIT_BTN)
        find_element_by_selector(self.driver, MASS_EDIT_BTN).click()
        find_element_by_selector(
            self.driver, MASS_DELETE_SEL, MASS_DELETE_SEL_IDX
        ).click()
        confirm_delete(self.driver)

        return wait_selector_to_disappear(
            self.driver, CLIENT_ID_SEL_N.format(client_id)
        )
