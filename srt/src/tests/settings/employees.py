# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.randomizer import make_login
from src.lib.dom import set_value, click_nth_node, make_selector
from src.lib.errors import assert_xpath_is_visible

from src.scaffolds.grid import test_grid_behaviour
from src.scaffolds.dialog import open_dialog, close_dialog

NEW_WORKER = {
    'name' : "Tuck",
    'lastname' : "Jackson",
    'password' : "test",
    'email' : "noemail@nodomain.com"
}
DELETE_WORKER = {
    'name' : "Aasper",
    'lastname' : "X-Ray",
    'password' : "test",
    'email' : "noemail@nodomain.com"
}

ADD_SEL = ".js-add-button"
EDIT_SEL = ".js-edit-button"
DELETE_SEL = ".js-remove-button"

SUBMIT_SEL = ".js-submit-dialog"

# Selector for the employee widget block
EMP_SEL = ".js-employee-widget"
EMP_TR = ".b-table__tr_mode_selectable"



def create_employee(driver, employee):
    open_dialog(driver, make_selector(EMP_SEL, ADD_SEL), "#l-e-name")

    login = make_login()
    set_value(driver, "#l-e-name", employee['name'])
    set_value(driver, "#l-e-lname", employee['lastname'])
    set_value(driver, "#l-e-login", login)
    set_value(driver, "#l-e-password", employee['password'])
    set_value(driver, "#l-e-email", employee['email'])

    close_dialog(
        driver, ".b-dialog .js-submit-dialog", ".b-dialog"
    )

    return assert_xpath_is_visible(
        driver, './/td[contains(text(),login)]'
    )



class CreateEmployeeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/settings/employee")

    def test_0_grid_behavior(self):
        return test_grid_behaviour(self.driver, EMP_SEL)

    def test_1_create_employee(self):
        return create_employee(self.driver, NEW_WORKER)


class DeleteEmployeeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/settings/employee")

    def test_1_delete_from_table(self):
        create_employee(self.driver, DELETE_WORKER)
        click_nth_node(self.driver, make_selector(EMP_SEL, EMP_TR))
        open_dialog(
            self.driver, make_selector(EMP_SEL, DELETE_SEL), \
            ".b-modal_type_remove_employee"
        )
        close_dialog(self.driver, ".js-submit", ".b-modal_type_remove_employee")
