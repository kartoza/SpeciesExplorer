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
import sys
from subprocess import call, CalledProcessError
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject, QgsMessageLog
from qgis.PyQt import uic
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'openmodeller_dialog_base.ui'))


class OpenModellerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(OpenModellerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.ok_button = self.button_box.button(
            QtWidgets.QDialogButtonBox.Ok)
        self.ok_button.clicked.connect(self.run)
        layers = QgsProject.instance().mapLayers()
        for layer in layers:
            self.dialog.point_layers.addItem(layer.name())

    def run(self):
        """Run openModeller with the current point file."""
        openmodeller_path = os.path.dirname(__file__)
        openmodeller_path = os.path.abspath(os.path.join(
            openmodeller_path, '..', 'openmodeller', 'bin'))
        binary = os.path.join(openmodeller_path, 'om_console')

    def _run_command(self, command):
        """Run a command and raise any error as needed.

        This is a simple runner for executing gdal commands.

        :param command: A command string to be run.
        :type command: str

        :raises: Any exceptions will be propagated.
        """
        try:
            my_result = call(command, shell=True)
            del my_result
        except CalledProcessError as e:
            QgsMessageLog.logMessage(
                'Running command failed %s' % command,
                'SpeciesExplorer',
                0)
            message = (
                'Error while executing the following shell '
                'command: %s\nError message: %s' % (command, str(e)))
            # shameless hack - see https://github.com/AIFDR/inasafe/issues/141
            if sys.platform == 'darwin':  # Mac OS X
                if 'Errno 4' in str(e):
                    # continue as the error seems to be non critical
                    pass
                else:
                    raise Exception(message)
            else:
                raise Exception(message)
