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
import time
import numpy as np

from qgis.gui import QgsFileWidget
from qgis.utils import iface
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from spectral_libraries.interfaces.imports import import_library_as_array, detect_reflectance_scale_factor
from spectral_libraries.interfaces.exports import save_square_to_envi
from spectral_libraries.core.square_array import SquareArray


class SquareArrayWidget(QDialog):
    """ QDialog to interactively set up the Square Array input and output. """

    def __init__(self):
        super(SquareArrayWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'square_array.ui'), self)

        # Library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)

        # Constraints
        self.constraintsGroup.clicked.connect(self._main_constraints_clicked)
        self.minFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxRMSECheck.clicked.connect(self._sub_constraints_clicked)

        # Output
        self.browseOut.lineEdit().setReadOnly(True)
        self.browseOut.lineEdit().setPlaceholderText('The SquareArray file (.sqr) ...')
        self.browseOut.setStorageMode(QgsFileWidget.SaveFile)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openInQGIS.setChecked(False)
            self.openInQGIS.setDisabled(True)

        # Run or Cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_square_array)
        self.OKClose.rejected.connect(self.close)

        # SquareArrayWidget variables
        self.library = None
        self.spectra_names = None

    def log(self, text):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _library_browse(self, path):
        """ When the users browses for a library, set the reflectance scale factor and output file automatically.
        :param path: the absolute path to the Spectral Library
        """
        try:
            if path == '':
                return

            # get te library and spectra_names
            self.library, self.spectra_names, _ = import_library_as_array(path, spectra_names=True)

            # set the library reflectance scale factor
            self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))

            # set default output name
            path_no_extension = os.path.splitext(path)[0]
            self.browseOut.lineEdit().setText(path_no_extension + '_sq.sqr')

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

    def _run_square_array(self):
        """ Read all parameters and pass them on to the SquareArray class. """
        try:
            # Check that a library is given
            if self.library is None:
                raise Exception('Choose a spectral library.')

            # Read the constraints
            constraints = [-9999, -9999, -9999]
            if self.constraintsGroup.isChecked():
                if self.minFracCheck.isChecked():
                    constraints[0] = self.minFracValue.value()
                if self.maxFracCheck.isChecked():
                    constraints[1] = self.maxFracValue.value()
                if self.maxRMSECheck.isChecked():
                    constraints[2] = self.maxRMSEValue.value()
            constraints = tuple(constraints)
            use_reset = self.resetCheck.isChecked()

            # Get output preferences
            out_rmse = self.outRmseCheck.isChecked()
            out_constraints = self.outConstrCheck.isChecked()
            out_angle = self.outAngleCheck.isChecked()
            out_fractions = self.outFracCheck.isChecked()
            out_shade = self.outShadeCheck.isChecked()
            if not out_rmse and not out_constraints and not out_angle and not out_fractions and not out_shade:
                raise Exception('At least one output band must be selected.')

            # Run square_array.py
            start = time.time()
            square_array = SquareArray().execute(library=self.library/self.libraryScaleValue.value(), reset=use_reset,
                                                 constraints=constraints, out_rmse=out_rmse, out_angle=out_angle,
                                                 out_fractions=out_fractions, out_constraints=out_constraints,
                                                 out_shade=out_shade, set_progress=self.progressBar.setValue,
                                                 log=self.log)
            duration = np.float16(time.time() - start)
            self.log('Process finished in ' + str(duration) + ' seconds')

            self.log("Writing to disk...")
            save_square_to_envi(square_array=square_array, outfile_path=self.browseOut.filePath(), duration=duration,
                                spectra_names=self.spectra_names, constraints=constraints, reset=use_reset,
                                library_name=os.path.basename(self.browseLibrary.filePath()), ngb=self.library.shape[0])
            self.log("Done.")
            if self.openInQGIS.isChecked():
                iface.addRasterLayer(self.browseOut.filePath(), "Square Array")

        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = SquareArrayWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
