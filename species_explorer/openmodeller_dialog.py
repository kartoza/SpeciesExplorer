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
from collections import OrderedDict
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt import QtWidgets
from qgis.core import (
    QgsSingleBandPseudoColorRenderer,
    QgsProject,
    QgsMessageLog,
    QgsWkbTypes,
    QgsExpression,
    QgsFeatureRequest,
    QgsMapLayer)
from qgis.PyQt import uic
from qgis.core import QgsApplication, QgsRasterLayer
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QVariant, QSettings
from qgis.PyQt.QtGui import QColor
from species_explorer.utilities import unique_filename
from qgis.core import (
    QgsColorRampShader,
    QgsRasterShader)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'openmodeller_dialog_base.ui'))


class OpenModellerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None, iface=None):
        """Constructor."""
        self.iface = iface
        super(OpenModellerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model_output = None
        self.model_taxon = None
        self.run_button = self.button_box.button(
            QtWidgets.QDialogButtonBox.Ok)
        self.run_button.setText('Run')
        self.run_button.clicked.connect(self.run)
        self.close_button = self.button_box.button(
            QtWidgets.QDialogButtonBox.Close)
        self.close_button.clicked.connect(self.reject)
        self.algorithm.currentIndexChanged.connect(self._show_parameters)
        self.point_layers.currentIndexChanged.connect(self._update_fields)
        self.taxon_column.currentIndexChanged.connect(self._update_taxon_list)
        self._populate_point_layer_combo()
        self._populate_algorithm_combo()
        self._populate_raster_list()

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyReadStandardError.connect(self.data_ready)
        self.process.readyReadStandardOutput.connect(self.data_ready)
        # Just to prevent accidentally running multiple times
        # Disable the button when process starts,
        # and enable it when it finishes
        self.process.started.connect(lambda: self.run_button.setEnabled(False))
        self.process.finished.connect(lambda: self.run_button.setEnabled(True))
        self.process.finished.connect(self.show_model_output)

    def show_model_output(self):
        """Slot to show morel output on completion."""
        if self.model_output is not None and os.path.exists(self.model_output):
            raster_layer = QgsRasterLayer(
                self.model_output, '%s niche' % self.model_taxon)
            self.style_layer(raster_layer)
            QgsProject.instance().addMapLayer(raster_layer, True)

    def data_ready(self):
        """Slot to handle updates to the log window from QProcess."""
        cursor = self.log.textCursor()
        cursor.movePosition(cursor.End)
        text = str(self.process.readAllStandardOutput(), 'utf-8')
        cursor.insertText(text)
        text = str(self.process.readAllStandardError(), 'utf-8')

        # TODO: Trying to make this next section work - need better parser of
        # TODO: stderr to see the model creation and projection progress....

        if text is None:
            pass
        elif 'Model creation:' in text:
            # we can get some progress info from this error message
            number_text = text.replace('[Info] Model creation: ', '')
            number_text.strip()
            number_text = number_text.replace('%%', '')
            try:
                progress = float(number_text)
                QgsMessageLog.logMessage(
                    'Progress for creation: %s' % progress,
                    'SpeciesExplorer',
                    0)
                self.creation_progress.setValue(progress)
            except:
                cursor.insertText('Error: %s' % text)
        elif 'Map creation:' in text:
            # we can get some progress info from this error message
            number_text = text.replace('[Info] Map creation: ', '')
            number_text.strip()
            number_text = number_text.replace('%%', '')

            try:
                progress = float(number_text)
                QgsMessageLog.logMessage(
                    'Progress for map: %s' % progress,
                    'SpeciesExplorer',
                    0)
                self.projection_progress.setValue(progress)
            except:
                cursor.insertText('Error: %s' % text)
        else:
            cursor.insertText('Error: %s' % text)
        cursor.movePosition(cursor.End)
        self.log.ensureCursorVisible()

    def run(self):
        """Run openModeller with the current point layer."""
        self.tabs.setCurrentIndex(1)
        self.creation_progress.setValue(0.0)
        self.projection_progress.setValue(0.0)
        layer_id = self.point_layers.itemData(
            self.point_layers.currentIndex()
        )
        layer = QgsProject.instance().mapLayer(layerId=layer_id)
        taxon_field = self.taxon_column.currentText()
        self.model_taxon = self.taxon.currentText()
        expression = QgsExpression('"%s"=\'%s\'' % (
            taxon_field, self.model_taxon))
        occurrences_path = unique_filename(prefix='occurrences', suffix='.txt')
        occurrence_file = open(occurrences_path, 'wt')
        # Format for occurrences file:
        # #id label   long    lat abundance
        # 1   Acacia aculeatissima    -67.845739  -11.327340  1
        occurrence_file.write(
            '#id label   long    lat abundance\n'
        )
        count = 1
        name_parts = self.model_taxon.split(' ')
        if len(name_parts) < 2:
            self.model_taxon = name_parts[0]
        else:
            self.model_taxon = name_parts[0] + ' ' + name_parts[1]
        for feature in layer.getFeatures(QgsFeatureRequest(expression)):
            lon = feature.geometry().asPoint().x()
            lat = feature.geometry().asPoint().y()
            line = '%i\t%s\t%s\t%s\t1\n' % (
                count,
                self.model_taxon,
                lon,
                lat
            )
            occurrence_file.write(line)
        occurrence_file.close()
        # Now prepare the config file
        rasters = []
        for item in self.raster_layers.selectedItems():
            layer_id = item.data(Qt.UserRole)
            layer = QgsProject.instance().mapLayer(layerId=layer_id)
            source = layer.source()
            rasters.append(source)
        request_path = unique_filename(prefix=clean_name, suffix='.txt')
        request_file = open(request_path, 'wt')
        request_file.writelines(
        """
WKT Coord System = GEOGCS["WGS84", DATUM["WGS84", SPHEROID["WGS84", 6378137.0, 298.257223563]], PRIMEM["Greenwich", 0.0], UNIT["degree", 0.017453292519943295], AXIS["Longitude",EAST], AXIS["Latitude",NORTH]]
Output file type = GreyTiff
Spatially unique = true
Environmentally unique = true\n""")
        request_file.write('Occurrences source = %s\n' % occurrences_path)
        request_file.write('Occurrences group = %s\n' % self.model_taxon)
        for layer in rasters:
            # We will use the same layers for both
            # model creation and projection
            request_file.write('Map = %s\n' % layer)
            request_file.write('Output map = %s\n' % layer)
        clean_name = self.model_taxon.replace(' ', '_')
        self.model_output = unique_filename(
            prefix=clean_name, suffix='.tif')
        # Just use the first raster as mask for now
        request_file.write('Mask = %s\n' % rasters[0])
        request_file.write('Output mask = %s\n' % rasters[0])
        # This determines the cell size and extents
        request_file.write('Output format = %s\n' % rasters[0])
        # Serialise the model created by openModeller
        model_path = unique_filename(prefix=clean_name, suffix='.xml')
        request_file.write('Output model = %s\n' % model_path)
        # Name of georeferenced output
        request_file.write('Output file = %s\n' % self.model_output)
        # Now write the algorithm name and parameters
        request_file.write(self.algorithm_parameters.toPlainText())

        request_file.close()

        om_console_path = QSettings().value(
            'SpeciesExplorer/om_console_path', False, type=str)

        if not os.path.exists(om_console_path):
            self.iface.messageBar().createMessage(
                'om_console not found',
                'Please check the search path in SpeciesExplorer options.')
            QgsMessageLog.logMessage(
                'Could not execute this this shell call:\n %s %s' % (
                    om_console_path, request_path),
                'SpeciesExplorer',
                0)
            return
        QgsMessageLog.logMessage(
            'executing this shell call:\n %s %s' % (
                om_console_path, request_path),
            'SpeciesExplorer',
            0)
        self._run_command(om_console_path, [request_path])


    def _update_fields(self, index):
        """Update the list of fields available for the selected point layer."""
        layer_id = self.point_layers.itemData(index)
        layer = QgsProject.instance().mapLayer(layerId=layer_id)
        fields = layer.fields()
        self.taxon_column.clear()
        for field in fields:
            if field.type() == QVariant.String:
                self.taxon_column.addItem(field.name())

    def _update_taxon_list(self, index):
        """Update the list of taxa available for the selected point layer."""
        self.taxon.clear()
        # Get the layer
        layer_id = self.point_layers.itemData(
            self.point_layers.currentIndex()
        )
        layer = QgsProject.instance().mapLayer(layerId=layer_id)
        # then the desired field
        field_name = self.taxon_column.currentText()
        # then iterate over the records collecting unique values and sort them
        unique_list = []
        for feature in layer.getFeatures():
            try:
                value = feature[field_name]
            except KeyError:
                return
            if value not in unique_list:
                unique_list.append(value)
        unique_list.sort()
        for value in unique_list:
            self.taxon.addItem(value)

    def _show_parameters(self, index):
        """Update the parametrs widget based on selected algorithm."""
        parameters = self.algorithm.itemData(index)
        self.algorithm_parameters.setPlainText(parameters)

    def _populate_point_layer_combo(self):
        """Set the list of vector layers."""
        layers = QgsProject.instance().mapLayers()
        QgsMessageLog.logMessage(
            'openModeller analysis using layers: %s' % layers,
            'SpeciesExplorer',
            0)
        for layer_id, layer in layers.items():
            if layer.type() == QgsMapLayer.RasterLayer:
                continue
            if layer.wkbType() == QgsWkbTypes.Point:
                self.point_layers.addItem(layer.name(), layer_id)

    def _populate_raster_list(self):
        """Set the list of raster layers."""
        layers = QgsProject.instance().mapLayers()
        for layer_id, layer in layers.items():
            if layer.type() == QgsMapLayer.RasterLayer:
                item = QtWidgets.QListWidgetItem(layer.name())
                item.setData(Qt.UserRole, layer_id)
                self.raster_layers.addItem(item)

    def _populate_algorithm_combo(self):
        algorithms = OrderedDict()
        algorithms['aquamaps'] = """
Algorithm = AQUAMAPS
Parameter = UseSurfaceLayers -1
Parameter = UseDepthRange 1
Parameter = UseIceConcentration 1
Parameter = UseDistanceToLand 0
Parameter = UsePrimaryProduction 1
Parameter = UseSalinity 1
Parameter = UseTemperature 1
            """
        algorithms['bioclim'] = """
Algorithm = BIOCLIM
Parameter = StandardDeviationCutoff 0.674
            """
        algorithms['climatic space model - broken-stick'] = """
Algorithm = CSMBS
Parameter = Randomisations 8
Parameter = StandardDeviations 2
Parameter = MinComponents 1
Parameter = VerboseDebugging 1
            """
        algorithms[
            'GARP: Genetic Algorithm for Rule Set Production (new implementation)'] = """
Algorithm = GARP
Parameter = MaxGenerations 400
Parameter = ConvergenceLimit 0.01
Parameter = PopulationSize 50
Parameter = Resamples 2500
            """
        algorithms[
            'GARP: Genetic Algorithm for Rule Set Production (original DesktopGarp implementation)'] = """
Algorithm = DG_GARP
Parameter = MaxGenerations 100
Parameter = ConvergenceLimit 0.05
Parameter = PopulationSize 50
Parameter = Resamples 2500
Parameter = MutationRate 0.25
Parameter = CrossoverRate 0.25
            """
        algorithms[
            'GARP with Best Subsets Procedure (using the new implementation)'] = """
Algorithm = GARP_BS
Parameter = TrainingProportion 50
Parameter = TotalRuns 20
Parameter = HardOmissionThreshold 100
Parameter = ModelsUnderOmissionThreshold 20
Parameter = CommissionThreshold 50
Parameter = CommissionSampleSize 10000
Parameter = MaxThreads 1
Parameter = MaxGenerations 400
Parameter = ConvergenceLimit 0.01
Parameter = PopulationSize 50
Parameter = Resamples 2500
            """
        algorithms[
            'GARP with Best Subsets Procedure (using the DesktopGarp implementation)'] = """
Algorithm = DG_GARP_BS
Parameter = TrainingProportion 50
Parameter = TotalRuns 10
Parameter = HardOmissionThreshold 100
Parameter = ModelsUnderOmissionThreshold 20
Parameter = CommissionThreshold 50
Parameter = CommissionSampleSize 10000
Parameter = MaxThreads 5
Parameter = MaxGenerations 20
Parameter = ConvergenceLimit 0.05
Parameter = PopulationSize 50
Parameter = Resamples 2500
Parameter = MutationRate 0.25
Parameter = CrossoverRate 0.25
            """
        algorithms['Environmental distance'] = """
Algorithm = ENVDIST
Valid values for the parameter DistanceType:
1=Euclidean, 2=Mahalanobis, 3=Manhattan, 4=Chebyshev
Parameter = DistanceType 1
Parameter = NearestPoints 1
Parameter = MaxDistance 0.1
            """
        algorithms['SVM'] = """
Algorithm = SVM
Parameter = SvmType 0
Parameter = KernelType 2
Parameter = Degree 3
Parameter = Gamma 0
Parameter = C 1
Parameter = Coef0 0
Parameter = Nu 0.5
Parameter = ProbabilisticOutput 0
Parameter = NumberOfPseudoAbsences 500
            """
        algorithms['Maximum Entropy'] = """
Algorithm = MAXENT
Parameter = NumberOfBackgroundPoints 10000
Parameter = UseAbsencesAsBackground 0
Parameter = IncludePresencePointsInBackground 1
Parameter = NumberOfIterations 500
Parameter = TerminateTolerance 0.00001
Valid values for the parameter Output Format:
1 = Raw, 2 = Logistic.
Parameter = OutputFormat 2
Valid values: enable = 1, disable = 0
Parameter = QuadraticFeatures 1
Valid values: enable = 1, disable = 0
Parameter = ProductFeatures 1
Valid values: enable = 1, disable = 0
Parameter = HingeFeatures 1
Valid values: enable = 1, disable = 0
Parameter = ThresholdFeatures 1
Valid values: enable = 1, disable = 0
Parameter = AutoFeatures 1
Parameter = MinSamplesForProductThreshold 80
Parameter = MinSamplesForQuadratic 10
Parameter = MinSamplesForHinge 15
            """
        algorithms['Artificial Neural Networks'] = """
Algorithm = ANN
Parameter = HiddenLayerNeurons 14
Parameter = LearningRate 0.3
Parameter = Momentum 0.05
Parameter = Choice 1
Parameter = Epoch 5000000
Parameter = MinimunError 0.01
            """
        algorithms['ENFA'] = """
Algorithm = ENFA
Parameter = NumberOfBackgroundPoints 10000
Parameter = NumberOfRetries 5
Parameter = DiscardMethod 2
Parameter = RetainComponents 2
Parameter = RetainVariation 0.75
Parameter = DisplayLoadings 0
Parameter = VerboseDebug 0
            """
        algorithms['Envelope score'] = """
Algorithm = ENVSCORE
            """
        algorithms['Niche Mosaic'] = """
Algorithm = NICHE_MOSAIC
Parameter = NumberOfIterations 2000
            """
        algorithms['Random Forests'] = """
Algorithm = RF
Parameter = NumTrees 10
Parameter = VarsPerTree 0
Parameter = ForceUnsupervisedLearning 0
            """
        algorithms['Consensus'] = """
Algorithm = CONSENSUS
Parameter = Alg1 RF(NumTrees=10,VarsPerTree=0,ForceUnsupervisedLearning=1)
Parameter = Alg2 BIOCLIM(StandardDeviationCutoff=0.8)
Parameter = Alg3 ENVSCORE
Parameter = Alg4
Parameter = Alg5
Parameter = Weights 1.0 1.0 1.0 0.0 0.0
Parameter = Agreement 2
            """
        algorithms['Virtual Niche Generator'] = """
Algorithm = VNG
Parameter = NumberOfBackgroundPoints 10000
Parameter = UseAbsencesAsBackground 0
Parameter = SuitabilityThreshold 1.0
Parameter = StandardDeviationFactor 0.0
            """
        for algorithm, parameters in algorithms.items():
            self.algorithm.addItem(algorithm, parameters)

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

    def style_layer(self, raster_layer):
        """Generate a probability ramp using range of 1-255.
    
        255 = high probability
        0 = low
    
        :param raster_layer: A raster layer that will have a style applied.
        :type raster_layer: QgsRasterLayer
    
        .. versionadded:: 0.2.0
        """
        instance = QgsColorRampShader()
        instance.setColorRampType(QgsColorRampShader.Interpolated)
        colour_range = [
            QgsColorRampShader.ColorRampItem(0, QColor(255, 0, 0)),
            QgsColorRampShader.ColorRampItem(255, QColor(0, 255, 0))
        ]
        instance.setColorRampItemList(colour_range)
        shader = QgsRasterShader()
        shader.setRasterShaderFunction(instance)
        renderer = QgsSingleBandPseudoColorRenderer(
            raster_layer.dataProvider(), 1, shader)
        raster_layer.setRenderer(renderer)
