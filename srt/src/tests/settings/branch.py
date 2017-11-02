# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from src import settings

from src.widget.color_picker import change_color

from src.scaffolds.grid import wait_grid_changed_rows_num, test_grid_behaviour
from src.scaffolds.dialog import open_dialog, close_dialog

from src.lib.dom import (
    find_displayed, find_element_by_selector, get_value, click_nth_node
)
from src.lib.url import navigate
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear, wait_to_click_selector,
    wait_condition, wait_to_see_selector
)
from src.lib.driver import get_driver
from src.lib.errors import assert_has_error_tooltip
from src.lib.randomizer import random_x


ADD_SEL = ".js-add-button"
EDIT_SEL = ".js-edit-button"
DELETE_SEL = ".js-remove-button"

SUBMIT_SEL = ".js-submit-dialog"
FIRST_ROW_IDX = 1

CREATE_BRANCH_DATA = {
    u'#l-b-name': u"First location {0}".format(random_x()),
    u'#l-b-address': u"1 Main Road, Arctic Circle",
}

UPDATE_BRANCH_DATA = {
    u'#l-b-name': u"Second location {0}".format(random_x()),
    u'#l-b-address': u"2 Main Road, Antarctic Circle",
}


def create_branch(driver, data):
    open_dialog(driver, ADD_SEL, "#l-b-name")

    color_idx = 2
    name = data['#l-b-name']

    for sel, value in data.iteritems():
        find_element_by_selector(driver, sel).send_keys(value)

    change_color(driver, ".b-dialog", idx=color_idx)
    find_element_by_selector(driver, SUBMIT_SEL).click()
    wait_grid_changed_rows_num(driver, ".b-table__tr")

    def _branch_appear(driver):
        displayed = find_displayed(
            driver.find_elements_by_css_selector(".js-grid .b-table__td"),
        )

        return len(filter(
            lambda element: name in element.text, displayed,
        )) == 1

    return wait_condition(driver, _branch_appear)

def delete_branch(driver):

    wait_for_selector(driver, ".js-grid .b-table__tr")
    click_nth_node(driver, ".js-grid .b-table__tr", FIRST_ROW_IDX)

    # Click on the delete button.
    find_element_by_selector(driver, DELETE_SEL).click()

    # Confirm delete.
    wait_to_click_selector(driver, ".b-modal_type_confirm .js-submit")
    find_element_by_selector(driver, ".b-modal_type_confirm .js-submit").click()
    wait_grid_changed_rows_num(driver, ".b-table__tr")

    return wait_selector_to_disappear(driver, ".reveal-modal-bg")


class CreateBranchTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/settings/branch")

    def test_1_dialog_behaviour(self):
        return test_grid_behaviour(self.driver, ".js-branch-widget")

    def test_2_invalid_data(self):
        open_dialog(self.driver, ADD_SEL, "#l-b-name")
        submit_node = find_element_by_selector(self.driver, SUBMIT_SEL)

        data = {
            u'#l-b-name': ["", "\t", "\n", " ", "    "],
        }

        for sel, values in data.iteritems():
            dom_node = find_element_by_selector(self.driver, sel)

            for value in values:
                dom_node.send_keys(value)
                submit_node.click()
                dom_node.clear()

                assert_has_error_tooltip(self.driver, dom_node)

        close_dialog(self.driver, ".h-dialog-mask", "#l-b-name")
        return True

    def test_3_create_branch(self):
        return create_branch(self.driver, CREATE_BRANCH_DATA)


class EditBranchTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/settings/branch")


    def test_1_update_branch(self):
        old_values = []

        # Wait until the grid is loaded.

        wait_to_see_selector(self.driver, ".js-grid .b-table__tr")
        click_nth_node(self.driver, ".js-grid .b-table__tr", FIRST_ROW_IDX)

        find_element_by_selector(self.driver, EDIT_SEL).click()
        wait_for_selector(self.driver, ".b-dialog #l-b-name")

        for sel, value in UPDATE_BRANCH_DATA.iteritems():
            element = find_element_by_selector(self.driver, sel)
            old_values.append(get_value(element))
            element.clear()
            element.send_keys(value)

        find_element_by_selector(self.driver, SUBMIT_SEL).click()
        wait_selector_to_disappear(self.driver, ".b-dialog")

        def _branch_updated(driver):
            # Old values should disappear from the table.
            texts = map(lambda element: element.text, find_displayed(
                driver.find_elements_by_css_selector(".js-grid .b-table__td"),
            ))

            return 0 == len(filter(
                lambda value: value in texts, old_values,
            ))

        return wait_condition(self.driver, _branch_updated)


class DeleteBranchTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, "/app#!/settings/branch")


    # Delete company branch from the grid.
    def test_1_delete_branch(self):
        return delete_branch(self.driver)

    # Delete company branch from edit dialog.
    def test_2_delete_branch(self):
        create_branch(self.driver, CREATE_BRANCH_DATA)

        # wait_to_click_selector(self.driver, ".js-grid tbody tr")
        click_nth_node(self.driver, ".js-grid .b-table__tr", FIRST_ROW_IDX)

        # Click on the edit button.
        find_element_by_selector(self.driver, EDIT_SEL).click()

        wait_for_selector(self.driver, ".b-dialog .h-trash-button")
        find_element_by_selector(
            self.driver, ".b-dialog .h-trash-button",
        ).click()

        # Confirm delete.
        wait_to_click_selector(self.driver, ".b-modal_type_confirm .js-submit")
        find_element_by_selector(
            self.driver, ".b-modal_type_confirm .js-submit",
        ).click()

        return True
