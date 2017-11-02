# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate, POSTING_URL, WRITE_OFF_URL
from src.lib.errors import raise_error

from src.tests.warehouse.lib.create import create_posting, make_write_off
from src.tests.warehouse.lib.clean_up import delete_trans

from src.tests.warehouse.lib.checkers import check_item_in_table

MSG = "Transactions is not deleted!"

W0_REMOVE_DATA = {
    u'supplier': {'name':u"China Cu."},
    u'title': u"Poroshok iz moluskov",
    u'quantity': u"5",
    u'price': u"66",
}


class DeleteWriteOff(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    def test_0_create_posting(self):
        navigate(self.driver, POSTING_URL)
        create_posting(self.driver, W0_REMOVE_DATA)
        return True

    def test_1_create_outcome(self):
        navigate(self.driver, WRITE_OFF_URL)
        make_write_off(self.driver, W0_REMOVE_DATA)
        return self.assertEqual(
            check_item_in_table(self.driver), W0_REMOVE_DATA['title']
        )

    def test_2_remove_outcome(self):
        return raise_error(delete_trans(self.driver), MSG)
