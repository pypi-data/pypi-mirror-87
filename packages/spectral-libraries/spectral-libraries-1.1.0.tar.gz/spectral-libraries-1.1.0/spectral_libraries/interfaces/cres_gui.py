# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : June 2018
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

from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, Qt, QSortFilterProxyModel, QVariant
from qgis.PyQt.QtWidgets import QLabel, QMainWindow, QSpinBox, QAbstractItemView, QFileDialog

from spectral_libraries.interfaces.imports import import_library, detect_reflectance_scale_factor, import_library_as_array, \
    import_library_metadata
from spectral_libraries.core.cres import Cres


# noinspection PyUnresolvedReferences
class CresWidget(QMainWindow):
    """
    QDialog to interactively set up the CRES  input and output (library, image spectrum, fraction estimates, ...).
    """

    def __init__(self):
        super(CresWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'cres.ui'), self)

        # Library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)
        self.classDropDown.currentTextChanged.connect(self._get_class_from_list)

        # Image Spectrum
        self.browseImage.lineEdit().setReadOnly(True)
        self.browseImage.fileChanged.connect(self._image_browse)

        # Shade spectrum
        self.browseShade.lineEdit().setReadOnly(True)
        self.browseShade.fileChanged.connect(self._shade_browse)

        # Shade spinbox
        self.shade_spinbox = QSpinBox()
        self.shade_spinbox.setMaximum(100)
        self.shade_spinbox.setDisabled(True)

        # Run CRES
        self.cres_object = Cres()
        self.calculateFractionsButton.clicked.connect(self._calculate_sma)
        self.calculateIndexButton.clicked.connect(self._calculate_index)

        # Filters
        self.filterRMSECheck.clicked.connect(self._set_filter_rmse)
        self.filterMinFracCheck.clicked.connect(self._set_filter_min_frac)
        self.filterMaxFracCheck.clicked.connect(self._set_filter_max_frac)
        self.filterRMSEValue.valueChanged.connect(self._filter_rmse)
        self.filterMinFracValue.valueChanged.connect(self._filter_min_frac)
        self.filterMaxFracValue.valueChanged.connect(self._filter_max_frac)

        # Export
        self.exportButton.clicked.connect(self._export)

        # Table
        self.table_model = CresTableModel()
        self.filter_model = SortFilterProxyModel()
        self.filter_model.setSourceModel(self.table_model)
        self.tableView.setModel(self.filter_model)
        self.tableView.setSortingEnabled(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_model.dataChanged.connect(self._update)

        # CRES widget variables
        self.image = None
        self.spectral_library_object = None
        self.class_list = None
        self.spectrum_names = None
        self.spectrum_names_per_class = {}
        self.shade = np.array([])

    def log(self, text: str):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _image_browse(self, path):
        """ When the users browses for a library, set the reflectance scale factor and the metadata drop down list.

        :param path: the absolute path to the image spectrum library
        """
        if path == '':
            return

        try:
            self.spectrumDropDown.clear()

            self.image, spectra_names, _ = import_library_as_array(path, spectra_names=True)
            self.imageScaleValue.setValue(detect_reflectance_scale_factor(self.image))

            # set drop down with spectra
            self.spectrumDropDown.addItems(['Select ...'] + list(spectra_names))
            if len(spectra_names) == 1:
                self.spectrumDropDown.setCurrentIndex(1)

        except Exception as e:
            self.log(e)
            self.browseImage.setFilePath('')

    def _library_browse(self, path):
        """ When the users browses for a library, set the reflectance scale factor and the metadata drop down list.

        :param path: the absolute path to the Spectral Library
        """
        if path == '':
            return

        try:
            self.classDropDown.clear()

            self.spectral_library_object = import_library(path)
            self.library, self.spectrum_names, _ = import_library_as_array(path, spectra_names=True)

            # set the library reflectance scale factor
            self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))

            # set the class drop down
            self.classDropDown.addItems(['Select ...'] + self.spectral_library_object.fieldNames())

        except Exception as e:
            self.log(e)
            self.browseImage.setFilePath('')

    def _get_class_from_list(self, class_name):
        """ Initiate MesmaModels with the selected metadata header and display a summary of the initial setup.

        :param index: the index of the metadata headers
        """
        try:
            if class_name == "Select ...":
                return

            self.class_list = import_library_metadata(self.spectral_library_object, class_name)
            unique_classes = np.unique(self.class_list)

            # check state for each endmember as unchecked
            n_models = 1
            for i, cl in enumerate(unique_classes):
                self.spectrum_names_per_class[cl] = {}
                names = self.spectrum_names[np.where(self.class_list == cl)[0]]
                n_models = n_models * len(names)
                for name in names:
                    self.spectrum_names_per_class[cl][name] = Qt.Unchecked

            # update label with number of models
            self.nModelsLabel.setText("Number of models:  " + str(n_models))
            # clear fractions group box and set new widgets:
            layout_fr = self.fractionsBox.layout()
            while layout_fr.count():
                widget_to_remove = layout_fr.itemAt(0).widget()
                layout_fr.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)

            for i, em_class in enumerate(unique_classes):
                layout_fr.addWidget(QLabel(text=em_class), i, 0)
                spinbox = QSpinBox()
                spinbox.setMaximum(100)
                spinbox.valueChanged.connect(self._set_shade_fraction)
                layout_fr.addWidget(spinbox, i, 1)

            label = QLabel(text='shade')
            label.setDisabled(True)
            layout_fr.addWidget(label, len(unique_classes), 0)
            layout_fr.addWidget(self.shade_spinbox, len(unique_classes), 1)

            layout_we = self.weightsBox.layout()
            while layout_we.count():
                widget_to_remove = layout_we.itemAt(0).widget()
                layout_we.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)

            for i, em_class in enumerate(unique_classes):
                layout_we.addWidget(QLabel(text='weight ' + em_class), i, 0)
                spinbox = QSpinBox()
                spinbox.setRange(1, 10)
                layout_we.addWidget(spinbox, i, 1)

            layout_we.addWidget(QLabel(text='weight RMSE'), len(unique_classes), 0)
            spinbox = QSpinBox()
            spinbox.setRange(1, 10)
            layout_we.addWidget(spinbox, len(unique_classes), 1)

        except Exception as e:
            self.log(e)

    def _shade_browse(self, path):
        """ When the users browses for a shade spectrum, set the reflectance scale factor.

        :param path: the absolute path to the Spectral Library
        """
        if path == '':
            return

        try:
            self.shade, _, _ = import_library_as_array(path)

            # shade can only be one spectrum
            if self.shade.shape[1] > 1:
                raise Exception("Library can only have one spectrum.")

            # set the shade reflectance scale factor
            self.shadeScaleValue.setValue(detect_reflectance_scale_factor(self.shade))

        except Exception as e:
            self.log(e)
            self.shade = None
            self.browseShade.setFilePath('')

    def _set_shade_fraction(self):
        try:
            target_fractions = 0
            for item in self.fractionsBox.children():
                if isinstance(item, QSpinBox) and item != self.shade_spinbox:
                    target_fractions += item.value()

            if target_fractions != 0:
                self.shade_spinbox.setValue(100 - target_fractions)

        except Exception as e:
            self.log(e)

    def _calculate_sma(self):
        """ Read all parameters and run CRES. """
        try:
            if self.image is None:
                raise Exception('Choose an library with image spectra.')
            if self.spectral_library_object is None:
                raise Exception('Choose a spectral library.')
            if self.spectrumDropDown.currentIndex() == 0:
                raise Exception('Choose one spectrum from the image spectra.')
            if self.classDropDown.currentIndex() == 0:
                raise Exception('Choose a class from the library metadata drop down list.')

            image_spectrum = self.image[:, self.spectrumDropDown.currentIndex() - 1] / self.imageScaleValue.value()

            if len(image_spectrum) != self.library.shape[0]:
                raise Exception('The image and library have different number of bands. CRES not possible.')
            if self.shade.size != 0 and self.shade.shape[0] != self.library.shape[0]:
                raise Exception('The library and shade spectrum have different number of bands. CRES not possible.')

            if self.shade is not None:
                self.shade = self.shade / self.shadeScaleValue.value()

            self.cres_object.execute(signal=image_spectrum,
                                     library=self.library / self.libraryScaleValue.value(),
                                     classes=self.class_list,
                                     spectrum_names=self.spectrum_names,
                                     rmse_constraint=self.maxRMSESpinBox.value(),
                                     shade=self.shade)
            self.table_model.insertHeader(self.cres_object.get_header())
            self.table_model.resetRows(self.cres_object.get_fractions(), self.spectrum_names_per_class)
            self.nModelsShown.setText("# models shown: " + str(self.table_model.rowCount()))

        except Exception as e:
            self.log(e)

    def _calculate_index(self):
        try:
            target_fractions = []
            for item in self.fractionsBox.children():
                if isinstance(item, QSpinBox):
                    target_fractions.append(item.value() / 100)

            if sum(target_fractions) != 1:
                raise Exception('The target fractions should sum to 100.')

            weights = []
            for item in self.weightsBox.children():
                if isinstance(item, QSpinBox):
                    weights.append(item.value())

            indices = self.cres_object.index(target_fractions=target_fractions, weight_per_target=weights[:-1],
                                             weight_rmse=weights[-1])
            self.table_model.addColumns(indices)

        except Exception as e:
            self.log(e)

    def _update(self):
        try:
            self.tableView.update()
            self.nModelsSelected.setText("# models selected: " + str(self.table_model.number_selected()))
        except Exception as e:
            self.log(e)

    def _set_filter_rmse(self, checked: bool = False):
        try:
            self._filter_rmse(value=self.filterRMSEValue.value()) if checked else self._filter_rmse()
        except Exception as e:
            self.log(e)

    def _filter_rmse(self, value: float = None):
        try:
            self.filter_model.setRMSEFilter(value=value)
            table_model = self.table_model
            table_model.dataChanged.emit(table_model.createIndex(0, 0),
                                         table_model.createIndex(table_model.rowCount() - 1,
                                                                 table_model.columnCount() - 1))
            self.nModelsShown.setText("# models shown: " + str(self.filter_model.rowCount()))

        except Exception as e:
            self.log(e)

    def _set_filter_min_frac(self, checked: bool = False):
        try:
            self._filter_min_frac(value=self.filterMinFracValue.value()) if checked else self._filter_min_frac()
        except Exception as e:
            self.log(e)

    def _filter_min_frac(self, value: float = None):
        try:
            self.filter_model.setMinFractionFilter(value=value)
            table_model = self.table_model
            table_model.dataChanged.emit(table_model.createIndex(0, 0),
                                         table_model.createIndex(table_model.rowCount() - 1,
                                                                 table_model.columnCount() - 1))

            self.nModelsShown.setText("# models shown: " + str(self.filter_model.rowCount()))

        except Exception as e:
            self.log(e)

    def _set_filter_max_frac(self, checked: bool = False):
        try:
            self._filter_max_frac(value=self.filterMaxFracValue.value()) if checked else self._filter_max_frac()
        except Exception as e:
            self.log(e)

    def _filter_max_frac(self, value: float = None):
        try:
            self.filter_model.setMaxFractionFilter(value=value)
            table_model = self.table_model
            table_model.dataChanged.emit(table_model.createIndex(0, 0),
                                         table_model.createIndex(table_model.rowCount() - 1,
                                                                 table_model.columnCount() - 1))
            self.nModelsShown.setText("# models shown: " + str(self.filter_model.rowCount()))

        except Exception as e:
            self.log(e)

    def _export(self):
        try:
            cres_selection = []

            i = 0
            for cl in self.table_model.spectrum_names_per_class:
                for spectrum in self.table_model.spectrum_names_per_class[cl]:
                    if self.table_model.spectrum_names_per_class[cl][spectrum] == Qt.Checked:
                        cres_selection.append(i)
                    i += 1

            if not cres_selection:
                raise Exception("No spectra selected.")

            output_path = QFileDialog.getSaveFileName(caption="Save as Spectral Library...",
                                                      filter="Spectral Library file (*.sli);;All Files (*)")[0]

            # write output library and metadata file
            profiles_list = list(self.spectral_library_object.profiles())
            fid_attribute_index = profiles_list[0].fieldNameIndex('fid')
            fid_list = []
            for selection in cres_selection:
                fid_list.append(profiles_list[selection].attributes()[fid_attribute_index])

            cres_library = self.spectral_library_object.speclibFromFeatureIDs(fid_list)
            cres_library.write(path=output_path)

        except Exception as e:
            self.log(e)


class CresTableModel(QAbstractTableModel):
    """ A QAbstractTableModel to handle CRES table information. """

    def __init__(self, parent=None):
        super(CresTableModel, self).__init__(parent)
        self.header = []
        self.models = []
        self.n_base_columns = 0
        self.spectrum_names_per_class = {}

    def __len__(self) -> int:
        return len(self.models)

    def resetRows(self, models: list, spectrum_names_per_class: dict):
        """"
        Reset the table content. Remove all rows and then add al new models.

        :param models: A list of models and their info (name, fractions, rmse...) stored in dictionaries. Dictionary
                       keys are the same as the header items.
        :param spectrum_names_per_class: A dictionary per class containing all spectra names and their check state.
        """
        self.beginRemoveRows(QModelIndex(), 0, len(self) - 1)
        del self.models[:]
        self.endRemoveRows()

        self.beginInsertRows(QModelIndex(), 0, len(models) - 1)
        self.models.extend(models)
        self.spectrum_names_per_class = spectrum_names_per_class
        self.endInsertRows()

        self.n_base_columns = len(self.header)

    def insertHeader(self, header: list):
        """
        Insert the header as columns, in order to set the correct number of columns.

        :param header: A list of header names [list-of-strings]
        """
        self.beginRemoveColumns(QModelIndex(), 0, len(self.header) - 1)
        del self.header[:]
        self.endRemoveColumns()

        self.beginInsertColumns(QModelIndex(), 0, len(header) - 1)
        self.header.extend(header)
        self.endInsertColumns()

    def addColumns(self, columns):
        """
        Add new columns to the table with indices. In cse they are already there: replace them.

        :param columns: A dictionary with additional index information for each model.
        """
        if len(self.header) != self.n_base_columns:
            self.beginRemoveColumns(QModelIndex(), self.n_base_columns, len(self.header) - 1)
            self.header = self.header[: self.n_base_columns]
            self.endRemoveColumns()

        self.beginInsertColumns(QModelIndex(), len(self.header), len(self.header) + len(columns) - 1)
        for key in columns:
            column_name = key + "_index"
            self.header.append(column_name)
            for model, new_value in zip(self.models, columns[key]):
                model[column_name] = new_value
        self.endInsertColumns()

    def rowCount(self, index=None):
        """
        The number of rows in the table. Overwritten from parent class.

        :param index: unused
        """
        return len(self.models)

    def columnCount(self, index=None):
        """
        The number of columns in the table. Overwritten from parent class.

        :param index: unused
        """
        return len(self.models[0]) if len(self.models) > 0 else 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """
        Access the data correctly to display in each cell. Overwritten from parent class.

        :param index: The index of the table cell.
        :param role: A value from the Qt.ItemDataRole enumeration.
        """
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole:
            return str(self.models[index.row()][self.header[index.column()]])
        elif role == Qt.CheckStateRole:
            column_name = self.header[index.column()]
            name_end = column_name.find('_name')
            if name_end > 0:
                return self.spectrum_names_per_class[column_name[:name_end]][index.data()]
            else:
                return QVariant()
        else:
            return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """
        Display the header data (horizontally and vertically) correctly.

        :param section: Column number in case of horizontal header, row number in case of vertical header.
        :param orientation: A value from the Qt.Orientation enumeration.
        :param role: A value from the Qt.ItemDataRole enumeration.
        """

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if self.header:
                return self.header[section]
            else:
                return section
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section
        return None

    def flags(self, index: QModelIndex):
        """ Implementation of the QAbstractTableModel function flags. """
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        column_name = self.header[index.column()]
        if column_name.find('_name') > 0:
            flags = flags | Qt.ItemIsUserCheckable
        return flags

    def setData(self, index: QModelIndex, value: QVariant, role: int = Qt.EditRole):
        """ Implementation of the QAbstractTableModel function setData. """

        if not index.isValid():
            return False

        column_name = self.header[index.column()]
        name_end = column_name.find('_name')

        if role == Qt.CheckStateRole and name_end > 0:
            self.spectrum_names_per_class[column_name[:name_end]][index.data()] = value
            self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount() - 1, name_end))
            return True

        else:
            return False

    def number_selected(self) -> int:
        """
        Get the total number of spectra selected for export.

        :return: The total number of spectra, intended for export.
        """
        n_selected = 0
        for cl in self.spectrum_names_per_class:
            for spectrum in self.spectrum_names_per_class[cl]:
                if self.spectrum_names_per_class[cl][spectrum] == Qt.Checked:
                    n_selected = n_selected + 1

        return n_selected


class SortFilterProxyModel(QSortFilterProxyModel):
    """A QSortFilterProxyModel to handle the CresTableModel. """

    def __init__(self, parent=None):
        super(SortFilterProxyModel, self).__init__(parent)

        self._rmse_filter = None
        self._min_frac_filter = None
        self._max_frac_filter = None

    def setRMSEFilter(self, value: float = None):
        """
        Set the RMSE filter value.

        :param value: The new filter value.
        """

        self._rmse_filter = value

    def setMinFractionFilter(self, value: float = None):
        """
        Set the Min Fraction filter value.

        :param value: The new filter value.
        """

        self._min_frac_filter = value

    def setMaxFractionFilter(self, value: float = None):
        """
        Set the Max Fraction filter value.

        :param value: The new filter value.
        """

        self._max_frac_filter = value

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """ Implementation of filterAcceptsRow function in parent class. """

        model = self.sourceModel()
        header = model.header

        # rmse filter
        if self._rmse_filter is None and self._min_frac_filter is None and self._max_frac_filter is None:
            return True
        else:
            return_value = True

            # check rmse
            rmse_col = header.index('RMSE')
            index = model.index(source_row, rmse_col, source_parent)
            data = float(model.data(index))
            if self._rmse_filter is not None:
                if data > self._rmse_filter:
                    return_value = False

            # check min and max frac
            frac_col = [i for i, s in enumerate(header) if '_fraction' in s]
            frac_col = frac_col[:-1]  # not shade

            for col in frac_col:
                index = model.index(source_row, col, source_parent)
                data = float(model.data(index))
                if self._min_frac_filter is not None:
                    if data < self._min_frac_filter:
                        return_value = False
                if self._max_frac_filter is not None:
                    if data > self._max_frac_filter:
                        return_value = False

        return return_value


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = CresWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
