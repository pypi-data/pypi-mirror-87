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
import copy
import numpy as np
from functools import partial
from multiprocessing import Pool

from .library_metrics import square_rmse


class Ies:
    """
    Iterative Endmember Selection (IES) is used to identify the spectral library subset that provides the best class
    separability. The basis for this is a RMSE-based kappa coefficient. In an iterative manner, endmembers are added
    and removed from the subset until the kappa coefficient no longer improves.

    Citations:

    Schaaf, A.N., Dennison, P.E., Fryer, G.K., Roth, K.L., and Roberts, D.A., 2011, Mapping Plant Functional Types at
    Multiple Spatial Resolutions using Imaging Spectrometer Data, GIScience Remote Sensing, 48, p. 324-344.

    Roth, K.L., Dennison, P.E., and Roberts, D.A., 2012, Comparing endmember selection techniques for accurate mapping
    of plant species and land cover using imaging spectrometer data, Remote Sensing of Environment, 127, p. 139-152.
    """

    def __init__(self):
        self.rmse_band = None
        self.mask = None
        self.original_classes = None
        self.original_classes_multiplied = None
        self.forced_list = None
        self.n_endmembers = None
        self.n_classes = None
        self.n_processes = 1
        self.summary = {}

    def _confusion_matrix(self, modeled_classes: np.array) -> np.array:
        """
        :param modeled_classes: the classes modeled based on a subset of models
        :return: confusion matrix (= 2D histogram) of the original vs. modeled classes
        """

        # self.original_classes_multiplied is the original classes multiplied by (n_classes +1)
        # by adding the modeled classes, we can create a n_classes^2 separate histogram bins
        confusion_matrix = self.original_classes_multiplied + modeled_classes
        # create a 1D histogram
        confusion_matrix = np.bincount(confusion_matrix, minlength=(self.n_classes + 1) ** 2)
        # reshape to 2D histogram
        return confusion_matrix.reshape([self.n_classes + 1, self.n_classes + 1]).T

    def _kappa(self, confusion_matrix: np.array) -> np.float32:
        """
        :param confusion_matrix: the confusion matrix
        :return: kappa coefficient: a measure of class separability
        """

        theta1 = np.float32(np.trace(confusion_matrix)) / self.n_endmembers
        theta2 = np.float32(np.sum(np.dot(confusion_matrix, confusion_matrix))) / (self.n_endmembers ** 2)
        return np.float32((theta1 - theta2) / (1 - theta2))

    def _add_model(self, current_selection: np.array):
        """ Routine for adding a new model to the selection, if it provides a better kappa than the previous situation
        :param current_selection: current pool of models
        :return: the kappa and index of the newly found model
        """

        n_models = current_selection.shape[0]
        selected_classes = self.original_classes[current_selection]

        # get the current min RMSE and model for each spectrum
        if n_models == 1:
            current_min_rmse = self.rmse_band[current_selection][0]
            current_modeled_classes = np.repeat(selected_classes, self.n_endmembers)
            current_modeled_classes[self.mask[current_selection][0]] = self.n_classes

        else:
            current_min_rmse = np.amin(self.rmse_band[current_selection], axis=0)
            min_index_current = np.argmin(self.rmse_band[current_selection], axis=0)
            min_index_current[np.all(self.mask[current_selection], axis=0)] = -1
            selected_classes = np.append(selected_classes, self.n_classes)
            current_modeled_classes = selected_classes[min_index_current]

        # calculate the kappa array
        if self.n_processes == 1:
            # avoid adding a model that is already in the current pool
            potential_indices = np.arange(self.n_endmembers)
            potential_indices = np.delete(potential_indices, current_selection)

            # try adding each model in an iterative way
            kappa_array = np.zeros(self.n_endmembers, dtype=np.float32)
            for i in potential_indices:
                kappa_array[i] = self._add_model_thread(i, min_rmse=current_min_rmse,
                                                        modeled_classes=current_modeled_classes)
        else:
            # not used for now - has no improvements
            pool = Pool(processes=self.n_processes)
            temp = partial(self._add_model_thread, min_rmse=current_min_rmse, modeled_classes=current_modeled_classes)
            kappa_array = pool.map(temp, np.arange(self.n_endmembers))
            kappa_array = np.array(kappa_array)
            kappa_array[current_selection] = 0

        # return only the model with the best kappa, and its index
        return kappa_array.max(), np.argmax(kappa_array)

    def _add_model_thread(self, i, min_rmse=None, modeled_classes=None):
        # the indices where the new model has a lower RMSE
        new_model_indices = np.where(self.rmse_band[i] < min_rmse)

        # change the current modeled classes where the new model has a better RMSE
        modeled_classes = copy.deepcopy(modeled_classes)
        modeled_classes[new_model_indices] = self.original_classes[i]

        confusion_matrix = self._confusion_matrix(modeled_classes)
        return self._kappa(confusion_matrix)

    def _remove_model(self, current_selection: np.array):
        """ Routine for removing a model from a selection, if it provides a better kappa than the previous situation
        :param current_selection: current pool of models
        :return: the kappa and index of the model to remove
        """

        n_models = current_selection.shape[0]
        # create these before the loop to save some time
        mask = np.ones(n_models, dtype=bool)
        current_rmse = self.rmse_band[current_selection]
        current_mask = self.mask[current_selection]
        current_classes = self.original_classes[current_selection]

        # calculate the kappa array
        if self.n_processes == 1:
            # try adding each model in an iterative way
            kappa_array = np.zeros(n_models, dtype=np.float32)
            for i in np.arange(n_models):
                kappa_array[i] = self._remove_model_thread(i, ones=mask, mask=current_mask, rmse=current_rmse,
                                                           classes=current_classes)
        else:
            pool = Pool(processes=self.n_processes)
            temp = partial(self._remove_model_thread, ones=mask, mask=current_mask, rmse=current_rmse,
                           classes=current_classes)
            kappa_array = pool.map(temp, np.arange(n_models))
            kappa_array = np.array(kappa_array)

        # no subtracting forced models
        kappa_array[np.where(np.in1d(current_selection, self.forced_list))] = 0

        # return only the model with the best kappa, and its index
        return kappa_array.max(), np.argmax(kappa_array)

    def _remove_model_thread(self, i, ones=None, mask=None, rmse=None, classes=None):
        # find the modeled classes after removing one model
        ones = copy.deepcopy(ones)
        ones[i] = False
        min_index_removed = np.argmin(rmse[ones], axis=0)
        min_index_removed[np.all(mask[ones], axis=0)] = -1
        classes_removed = np.append(classes[ones], self.n_classes)
        modeled_classes_removed = classes_removed[min_index_removed]

        # confusion matrix and kappa
        confusion_matrix = self._confusion_matrix(modeled_classes_removed)
        return self._kappa(confusion_matrix)

    def _evaluate_selection(self, selection: np.array):
        """ Routine for evaluating the kappa and confusion matrix of a given selection of models
        :param selection: current pool of models
        :return: the kappa and confusion matrix for this selection
        """

        n_models = selection.shape[0]
        selected_classes = self.original_classes[selection]

        # get the current min RMSE and model for each spectrum
        if n_models == 1:
            current_modeled_classes = np.repeat(selected_classes, self.n_endmembers)
            current_modeled_classes[self.mask[selection][0]] = self.n_classes

        else:
            min_index_current = np.argmin(self.rmse_band[selection], axis=0)
            min_index_current[np.all(self.mask[selection], axis=0)] = -1
            selected_classes = np.append(selected_classes, self.n_classes)
            current_modeled_classes = selected_classes[min_index_current]

        confusion_matrix = self._confusion_matrix(current_modeled_classes)
        kappa = self._kappa(confusion_matrix)

        # return the kappa and confusion matrix the model with the best kappa, and its index
        return kappa, confusion_matrix

    def execute(self, library: np.array, class_list: np.array, constraints: tuple = (-0.05, 1.05, 0.025),
                forced_list: np.array = None, forced_step: int = None, multiprocessing: bool = True,
                summary: bool = False, set_progress: callable = None, log: callable = print):
        """
        Execute the IES algorithm. The result is a 1-D numpy array of selected endmembers. In case a summary is
        requested, it is delivered as a second output variable.

        :param library: spectral library [spectra as columns], scaled to reflectance values, without bad bands
        :param class_list: int array with the *numerical* class for each spectrum (e.g. GV = 1, SOIL = 2)
        :param constraints: min fraction, max fraction and max RMSE.
        :param forced_list: int array with indices of the endmembers that should be forcefully included
        :param forced_step: the loop in which the forced_list should be included (starting from 0)
        :param multiprocessing: use multiprocessing or not (option is deactivated)
        :param summary: return a summary of the process or not
        :param set_progress: communicate progress (refer to the progress bar in case of GUI; otherwise print to console)
        :param log: communicate messages (refer to the print_log tab in the GUI; otherwise print to the console)
        :return: numpy array with the indices of the selected endmembers [+ summary as a dict in case requested]
        """
        log('IES calculations started')
        set_progress = set_progress if set_progress else printProgress
        progress_int = 0

        # store the variables
        self.original_classes = class_list
        self.n_endmembers = self.original_classes.shape[0]
        self.n_classes = self.original_classes.max() + 1
        self.original_classes_multiplied = class_list * (self.n_classes + 1)  # for later use in the confusion matrix
        self.forced_list = forced_list

        if multiprocessing:
            self.n_processes = 1                # option is turned off for now
            # try:
            #     self.n_processes = len(os.sched_getaffinity(0))
            #     log("CPU cores available for use: {}".format(self.n_processes))
            # except AttributeError:
            #     self.n_processes = 1

        log('Calculating the RMSE')
        self.rmse_band, constraints_band = square_rmse(library=library, constraints=constraints, reset=True)
        self.mask = constraints_band > 0
        self.rmse_band[self.mask] = 9999

        stop_adding = 0
        stop_removing = 0

        # find the first endmember: the modeled class with 1 model is always the model itself, except constraint breach,
        # unless we have to use the forced library right away
        if forced_step == 0:
            selected_indices = forced_list
            max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
            log("0: forced library entered: " + np.array2string(forced_list, separator=", ") +
                " - Kappa at this point: " + str(max_kappa))
            progress_int = progress_int + 1
            set_progress(progress_int)
            if summary:
                self.summary[0] = {'add': forced_list, 'kappa': max_kappa, 'confusion_matrix': confusion_matrix}
        else:
            modeled_classes_one_model = np.repeat(self.original_classes, self.n_endmembers).reshape((self.n_endmembers,
                                                                                                     self.n_endmembers))
            modeled_classes_one_model[self.mask] = self.n_classes

            kappa_array = np.zeros(self.n_endmembers, dtype=np.float32)
            for i in np.arange(self.n_endmembers):
                confusion_matrix = self._confusion_matrix(modeled_classes_one_model[i])
                kappa_array[i] = self._kappa(confusion_matrix)

            max_kappa = kappa_array.max()
            new_index = np.argmax(kappa_array)
            selected_indices = np.array([new_index])
            log("0: new endmember: " + str(new_index) + " - Kappa at this point: " + str(max_kappa))
            progress_int = progress_int + 1
            set_progress(progress_int)
            if summary:
                self.summary[0] = {'add': new_index, 'kappa': max_kappa,
                                   'confusion_matrix': self._confusion_matrix(modeled_classes_one_model[new_index])}

        # find the second endmember, unless we have to use the forced library in this step or unless we already have 2
        if forced_step == 1:
            selected_indices = np.sort(np.append(selected_indices, forced_list))
            max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
            log("1: forced library entered: " + np.array2string(forced_list, separator=", ") +
                " - Kappa at this point: " + str(max_kappa))
            progress_int = progress_int + 1
            set_progress(progress_int)
            if summary:
                self.summary[1] = {'add': forced_list, 'kappa': max_kappa, 'confusion_matrix': confusion_matrix}
        elif selected_indices.shape[0] < 2:
            new_kappa, new_index = self._add_model(selected_indices)

            if new_kappa > max_kappa:
                max_kappa = new_kappa
                selected_indices = np.sort(np.append(selected_indices, new_index))
                log("1: new endmember: " + str(new_index) + " - Kappa at this point: " + str(max_kappa))
                progress_int = progress_int + 1
                set_progress(progress_int)
                if summary:
                    self.summary[1] = {'add': new_index, 'kappa': max_kappa,
                                       'confusion_matrix': self._evaluate_selection(selected_indices)[1]}
            else:
                log("No second endmember found. Returning without result.")
                set_progress(progress_int)
                return None
        else:
            log("1: second loop skipped because forced library contained more than one endmember")
            progress_int = progress_int + 1
            set_progress(progress_int)
            if summary:
                self.summary[1] = {'add': None}

        # IES loop
        loop_counter = 2
        while stop_adding == 0 or stop_removing == 0:

            if loop_counter == 100:
                pass

            if forced_step == loop_counter:
                selected_indices = np.sort(np.append(selected_indices, forced_list))
                max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
                log(str(loop_counter) + ": forced library entered: " + np.array2string(forced_list, separator=", ") +
                    " - Kappa at this point: " + str(max_kappa))
                progress_int = progress_int + 1 if progress_int < 99 else 0
                set_progress(progress_int)
                if summary:
                    self.summary[loop_counter] = {'add': forced_list, 'kappa': max_kappa,
                                                  'confusion_matrix': confusion_matrix}
            else:
                # process of adding a new model
                new_kappa, new_index = self._add_model(selected_indices)

                if new_kappa > max_kappa:
                    max_kappa = new_kappa
                    selected_indices = np.sort(np.append(selected_indices, new_index))
                    log(str(loop_counter) + ": new endmember: " + str(new_index) +
                        " - Kappa at this point: " + str(max_kappa))
                    progress_int = progress_int + 1 if progress_int < 99 else 0
                    set_progress(progress_int)
                    stop_adding = 0
                    if summary:
                        self.summary[loop_counter] = {'add': new_index, 'kappa': max_kappa,
                                                      'confusion_matrix': self._evaluate_selection(selected_indices)[1]}
                else:
                    stop_adding = 1

                # process of subtracting a selected model
                new_kappa, remove_index = self._remove_model(selected_indices)

                if new_kappa > max_kappa:
                    max_kappa = new_kappa
                    log(str(loop_counter) + ": removed endmember: " + str(selected_indices[remove_index]) +
                        " - Kappa at this point: " + str(max_kappa))
                    progress_int = progress_int + 1 if progress_int < 99 else 0
                    set_progress(progress_int)
                    selected_indices = np.delete(selected_indices, remove_index)
                    stop_removing = 0
                    if summary:
                        self.summary[loop_counter] = {'remove': selected_indices[remove_index], 'r_kappa': max_kappa,
                                                      'r_confusion_matrix':
                                                          self._evaluate_selection(selected_indices)[1]}

                else:
                    stop_removing = 1

            loop_counter += 1
        if summary:
            return selected_indices, self.summary
        else:
            return selected_indices


def printProgress(value: int):
    """ Replacement for the GUI progress bar """

    print('progress: {} %'.format(value))
