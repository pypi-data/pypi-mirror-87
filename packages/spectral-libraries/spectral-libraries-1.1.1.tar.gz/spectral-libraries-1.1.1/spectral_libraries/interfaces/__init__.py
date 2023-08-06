# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : March 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
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


def check_path(path):
    """ Check if path exists. Skip paths which are in memory

    :param path: the absolute path to the input file
    """
    if path == '':
        raise Exception("Path empty")

    elif not os.path.exists(path):
        raise Exception("Path {} does not exist.".format(path))
