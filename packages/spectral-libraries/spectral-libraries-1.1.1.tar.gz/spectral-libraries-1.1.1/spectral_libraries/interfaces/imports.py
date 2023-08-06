# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : July 2018
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
from osgeo import gdal
from spectral_libraries.interfaces import check_path
from spectral_libraries.qps.speclib.core import SpectralLibrary


def import_library(path: str) -> SpectralLibrary:
    """ Browse for a spectral library and return it as a SpectralLibrary object.

    :param str path: the absolute path to the spectral library
    :return: Spectral Library object
    """
    check_path(path)
    spectral_library = SpectralLibrary.readFrom(path)

    if not spectral_library or len(spectral_library) == 0:
        raise Exception("Spectral Library with path {} is empty.".format(path))

    return spectral_library


def import_library_as_array(path: str, spectra_names: bool = False, metadata: str = None) -> (np.ndarray, np.ndarray,
                                                                                              np.ndarray):
    """ Browse for a spectral library and return it as an array. Optionally along with the spectra names and a metadata
    element

    :param path: the absolute path to the spectral library
    :param spectra_names: set to True if you would like to get the spectra names
    :param metadata: the name of the metadata element to return
    :return: numpy array [#good bands x #spectra] + string array with spectra names and/or metadata [#spectra]
    """
    library = import_library(path)
    array = np.array([np.array(x.values()['y'])[np.where(x.bbl())[0]] for x in library.profiles()]).T
    names = np.array([str(x.name()).strip() for x in library.profiles()], dtype=str) if spectra_names else None

    if not metadata:
        classes = None
    elif metadata not in library.fieldNames():
        raise Exception("{} not found as metadata header; classes found: {}".format(metadata, library.fieldNames()))
    else:
        classes = np.array([str(x.metadata(metadata)).strip().lower() for x in library.profiles()], dtype=str)

    return array, names, classes


def import_library_metadata(spectral_library: SpectralLibrary, metadata: str) -> np.ndarray:
    """ Return a metadata element of a Spectral Library object.

    :param spectral_library: SpectralLibrary object
    :param metadata: the name of the metadata element to return
    :return: string array with spectra metadata [#spectra]
    """
    return np.array([str(x.metadata(metadata)).strip().lower() for x in spectral_library.profiles()], dtype=str)


def import_image(path: str) -> np.ndarray:
    """ Browse for a spectral image and return it without bad bands.

    :param path: the absolute path to the image
    :return: float32 numpy array [#good bands x #rows x #columns]
    """
    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        array = data.ReadAsArray()
        gbl = data.GetMetadataItem('bbl', 'ENVI')
        if gbl is not None:
            gbl = np.asarray(gbl[1:-1].split(","), dtype=int)
            gbl = np.where(gbl == 1)[0]
            array = array[gbl, :, :]
    except Exception as e:
        raise Exception(str(e))

    if array is None or len(array) == 0:
        raise Exception("Image with path {} is empty.".format(path))

    return array


def import_band_names(path):
    """ Browse for a spectral image's band names and return them as a list.
    :param path: the absolute path to the spectral library
    :return: string list of band names
    """
    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        band_names = data.GetMetadataItem('band_names', 'ENVI')
        if band_names is not None:
            band_names = band_names[1:-1].split(",")
            band_names = [x.strip().lower() for x in band_names]
        return band_names

    except Exception as e:
        raise Exception(str(e))


def detect_reflectance_scale_factor(array: np.ndarray) -> int:
    """ Determine the reflectance scale factor [1, 1000 or 10 000] by looking for the largest value in the array.

    :param array: the array for which the reflectance scale factor is to be found
    :return: the reflectance scale factor
    """
    limit = np.nanmax(array)
    if limit < 1.1:
        return 1
    if limit < 1100:
        return 1000
    if limit < 11000:
        return 10000
    else:
        raise ValueError("Image has values larger than 10000. Cannot process.")


def import_square(path: str) -> (dict, np.ndarray):
    """ Browse for a square array and return it along the list of spectra names from the header.

    :param path: the absolute path to the square array
    :return: dictionary of float32 numpy arrays [#metrics] + string array with spectra names [#spectra]
    """
    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        if data:
            array = data.ReadAsArray()
        else:
            raise Exception("Image cannot be read or is empty.")

        band_names = data.GetMetadataItem('band_names', 'ENVI')
        if band_names:
            band_names = band_names[1:-1].split(",")
            band_names = [x.strip().lower() for x in band_names]
        else:
            raise Exception("No band names found.")

        spectra_names = data.GetMetadataItem('spectra_names', 'ENVI')
        if spectra_names:
            spectra_names = spectra_names[1:-1].split(",")
            spectra_names = [x.strip() for x in spectra_names]
        else:
            raise Exception("No spectra names found.")

    except Exception as e:
        raise Exception(str(e))

    if array.shape[1] != array.shape[2]:
        raise Exception('Array is not square. Cannot proceed.')

    square = {}
    for i, band in enumerate(band_names):
        square[band] = array[i, :, :]

    return square, spectra_names
