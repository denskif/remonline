# ~*~ coding: utf-8 ~*~


from src.lib.dom import (
    set_value, find_element_by_selector, find_elements_by_selector,
    hover_and_click,
)
from src.lib.randomizer import make_cashbox
from src.lib.formatting import format_cash_amount
from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear

from src.scaffolds.dialog import confirm_delete

from src.tests.cashflow.lib import (
    open_create_cashbox_dialog, submit_cashbox_dialog, open_cashbox_settings,
    NAME_INPUT_SEL, SETTING_SEL, TRASH_BTN_SEL, make_box_sel, ACTIVE_BOX_SEL
)
from src.tests.cashflow.lib.select import select_cashbox
from src.tests.cashflow.lib.transactions import make_income, make_expense


BOX_PRICE_SELECTOR = ".b-cashbox__form h2"


def create_local_cashbox(driver, data=None):
    cashbox_name = data or make_cashbox()

    open_create_cashbox_dialog(driver)
    wait_to_see_selector(driver, NAME_INPUT_SEL)
    set_value(driver, NAME_INPUT_SEL, cashbox_name)
    find_element_by_selector(driver, "[for=l-cb-type-local]").click()
    submit_cashbox_dialog(driver)

    return cashbox_name


def create_global_cashbox(driver, data=None):
    cashbox_name = data or make_cashbox()

    open_create_cashbox_dialog(driver)
    wait_to_see_selector(driver, NAME_INPUT_SEL)
    set_value(driver, NAME_INPUT_SEL, cashbox_name)
    find_element_by_selector(driver, "[for=l-cb-type-global]").click()
    submit_cashbox_dialog(driver)

    return cashbox_name


def set_cashbox_to_zero(driver, cashbox_sel):
    zero_sum = 0.0
    minus = "-"
    first_char = 0
    data = {
                'amount' : None,
                'comment' : "Setting cashbox to zero",
            }

    select_cashbox(driver, cashbox_sel)
    row_box_sum = find_element_by_selector(
        driver, 
        make_box_sel(BOX_PRICE_SELECTOR)
    ).text
    box_sum = format_cash_amount(row_box_sum)

    if not float(box_sum) == zero_sum:
        if box_sum[first_char] == minus:
            data['amount'] = box_sum.replace(minus, "")
            make_income(driver, data)
        else:
            data['amount'] = box_sum
            make_expense(driver, data)
    return wait_to_see_selector(driver, ACTIVE_BOX_SEL)


def clean_up_cashboxes(driver):
    cashboxes = driver.find_elements_by_css_selector(SETTING_SEL)
    one_cashbox = 1
    last_cashbox = -1

    # remove cashboxes from bottom to top
    while len(cashboxes) > one_cashbox:
        
        set_cashbox_to_zero(driver, cashboxes[last_cashbox])

        cashboxes = driver.find_elements_by_css_selector(SETTING_SEL)
        cashboxes.pop().click()

        wait_to_see_selector(driver, TRASH_BTN_SEL)
        find_element_by_selector(driver, TRASH_BTN_SEL).click()
        confirm_delete(driver)
        cashboxes = driver.find_elements_by_css_selector(SETTING_SEL)