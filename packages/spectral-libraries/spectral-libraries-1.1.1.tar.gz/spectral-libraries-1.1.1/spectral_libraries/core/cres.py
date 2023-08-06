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
import numpy as np
import itertools as it


class Cres:
    """  Constrained Reference Endmember Selection. Unmix a given signal with all models in a library. Then create an
    index to see which models are a close match to estimated fractions.

    Citations:

    Roberts, D.A., Smith, M.O., Adams, J.B., 1993, Green vegetation, non-photosynthetic vegetation and soils in AVIRIS
    data, Remote Sensing of Environment, 44, p. 255-270.

    Roberts, D.A., Batista, G., Pereira, J., Waller, E., and Nelson, B., 1999, Change Identification using Multitemporal
    Spectral Mixture Analysis: Applications in Eastern Amazonia, Remote Sensing Change Detection: Environmental
    Monitoring Methods and Applications, Edited by Elvidge, C. and Lunetta R., Chapter 9, p. 137-161.
    """
    def __init__(self):
        # input
        self.signal = None
        self.library = None
        self.classes = None
        self.spectrum_names = None

        # output
        self.unique_classes = None
        self.models = None
        self.fractions = None
        self.rmse = None

    def _subtract_shade(self, shade_spectrum: np.array):
        """ Correct image and library for photometric shade

        :param shade_spectrum: spectrum of shade in case of non-photometric shade
        """
        self.signal = self.signal - shade_spectrum
        self.library = self.library - shade_spectrum[:, np.newaxis]

    def _look_up_table(self) -> np.array:
        """
        :return: a look-up-table of possible models as a numpy array of n_models rows and n_em columns
        """
        # we don't know beforehand how many endmembers (1, 2 or 3), so we append the arguments and unpack them later
        args = []  # list of arguments
        for cl in self.unique_classes:
            indices = np.where(self.classes == cl)[0]
            args.append(indices)

        # we use the itertools.product function to generate all EM combinations of a model (e.g. GV-NPV)
        return np.array(list(it.product(*args)))

    def _fractions(self, rmse_constraint: float):
        """ Calculate the fractions and RMSE using SMA and SVD (see Mesma algorithm for more details).

        :param rmse_constraint: only keep models that fulfill this constraint
        """
        models = self._look_up_table()
        endmembers = self.library[:, models.T]

        # run a singular value decomposition on the endmember array where:
        #   w = vector (n_em) with the eigenvalues
        #   u = orthogonal array (n_b x n_b) used in decomposition
        #   v = orthogonal array (n_em x n_em) used in decomposition
        #  --> then   library = u . diagonal(w) . transpose(v)
        u, w, v = np.linalg.svd(endmembers.T, full_matrices=False)

        # inverse endmembers + fraction for each endmember
        temp = v * 1 / w[:, :, np.newaxis]
        endmembers_inverse = np.array([np.dot(y, x) for (x, y) in zip(temp, u)])
        fractions = np.einsum('ijk, k -> ij', endmembers_inverse, self.signal)

        # residuals + root mean square error
        residuals = self.signal[:, np.newaxis] - np.einsum('ijk, kj -> ik', endmembers, fractions)
        rmse = np.sqrt(np.sum(residuals * residuals, axis=0) / self.signal.shape[0])

        # shade fraction (last column of the fractions array)
        shade = 1 - np.sum(fractions, axis=1)
        fractions = np.concatenate((fractions, shade[:, np.newaxis]), axis=1)

        # only return the models that have a good RMSE value
        good_models = np.where(rmse < rmse_constraint)[0]
        self.models = models[good_models, :]
        self.fractions = fractions[good_models, :]
        self.rmse = rmse[good_models]

    def get_header(self) -> list:
        """
        Get the header for the QTableModel. It has header names for the spectra names, fractions and RMSE. The header
        names match the keys in the table dictionaries.

        Example for gv-soil mixture::

            ['gv_name', 'soil_name', 'gv_fraction', 'soil_fraction', 'shade_fraction', 'RMSE']

        :return: The header for the GUI QTableModel.
        """
        header = [x + "_name" for x in self.unique_classes] + [x + "_fraction" for x in self.unique_classes] + \
                 ['shade_fraction', 'RMSE']
        return header

    def get_fractions(self) -> list:
        """
        Get the calculated fractions (and RMSE) as a list of dictionaries, specifically designed for a QTableModel.
        In the list, each dictionary represents one endmember combination from the library (=one model).
        Assuming we have n classes in the library, each model's dictionary has n key-value pairs with the spectra names,
        n key-value pairs with the fractions, one key-value pair with the shade fraction and one key-value pair with the
        RMSE.

        The dictionary keys match the table header names.

        Example for gv-soil mixture::

            {gv_name: tree1, soil_name: clay4, gv_fraction: 0.25, soil_fraction: 0.55, shade_fraction: 0.20, rmse: 0.01}

        :return: A list of dictionaries, one per model, containing the spectra names, fractions and RMSE.
        """
        header_names = [x + "_name" for x in self.unique_classes]
        header_fractions = [x + "_fraction" for x in self.unique_classes] + ['shade_fraction']

        models = []
        table_spectra_names = self.spectrum_names[self.models]
        for (row_names, row_fractions, rmse) in zip(table_spectra_names, self.fractions, self.rmse):
            new_model = {}
            for i, col in enumerate(header_names):
                new_model[col] = row_names[i]
            for i, col in enumerate(header_fractions):
                new_model[col] = row_fractions[i]
            new_model['RMSE'] = rmse
            models.append(new_model)

        return models

    def index(self, target_fractions: list, weight_per_target: list, weight_rmse: int) -> dict:
        """
        Calculate the CRES indices based on input from the user.

        Example for GV-SOIL-NPV mixture::

            GV index = rmse weight * rmse
            + |GV calculated - estimated fraction| * GV weight
            + |SOIL calculated - estimated fraction|
            + |NPV calculated - estimated fraction|
            + |Shade calculated - estimated fraction|

        :param target_fractions: The estimated fractions of the spectrum that is being unmixed (list-of-floats).
        :param weight_per_target: The weights per class for calculating the indices (list-of-ints between 1 and 10).
        :param weight_rmse: The weight attached to the RMSE for calculating the indices (int between 1 and 10).
        :return: Indices for each endmember and each class. The unique classes from the library metadata are the keys.
        """
        indices = dict()
        n_classes = len(self.unique_classes)

        difference = np.abs(self.fractions - target_fractions)

        for u, uc in enumerate(self.unique_classes):
            indices[uc] = weight_rmse * self.rmse
            for c in np.arange(n_classes + 1):
                if c == u:
                    indices[uc] += weight_per_target[c] * difference[:, c]
                else:
                    indices[uc] += difference[:, c]

        return indices

    def execute(self, signal: np.array, library: np.array, classes: list, spectrum_names: list,
                rmse_constraint: float = 0.025, shade: np.array = np.array([])):
        """
        Unmix a given signal with a library and create fractions and RMSE values for each endmember in that library.

        :param signal: The signal to unmix, without bad bands and scaled to reflectance values.
        :param library: The library used for unmixing, without bad bands and scaled to reflectance values.
        :param classes: The class of each spectrum in the library (e.g. GV, SOIL, ...) [list-of-str]
        :param spectrum_names: The name of each spectrum in the library [list-of-str]
        :param rmse_constraint: Only keep models that fulfill this constraint.
        :param shade: Shade-spectrum in case of non-photometric shade.
        """
        if len(signal) != len(library):  # same number of bands
            return -1

        if library.shape[1] != len(classes) or len(classes) != len(spectrum_names):  # same number of spectra
            return -1

        self.signal = signal
        self.library = library
        self.classes = np.array(classes)
        self.unique_classes = np.unique(classes)
        self.spectrum_names = np.array(spectrum_names)

        if len(shade) > 0:
            if len(signal) != len(shade):
                return -1
            self._subtract_shade(shade)

        self._fractions(rmse_constraint)
