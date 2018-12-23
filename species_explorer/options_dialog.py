# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenModellerDialog
                                 A QGIS plugin
 
 
 
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
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import QSettings


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'options_dialog_base.ui'))


class OptionsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(OptionsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.run_button = self.button_box.button(
            QtWidgets.QDialogButtonBox.Ok)
        self.run_button.clicked.connect(self.ok)
        self.cancel_button = self.button_box.button(
            QtWidgets.QDialogButtonBox.Cancel)
        self.cancel_button.clicked.connect(self.reject)
        self.path_button.clicked.connect(
            self.openmodeller_path)

        om_console_path = QSettings().value(
            'SpeciesExplorer/om_console_path', False, type=str)
        self.path.setText(om_console_path)

    def openmodeller_path(self):
        """Set the path for the openModeller binary directory."""
        # noinspection PyCallByClass,PyTypeChecker
        directory_name = QFileDialog.getOpenFileName(
            self,
            self.tr('openModeller directory'),
            self.path.text())
        QSettings().setValue(
            'SpeciesExplorer/om_console_path', directory_name)

    def ok(self):
        pass

    def reject(self):
        pass

