# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
| Copyright           : © 2018 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab).
|                       Dar Roberts, Kerry Halligan, Philip Dennison, Kenneth Dudley, Ben Somers, Ann Crabbé
|
| This file is part of the Spectral Libraries QGIS plugin and python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
import os

from qgis.gui import QgsFileWidget
from qgis.core import QgsField
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from spectral_libraries.interfaces.imports import import_library, import_library_metadata, import_library_as_array, \
    detect_reflectance_scale_factor
from spectral_libraries.core.ear_masa_cob import EarMasaCob


class EarMasaCobWidget(QDialog):
    """ QDialog to interactively set up the Ear/Masa/Cob input and output. """

    def __init__(self):
        super(EarMasaCobWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'ear_masa_cob.ui'), self)

        # library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)

        # Constraints
        self.constraintsGroup.clicked.connect(self._main_constraints_clicked)
        self.minFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxRMSECheck.clicked.connect(self._sub_constraints_clicked)

        # output
        self.browseOut.lineEdit().setReadOnly(True)
        self.browseOut.lineEdit().setPlaceholderText('The Spectral Library output file (.sli) ...')
        self.browseOut.setStorageMode(QgsFileWidget.SaveFile)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_ear_masa_cob)
        self.OKClose.rejected.connect(self.close)

        # widget variables
        self.library = None
        self.library_object = None

    def log(self, text):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _library_browse(self, path):
        """ When the users browses for a library, set the reflectance scale factor and output file automatically.
        :param path: the absolute path to the Spectral Library
        """
        if path == '':
            return

        try:
            # get te library and spectra_names
            self.library_object = import_library(path)
            self.library, _, _ = import_library_as_array(path)

            # set the library reflectance scale factor
            self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))

            # add metadata values to drop down
            self.classDropDown.clear()
            self.classDropDown.addItems(['Select ...'] + self.library_object.fieldNames())

            # set default output name
            out_path = os.path.splitext(path)[0] + '_ies.sli'
            if not os.path.exists(out_path):
                self.browseOut.lineEdit().setText(out_path)

        except Exception as e:
            self.browseLibrary.setFilePath('')
            self.log(e)

    def _main_constraints_clicked(self, checked):
        """ Disable the constraints band when no constraints are chosen in general.
        :param checked: state of the checkbox
        """
        try:
            if checked is False:
                self.outConstrCheck.setCheckState(Qt.Unchecked)
                self.outConstrCheck.setEnabled(False)
            else:
                self.outConstrCheck.setEnabled(True)
        except Exception as e:
            self.log(e)

    def _sub_constraints_clicked(self):
        """ Disable the constraints band and reset option when all individual constraints are checked off. """
        try:
            min_frac = self.minFracCheck.isChecked()
            max_frac = self.maxFracCheck.isChecked()
            max_rmse = self.maxRMSECheck.isChecked()

            if not min_frac and not max_frac and not max_rmse:
                self.outConstrCheck.setCheckState(Qt.Unchecked)
                self.outConstrCheck.setEnabled(False)
                self.resetCheck.setEnabled(False)
            else:
                self.outConstrCheck.setEnabled(True)
                self.resetCheck.setEnabled(True)
        except Exception as e:
            self.log(e)

    def _run_ear_masa_cob(self):
        """ Read all parameters and pass them on to the SquareArray class. """
        try:
            if self.library is None:
                raise Exception('Choose a spectral library.')

            # Read the constraints
            con = [-9999, -9999, -9999]
            if self.constraintsGroup.isChecked():
                if self.minFracCheck.isChecked():
                    con[0] = self.minFracValue.value()
                if self.maxFracCheck.isChecked():
                    con[1] = self.maxFracValue.value()
                if self.maxRMSECheck.isChecked():
                    con[2] = self.maxRMSEValue.value()
            con = None if con == [-9999, -9999, -9999] else tuple(con)
            use_reset = self.resetCheck.isChecked()

            # Get the class_list
            class_name = self.classDropDown.currentText()
            if class_name == "Select ...":
                raise Exception('Choose a metadata class.')
            class_list = import_library_metadata(self.library_object, class_name)

            # Run EMC
            result = EarMasaCob().execute(library=self.library/self.libraryScaleValue.value(),
                                          class_list=class_list, constraints=con, reset=use_reset)

            # append metadata to spectral library
            self.library_object.startEditing()
            self.library_object.addAttribute(QgsField(name="EAR", type=QVariant.Double))
            self.library_object.addAttribute(QgsField(name="MASA", type=QVariant.Double))
            if con:
                self.library_object.addAttribute(QgsField(name="InCOB", type=QVariant.Int))
                self.library_object.addAttribute(QgsField(name="OutCOB", type=QVariant.Int))
                self.library_object.addAttribute(QgsField(name="COBI", type=QVariant.Double))
            self.library_object.commitChanges()

            # add extra attribute data
            self.library_object.startEditing()

            fields = self.library_object.fields()
            ear_index = fields.indexFromName("EAR")
            masa_index = fields.indexFromName("MASA")
            profiles = self.library_object.profiles()
            for (profile, ear, masa) in zip(profiles, result[0], result[1]):
                self.library_object.changeAttributeValue(profile.id(), ear_index, ear)
                self.library_object.changeAttributeValue(profile.id(), masa_index, masa)

            if con:
                cob_in_index = fields.indexFromName("InCOB")
                cob_out_index = fields.indexFromName("OutCOB")
                cob_ratio_index = fields.indexFromName("COBI")
                profiles = self.library_object.profiles()         # again  because iterator
                for (profile, ci, co, cr) in zip(profiles, result[2], result[3], result[4]):
                    self.library_object.changeAttributeValue(profile.id(), cob_in_index, ci)
                    self.library_object.changeAttributeValue(profile.id(), cob_out_index, co)
                    self.library_object.changeAttributeValue(profile.id(), cob_ratio_index, cr)

            # Export to new library
            self.library_object.write(self.browseOut.filePath())

            self.progressBar.setValue(100)

        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = EarMasaCobWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
