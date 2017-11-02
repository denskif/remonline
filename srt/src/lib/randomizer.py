# ~*~ coding: utf-8 ~*~

from time import strftime
from datetime import datetime
from random import randint, random


def random_x():
    return str(strftime("%d%m%H%M%S"))

def random_z():
    return str(datetime.now().strftime("%M%S%f"))

def random_int(l=None, r=None):
    # Left bound.
    l = l or 0
    # Right bound.
    r = r or 10000

    return randint(l, r)

def make_login():
    return "test-{0}".format(random_x())

def make_phone_number():
    return random_z()

def make_email():
    return "{0}@test.com".format(random_x())

def make_spare_part():
    return "Spare_{0}".format(random_x())

def make_cashbox():
    return "Box_{0}".format(random_x())

def make_address():
    return "The {0} Driver".format(random_x())

def make_client_name():
    return "Mr {0}".format(random_x())
