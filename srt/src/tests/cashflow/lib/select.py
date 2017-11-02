# ~*~ coding: utf-8 ~*~


from src.lib.formatting import make_double_text_xpath
from src.lib.dom import find_element_by_xpath, get_value, find_element_by_selector
from src.lib.wait import wait_to_see_selector

from src.tests.cashflow.lib import ACTIVE_BOX_SEL


def select_cashbox_by_name(driver, box_name):
    wait_to_see_selector(driver, ".js-cashboxes-list")

    box_path = make_double_text_xpath(
            "p", "@class, 'b-cashbox__name'", box_name
        )

    cashbox_name = find_element_by_xpath(driver, box_path)

    cashbox_form = cashbox_name.find_element_by_xpath("..")
    cashbox_form.click()

    active_class = cashbox_form.find_element_by_xpath("..").get_attribute('class')

    return ACTIVE_BOX_SEL in active_class


def select_cashbox(driver, any_cashbox_sel):
    wait_to_see_selector(driver, ".js-cashboxes-list")

    cashbox_form = any_cashbox_sel.find_element_by_xpath("..")
    cashbox_form.click()

    active_class = cashbox_form.find_element_by_xpath("..").get_attribute('class')

    return ACTIVE_BOX_SEL in active_class
