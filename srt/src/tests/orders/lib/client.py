# ~*~ coding: utf-8 ~*~

from src.lib.dom import set_value, get_value

from src.lib.formatting import format_phone_ua


# Dictionary client consist of: name, phone, email, and address
def add_new_client(driver, client):
    set_value(driver, "#js-o-name", client['name'])
    set_value(driver, "#js-o-phone", client['phone'])
    set_value(driver, "#js-o-email", client['email'])
    set_value(driver, "#js-o-address", client['address'])
    return True

def assert_client(driver, test_self, client):
    name = get_value(driver.find_element_by_css_selector("#js-o-name"))
    phone = get_value(driver.find_element_by_css_selector("#js-o-phone"))
    email = get_value(driver.find_element_by_css_selector("#js-o-email"))
    address = get_value(driver.find_element_by_css_selector("#js-o-address"))

    test_self.assertEqual(name, client['name'])
    test_self.assertEqual(phone, format_phone_ua(client['phone']))
    test_self.assertEqual(email, client['email'])
    return test_self.assertEqual(address, client['address'])
