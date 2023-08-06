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
import math
import numpy as np

"""
In a spectral library, each endmember is used to model all others, using metrics like RMSE, Spectral Angle, ...
These metrics can be used for library optimization techniques like IES or EMC.

Possible metrics (bands) are RMSE, Spectral Angle, SMA fractions, SMA shade fraction, Constraints fulfilled.

Based on the Square Array in Viper Tools 2.0.

Citation: Roberts, D.A., Gardner, M.E., Church, R., Ustin, S.L., and Green, R.O., 1997, Optimum Strategies for
Mapping Vegetation using Multiple Endmember Spectral Mixture Models, Proceedings of the SPIE, 3118, p. 108-119
"""


def square_angle(library: np.array):
    """
    Calculate the spectral angle between all members of a spectral library and return the results as a matrix.

    :param library: spectral library [spectra as columns], scaled to reflectance values, without bad bands
    """
    library = np.array(library, dtype=np.float32)
    n_bands, n_spectra = library.shape

    angles_self = library / np.sqrt(np.sum(library * library, 0))
    angles_cross = np.dot(angles_self.transpose(), angles_self)
    angles_cross[angles_cross > 1] = 1  # np.across can only handle values up to 0
    angle = np.arccos(angles_cross)
    x = np.arange(n_spectra)
    angle[x, x] = 0.0

    return np.float32(angle)


def square_fractions(library: np.array, constraints: tuple = (-0.05, 1.05), reset: bool = True):
    """
    Calculate the fractions of applying SMA between all members of a spectral library and return the results as a
    matrix.

    Export whether the fraction constraint was breached and force fractions to threshold in case reset = True:

        * 0: no breach
        * 1: fraction constraint breach + fraction reset
        * 2: fraction constraint breach + no fraction reset

    :param library: spectral library [spectra as columns], scaled to reflectance values, without bad bands.
    :param constraints: the min and max allowable fractions
    :param reset: fractions are reset to threshold values in case of breach
    """
    constraints = (-9999, -9999) if not constraints else constraints
    if len(constraints) != 2:
        raise Exception("Constraints must be a tuple with 2 values.")
    if constraints[0] != -9999 and constraints[0] < -0.5:
        raise Exception("The minimum fraction constraint cannot be below -0.50.")
    if constraints[1] != -9999 and constraints[1] > 1.5:
        raise Exception("The maximum fraction constraint cannot be over 1.50.")

    library = np.array(library, dtype=np.float32)
    n_bands, n_spectra = library.shape
    # STEP 1: get the inverse endmembers (= the result of singular value decomposition)
    #       svdc says: endmember = u * v * w        with u = decomposition array, v = -1 and w = eigenvalue
    #            and:  inverse endmember = u * v / w
    #            so:   total(endmember * inverse endmember) = 1
    #
    # we can manually determine the eigenvalue of a 1D array (look it up...):
    #       w * w = total(endmember * endmember)
    #
    # substitute in the formula for the inverse endmember gives us
    #       inverse endmember = endmember / (w * w) = endmember / total(endmember * endmember)
    em_inverse = library / np.sum(library * library, 0)

    # STEP 2: get the fractions of modelling all endmembers with each other
    fractions = np.dot(em_inverse.transpose(), library)
    x = np.arange(n_spectra)
    fractions[x, x] = 0.0

    # APPLY CONSTRAINTS
    min_fraction = constraints[0] if constraints[0] != -9999 else None
    max_fraction = constraints[1] if constraints[1] != -9999 else None
    constraints = np.zeros([n_spectra, n_spectra], dtype=np.int8)

    if min_fraction:
        min_indices = np.where(fractions < min_fraction)
        constraints[min_indices] = 1 if reset else 2
        if reset:
            constraints[min_indices] = 1
            fractions[min_indices] = min_fraction
        else:
            constraints[min_indices] = 2

    if max_fraction:
        max_indices = np.where(fractions > max_fraction)
        if reset:
            constraints[max_indices] = 1
            fractions[max_indices] = max_fraction
        else:
            constraints[max_indices] = 2

    return fractions, constraints


def square_rmse(library: np.array, constraints: tuple = (-0.05, 1.05, 0.025), reset: bool = True,
                include_fractions: bool = False):
    """
    Calculate the RMSE of applying SMA between all members of a spectral library and return the results as a matrix.
    Optionally: also export the fractions (intermediate result)

    Export whether the fraction or RMSE constraint was breached and force fractions to threshold in case reset=True.

        * 0: no breach
        * 1: fraction constraint breach + fraction reset + no RMSE constraint breach
        * 2: fraction constraint breach + no fraction reset + no RMSE constraint breach
        * 3: no fraction constraint breach + RMSE constraint breach
        * 4: fraction constraint breach + fraction reset + RMSE constraint breach
        * 5: fraction constraint breach + no fraction reset + RMSE constraint breach

    :param library: spectral library [spectra as columns], scaled to reflectance values, without bad bands
    :param constraints: min fraction, max fraction and max RMSE. Use (-9999, -9999, -9999) for unconstrained.
    :param reset: fractions are reset to threshold values in case of breach
    :param include_fractions: set to true if you want to include the fractions in the output
    """
    constraints = (-9999, -9999, -9999) if not constraints else constraints
    if len(constraints) != 3:
        raise Exception("Constraints must be a tuple with 3 values.")
    if constraints[0] != -9999 and constraints[0] < -0.5:
        raise Exception("The minimum fraction constraint cannot be below -0.50.")
    if constraints[1] != -9999 and constraints[1] > 1.5:
        raise Exception("The maximum fraction constraint cannot be over 1.50.")
    if constraints[2] != -9999 and constraints[2] > 0.1:
        raise Exception("The maximum RMSE constraint cannot be over 0.10.")

    library = np.array(library, dtype=np.float32)
    n_bands, n_spec = library.shape

    block_size = math.ceil(250000000 / n_bands / n_spec)
    n_blocks = math.ceil(n_spec / block_size)

    fractions, con = square_fractions(library=library, constraints=constraints[0:2], reset=reset)
    rmse = np.zeros([n_spec, n_spec], dtype=np.float32)

    for b in range(n_blocks):
        start = b * block_size
        end = min((b + 1) * block_size, n_spec)

        residuals = library[:, np.newaxis, :] - (library[:, start:end, np.newaxis] * fractions[np.newaxis,
                                                                                               start:end, :])
        rmse[start:end, :] = np.sqrt(np.sum(residuals * residuals, axis=0) / n_bands)

    x = np.arange(n_spec)
    rmse[x, x] = 0.0
    rmse = np.float32(rmse)

    max_rmse = constraints[2] if constraints[2] != -9999 else None
    if max_rmse:
        rmse_indices = np.where(rmse > max_rmse)
        con[rmse_indices] += 3

    return (rmse, con, fractions) if include_fractions else (rmse, con)


def square_shade(fractions: np.array):
    """
    Fractions should sum to 1 so the shade fraction is 1 minus the other fractions.

    :param: fractions as calculated by LibraryMetrics.square_fractions
    """

    shade = 1.0 - fractions
    x = np.arange(shade.shape[0])
    shade[x, x] = 0.0

    return shade
