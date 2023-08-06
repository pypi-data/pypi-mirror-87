# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : June 2020
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
import numpy as np
from spectral_libraries.core.music import Music


class Amuses:
    """
    AMUSES Prunes a spectral library with regard to an image and internal redundancy.

    Degerickx, J.; Okujeni, A.; Iordache, M.-D.; Hermy, M.; van der Linden, S.; Somers, B.	
    A Novel Spectral Library Pruning Technique for Spectral Unmixing of Urban Land Cover. 
    Remote Sens. 2017, 9, 565.

    """

    def __init__(self):
        pass

    @staticmethod
    def execute(image: np.array, library: np.array, music_pct: float = 0.9, amuses_pct: float = 0.95, min_eig: int = 15,
                thresholds: tuple = (0.0002, 0.02), log: callable = print, set_progress: callable = None) -> dict:
        """
        AMUSES Prunes a spectral library with regard to an image and internal redundancy.

        :param image: image used for pruning (bands x rows x columns), reflectance, no bad bands
        :param library: the original spectral library to be pruned (bands x spectra), reflectance, no bad bands
        :param music_pct: final pruned library size for the MUSIC algorithm (in pct)
        :param amuses_pct: library size for the AMUSES algorithm (in pct)
        :param min_eig: minimum number of eigenvectors to be retained from the image to calculate MUSIC distances,
        :param thresholds: low and high threshold for the AMUSES algorithm
        :param log: log function
        :param set_progress: communicate progress (refer to the progress bar in case of GUI; otherwise print to console)
        :return: dictionary with each output metric as a numpy array in a key-value pair
                 - music_indices: library indices after pruning with the MUSIC algorithm
                 - music_eigenvectors: first kf eigenvectors of image subspace (needed for sparse unmixing)
                                       kf = estimated number of eigenvectors in the image estimated by Hysime algorithm
                 - music_distances: MUSIC distances of the pruned library spectra to the image, sorted from low to high
                 - amuses_indices: library indices after pruning with the AMUSES algorithm

        """
        log = log if log else print
        set_progress = set_progress if set_progress else printProgress

        music_size = int(np.round(library.shape[1] * music_pct))
        amuses_first_index = int(np.round(library.shape[1] * (1-amuses_pct)))
        set_progress(2)

        # run music
        result = Music().execute(image=image, library=library, library_size=music_size, min_eig=min_eig, log=log)
        music_distances = result['music_distances'][amuses_first_index:]
        music_indices = result['music_indices']
        set_progress(50)

        # set threshold
        min_distance = min(music_distances)
        max_distance = max(music_distances)

        threshold = (((music_distances - min_distance) / (max_distance - min_distance)) * thresholds[1]) + thresholds[0]
        threshold = np.hstack((np.tile(thresholds[0], amuses_first_index), threshold))
        set_progress(52)

        # start by selecting the first music spectrum
        log('AMUSES: Iteratively select most similar spectra')
        amuses_indices = np.array([music_indices[0]])
        progress = 52

        # run through MUSIC result and select only spectra with similarity > threshold
        for j in range(1, music_size):
            stop = 0
            check = 0
            i = 0
            while not stop:
                # Combination of Jeffries-Matusita Distance and Spectral Angle
                # Padma, 2014, JM based mixed-measure for improved spectral matching in hyperspectral image analysis
                x1 = library[:, music_indices[j]]
                x2 = library[:, amuses_indices[i]]
                jmd = np.sqrt(np.sum((np.sqrt(x1 / np.sum(x1)) - np.sqrt(x2 / np.sum(x2))) ** 2))
                sam = np.arccos(np.dot(x1.T, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2)))
                jmd_sam = jmd * np.tan(sam)

                # if threshold is reached: stop loop and do not set check flag
                stop = (jmd_sam < threshold[j])
                i = i + 1

                # if threshold is never reached for selected indices: stop loop and set check flag
                if (i >= len(amuses_indices)) and (stop == 0):
                    check = 1
                    stop = 1

            if check:
                amuses_indices = np.hstack((amuses_indices, music_indices[j]))

            new_progress = 52 + int(j / music_size * 0.4 * 100)
            if new_progress >= progress + 5:
                progress = new_progress
                set_progress(progress)

        log('AMUSES: ' + str(len(amuses_indices)) + ' spectra selected')
        result['amuses_indices'] = amuses_indices
        set_progress(95)
        return result


def printProgress(value: int):
    """ Replacement for the GUI progress bar """

    print('progress: {} %'.format(value))
