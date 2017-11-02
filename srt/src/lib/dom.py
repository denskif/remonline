# ~*~ coding: utf-8 ~*~

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


ERROR_TOOLTIP_CLASS_NAME = 'h-errors-tooltip'

def get_attribute(element, attribute):
    return element.get_attribute(attribute).encode('utf-8')

def get_value(element):
    return element.get_attribute('value').encode('utf-8')

def find_displayed(elements):
    if not elements:
        return []

    return filter(
        lambda element: element.is_displayed(), elements,
    )

# Find fisrt displayed class name.
def find_element_by_class_name(driver, class_name, idx=None):
    displayed = find_displayed(
        driver.find_elements_by_class_name(class_name)
    )

    if not displayed:
        return None

    return displayed[idx or 0]

def find_element_by_selector(driver, selector, idx=None):
    displayed = find_displayed(
        driver.find_elements_by_css_selector(selector)
    )

    if not displayed:
        return None

    return displayed[idx or 0]

def find_elements_by_selector(driver, selector):
    displayed = find_displayed(
        driver.find_elements_by_css_selector(selector)
    )

    if not displayed:
        return None

    return displayed

def find_input_by_selector(driver, selector):
    return driver.find_element_by_css_selector(selector)

# Find first displayed tag name.
def find_element_by_partial_link_text(driver,link_text):
    displayed = find_displayed(
        driver.find_elements_by_partial_link_text(link_text)
    )

    if not displayed:
        return None

    return displayed[0]

# Find text by the xpath contains.
def find_element_by_xpath(driver, xpath, idx=None):
    displayed = driver.find_elements_by_xpath(xpath)

    if not displayed:
        return None

    return displayed[idx or 0]

# Find if error tooltips were displayed.
def has_error_tooltip(driver, input_field):
    parent = input_field.find_element_by_xpath("..")
    css_class = parent.get_attribute('class')

    return ERROR_TOOLTIP_CLASS_NAME in css_class

def make_selector(*selectors, **kwargs):
    sep = kwargs.get('sep', " ")
    return sep.join(selectors)

def set_value(driver, sel, value, sel_idx=None):
    field = find_element_by_selector(driver, sel, sel_idx)
    field.clear()
    field.send_keys(value)
    return value

def is_select(node):
    return node.tag_name == "select"

def double_click(driver, node):
    chain = ActionChains(driver)
    return chain.double_click(node).perform()

def hover_and_click(driver, selector):
    element = driver.find_element_by_css_selector(selector)

    # Hover and select target node.
    ActionChains(driver).move_to_element(element).perform()
    element.click()

    return element

def click_nth_node(driver, selector, nth=None):
    nth = nth or 0

    element = find_element_by_selector(driver, selector, idx=nth)

    # Hover and select target node.
    ActionChains(driver).move_to_element(element).perform()

    # Select nth element.
    element.click()

    return element

def hover(driver, selector):
    element = driver.find_element_by_css_selector(selector)
    ActionChains(driver).move_to_element(element).perform()
    return element


def try_find_by_tag_name(driver,tag_name):
    if driver.find_element_by_tag_name(tag_name) == NoSuchElementException:
        return None
    else:
        return driver.find_element_by_tag_name(tag_name)
