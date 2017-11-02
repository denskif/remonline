# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, WORKERS_URL, ORDERS_URL
from src.lib.wait import wait_for_xpath
from src.lib.dom import find_element_by_selector
from src.lib.errors import assert_xpath_is_visible, assert_selector_is_visible
from src.lib.formatting import make_double_text_xpath, make_text_xpath

from src.scaffolds.dialog import open_dialog, close_dialog
from src.scaffolds.dropdown import choose_from_select
from src.scaffolds.grid import remove_item_from_grid

from src.tests.orders.lib.save_order import save_order
from src.tests.orders.lib.create_order import create_order
from src.tests.orders.lib.open import open_order, open_tab, TAB_INFO, TAB_WORKS

from src.tests.orders.spare_parts_and_works.lib.service import manual_add_new_srvc
from src.tests.orders.spare_parts_and_works.lib.part import manual_add_new_part
from src.tests.orders.spare_parts_and_works.lib.create import delete_str
from src.tests.orders.spare_parts_and_works.lib.data import data_f_worker

from src.tests.settings.lib.employee import add_worker


MSG = 'I am just an ordinary comment'
WORK = {
    'name': u'TL work',
    'quantity': u'1.0',
    'price': u'45.55',
}
PART = {
    'name': u'TL Part',
    'quantity': u'2',
    'cost': u'200',
    'price': u'400',
}

TECHNICIAN_IDX = 2
TIMELINE_TEXT_SEL = "@class, 'b-timeline__message'"
TIMELINE_WORKER_SEL = "@class, 'b-timeline__dsc'"


class TimelineComment(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()
        navigate(cls.driver, ORDERS_URL)

    def test_1_add_comment(self):
        create_order(self.driver)
        open_order(self.driver)

        open_dialog(self.driver, ".js-add-comment", ".js-submit-dialog")
        find_element_by_selector(self.driver, "#l-c-message").send_keys(MSG)
        close_dialog(self.driver, ".js-submit-dialog", ".js-submit-dialog")

        # Name the xpath for our comment
        comment = make_double_text_xpath("p", TIMELINE_TEXT_SEL, MSG)

        wait_for_xpath(self.driver, comment)
        return assert_xpath_is_visible(self.driver, comment)

    def test_2_add_url(self):
        open_dialog(self.driver, ".js-add-comment", ".js-submit-dialog")

        URL = self.driver.current_url
        find_element_by_selector(self.driver, "#l-c-message").send_keys(URL)
        close_dialog(self.driver, ".js-submit-dialog", ".js-submit-dialog")

        # Make sure comment was added and is visible

        url_comment = find_element_by_selector(
            self.driver, ".b-timeline__message [href]"
        ).text

        self.assertEqual(url_comment, URL)

        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True


# class TimelineAddFile(unittest.TestCase):

#     @classmethod
#     def setUp(cls):
#         cls.driver = get_driver()


#     def test_1_add_file(self):
#         create_order(self.driver)
#         open_order(self.driver)

#         file_name = "warehouse.xls"

#         add_file = self.driver.find_element_by_css_selector(".js-upload [name]")
#         add_file.send_keys(
#             "/home/max/Desktop/Orderry.com/Files\ for\ regression/" + file_name
#         )

#         uploaded_file = self.driver.find_element_by_xpath(
#             make_text_xpath("a", file_name)
#         )

#         wait_for_xpath(self.driver, uploaded_file, time=25)
#         return assert_xpath_is_visible(self.driver, file_name,)


class TimelineAddWorker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.worker = data_f_worker()
        navigate(cls.driver, WORKERS_URL)
        add_worker(cls.driver, cls.worker)
        navigate(cls.driver, ORDERS_URL)


    def tearDown(self):
        close_dialog(self.driver, ".js-close-dialog", ".b-order")

    def test_1_add_technician(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        find_element_by_selector(self.driver, ".js-engineer").click()
        manager = find_element_by_selector(
            self.driver, ".js-engineer option", idx=TECHNICIAN_IDX
        )
        tech_name = manager.text

        choose_from_select(self.driver, ".js-engineer", TECHNICIAN_IDX)

        save_order(self.driver)
        open_order(self.driver)

        event = make_double_text_xpath("p", TIMELINE_WORKER_SEL, tech_name)
        return assert_xpath_is_visible(self.driver, event)


    def test_2_add_manager(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_INFO)
        find_element_by_selector(self.driver, ".js-manager").click()
        manager = find_element_by_selector(
            self.driver, ".js-manager option", idx=TECHNICIAN_IDX
        )
        managers_name = manager.text

        choose_from_select(self.driver, ".js-manager", TECHNICIAN_IDX)

        save_order(self.driver)
        open_order(self.driver)

        event = make_double_text_xpath("p", TIMELINE_WORKER_SEL, managers_name)
        return assert_xpath_is_visible(self.driver, event)



class TimelineAddWork(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_1_add_work(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        manual_add_new_srvc(self.driver)

        save_order(self.driver)
        open_order(self.driver)

        assert_selector_is_visible(
            self.driver, ".js-timeline .i-wrench"
        )

        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True

    def test_2_delete_work(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        delete_str(self.driver)

        save_order(self.driver)
        open_order(self.driver)

        assert_selector_is_visible(
            self.driver, ".js-timeline .i-trash"
        )

        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True


class TimelineAddParts(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_1_add_part(self):
        create_order(self.driver)
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        manual_add_new_part(self.driver)

        save_order(self.driver)
        open_order(self.driver)

        assert_selector_is_visible(
            self.driver, ".js-timeline .i-settings"
        )

        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True

    def test_2_delete_part(self):
        open_order(self.driver)
        open_tab(self.driver, TAB_WORKS)
        delete_str(self.driver)

        save_order(self.driver)
        open_order(self.driver)

        assert_selector_is_visible(
            self.driver, ".js-timeline .i-trash"
        )

        close_dialog(self.driver, ".js-close-dialog", ".b-order")
        return True
