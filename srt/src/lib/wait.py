# ~*~ coding: utf-8 ~*~

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.settings import TIME


# Deprecated: remove out
def wait_for_id(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.ID, name))
    )

# Deprecated: to remove
def wait_for_xpath(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.XPATH, name))
    )

def wait_for_selector(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, name))
    )

def wait_to_see_selector(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, name))
    )

def wait_to_click_selector(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, name))
    )

def wait_selector_to_disappear(driver, selector, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
    )

def wait_tag_to_disappear(driver, selector, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located((By.TAG_NAME, selector))
    )

def wait_xpath_to_disappear(driver, name, time=None):
    time = time or TIME

    WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located((By.XPATH, name))
    )

def wait_condition(driver, fn, time=None):
    time = time or TIME
    return WebDriverWait(driver, time).until(fn)
