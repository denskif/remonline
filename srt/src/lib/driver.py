# ~*~ coding: utf-8 ~*~

from selenium import webdriver

from src import settings


driver = webdriver.Chrome()
driver.maximize_window()
driver.get(settings.HOST)


def get_driver():
    return driver

def refresh():
    return driver.refresh()

def close_driver():
    return driver.quit()
