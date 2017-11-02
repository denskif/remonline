#!/usr/bin/env python

from functools import partial

import unittest
import HTMLTestRunner

import src.tests.auth as t_auth
import src.tests.orders as t_orders
import src.tests.settings as t_settings
import src.tests.warehouse as t_warehouse
import src.tests.cashflow as t_cashflow
import src.tests.shop as t_shop
import src.tests.invoices as t_invoices
import src.tests.clients as t_client
import src.tests.api as t_api
import src.tests.refunds as t_refund

import src.scaffolds.auth as s_auth

from src.lib.driver import close_driver


VERBOSE_LEVEL = 2
SUITE = unittest.TestSuite


def load_test(test_case):
    return unittest.TestLoader().loadTestsFromTestCase(test_case)

def run_dev_test(test_suite):
    return unittest.TextTestRunner(verbosity=VERBOSE_LEVEL).run(test_suite)


AUTH = [
    # s_auth.Login,
    s_auth.Signup,
]
DEV = [
    t_orders.ChangeDiscount
]


### Regular development test
run_dev_test(SUITE(map(load_test, AUTH)))
run_dev_test(SUITE(map(load_test, DEV)))


close_driver()
