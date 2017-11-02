# ~*~ coding: utf-8 ~*~

import os
import sys

from datetime import datetime

from selenium.common.exceptions import ElementNotVisibleException

from src.settings import SCREEN_PATH

from src.lib.dom import (
    has_error_tooltip, find_element_by_class_name, find_element_by_xpath,
    find_element_by_selector
)


ERROR_TOOLTIP_CLASS_NAME = "h-errors-tooltip"


# Check for tooltip error
def assert_has_error_tooltip(driver, input_field):
    if has_error_tooltip(driver, input_field):
        return True

    raise ElementNotVisibleException(ERROR_TOOLTIP_CLASS_NAME, input_field)

# Method is deprecated we use customs waits - /lib/wait.py
def assert_class_is_visible(driver, class_name):
    if find_element_by_class_name(driver, class_name):
        return True

    raise ElementNotVisibleException(class_name)

def assert_xpath_is_visible(driver, xpath_name, idx=None):
    if find_element_by_xpath(driver, xpath_name, idx=None):
        return True

    raise ElementNotVisibleException("Maan, your xpath is not visible!")

def assert_selector_is_visible(driver, selector):
    if find_element_by_selector(driver, selector):
        return True

    raise ElementNotVisibleException("Maan, your css selector is not visible!")

def shoot_test_error(driver, test_method_name):
    has_exception = sys.exc_info()[0]
    if not has_exception:
        return None

    def _make_file_name():
        return "{0}-{1}.png".format(
            test_method_name,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        )

    print ">>> ", os.path.join(SCREEN_PATH, _make_file_name())
    driver.save_screenshot(os.path.join(SCREEN_PATH, _make_file_name()))

def raise_error(fn, msg):
    if fn != True:
        raise ValueError(msg)
    else:
        return True
