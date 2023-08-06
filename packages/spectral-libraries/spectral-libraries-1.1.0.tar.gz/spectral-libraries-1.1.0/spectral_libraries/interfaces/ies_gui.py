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
import numpy as np

from qgis.gui import QgsFileWidget
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from spectral_libraries.interfaces.imports import import_library, import_library_metadata, import_library_as_array, \
    detect_reflectance_scale_factor
from spectral_libraries.interfaces.exports import save_ies_metadata
from spectral_libraries.core.ies import Ies


class IesWidget(QDialog):
    """ QDialog to interactively set up the IES input and output. """

    def __init__(self):
        super(IesWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'ies.ui'), self)

        # library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)

        # forced library
        self.forcedDropDown.checkedItemsChanged.connect(self._select_endmembers)

        # output
        self.browseOut.lineEdit().setReadOnly(True)
        self.browseOut.lineEdit().setPlaceholderText('The output spectral library (.sli) ...')
        self.browseOut.setStorageMode(QgsFileWidget.SaveFile)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_ies)
        self.OKClose.rejected.connect(self.close)

        # widget variables
        self.library = None
        self.library_object = None
        self.library_path = None
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
        if path == '':
            return

        try:
            # get te library and spectra_names
            self.library_object = import_library(path)
            self.library, spectra_names, _ = import_library_as_array(path, spectra_names=True)
            self.spectra_names = list(spectra_names)
            self.library_path = os.path.basename(path)

            # set the library reflectance scale factor
            self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))

            # add spectra to drop down
            self.forcedDropDown.clear()
            self.forcedDropDown.addItems(self.spectra_names)

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

    def _select_endmembers(self):
        try:
            count = len(self.forcedDropDown.checkedItems())
            self.forcedLabel.setText(str(count) + " selected")
        except Exception as e:
            self.log(e)

    def _run_ies(self, test_mode=False):
        """ Read all parameters and pass them on to the SquareArray class. """
        try:
            if self.library is None:
                raise Exception('Choose a spectral library.')

            # Read the constraints
            con = (self.minFracValue.value(), self.maxFracValue.value(), self.maxRMSEValue.value())

            # Get the class_list
            class_name = self.classDropDown.currentText()
            if class_name == "Select ...":
                raise Exception('Choose a metadata class.')
            class_str = import_library_metadata(self.library_object, metadata=class_name)
            class_unique, class_list = np.unique(class_str, return_inverse=True)

            if len(class_unique) == 1:
                raise Exception('IES requires more than one class, please select another column')

            # Output file
            if self.browseOut.filePath() == '':
                raise Exception('Specify an output file.')
            else:
                output_file = self.browseOut.filePath()

            # Forced endmembers
            if self.forcedGroup.isChecked():
                items = self.forcedDropDown.checkedItems()
                if len(items) == 0:
                    raise Exception('No endmembers selected to forcefully add to the ies process.')
                else:
                    forced_list = np.array([self.spectra_names.index(x) for x in items])
                    forced_step = self.forcedStep.value()
            else:
                forced_list = None
                forced_step = None

            # Run IES
            ies_selection, ies_metadata = Ies().execute(library=self.library/self.libraryScaleValue.value(),
                                                        class_list=class_list, constraints=con,
                                                        forced_list=forced_list, forced_step=forced_step, summary=True,
                                                        set_progress=self.progressBar.setValue, log=self.log)

            if ies_selection is None:
                raise Exception("IES selected no spectra. Output empty.")

            # write output library and metadata file
            profiles_list = list(self.library_object.profiles())
            fid_attribute_index = profiles_list[0].fieldNameIndex('fid')
            fid_list = [profiles_list[x].attributes()[fid_attribute_index] for x in ies_selection]

            ies_library = self.library_object.speclibFromFeatureIDs(fid_list)
            ies_library.write(path=output_file)

            save_ies_metadata(metadata=ies_metadata, library_path=self.library_path,
                              outfile_path=os.path.splitext(output_file)[0] + '_summary.txt',
                              forced_list=forced_list, forced_position=forced_step,
                              class_header=class_name,
                              class_list=class_str,
                              spectra_names=self.spectra_names,
                              selection=ies_selection)
            if not test_mode:
                os.startfile(os.path.splitext(output_file)[0] + '_summary.txt')
            self.progressBar.setValue(100)

        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = IesWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
