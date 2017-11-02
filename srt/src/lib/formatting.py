# ~*~ coding: utf-8 ~*~


def format_phone(phone):
    return "(%s) %s-%s-%s" % (phone[0:3], phone[3:6], phone[6:8], phone[8:10])

def format_phone_ua(phone):
    return "+38 (%s) %s-%s-%s" % (phone[0:3], phone[3:6], phone[6:8], phone[8:10])

def format_price(price):
    price_elmnts = price.split()
    return price_elmnts[0]

# removes whitespaces and tail currency code
def format_cash_amount(amount):
    value = amount.split()

    if value[-1].isalpha():
        value.pop(-1)

    new_value = float("".join(value))
    return str(new_value)

## IS DEPRECATED

def make_text_xpath(xpath_sel, data):
    return u".//{0}[contains(text(), '{1}')]".format(xpath_sel, data)

## IS DEPRECATED

# Makes xpath with two 'contains', second of wich is text
def make_double_text_xpath(xpath_sel, contains, data):
    return u".//{0}[contains({1}) and contains(text(), '{2}')]".format(
        xpath_sel, contains, data
    )

