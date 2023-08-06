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
from datetime import datetime


def save_square_to_envi(square_array, outfile_path, spectra_names, library_name, constraints, reset, duration, ngb):
    """
    Save the square array as an ENVI file.
    :param square_array: the square array as a dictionary
    :param outfile_path: the path of the output file
    :param spectra_names: the names of the endmembers
    :param library_name: the name of the spectral library used to create the square array
    :param constraints: the constraints
    :param reset:
    :param duration
    :param ngb
    :return: a square array saved to file
    """

    bands = list(square_array.keys())
    n_bands = len(bands)
    size = square_array[bands[0]].shape[0]

    # prepare the output array
    driver = gdal.GetDriverByName('ENVI')
    raster = driver.Create(outfile_path, size, size, n_bands, gdal.GDT_Float32)

    i = 1
    if 'rmse' in bands:
        raster.GetRasterBand(i).SetDescription(' RMSE')
        raster.GetRasterBand(i).WriteArray(square_array['rmse'])
        i += 1
    if 'constraints' in bands:
        raster.GetRasterBand(i).SetDescription(' Constraints')
        raster.GetRasterBand(i).WriteArray(square_array['constraints'])
        i += 1
    if 'spectral angle' in bands:
        raster.GetRasterBand(i).SetDescription(' Spectral Angle')
        raster.GetRasterBand(i).WriteArray(square_array['spectral angle'])
        i += 1
    if 'em fraction' in bands:
        raster.GetRasterBand(i).SetDescription(' EM Fraction')
        raster.GetRasterBand(i).WriteArray(square_array['em fraction'])
        i += 1
    if 'shade fraction' in bands:
        raster.GetRasterBand(i).SetDescription(' Shade Fraction')
        raster.GetRasterBand(i).WriteArray(square_array['shade fraction'])

    # change header description with UTC timestamp
    raster.SetDescription('  Viper 2 Square Array  {' + datetime.now().isoformat() + ']')
    # make sure spectra_names are a character string and not unicode
    spectra_names = [' ' + str(x) for x in spectra_names]
    raster.SetMetadataItem('spectra_names', '{\n' + ',\n'.join(spectra_names) + '}', 'ENVI')
    raster.SetMetadataItem('spectral library name', str(library_name), 'ENVI')
    raster.SetMetadataItem('number of good bands', str(ngb), 'ENVI')
    if reset:
        raster.SetMetadataItem('reset to threshold', 'Yes', 'ENVI')
    else:
        raster.SetMetadataItem('reset to threshold', 'No', 'ENVI')
    if constraints[0] != -9999:
        raster.SetMetadataItem('constraint minimum non-shade fraction', str(constraints[0]), 'ENVI')
    else:
        raster.SetMetadataItem('constraint minimum non-shade fraction', 'None', 'ENVI')
    if constraints[1] != -9999:
        raster.SetMetadataItem('constraint maximum non-shade fraction', str(constraints[1]), 'ENVI')
    else:
        raster.SetMetadataItem('constraint maximum non-shade fraction', 'None', 'ENVI')
    if constraints[2] != -9999:
        raster.SetMetadataItem('constraint maximum RMSE', str(constraints[2]), 'ENVI')
    else:
        raster.SetMetadataItem('constraint maximum RMSE', 'None', 'ENVI')
    raster.SetMetadataItem('time required for processing (sec)', str(duration), 'ENVI')


def save_ies_metadata(metadata, library_path, outfile_path, forced_list, forced_position, class_header, class_list,
                      spectra_names, selection):
    spectra_names = np.array(spectra_names)
    file = open(outfile_path, "w")
    file.write("IES SUMMARY \n----------------------------------------\n\n")

    file.write("Based on the spectral library: " + library_path + "\n\n")
    file.write("Metadata\n")
    file.write("	Cass header: " + class_header + "\n")
    classes = np.unique(class_list)
    classes = [x.upper() for x in classes]
    file.write("    Unique classes: " + "  ".join(classes) + "\n\n")

    if forced_position is not None:
        file.write("Used a forced library? Yes\n")
        file.write("    Entry point: " + str(forced_position) + "\n")
        file.write("    Endmember numbers: " + ", ".join([str(x) for x in forced_list]) + "\n")
    else:
        file.write("Used a forced library? No\n")

    file.write("\n\n")

    classes = classes + ['Unclas']
    row_format = ("{:>" + str(len(max(classes, key=len)) + 2) + "}") * (len(classes) + 1)
    loops = metadata.keys()
    file.write("Final Confusion Matrix (Kappa: " + str(metadata[max(loops)]['kappa']) + ")\n")
    file.write("----------------------------------------\n")
    file.write(row_format.format("", *classes) + "\n")
    for (cl, row) in zip(classes, metadata[max(loops)]['confusion_matrix']):
        file.write(row_format.format(cl, *row) + "\n")

    file.write("\n")
    file.write("\nEndmember names (#EM: " + str(len(selection)) + ")\n")
    file.write("----------------------------------------\n\n")
    for (nr, name) in zip(selection, spectra_names[selection]):
        file.write(str(nr) + ": " + name + "\n")
    file.write("\n\n")

    file.write("ITERATIVE PROCESS\n----------------------------------------\n")

    for i in metadata.keys():
        record = metadata[i]
        if i == forced_position:
            file.write("\nLoop " + str(i) + ": new endmembers (forced library): " + ", ".join(spectra_names[
                                                                                                  record['add']])
                       + " (" + ", ".join([str(x) for x in record['add']]) + ")" + "\n")
            file.write(" - Kappa at this point: " + str(record['kappa']) + "\n")
            file.write(" - Confusion Matrix:" + "\n")
            file.write(row_format.format("", *classes) + "\n")
            for (cl, row) in zip(classes, record['confusion_matrix']):
                file.write(row_format.format(cl, *row) + "\n")
        else:
            if 'add' in record.keys():
                if record['add'] is None:
                    file.write("\nLoop 1: skipped because forced library contained more than one endmember\n")
                else:
                    file.write("\nLoop " + str(i) + ": new endmember: " + spectra_names[record['add']] + " (" +
                               str(record['add']) + ")" + "\n")
                    file.write(" - Kappa at this point: " + str(record['kappa']) + "\n")
                    file.write(" - Confusion Matrix:" + "\n")
                    file.write(row_format.format("", *classes) + "\n")
                    for (cl, row) in zip(classes, record['confusion_matrix']):
                        file.write(row_format.format(cl, *row) + "\n")
            if 'remove' in record.keys():
                file.write("\nLoop " + str(i) + ": removed endmember " + spectra_names[record['remove']] + "(" +
                           str(record['remove']) + ")" + "\n")
                file.write(" - Kappa at this point: " + str(record['r_kappa']) + "\n")
                file.write(" - Confusion Matrix:" + "\n")
                file.write(row_format.format("", *classes) + "\n")
                for (cl, row) in zip(classes, record['r_confusion_matrix']):
                    file.write(row_format.format(cl, *row) + "\n")

    file.close()
