# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpeciesExplorer
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
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .species_explorer_dialog import SpeciesExplorerDialog
from .openmodeller_dialog import OpenModellerDialog
import os.path


class SpeciesExplorer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at gbif_downloader time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SpeciesExplorer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Species Explorer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SpeciesExplorer')
        self.toolbar.setObjectName(u'SpeciesExplorer')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SpeciesExplorer', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/species_explorer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GBIF Downloader'),
            callback=self.gbif_downloader,
            parent=self.iface.mainWindow())
        icon_path = ':/plugins/species_explorer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'openModeller'),
            callback=self.openmodeller,
            parent=self.iface.mainWindow())
        # Only show the tests menubar item if we have a source check out
        # determined to be true if the tests directory is present...
        if os.path.exists(os.path.dirname(__file__) + '/tests/'):
            self.add_action(
                icon_path,
                text=self.tr(u'Species Explorer Tests'),
                callback=self.run_tests,
                parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Species Explorer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def gbif_downloader(self):
        """Run method that performs all the real work"""
        # show the dialog
        # Create the dialog (after translation) and keep reference
        gbif_dialog = SpeciesExplorerDialog()
        # Run the dialog event loop
        result = gbif_dialog.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def openmodeller(self):
        """Show the openModeller Dialog"""
        # show the dialog
        openmodeller_dialog = OpenModellerDialog()
        # Run the dialog event loop
        result = openmodeller_dialog.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
    def run_tests(self):
        """Run unit tests in the python console."""
        from qgis.PyQt.QtWidgets import QDockWidget
        main_window = self.iface.mainWindow()
        action = main_window.findChild(QAction, 'mActionShowPythonDialog')
        action.trigger()
        package = 'test'
        for child in main_window.findChildren(QDockWidget, 'PythonConsole'):
            if child.objectName() == 'PythonConsole':
                child.show()
                for widget in child.children():
                    if 'PythonConsoleWidget' in str(widget.__class__):
                        # print "Console widget found"
                        shell = widget.shell
                        shell.runCommand(
                            'from SpeciesExplorer.test_suite import test_package')
                        shell.runCommand('test_package(\'%s\')' % package)
                        break
