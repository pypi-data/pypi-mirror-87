# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : September 2020
| Copyright           : © 2020 by Arthur Maenhout (Locus) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Jeroen Degerickx (KU Leuven). Documentation: https://doi.org/10.3390/rs9060565.
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
from qgis.utils import iface
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from spectral_libraries.interfaces.imports import import_image, import_library_as_array, \
    detect_reflectance_scale_factor, import_library
from spectral_libraries.core.music import Music


class MusicWidget(QDialog):
    """ Main GUI widget to set up the Music environment (library, constraints, image, ...) """

    def __init__(self):
        super(MusicWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'music.ui'), self)

        # Library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)

        # Input
        self.browseImage.lineEdit().setReadOnly(True)
        self.browseImage.fileChanged.connect(self._image_browse)

        # Output
        self.browseOut.lineEdit().setReadOnly(True)
        self.browseOut.lineEdit().setPlaceholderText('The Music result (models) ...')
        self.browseOut.setStorageMode(QgsFileWidget.SaveFile)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openInQGIS.setChecked(False)
            self.openInQGIS.setDisabled(True)

        # Run Music
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_music)
        self.OKClose.rejected.connect(self.close)

        # Music widget variables
        self.image = None
        self.library_path = None
        self.library_object = None
        self.library = None

    def log(self, text):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _library_browse(self, path):
        """ The user browses for a library. Set pruned library size
            :param path: the absolute path to the Spectral Library
        """
        if path == '':
            return

        try:
            self.library_path = path
            self.library_object = import_library(path)
            self.library, _, _ = import_library_as_array(path)
            self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))
            self.sizeValue.setValue(int(np.round(self.library.shape[1] * 0.9)))

            # set default output name(s)
            basename, extension = os.path.splitext(path)
            output = '{}_music{}'.format(basename, extension)
            self.browseOut.lineEdit().setText(output)

        except ValueError as e:
            self.log(e)
            self.browseLibrary.setFilePath('')
        except Exception as e:
            self.log(e)
            self.browseLibrary.setFilePath('')

    def _image_browse(self, path):
        """ When the users browses for an image, set the factor and the min eigenvectors
        :param path: the absolute path to the image
        """
        if path == '':
            return
        try:
            self.image = import_image(path)
            self.imageScaleValue.setValue(detect_reflectance_scale_factor(self.image))

        except Exception as e:
            self.log(e)
            self.image_path = None
            self.browseImage.setFilePath('')

    def _run_music(self):
        """ Read all parameters and pass them on to the Music Applier class 'Music'. """

        try:
            if self.image is None:
                raise Exception('Choose an image')

            if self.library is None:
                raise Exception('Choose a spectral library')

            # Output file
            output = self.browseOut.filePath()
            if len(output) == 0:
                basename, extension = os.path.splitext(self.library_path)
                output = '{}_music{}'.format(basename, extension)

            result = Music().execute(library=self.library/self.libraryScaleValue.value(),
                                     image=self.image/self.imageScaleValue.value(),
                                     library_size=self.sizeValue.value(),
                                     min_eig=self.eigenvectorValue.value(),
                                     log=self.log)
            if result is None:
                raise Exception("No spectra in the final result. Output empty.")

            self.progressBar.setValue(80)

            # write output library
            profiles_list = list(self.library_object.profiles())
            fid_attribute_index = profiles_list[0].fieldNameIndex('fid')
            fid_list = [profiles_list[x].attributes()[fid_attribute_index] for x in result['music_indices']]

            new_library = self.library_object.speclibFromFeatureIDs(fid_list)
            new_library.write(path=output)

            self.progressBar.setValue(100)

        except ValueError as e:
            self.log(e)
        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = MusicWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
