# ~*~ coding: utf-8 ~*~

from src.lib.dom import find_element_by_selector
from src.lib.wait import wait_for_selector, wait_to_see_selector, wait_to_click_selector

# Signature buttons
SIGN_IN_SEL = ".js-auth-signin"
SIGN_UP_BTN = ".js-auth-signup"

# Login form fields
LOGIN_SEL = "#l-auth-login"
PASS_SEL = "#l-auth-pass"

# First registraion form fields
EMAIL_SEL = "#l-auth-email"
LOGIN_SEL = "#l-auth-login"
PASS_SEL = "#l-auth-pass"

# Second registraion form fields
NAME_SEL = "#l-auth-name"
LAST_NAME_SEL = "#l-auth-lname"
COMPANY_SEL = "#l-auth-company"
CITY_SEL = "#l-auth-city"
PHONE_SEL = "#l-auth-phone"

SUBMIT_SEL = ".js-submit"

PARTNERS_PAGE_LINK = "[href='/partners']"
PARTNER_BTN_SEL = ".js-auth-signup-partner"


def click_submit(driver):
    return find_element_by_selector(driver, SUBMIT_SEL).click()

def click_sign_up(driver):
    find_element_by_selector(driver, SIGN_UP_BTN).click()
    return wait_to_see_selector(driver, SUBMIT_SEL)

def log_out(driver):
    wait_to_click_selector(driver, ".h-avatar")
    find_element_by_selector(driver, ".h-avatar").click()
    wait_for_selector(driver, ".b-employee-menu_state_displayed")
    find_element_by_selector(driver, "[href='/auth/logout']").click()
    return wait_for_selector(driver, SIGN_IN_SEL)
