# ~*~ coding: utf-8 ~*~

import time

from selenium.common.exceptions import WebDriverException

from src.lib.wait import (
    wait_for_xpath, wait_condition, wait_selector_to_disappear, wait_for_selector
)
from src.lib.dom import find_element_by_selector, set_value
from src.lib.notify import wait_notify_to_disappear, wait_notify_worked
from src.lib.errors import assert_xpath_is_visible
from src.lib.formatting import make_double_text_xpath

from src.tests.orders.lib import make_orders_grid_selector

from src.scaffolds.dropdown import choose_cashbox
from src.scaffolds.dialog import close_dialog

CASHBOX_SEL = ".js-cbp-cbpicker [name=cashbox]"
SUBMIT_ORDER_PAYMENT_SEL = ".js-cbp-submit"
NOTIFY_SEL = ".humane-jackedup-info"


#TODO: This method should be refactored or killed

def change_status_in_order(driver, status_idx):
    # import ipdb; ipdb.set_trace()
    wait_notify_to_disappear(driver)
    find_element_by_selector(driver, ".b-order .js-status").click()

    choose_status = find_element_by_selector(
        driver, ".b-order .js-switch-status", idx=status_idx
    )
    status_name = choose_status.text
    choose_status.click()

    status = make_double_text_xpath(
        "div" , "@class, 'b-timeline__status'", status_name
    )

    wait_for_xpath(driver, status)
    return assert_xpath_is_visible(driver, status)

#TODO: This method should be refactored or killed

# Den method
def change_status_in_order_without_pay(driver, status_idx):

    wait_notify_to_disappear(driver)
    find_element_by_selector(driver, ".b-order .js-status").click()

    choose_status = find_element_by_selector(
        driver, ".b-order .js-switch-status", idx=status_idx
    )

    if status_idx == 4:
        choose_status.click()
        wait_for_selector(driver, ".b-dialog_type_cashbox")


    status_name = choose_status.text
    choose_status.click()
    status = make_double_text_xpath(
        "div", "@class, 'b-timeline__status'", status_name
    )
    wait_for_xpath(driver, status)
    return assert_xpath_is_visible(driver, status)

def change_status_in_order_new(driver, status_idx):
    wait_notify_to_disappear(driver)
    find_element_by_selector(driver, ".b-order .js-status").click()
    choose_status = find_element_by_selector(
        driver, ".b-order .js-switch-status", idx=status_idx
    )
    choose_status.click()

def change_status_from_table(driver, status_idx):
    # Fire: open statuses popup.
    wait_selector_to_disappear(driver, ".k-loading-color")
    find_element_by_selector(
        driver, make_orders_grid_selector(".js-status")
    ).click()

    target = find_element_by_selector(
        driver, make_orders_grid_selector(".js-switch-status"), idx=status_idx
    )

    target_status_id = target.get_attribute("data-status-id")

    # Fire: switch status.
    target.click()
    wait_selector_to_disappear(driver, ".h-order-row_blink_yellow", time=10)

    def _is_same_statuses(_driver):
        return target_status_id == find_element_by_selector(
            _driver, make_orders_grid_selector("[data-status-id]"),
        ).get_attribute("data-status-id")

    return wait_condition(driver, _is_same_statuses)

def close_and_pay_from_table(driver, status_idx, cashbox_idx):
    wait_selector_to_disappear(driver, ".k-loading-color")
    find_element_by_selector(
        driver, make_orders_grid_selector(".js-status")
    ).click()

    target = find_element_by_selector(
        driver, make_orders_grid_selector(".js-switch-status"), idx=status_idx
    )

    target_status_id = target.get_attribute("data-status-id")

    # Fire: switch status.
    target.click()

    choose_cashbox(driver, CASHBOX_SEL, cashbox_idx)
    close_dialog(driver, SUBMIT_ORDER_PAYMENT_SEL, ".b-dialog_type_cashbox")
    wait_selector_to_disappear(driver, ".h-order-row_blink_yellow", time=15)
    def _is_same_statuses(_driver):
        return target_status_id == find_element_by_selector(
            _driver, make_orders_grid_selector("[data-status-id]"),
        ).get_attribute("data-status-id")
    import time; time.sleep(1)
    return wait_condition(driver, _is_same_statuses)

def close_and_pay_from_order(driver, status_idx, cashbox_idx):
    # Trying to change status straightaway.
    # If system notify blocks us, we wait until it disappear
    try:
        find_element_by_selector(driver, ".b-order .js-status").click()
    except WebDriverException:
        wait_selector_to_disappear(driver, NOTIFY_SEL)
        find_element_by_selector(driver, ".b-order .js-status").click()

    choose_status = find_element_by_selector(
        driver, ".b-order .js-switch-status", idx=status_idx
    )
    status_name = choose_status.text
    choose_status.click()

    wait_for_selector(driver, ".b-dialog_type_cashbox")

    choose_cashbox(driver, CASHBOX_SEL, cashbox_idx)
    close_dialog(
        driver, SUBMIT_ORDER_PAYMENT_SEL, ".b-dialog_type_cashbox"
    )

    status = make_double_text_xpath(
        "div" , "@class, 'b-timeline__status'", status_name
    )

    wait_for_xpath(driver, status)
    return assert_xpath_is_visible(driver, status)
