# ~*~ coding: utf-8 ~*~

import unittest

from src.lib.driver import get_driver
from src.lib.url import navigate
from src.lib.errors import raise_error

from src.scaffolds.grid import wait_grid_updated, wait_grid_changed_rows_num
from src.scaffolds.search import search_for

from src.tests.warehouse.lib.create import create_posting
from src.tests.warehouse.lib.checkers import assert_added_to_table, TABLE_ERROR_MSG


RESIDUE_DATA = {
    u'supplier' : {'name':u"Kortic Supplies"},
    u'title' : u"Fentuzler",
    u'quantity' : u"2",
    u'price' : u"78",
}
TITLE_CELL = 3
GRID_SEL = ".js-grid"


class CreateResidue(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = get_driver()

    def test_1_create_residue(self):
        navigate(self.driver, "/app#!/warehouse/posting")
        create_posting(self.driver, RESIDUE_DATA)

        navigate(self.driver, "/app#!/warehouse/residue")
        wait_grid_updated(self.driver, GRID_SEL)

        search_for(self.driver, RESIDUE_DATA['title'])

        table_result = assert_added_to_table(
            self.driver, GRID_SEL, TITLE_CELL, RESIDUE_DATA['title']
        )
        return raise_error(table_result, TABLE_ERROR_MSG)
