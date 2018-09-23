# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'tim@kartoza.com'
__date__ = '2018-06-22'
__copyright__ = 'Copyright 2018, Kartoza'

import unittest

from species_explorer_dialog import SpeciesExplorerDialog
from test.utilities import get_qgis_app
QGIS_APP = get_qgis_app()


class SpeciesExplorerDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = SpeciesExplorerDialog(None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_dialog_find(self):
        """Test we can click OK."""
        self.dialog.search_text.setText('Acacia saligna')
        button = self.dialog.search_button
        button.click()
        result = self.dialog.results_list.item(0).text()
        self.assertEqual(result, 'Acacia saligna')


if __name__ == "__main__":
    suite = unittest.makeSuite(SpeciesExplorerDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

