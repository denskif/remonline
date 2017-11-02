# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, ORDERS_URL, WORKERS_URL
from src.lib.dom import find_element_by_selector, get_value
from src.lib.wait import (
    wait_for_selector, wait_selector_to_disappear ,wait_to_click_selector
)
from src.lib.errors import assert_selector_is_visible, assert_xpath_is_visible

from src.scaffolds.dropdown import choose_from_select, switch_location
from src.scaffolds.dialog import *
from src.scaffolds.mass_edit import test_mass_edit

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import  open_order, open_tab, TAB_INFO
from src.tests.orders.spare_parts_and_works.lib.data import data_f_worker

from src.tests.settings.lib.employee import add_worker


MASS_EDIT_MENU = ".b-modal_type_confirm"
MENU_STRING = ".js-action"
MAIN_CHECKBOX_SEL = ".k-grid-header .h-checkbox"
MAIN_SELECTED_SEL = ".js-selected-h"
ALL_CHECKBOXES_SEL = ".js-selected"
MASS_EDIT_BTN = ".b-mass .b-btn"
DEL_IDX = -1
TECH_IDX = -2


class MassEditChooseOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_check_mass_edit(self):
        test_mass_edit(self.driver)


class MassEditTransferOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_1_transfer_order(self):
        create_order(self.driver)
        find_element_by_selector(
            self.driver, ".k-grid-content .h-checkbox"
        ).click()

        order_id = self.driver.find_element_by_css_selector(
            "[data-order-id]"
        ).get_attribute("data-order-id")

        wait_to_click_selector(self.driver, MASS_EDIT_BTN)

        find_element_by_selector(
            self.driver, MASS_EDIT_BTN
        ).click()

        Transfer_btn_idx = 3

        open_dialog(
            self.driver, MENU_STRING, MASS_EDIT_MENU, Transfer_btn_idx
        )

        LOCATION_IDX = 0
        choose_from_select(self.driver, ".js-branch", LOCATION_IDX)
        close_dialog(self.driver, ".js-submit", ".reveal-modal-bg")
        switch_location(self.driver, LOCATION_IDX)

        id_of_removed_order = self.driver.find_element_by_css_selector(
            "[data-order-id]"
        ).get_attribute("data-order-id")

        return self.assertTrue(order_id == id_of_removed_order)


class MassEditDeleteOrderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_1_delete_order(self):
        create_order(self.driver)

        find_element_by_selector(
            self.driver, ".k-grid-content .h-checkbox"
        ).click()

        remove_order_id = self.driver.find_element_by_css_selector(
            "[data-order-id]"
        ).get_attribute("data-order-id")

        wait_to_click_selector(self.driver, MASS_EDIT_BTN)

        find_element_by_selector(
            self.driver, MASS_EDIT_BTN
        ).click()

        open_dialog(
            self.driver, "[data-action-key]", MASS_EDIT_MENU, DEL_IDX
        )

        confirm_delete(self.driver)

        new_first_order_id = self.driver.find_element_by_css_selector(
            "[data-order-id]"
        ).get_attribute("data-order-id")

        return self.assertNotEqual(remove_order_id, new_first_order_id)


class MassEditAssignWorkerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.worker = data_f_worker()
        navigate(cls.driver, WORKERS_URL)
        add_worker(cls.driver, cls.worker)
        navigate(cls.driver, ORDERS_URL)

    def tearDown(self):
        close_dialog(self.driver, ".js-close-dialog", ".b-order")

    """
       Function temporarily disabled
    """
    # def test_1_assign_manager(self):
    #     create_order(self.driver)
    #     find_element_by_selector(
    #         self.driver, ".k-grid-content .h-checkbox"
    #     ).click()

    #     wait_to_click_selector(self.driver, MASS_EDIT_BTN)

    #     find_element_by_selector(
    #         self.driver, MASS_EDIT_BTN
    #     ).click()

    #     open_dialog(
    #         self.driver, "[data-action-key=change-manager]", MASS_EDIT_MENU
    #     )

    #     MANAGER_IDX = 1
    #     choose_from_select(self.driver, ".js-employee", MANAGER_IDX)
    #     manager = get_value(
    #         find_element_by_selector(
    #             self.driver, ".js-employee option", MANAGER_IDX
    #         )
    #     )

    #     close_dialog(self.driver, ".js-submit", ".b-modal_type_confirm .js-submit")
    #     open_order(self.driver)
    #     open_tab(self.driver, TAB_INFO)
    #     changed_manager = get_value(
    #         find_element_by_selector(self.driver, ".t-manager")
    #     )

    #     return self.assertEqual(manager, changed_manager)


    def test_2_assign_engineer(self):
        create_order(self.driver)
        find_element_by_selector(
            self.driver, ".k-grid-content .h-checkbox"
        ).click()

        wait_to_click_selector(self.driver, MASS_EDIT_BTN)

        find_element_by_selector(
            self.driver, MASS_EDIT_BTN
        ).click()

        open_dialog(
            self.driver, "[data-action-key]", MASS_EDIT_MENU, TECH_IDX
        )

        ENGINEER_IDX = 1
        choose_from_select(self.driver, ".js-employee", ENGINEER_IDX)
        engineer = get_value(
            find_element_by_selector(
                self.driver, ".js-employee option", ENGINEER_IDX
            )
        )

        close_dialog(self.driver, ".js-submit", ".b-modal_type_confirm .js-submit")
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        changed_engineer = get_value(
            find_element_by_selector(self.driver, ".js-engineer")
        )

        return self.assertEqual(engineer, changed_engineer)


class MassEditDialogTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_1_mass_edit_close_dialog(self):
        # Close dialog by "Close" button
        create_order(self.driver)
        find_element_by_selector(
            self.driver, ".k-grid-content .h-checkbox"
        ).click()

        wait_to_click_selector(self.driver, MASS_EDIT_BTN)

        find_element_by_selector(
            self.driver, MASS_EDIT_BTN
        ).click()
        actions = self.driver.find_elements_by_css_selector(MENU_STRING)

        # First element - invoice, openes ticket dialog - skiping this case
        # Starting checks from second element in the list
        for action in actions[1:]:
            action.click()
            wait_for_selector(self.driver, MASS_EDIT_MENU)
            close_dialog(
                self.driver, ".js-close", MASS_EDIT_MENU
            )
            find_element_by_selector(
                self.driver, MASS_EDIT_BTN
            ).click()
        return True

    def test_2_mass_edit_close_dialog(self):
        # Close dialog by "x" button
        create_order(self.driver)
        find_element_by_selector(
            self.driver, ".k-grid-content .h-checkbox"
        ).click()

        wait_to_click_selector(self.driver, MASS_EDIT_BTN)

        find_element_by_selector(
            self.driver, ".b-mass .b-btn"
        ).click()
        actions = self.driver.find_elements_by_css_selector(MENU_STRING)

        # First element - invoice, openes ticket dialog - skiping this case
        # Starting checks from second element in the list
        for action in actions[1:]:
            action.click()
            wait_for_selector(self.driver, MASS_EDIT_MENU)
            close_dialog(
                self.driver, ".b-modal__close", MASS_EDIT_MENU
            )
            find_element_by_selector(
                self.driver, MASS_EDIT_BTN
            ).click()
        return True

    @classmethod
    def tearDownClass(cls):
        find_element_by_selector(cls.driver, ".b-mass__close").click()
        wait_selector_to_disappear(
            cls.driver, ".b-mass .js-mass-text"
        )
