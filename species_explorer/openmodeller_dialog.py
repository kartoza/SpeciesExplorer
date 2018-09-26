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
from collections import OrderedDict
from subprocess import call, CalledProcessError
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject, QgsMessageLog
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QVariant
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
        # Widgets
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
        algorithms['GARP: Genetic Algorithm for Rule Set Production (new implementation)'] = """
            Algorithm = GARP
            Parameter = MaxGenerations 400
            Parameter = ConvergenceLimit 0.01
            Parameter = PopulationSize 50
            Parameter = Resamples 2500
            """
        algorithms['GARP: Genetic Algorithm for Rule Set Production (original DesktopGarp implementation)'] = """
            Algorithm = DG_GARP
            Parameter = MaxGenerations 100
            Parameter = ConvergenceLimit 0.05
            Parameter = PopulationSize 50
            Parameter = Resamples 2500
            Parameter = MutationRate 0.25
            Parameter = CrossoverRate 0.25
            """
        algorithms['GARP with Best Subsets Procedure (using the new implementation)'] = """
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
        algorithms['GARP with Best Subsets Procedure (using the DesktopGarp implementation)'] = """
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
