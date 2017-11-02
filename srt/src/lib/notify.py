# ~*~ coding: utf-8 ~*~

from src.lib.wait import wait_to_see_selector, wait_selector_to_disappear


NOTIFY_SEL = ".humane-jackedup-animate"
ERROR_NOTIFY_SEL = ".humane-jackedup-error"
INFO_NOTIFY_SEL = ".humane-jackedup-info"

def wait_notify_to_appear(driver):
    return wait_to_see_selector(driver, NOTIFY_SEL)

def wait_notify_to_disappear(driver):
    return wait_selector_to_disappear(driver, NOTIFY_SEL, time=20)

def wait_notify_worked(driver):
    wait_notify_to_appear(driver)
    return wait_notify_to_disappear(driver)

def wait_error_notify(driver):
	wait_to_see_selector(driver, ERROR_NOTIFY_SEL)
	return wait_selector_to_disappear(driver, ERROR_NOTIFY_SEL)

def wait_info_notify(driver):
	wait_to_see_selector(driver, INFO_NOTIFY_SEL)
	return wait_selector_to_disappear(driver, INFO_NOTIFY_SEL)

