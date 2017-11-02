# ~*~ coding: utf-8 ~*~

from unittest import TestCase

from src.scaffolds.dropdown import choose_from_select

from src.lib.dom import find_element_by_selector, get_value, is_select
from src.lib.url import navigate
from src.lib.wait import (
    wait_to_click_selector, wait_for_selector, wait_selector_to_disappear
)
from src.lib.notify import wait_notify_worked
from src.lib.driver import get_driver, refresh
from src.lib.randomizer import random_x, random_int, make_email


URL = "/app#!/settings/general"


def click_on_save(driver):
    wait_to_click_selector(driver, "button.btn-primary")
    wait_selector_to_disappear(driver, ".reveal-modal-bg")
    return find_element_by_selector(driver, "button.btn-primary").click()

def save_form(driver):
    click_on_save(driver)
    return wait_notify_worked(driver)

def change_value(driver, selector, value=None):
    node = find_element_by_selector(driver, selector)
    new_value = value or u"New value {0}".format(random_x())
    old_value = get_value(node)

    # Various methods to set value.
    if is_select(node):
        choose_from_select(driver, selector)
    else:
        node.clear()
        node.send_keys(new_value)

    return old_value

def mass_set_values(driver):
    return [
        change_value(driver, "#l-settings-name"),
        change_value(driver, "#l-settings-address"),
        change_value(driver, "#l-settings-email", value=make_email()),
        change_value(driver, "#js-settings-country"),
        change_value(driver, "#l-settings-currency"),
        change_value(driver, "#l-settings-language"),
    ]

def mass_get_values(driver):
    return [
        get_value(find_element_by_selector(driver, "#l-settings-name")),
        get_value(find_element_by_selector(driver, "#l-settings-address")),
        get_value(find_element_by_selector(driver, "#l-settings-email")),
        get_value(find_element_by_selector(driver, "#js-settings-country")),
        get_value(find_element_by_selector(driver, "#l-settings-currency")),
        get_value(find_element_by_selector(driver, "#l-settings-language")),
    ]


class SaveGeneralSettingsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        navigate(cls.driver, URL)

    def test_1_save_any(self):
        return save_form(self.driver)

    def test_2_change_form_values(self):
        old_values = mass_set_values(self.driver)
        save_form(self.driver)

        # Do not reload page, we must to be shure that state is working properly.
        navigate(self.driver, "/app")
        navigate(self.driver, URL)
        wait_for_selector(self.driver, "#l-settings-name")

        new_values = mass_get_values(self.driver)
        map(lambda args: self.assertNotEqual(*args), zip(old_values, new_values))

        # Check if data saved to the DB after reloading the page.
        refresh()
        wait_for_selector(self.driver, "#l-settings-name")

        new_values = mass_get_values(self.driver)
        map(lambda args: self.assertNotEqual(*args), zip(old_values, new_values))
