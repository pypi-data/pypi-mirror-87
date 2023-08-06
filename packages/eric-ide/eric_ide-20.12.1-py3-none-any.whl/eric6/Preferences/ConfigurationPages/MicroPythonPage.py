# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the MicroPython configuration page.
"""

from E5Gui.E5PathPicker import E5PathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_MicroPythonPage import Ui_MicroPythonPage

import Preferences

from MicroPython.MicroPythonWidget import AnsiColorSchemes


class MicroPythonPage(ConfigurationPageBase, Ui_MicroPythonPage):
    """
    Class implementing the MicroPython configuration page.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MicroPythonPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("MicroPythonPage")
        
        self.colorSchemeComboBox.addItems(sorted(AnsiColorSchemes.keys()))
        
        # populate the chart theme combobox
        try:
            from PyQt5.QtChart import QChart
            
            self.chartThemeComboBox.addItem(
                self.tr("Automatic"), -1)
            self.chartThemeComboBox.addItem(
                self.tr("Light"), QChart.ChartThemeLight)
            self.chartThemeComboBox.addItem(
                self.tr("Dark"), QChart.ChartThemeDark)
            self.chartThemeComboBox.addItem(
                self.tr("Blue Cerulean"), QChart.ChartThemeBlueCerulean)
            self.chartThemeComboBox.addItem(
                self.tr("Brown Sand"), QChart.ChartThemeBrownSand)
            self.chartThemeComboBox.addItem(
                self.tr("Blue NCS"), QChart.ChartThemeBlueNcs)
            self.chartThemeComboBox.addItem(
                self.tr("High Contrast"), QChart.ChartThemeHighContrast)
            self.chartThemeComboBox.addItem(
                self.tr("Blue Icy"), QChart.ChartThemeBlueIcy)
            self.chartThemeComboBox.addItem(
                self.tr("Qt"), QChart.ChartThemeQt)
        except ImportError:
            self.chartThemeComboBox.setEnabled(False)
        
        self.mpyCrossPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.mpyCrossPicker.setFilters(self.tr("All Files (*)"))
        
        self.dfuUtilPathPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.dfuUtilPathPicker.setFilters(self.tr("All Files (*)"))
        
        # set initial values
        # serial link parameters
        self.timeoutSpinBox.setValue(
            Preferences.getMicroPython("SerialTimeout") / 1000)
        # converted to seconds
        self.syncTimeCheckBox.setChecked(
            Preferences.getMicroPython("SyncTimeAfterConnect"))
        
        # REPL Pane
        self.colorSchemeComboBox.setCurrentIndex(
            self.colorSchemeComboBox.findText(
                Preferences.getMicroPython("ColorScheme")))
        self.replWrapCheckBox.setChecked(
            Preferences.getMicroPython("ReplLineWrap"))
        
        # Chart Pane
        index = self.chartThemeComboBox.findData(
            Preferences.getMicroPython("ChartColorTheme"))
        if index < 0:
            index = 0
        self.chartThemeComboBox.setCurrentIndex(index)
        
        # MPY Cross Compiler
        self.mpyCrossPicker.setText(
            Preferences.getMicroPython("MpyCrossCompiler"))
        
        # PyBoard specifics
        self.dfuUtilPathPicker.setText(
            Preferences.getMicroPython("DfuUtilPath"))
        
        # firmware URL
        self.micropythonFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("MicroPythonFirmwareUrl"))
        self.circuitpythonFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("CircuitPythonFirmwareUrl"))
        self.microbitFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitFirmwareUrl"))
        self.calliopeFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("CalliopeFirmwareUrl"))
        
        # documentation URL
        self.micropythonDocuUrlLineEdit.setText(
            Preferences.getMicroPython("MicroPythonDocuUrl"))
        self.circuitpythonDocuUrlLineEdit.setText(
            Preferences.getMicroPython("CircuitPythonDocuUrl"))
        self.microbitDocuUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitDocuUrl"))
        self.calliopeDocuUrlLineEdit.setText(
            Preferences.getMicroPython("CalliopeDocuUrl"))
    
    def save(self):
        """
        Public slot to save the MicroPython configuration.
        """
        # serial link parameters
        Preferences.setMicroPython(
            "SerialTimeout",
            self.timeoutSpinBox.value() * 1000)
        # converted to milliseconds
        Preferences.setMicroPython(
            "SyncTimeAfterConnect",
            self.syncTimeCheckBox.isChecked())
        
        # REPL Pane
        Preferences.setMicroPython(
            "ColorScheme",
            self.colorSchemeComboBox.currentText())
        Preferences.setMicroPython(
            "ReplLineWrap",
            self.replWrapCheckBox.isChecked())
        
        # Chart Pane
        Preferences.setMicroPython(
            "ChartColorTheme",
            self.chartThemeComboBox.currentData())
        
        # MPY Cross Compiler
        Preferences.setMicroPython(
            "MpyCrossCompiler",
            self.mpyCrossPicker.text())
        
        # PyBoard specifics
        Preferences.setMicroPython(
            "DfuUtilPath",
            self.dfuUtilPathPicker.text())
        
        # firmware URL
        Preferences.setMicroPython(
            "MicroPythonFirmwareUrl",
            self.micropythonFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "CircuitPythonFirmwareUrl",
            self.circuitpythonFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicrobitFirmwareUrl",
            self.microbitFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "CalliopeFirmwareUrl",
            self.calliopeFirmwareUrlLineEdit.text())
        
        # documentation URL
        Preferences.setMicroPython(
            "MicroPythonDocuUrl",
            self.micropythonDocuUrlLineEdit.text())
        Preferences.setMicroPython(
            "CircuitPythonDocuUrl",
            self.circuitpythonDocuUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicrobitDocuUrl",
            self.microbitDocuUrlLineEdit.text())
        Preferences.setMicroPython(
            "CalliopeDocuUrl",
            self.calliopeDocuUrlLineEdit.text())


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    return MicroPythonPage()
