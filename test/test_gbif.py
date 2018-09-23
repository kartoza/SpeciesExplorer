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
from gbifutils import name_usage
from test.utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class TestGBIF(unittest.TestCase):
    """Test GBIF Client works."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_species(self):
        """Test we can use the species API."""

        species = name_usage(3329049)

if __name__ == "__main__":
    suite = unittest.makeSuite(TestGBIF)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

