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


class Music:
    """
    MUSIC (multiple signal classification) is a library pruning technique that operates on a full image.

    This technique reduces the dimensionality of an image to kf eigenvectors, and prunes a library according to the
    smallest distances to this subspace.

    Citation: Iordache, M.D., Bioucas-Dias, J.M., Plaza, A., Somers, B., 2014, MUSIC-CSR: Hyperspectral unmixing via
    multiple signal classification and collaborative sparse regression, IEEE Transactions on Geoscience and Remote
    Sensing, 52, p. 4364–4382.
    """

    def __init__(self):
        self.log = None

    @staticmethod
    def flatten_image(image: np.array) -> np.array:
        """ Store the image as a line (2D array).

        :param image: 3D image (m bands x n rows x p columns)
        :return: 2D image (m bands x n.p spectra
        """

        n_bands = image.shape[0]
        n_pixels = image.shape[1] * image.shape[2]
        return np.reshape(image, [n_bands, n_pixels], order='F')

    @staticmethod
    def normalize_brightness(spectra: np.array) -> np.array:
        """
        Brightness normalization of spectral library or 2D-image

        :param spectra: array with m bands x n spectra
        :return: array with normalized spectral
        """

        spectra_mean = np.mean(spectra, axis=0)
        normalized_spectra = np.divide(spectra, spectra_mean)

        return normalized_spectra

    def estimate_noise(self, image):
        """
        Hyperspectral noise estimation, by assuming that the reflectance at a given band is well modelled by a linear
        regression on the remaining bands.

        :param image: 2D hyperspectral data set (m bands x n pixels)
        :return: the noise estimates for every pixel (m x n)
        """
        if image.shape[0] < 2:
            self.log('MUSIC: Too few bands to estimate the noise')
            return -1

        small = 1e-6
        n_bands, n_pixels = image.shape

        noise = np.zeros((n_bands, n_pixels))
        rr = np.dot(image, np.transpose(image))

        rri = np.linalg.inv(rr+small*np.eye(n_bands))
        self.log('MUSIC: Computing noise for each band')

        for i in range(0, n_bands):
            part1 = rri - np.outer(rri[:, i], rri[i, :]) / rri[i, i]
            part2 = rr[:, i]
            part2[i] = 0
            beta = np.matmul(part1, part2)
            beta[i] = 0
            noise[i, :] = np.subtract(image[i, :], np.matmul(np.transpose(beta), image))

        # noise_correlation = np.diag(np.diag(np.divide(np.matmul(noise, np.transpose(noise)), n_pixels)))

        return noise

    def hysime2(self, image, min_eig):
        """
        Hysime2 algorithm

        :param image: 2D hyperspectral data set (m bands x n pixels)
        :param min_eig: minimum number of eigenvectors to be retained from the image to calculate MUSIC distances
        :return: signal subspace dimension (tuple), eigenvectors that span the signal subspace (in the columns)
        """
        noise = self.estimate_noise(image)   # mxn

        n_bands, n_pixels = image.shape
        x = image - noise

        eigenvalue, eigenvector = np.linalg.eig(np.dot(x, x.T) / n_pixels)
        # the sign of eigenvectors changes from MATLAB to python,
        # since eigenvectors do not have a sign, this should not be relevant

        self.log('MUSIC: Estimating the number of endmembers')
        # calculate % variance explained by eigenvectors
        eigenvalue = eigenvalue / np.sum(eigenvalue)
        # [::-1] is added for descend sorting
        eigenvalue_sort = np.sort(eigenvalue)[::-1]
        eigenvalue_index = np.argsort(eigenvalue)[::-1]

        # sort the eigenvectors based on the sort of the eigenvalues
        eigenvector = eigenvector[:, eigenvalue_index]

        v_threshold = 0.999
        v_sum = 0
        kf = 0
        while v_sum < v_threshold:
            v_sum = v_sum + eigenvalue_sort[kf]
            kf += 1

        self.log('MUSIC: The first {} elements explain 99.9 percent of the variation'.format(kf))
        if kf < min_eig:
            kf = min_eig

        self.log("MUSIC: Selecting the first {} eigenvectors".format(kf))

        return eigenvector[:, 0:kf]

    def execute(self, library: np.array, image: np.array, library_size: int, min_eig: int = 15,
                log: callable = print) -> dict:
        """
        This technique reduces the dimensionality of an image to kf eigenvectors, and select library spectra according
        to the smallest distances to this subspace.

        :param library: the original spectral library to be pruned (bands x spectra), reflectance, no bad bands
        :param image: image used for pruning (bands x rows x columns) reflectance, no bad bands
        :param library_size: pruned library size
        :param min_eig: minimum number of eigenvectors to be retained from the image to calculate MUSIC distances
        :param log: communicate messages (point to the print_log tab in the GUI; otherwise print to the console)
        :return: dictionary with each output metric as a numpy array in a key-value pair
                 - music_indices: indices of the pruned library
                 - eigenvectors: first kf eigenvectors of image subspace (needed for sparse unmixing)
                                 kf = estimated number of eigenvectors in the image estimated by Hysime algorithm
                 - music_distances: MUSIC distances of the pruned library spectra to the image, sorted from low to high

        """
        self.log = log if log else print

        # reshape image to 2D
        image = self.flatten_image(image)

        # brightness normalization of library and image
        library = self.normalize_brightness(library)
        image = self.normalize_brightness(image)

        # delete all zero-spectra in the image
        image = np.delete(image, np.where(np.sum(image, axis=0) == 0)[0], axis=1)

        # hysime2 + final size of pruned library
        eigenvectors = self.hysime2(image, min_eig)

        # calculate distances from library spectra to image subspace
        n_bands = library.shape[0]

        # Euclidean distances between spectra and the hyperplane formed by the retained eigenvectors
        p = np.identity(n_bands) - np.matmul(eigenvectors, eigenvectors.T)
        error = np.sqrt((np.matmul(p, library) ** 2).sum(axis=0)) / np.sqrt((library ** 2).sum(axis=0))

        # sort these distances
        error_sorted = np.sort(error)
        error_sorted_indices = np.argsort(error)

        library_indices = error_sorted_indices[0:library_size]

        self.log('MUSIC: {} spectra selected'.format(len(library_indices)))

        return {'music_indices': library_indices,
                'music_eigenvectors': eigenvectors,
                'music_distances': error_sorted[0:library_size]}
