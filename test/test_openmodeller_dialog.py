# coding=utf-8
import unittest
import os
from qgis.PyQt import QtWidgets
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer
)
from species_explorer.openmodeller_dialog import OpenModellerDialog
from test.utilities import get_qgis_app

"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'tim@kartoza.com'
__date__ = '2018-06-22'
__copyright__ = 'Copyright 2018, Kartoza'

QGIS_APP = get_qgis_app()


class OpenModellerDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = OpenModellerDialog(None)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        rain_coolest = os.path.join(current_dir, 'rain_coolest.tif')
        name = os.path.basename('rain_coolest')
        rain_coolest_layer = QgsRasterLayer(rain_coolest, name)
        temp_avg = os.path.join(current_dir, 'temp_avg.tif')
        name = os.path.basename('temp_avg')
        temp_avg_layer = QgsRasterLayer(temp_avg, name)
        furcata = os.path.join(current_dir, 'furcata_bolvana.geojson')
        furcata_layer = QgsVectorLayer(furcata, 'Furcata boliviana', 'ogr')
        QgsProject.instance().addMapLayer(temp_avg_layer, True)
        QgsProject.instance().addMapLayer(rain_coolest_layer, True)
        QgsProject.instance().addMapLayer(furcata_layer, True)




    def tearDown(self):
        """Runs after each test."""
        self.dialog = None


    def test_dialog_run(self):
        """Test we can click OK."""
        # Set the current index for the taxon column to 'scientificName'
        self.dialog.taxon_column.setCurrentIndex(0)
        # Set the algorithm to 'Maximum Entropy'
        self.dialog.algorithm.setCurrentIndex(9)
        # Select all raster layers
        self.dialog.raster_layers.selectAll()
        # Run the analysis
        button = self.dialog.button_box.button(
            QtWidgets.QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.results_list.item(0).text()
        # Get the output log from the analysis
        log_text = self.dialog.log.text()
        self.assertEqual(result, 'Acacia saligna')


if __name__ == "__main__":
    suite = unittest.makeSuite(SpeciesExplorerDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

