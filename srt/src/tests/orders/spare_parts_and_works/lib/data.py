# ~*~ coding: utf-8 ~*~
from src.lib.randomizer import random_x

"""-----------------------
"""

RATE = True
DAY = True
CURRENCY = False
MONTH = False


def data_f_srvc(discount = None, discount_type = None):
    return {
    'name' : u"0It's manual add service num{0}".format(random_x()),
    'add_to_book' : False,
    'quantity' : u"10",
    'price' : u"100",
    'cost' : u"50",
    'discount' : discount or True,
    'discount_type' : discount_type or RATE,
    'discount_value' : u'10',
    'warranty' : True,
    'warranty_type' : DAY,
    'warranty_value' : u"14",
}


def data_f_edit_srvc():
    return {
    'name' : u"It's edit service name",
    'add_to_book' : False,
    'quantity' : u"20",
    'price' : u"200",
    'cost' : u"100",
    'discount' : True,
    'discount_type' : RATE,
    'discount_value' : u'15',
    'warranty' : True,
    'warranty_type' : DAY,
    'warranty_value' : u"7",
    }


def data_f_part(discount = None, discount_type = None):
    return {
    'name' : u"It's manual add PART num{0}".format(random_x()),
    'quantity' : u"15",
    'price' : u"200",
    'cost' : u"50",
    'discount' : discount or False,
    'discount_type' : discount_type or CURRENCY,
    'discount_value' : u'25',
    'warranty' : False,
    'warranty_type' : DAY,
    'warranty_value' : u"7",
    }

def data_for_edit_part():
    return {
    'name' : u"It's manual add PART num{0}".format(random_x()),
    'quantity' : u"30",
    'price' : u"100",
    'cost' : u"50",
    'discount' : False,
    'discount_type' : CURRENCY,
    'discount_value' : u'25',
    'warranty' : False,
    'warranty_type' : DAY,
    'warranty_value' : u"7",
    }


def data_f_book():
    return {
        'name' : u"Autocomplete add srvc{0}".format(random_x()),
        'price' : u'50',
    }

#
def data_f_wharehouse():
    return {
    u'supplier' : {'name': u"Supplier n{0}".format(random_x())},
    u'title' : u"Bot n{0}".format(random_x()),
    u'quantity' : u"27",
    u'price' : u"100",
    }

def data_f_worker():
    return {
        u'name' : u"Not good worker n{0}".format(random_x()),
        u'login' : u"logNum1{0}".format(random_x()),
        u'pass' : u"test",
        u'email' : u"{0}@mail.com".format(random_x()),
    }


def comment():
    return {
    'comment' : u"It's cool comment or not {0}".format(random_x()),
    'edit_comment' : u"Edit comment{0}".format(random_x()),
    }


def data_f_book():
    return {
    'name' : u"Autocomplete add srvc{0}".format(random_x()),
    'price' : u'50',
    }

def data_f_edit_discount(d_type, value):
    # d_type must be RATE or currency
    return{
    'discount' : True,
    'discount_type' : d_type,
    'discount_value' : u"{0}".format(value),
    }



class RelationFromDiscountType():

    def __init__(self, data):
        self._price = data['price']
        self._discount = data['discount_value']
        self._quantity = data['quantity']
        self.is_discount_type = data.get('discount_type')

    def price(self):
        if self.is_discount_type:
            return str(int(self._price) - int(self._discount))

        return str(
            int(self._price) - int(self._price)*int(self._discount)/100.0
        )

    def discount(self, tooltip_str):
        if self.is_discount_type:
            return tooltip_str[0][0]

        return tooltip_str[0][1]

    def final_discount_rate(self):
        if self.is_discount_type:
            return str(int(self._discount) * int(self._quantity))

        return str(int(self._quantity)*int(self._price)*int(self._discount)/100.0)

    def final_discount_currency(self):
        if self.is_discount_type:
            return str((100.0/int(self._price))*int(self._discount))

        return str(int(self._discount))

    def final_price(self):
        if self.is_discount_type:
            return int(self._quantity)*(int(self._price) - int(self._discount))

        return int(self._quantity)*(int(self._price)-(int(self._price)*int(self._discount)/100))


class RelationFromFinalDiscount():
    def __init__(self, data, final_discount_data):
        self._price = data['price']
        self._discount = final_discount_data['discount_value']
        self._quantity = data['quantity']
        self.is_discount_type = final_discount_data.get('discount_type')

    def price(self):
        if self.is_discount_type:
            return str(int(self._price) - int(self._discount)/int(self._quantity))

        return str(
            int(self._price) - int(self._price)*int(self._discount)/100
        )


    def discount(self, tooltip_str):
        if self.is_discount_type:
            return str(int(self._discount)/int(self._quantity))

        return tooltip_str[0][1]

    def final_discount_rate(self):
        if self.is_discount_type:
            return str(int(self._discount))

        return str(int(self._quantity)*int(self._price)*int(self._discount)/100)

    def amount(self):
        if self.is_discount_type:
            pr = int(self._price) - int(self._discount)
            return str(int(self._quantity)*pr)

        d = int(self._price)*int(self._discount)/100.0
        pr = int(self._price) - int(d)
        return str(int(self._quantity)*pr)

    def final_discount_currency(self):
        if self.is_discount_type:
            return str((100.0/int(self._price))*int(self._discount))

        return str(int(self._discount))

    def final_price(self):
        if self.is_discount_type:
            return str((int(self._quantity)*(int(self._price)) - int(self._discount)))

        return str(int(self._quantity)*(int(self._price)-(int(self._price)*int(self._discount)/100)))
