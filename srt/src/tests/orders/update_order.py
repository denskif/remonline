# ~*~ coding: utf-8 ~*~

import unittest
import time

from selenium.webdriver.support.select import Select

from src.lib.driver import get_driver
from src.lib.dom import (
    find_element_by_selector, find_element_by_xpath, set_value, get_value,
    make_selector
)
from src.lib.errors import assert_xpath_is_visible, assert_selector_is_visible
from src.lib.url import navigate, BOOK_URL, WORKERS_URL, ORDERS_URL
from src.lib.wait import wait_for_selector

from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, TAB_INFO, TAB_WORKS
from src.tests.orders.lib.delete import delete_order
from src.tests.orders.lib.save_order import save_order
from src.tests.orders.spare_parts_and_works.lib.data import data_f_worker

from src.tests.settings.lib.employee import add_worker

from src.scaffolds.dropdown import choose_from_select, test_caret, autocomplete_add
from src.scaffolds.dialog import close_dialog, open_dialog

EDIT_ORDER_DATA = {
    'brand' : u"famous brand",
    'model' : u"mega device",
    'manager_notes' : u"Device is not looking good",
    'will_cost' : u"1200",
    'tech_notes' : u"Fixed in the very best way",
    'resume' : u"Next time just buy new one",
}
IMEI_DATA = {
    'imei' : u"013206002391108",
    'brand' : u"Apple",
    'model' : u"iPhone 4S",
    'malfunction' : u"This one is surely broken",
}
DEVICE_DATA = [
    ['type', u'smartphone'],
    ['brand', u'Sony'],
    ['model', u'Super S'],
    ['malfunction', u'Blocked as hell'],
    ['appearence', u'too much pink'],
    ['package', u'phone case and sim'],
]
# data for autocomplete tests
DATA_AC_TEST = {
    'type' : u"mega-phone",
    'brand' : u"T-Rex",
    'model' : u"TT-34",
    'malfunction' : u"The very serious problems with device",
    'package' : u"mini camera",
}

ORDER_TYPE = 1
NOT_ASSIGNED_IDX = 0
MANAGER_SEL = ".js-manager"
ENGINEER_SEL = ".js-engineer"
MANAGER_IDX = 2  # "Not Assigned" = 0
TECHNICIAN_IDX = 2 # "Not Assigned" = 0


class EditOrderType(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    @classmethod
    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_change_order_type(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        old_type = get_value(
            find_element_by_selector(self.driver, ".js-change-order-type")
        )
        choose_from_select(self.driver, ".js-change-order-type", ORDER_TYPE)
        new_type = get_value(
            find_element_by_selector(self.driver, ".js-change-order-type")
        )
        return self.assertNotEqual(old_type, new_type)

    def test_2_edit_order_type(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        choose_from_select(self.driver, ".js-change-order-type", ORDER_TYPE)
        new_type = get_value(find_element_by_selector(
            self.driver, ".js-change-order-type option", ORDER_TYPE
        ))

        save_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        order_type = get_value(
            find_element_by_selector(self.driver, ".js-change-order-type")
        )
        return self.assertEqual(new_type, order_type)


class EditUrgentOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_urgent_checkbox(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        find_element_by_selector(
            self.driver, "label[for=l-o-urgent]", idx=1
        ).click()
        save_order(self.driver)

        return assert_selector_is_visible(self.driver, ".i-fire")


class EditInfoAndWorks(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    @classmethod
    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_additional_info(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        set_value(
            self.driver, "#js-o-manager_notes", EDIT_ORDER_DATA['manager_notes']
        )
        set_value(self.driver, "#l-o-will_cost", EDIT_ORDER_DATA['will_cost'])
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        manager_notes = get_value(
            find_element_by_selector(self.driver, "#js-o-manager_notes")
        )
        will_cost = get_value(
            find_element_by_selector(self.driver, "#l-o-will_cost")
        )
        self.assertEqual(manager_notes, EDIT_ORDER_DATA['manager_notes'])
        return self.assertEqual(will_cost, EDIT_ORDER_DATA['will_cost'])

    def test_2_edit_works_materials(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        set_value(self.driver, ".js-eng-notes", EDIT_ORDER_DATA['tech_notes'])
        set_value(self.driver, ".js-resume", EDIT_ORDER_DATA['resume'])

        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)

        tech_notes = get_value(find_element_by_selector(self.driver, ".js-eng-notes"))
        resume = get_value(find_element_by_selector(self.driver, ".js-resume"))

        self.assertEqual(tech_notes, EDIT_ORDER_DATA['tech_notes'])
        return self.assertEqual(resume, EDIT_ORDER_DATA['resume'])


class EditDeviceAndMalfunctions(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    @classmethod
    def tearDown(cls):
        close_dialog(cls.driver, ".js-close-dialog", ".b-order")

    def test_1_device_and_malfunctions(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        device = [value[1] for value in DEVICE_DATA]

        set_value(self.driver, "#js-o-kindof_good", device[0])
        set_value(self.driver, "#js-o-brand", device[1])
        set_value(self.driver, "#js-o-model", device[2])
        set_value(self.driver, "#js-o-malfunction", device[3])
        set_value(self.driver, "#js-o-appearance", device[4])
        set_value(self.driver, "#js-o-packagelist", device[5])
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        new_device = [
            get_value(find_element_by_selector(self.driver, "#js-o-kindof_good")),
            get_value(find_element_by_selector(self.driver, "#js-o-brand")),
            get_value(find_element_by_selector(self.driver, "#js-o-model")),
            get_value(find_element_by_selector(self.driver, "#js-o-malfunction")),
            get_value(find_element_by_selector(self.driver, "#js-o-appearance")),
            get_value(find_element_by_selector(self.driver, "#js-o-packagelist")),
        ]

        return map(lambda args: self.assertEqual(*args), zip(new_device, device))

    def test_2_imei_autocomplete(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        find_element_by_selector(self.driver, "#js-o-brand").clear()
        find_element_by_selector(self.driver, "#js-o-model").clear()

        set_value(self.driver, "#js-o-serial", IMEI_DATA['imei'])
        set_value(self.driver, "#js-o-malfunction", IMEI_DATA['malfunction'])
        save_order(self.driver)

        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        serial = get_value(find_element_by_selector(self.driver, "#js-o-serial"))
        brand = get_value(find_element_by_selector(self.driver, "#js-o-brand"))
        model = get_value(find_element_by_selector(self.driver, "#js-o-model"))

        self.assertEqual(serial, IMEI_DATA['imei'])
        self.assertEqual(brand, IMEI_DATA['brand'])
        return self.assertEqual(model, IMEI_DATA['model'])


class EditManagerAndTech(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.worker = data_f_worker()
        navigate(cls.driver, WORKERS_URL)
        add_worker(cls.driver, cls.worker)
        navigate(cls.driver, ORDERS_URL)

    def tearDown(self):
        close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_1_manager_changes(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        old_manager = get_value(
            find_element_by_selector(self.driver, MANAGER_SEL)
        )
        choose_from_select(self.driver, MANAGER_SEL, NOT_ASSIGNED_IDX)
        new_manager = get_value(
            find_element_by_selector(self.driver, MANAGER_SEL)
        )
        return self.assertNotEqual(old_manager, new_manager)

    def test_2_technician_changes(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        old_technician = get_value(
            find_element_by_selector(self.driver, ENGINEER_SEL)
        )
        choose_from_select(self.driver, ENGINEER_SEL, TECHNICIAN_IDX)
        new_technician = get_value(
            find_element_by_selector(self.driver, ENGINEER_SEL)
        )
        return self.assertNotEqual(old_technician, new_technician)

    def test_3_edit_manager(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        choose_from_select(self.driver, MANAGER_SEL, MANAGER_IDX)
        new_manager = get_value(find_element_by_selector(
            self.driver, make_selector(MANAGER_SEL, "option"), MANAGER_IDX
        ))

        save_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        assigned = get_value(
            find_element_by_selector(self.driver, MANAGER_SEL)
        )
        return self.assertEqual(new_manager, assigned)

    def test_4_edit_technician(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        choose_from_select(self.driver, ENGINEER_SEL, TECHNICIAN_IDX)
        new_engineer = get_value(find_element_by_selector(
            self.driver, make_selector(ENGINEER_SEL, "option"), TECHNICIAN_IDX
        ))

        save_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        assigned = get_value(
            find_element_by_selector(self.driver, ENGINEER_SEL)
        )
        return self.assertEqual(new_engineer, assigned)


class EditOrderAutocomplete(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_preconditions(self):
        navigate(self.driver, BOOK_URL)

        time.sleep(1)
        wait_for_selector(self.driver, ".js-kinds-widget")
        open_dialog(
            self.driver, ".js-kinds-widget .js-add-button", "#l-kinds-title"
        )
        set_value(self.driver, "#l-kinds-title", DATA_AC_TEST['type'])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        open_dialog(
            self.driver, ".js-brand-widget .js-add-button", "#l-brand-title"
        )
        set_value(self.driver, "#l-brand-title", DATA_AC_TEST['brand'])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        open_dialog(
            self.driver, ".js-model-widget .js-add-button", "#l-model-title"
        )
        set_value(self.driver, "#l-model-title", DATA_AC_TEST['model'])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        open_dialog(
            self.driver, ".js-malfunction-widget .js-add-button", "#l-margin-title"
        )
        set_value(self.driver, "#l-margin-title", DATA_AC_TEST['malfunction'])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")

        open_dialog(
            self.driver, ".js-packagelist-widget .js-add-button", "#l-packagelist-title"
        )
        set_value(self.driver, "#l-packagelist-title", DATA_AC_TEST['package'])
        close_dialog(self.driver, ".js-submit-dialog", ".b-dialog")
        return navigate(self.driver, "/app#!/orders")

    def test_1_device_type(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        test_caret(self.driver, "[data-opts-relate=js-o-kindof_good]")
        autocomplete_add(self.driver, self, "#js-o-kindof_good", DATA_AC_TEST['type'])

        device_type = get_value(
            find_element_by_selector(self.driver, "#js-o-kindof_good")
        )

        self.assertEqual(device_type, DATA_AC_TEST['type'])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_2_device_brand(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        test_caret(self.driver, "[data-opts-relate=js-o-brand]")
        autocomplete_add(self.driver, self, "#js-o-brand", DATA_AC_TEST['brand'])

        device_brand = get_value(
            find_element_by_selector(self.driver, "#js-o-brand")
        )

        self.assertEqual(device_brand, DATA_AC_TEST['brand'])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_3_device_model(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        test_caret(self.driver, "[data-opts-relate=js-o-model]")
        autocomplete_add(self.driver, self, "#js-o-model", DATA_AC_TEST['model'])

        device_model = get_value(
            find_element_by_selector(self.driver, "#js-o-model")
        )

        self.assertEqual(device_model, DATA_AC_TEST['model'])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_4_device_malfunction(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        test_caret(self.driver, "[data-opts-relate=js-o-malfunction]")
        autocomplete_add(
            self.driver, self, "#js-o-malfunction", DATA_AC_TEST['malfunction']
        )

        device_malfunction = get_value(
            find_element_by_selector(self.driver, "#js-o-malfunction")
        )

        self.assertEqual(device_malfunction, DATA_AC_TEST['malfunction'])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_5_device_package(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)

        test_caret(self.driver, "[data-opts-relate=js-o-packagelist]")
        autocomplete_add(
            self.driver, self, "#js-o-packagelist", DATA_AC_TEST['package']
        )

        device_package = get_value(
            find_element_by_selector(self.driver, "#js-o-packagelist")
        )

        self.assertEqual(device_package, DATA_AC_TEST['package'])
        return close_dialog(self.driver, ".js-close-dialog", ".b-order")
