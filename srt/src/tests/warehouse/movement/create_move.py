# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate

from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.clean_up import delete_trans


MOVE_DATA = {
    u'supplier' : {'name': u"Korea lmt."},
    u'title' : u"Magic Spark",
    u'quantity' : u"1",
    u'price' : u"78",
}


class CreateMovement(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_0_create_posting(self):
        navigate(self.driver, "/app#!/warehouse/posting")
        create_posting(self.driver, self, MOVE_DATA)
        return True

