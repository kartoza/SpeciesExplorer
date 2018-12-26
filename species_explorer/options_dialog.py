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
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QSettings
from qgis.core import QgsMessageLog

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
        self.path_button.clicked.connect(self.path_button_clicked)

        om_console_path = QSettings().value(
            'SpeciesExplorer/om_console_path', False, type=str)
        self.path.setText(om_console_path)
        # For veriifying om_console works properly:
        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyReadStandardError.connect(self.data_ready)
        self.process.readyReadStandardOutput.connect(self.data_ready)
        # Just to prevent accidentally running multiple times
        # Disable the button when process starts,
        # and enable it when it finishes
        self.process.started.connect(
            lambda: self.path_button.setEnabled(False))
        self.process.finished.connect(
            lambda: self.path_button.setEnabled(True))
        self.process.started.connect(
            lambda: self.path.setEnabled(False))
        self.process.finished.connect(
            lambda: self.path.setEnabled(True))
        #self.process.finished.connect(self.show_model_output)

    def on_path_changed(self):
        """Autoslot for change in path."""
        om_console_path = QSettings().value(
            'SpeciesExplorer/om_console_path', False, type=str)
        self._run_command(om_console_path)

    def path_button_clicked(self):
        """Slot for when path button is clicked.
        
        Set the path for the openModeller binary directory."""
        # noinspection PyCallByClass,PyTypeChecker
        om_console_path = QFileDialog.getOpenFileName(
            self,
            self.tr('openModeller directory'),
            self.path.text())[0]
        QgsMessageLog.logMessage(
            'om_console path: %s' % str(om_console_path),
            'SpeciesExplorer',
            0)
        QSettings().setValue(
            'SpeciesExplorer/om_console_path', om_console_path)
        # verify the output from openmodeller is correct:
        # Usage: om_console request_file [log_level [config_file]]
        # That way we know we have a working installation

        # This should trigger the path_changed slot and run the
        # om_console test
        self.path.setText(om_console_path)


    def _run_command(self, command, arguments):
        """Run a command and raise any error as needed.

        This is a simple runner for executing shell commands.

        :param command: A command string and its prameters to be run.
        Pass the command as a list e.g.['ls', '-lah']
        :type command: str

        :raises: Any exceptions will be propagated.
        """
        QgsApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor)
        )

        try:
            self.process.start(command, arguments)
        finally:
            # recursively walk back the cursor to a pointer
            while QgsApplication.instance().overrideCursor() is not None and \
                QgsApplication.instance().overrideCursor().shape() == \
                    QtCore.Qt.WaitCursor:
                QgsApplication.instance().restoreOverrideCursor()


    def data_ready(self):
        """Slot to handle updates to the log window from QProcess."""
        cursor = self.log.textCursor()
        cursor.movePosition(cursor.End)
        text = str(self.process.readAllStandardOutput(), 'utf-8')
        cursor.insertText(text)
        text = str(self.process.readAllStandardError(), 'utf-8')
        cursor.insertText(text)
        cursor.movePosition(cursor.End)
        self.log.ensureCursorVisible()
