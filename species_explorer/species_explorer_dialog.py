# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpeciesExplorerDialog
                                 A QGIS plugin
 Quickly fetch and visualise species occurrence data.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-06-22
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Kartoza
        email                : tim@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, QtCore
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsApplication
from qgis.core import (
    QgsFields,
    QgsPointXY,
    QgsGeometry,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsField,
    QgsWkbTypes,
    QgsMemoryProviderUtils,
)
from qgis.core import QgsMessageLog  # NOQA

from species_explorer.gbifutils import name_parser, name_usage, gbif_GET

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'species_explorer_dialog_base.ui'))


class SpeciesExplorerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SpeciesExplorerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.search_button.clicked.connect(self.find)
        self.fetch_button.clicked.connect(self.fetch)
        self.results_list.itemClicked.connect(self.select)

    def find(self):
        """Search GBIF for the species provided."""
        text = self.search_text.text()
        self.taxonomy_list.clear()
        parsed_species = name_parser(text)[0]
        genus = parsed_species['genusOrAbove']
        try:
            species = parsed_species['specificEpithet']
        except KeyError:
            species = ''
        QgsMessageLog.logMessage(
            'Searching for %s' % text,
            'SpeciesExplorer',
            0)
        # https: // www.gbif.org / species / search?q = Protea % 20
        # repens & rank = SPECIES & qField = SCIENTIFIC & status = ACCEPTED
        url = (
            'https://api.gbif.org/v1/species/search?'
            'q=%s%%20%s&rank=SPECIES&qField=SCIENTIFIC&status=ACCEPTED' % (
                genus, species))
        matches = gbif_GET(url, None)
        QgsMessageLog.logMessage(str(matches), 'SpeciesExplorer', 0)
        self.results_list.clear()
        names = {}
        for match in matches['results']:
            try:
                name = match['canonicalName']
            except KeyError:
                continue
            if name not in names:
                QgsMessageLog.logMessage(str(match), 'SpeciesExplorer', 0)
                speciesItem = QtWidgets.QListWidgetItem(name)
                if 'nubKey' in match:
                    taxon_key = match['nubKey']
                elif 'speciesKey' in match:
                    taxon_key = match['speciesKey']
                else:
                    continue
                speciesItem.setData(Qt.UserRole, taxon_key)
                self.results_list.addItem(speciesItem)
                names[name] = taxon_key

    def select(self, item):
        """
        Event handler for when an item is clicked in the search result lisl.
        :param item: QListWidgetItem that was clicked
        :return: 
        """
        QgsMessageLog.logMessage(
            '%s selected' % item.text(),
            'SpeciesExplorer',

        )

        species = name_usage(item.data(Qt.UserRole))
        self.taxonomy_list.clear()
        # QgsMessageLog.logMessage(str(species), 'SpeciesExplorer', 0)
        self.taxonomy_list.addItem('Kingdom: %s' % species['kingdom'])
        self.taxonomy_list.addItem('Phylum: %s' % species['phylum'])
        self.taxonomy_list.addItem('Class: %s' % species['class'])
        self.taxonomy_list.addItem('Order: %s' % species['order'])
        self.taxonomy_list.addItem('Family: %s' % species['family'])
        self.taxonomy_list.addItem('Genus: %s' % species['genus'])
        self.taxonomy_list.addItem('Species: %s' % species['species'])
        self.taxonomy_list.addItem('Taxon ID: %s' % species['taxonID'])
        try:
            self.taxonomy_list.addItem(
                'Accepted Name: %s' % species['accepted'])
        except:
            pass
        self.taxonomy_list.addItem(
            'Canonical Name: %s' % species['canonicalName'])
        self.taxonomy_list.addItem(
            'Accepted Key: %s' % item.data(Qt.UserRole))

    def fetch(self):
        """
        Fetch Occurrence records for selected taxon.
        """
        QgsApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor)
        )
        QgsMessageLog.logMessage('Fetching occurrences', 'SpeciesExplorer', 0)
        name = self.results_list.selectedItems()[0].text()

        end_of_records = False
        offset = 0
        layer = QgsMemoryProviderUtils.createMemoryLayer(
            name=name,
            fields=QgsFields(),
            geometryType=QgsWkbTypes.Point,
            crs=QgsCoordinateReferenceSystem('EPSG:4326'))
        layer.dataProvider().createSpatialIndex()
        provider = layer.dataProvider()
        counter = 0

        while not end_of_records:

            url = (
                'https://api.gbif.org/v1/occurrence/search?'
                'scientificName=%s&offset=%i' % (name, offset))
            offset += 100
            result = gbif_GET(url, None)
            count = int(result['count'])
            end_of_records = result['endOfRecords']
            records = result['results']

            QgsMessageLog.logMessage(
                'Fetching record %s of %s occurrences' % (offset, count),
                'SpeciesExplorer',
                0)
            # Will populate this in create_fields call
            if len(records) == 0:
                QgsMessageLog.logMessage(
                    'No records found',
                    'SpeciesExplorer',
                    0)
                QMessageBox.information(
                    self,
                    'Species Explorer',
                    'No records found for %s' % name
                )
                return
            field_lookups = self.create_fields(layer, records[0])
            QgsMessageLog.logMessage(
                'Field lookup: %s' % field_lookups,
                'SpeciesExplorer',
                0)
            for record in records:
                QgsMessageLog.logMessage(
                    'Record: %s' % record,
                    'SpeciesExplorer',
                    0)
                if ('decimalLongitude' not in record or
                        'decimalLatitude' not in record):
                    continue

                feature = QgsFeature()
                feature.setGeometry(
                    QgsGeometry.fromPointXY(QgsPointXY(
                        record['decimalLongitude'],
                        record['decimalLatitude']
                    )))
                attributes = [counter]
                for key in field_lookups:
                    try:
                        attributes.append(record[key])
                    except KeyError:
                        # just append an empty item to make sure the list
                        # size is correct
                        attributes.append('')

                feature.setAttributes(attributes)
                provider.addFeatures([feature])
                counter += 1

            if offset > count:
                end_of_records = True

            QgsMessageLog.logMessage(
                'End of records: %s' % end_of_records,
                'SpeciesExplorer',
                0)

        layer.commitChanges()
        QgsProject.instance().addMapLayer(layer)

        # recursively walk back the cursor to a pointer
        while QgsApplication.instance().overrideCursor() is not None and \
            QgsApplication.instance().overrideCursor().shape() == \
            QtCore.Qt.WaitCursor:
            QgsApplication.instance().restoreOverrideCursor()

    def create_fields(self, layer, record):
        """Create the attributes for the gbif response table."""
        layer.startEditing()
        id_field = QgsField()
        id_field.setName('id')
        id_field.setType(QVariant.Int)
        id_field.setPrecision(0)
        id_field.setLength(10)
        layer.addAttribute(id_field)
        # A dict to store the field offeset for each property
        field_lookups = []
        for key in record.keys():
            new_field = QgsField()
            new_field.setName(key)
            new_field.setType(QVariant.String)
            new_field.setLength(255)
            layer.addAttribute(new_field)
            field_lookups.append(key)

        layer.commitChanges()
        return field_lookups
