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

from .library_metrics import square_rmse, square_angle


class EarMasaCob:
    """  Calculate EAR, MASA, and CoB values from a spectral library.

     * EAR = Endmember Average RMSE
     * MASA = Minimum Average Spectral Angle
     * CoB = Count based Endmember selection (CoB)

    Citation EAR:

    Dennison, P.E., Roberts, D.A., 2003, Endmember Selection for Multiple Endmember Spectral Mixture Analysis using
    Endmember Average RMSE, Remote Sensing of Environment, 87, p. 123-135.

    Citation MASA:

    Dennison, P.E., Halligan, K. Q., Roberts, D.A., 2004, A Comparison of Error Metrics and Constraints for Multiple
    Endmember Spectral Mixture Analysis and Spectral Angle Mapper, Remote Sensing of Environment, 93, p. 359-367.

    Citations CoB:

    Roberts, D.A., Dennison, P.E., Gardner, M.E., Hetzel, Y., Ustin, S.L., Lee, C.T., 2003, Evaluation of the potential
    of Hyperion for fire danger assessment by comparison to the Airborne Visible/Infrared Imaging Spectrometer, IEEE
    Transactions on Geoscience and Remote Sensing, 41, p. 1297-1310.

    Clark, M., 2005, An assessment of Hyperspectral and LIDAR Remote Sensing for the Monitoring of Tropical Rain Forest
    Trees, PhD Dissertation, UC Santa Barbara, 319 p.
    """

    def __init__(self):
        pass

    @staticmethod
    def execute(library: np.array, class_list: np.array, constraints: tuple = (-0.05, 1.05, 0.025), reset: bool = True,
                log: callable = print):
        """
        Calculate EAR, MASA and COB parameters.

        Beware of the square array used as input! Ideally it is built in 'reset' mode. The constraints band
        has 6 possible values indicating which constraint was breached:

            * 0 = no breach
            * 1/2 = a fraction constraint breached (reset/no reset)
            * 3 = RMSE constraint breached
            * 4/5 = 1/2 (fractions reset/no reset) + 3 (RMSE)

        :param library: spectral library [spectra as columns], scaled to reflectance values, without bad bands
        :param class_list: str array with the class for each spectrum (e.g. GV or SOIL)
        :param constraints: min fraction, max fraction and max RMSE. Use (-9999, -9999, -9999) for unconstrained.
        :param reset: fractions are reset to threshold values in case of breach, BEST TURNED ON
        :param log: log function
        :return: ear, masa, cob_in, cob_out, cob_ratio: all 1-D arrays complementing the original library's metadata.
        """
        n_spec = class_list.shape[0]
        n_spec_range = np.arange(n_spec)
        log = print if log is None else log

        if constraints == (-9999, -9999, -9999) or not constraints:
            constraints = None
            log("Unconstrained mode: no COB values calculated.")

        if reset is False:
            log("Fractions are not reset when calculating the RMSE. This can influence the EAR and COB values.")

        log('Calculating the RMSE')

        rmse_band, constraints_band = square_rmse(library=library, constraints=constraints, reset=reset)

        # change the constraints band to hold '1' if no constrained was breached and '0' otherwise,
        # in other words '1' indicates a successful unmixing
        x, y = np.where(constraints_band == 0)
        constraints_band = np.zeros([n_spec, n_spec], dtype=np.bool)
        constraints_band[x, y] = 1
        constraints_band[n_spec_range, n_spec_range] = 0  # diagonal

        log('EMC calculations started')

        # get the unique groups
        class_list = np.asarray([x.lower() for x in class_list])
        groups = np.unique(class_list)
        log('Number of groups: ' + str(groups.shape[0]))

        # prep the output arrays
        ear = np.zeros(n_spec, dtype=float)  # EAR: average RMSE within the group
        masa = np.zeros(n_spec, dtype=float)  # MASA: average Spectral Angle within the group
        if constraints:
            cob_in = np.zeros(n_spec, dtype=float)  # InCoB: number of spectra modeled by EM within the group
            cob_out = np.zeros(n_spec, dtype=int)  # OutCoB: number of spectra modeled by EM outside the group
            groups_n = np.zeros(n_spec, dtype=int)  # Helper for the CoBI calculation
        else:
            cob_in = None
            cob_out = None
            groups_n = None

        # remember in the square array: rows are the 'models' and columns are the 'pixels to be unmixed' by the models
        for group in groups:
            log('     Current group: ' + group)
            inside_indices = np.where(class_list == group)[0]

            # MASA
            spectral_angle_inside = square_angle(library[:, inside_indices])

            # number of nonzero spectral angle elements per column, to account for the effect of duplicate spectra
            n_nonzero_items = np.sum(spectral_angle_inside != 0, 1)

            # mean of the spectral angle of non-zero elements
            with np.errstate(invalid='ignore'):
                masa[inside_indices] = np.sum(spectral_angle_inside, 1) / n_nonzero_items

            # EAR
            rmse_inside = rmse_band[inside_indices[:, None], inside_indices[None, :]]

            # mean of the rmse of non-zero elements
            with np.errstate(invalid='ignore'):
                ear[inside_indices] = np.sum(rmse_inside, 1) / n_nonzero_items

            # COB
            if constraints:
                outside_indices = np.where(class_list != group)[0]
                n = inside_indices.shape[0]
                groups_n[inside_indices] = n

                constraints_inside = constraints_band[inside_indices[:, None], inside_indices[None, :]]
                constraints_outside = constraints_band[inside_indices[:, None], outside_indices[None, :]]

                """
                Until all spectra have been used, do:
                1) Calculate CoB as count of all spectra (col) successfully unmixed by each model (row)
                2) Find the highest CoB (there may be ties!) and save this value
                3) Remove rows/cols of highest CoB + all spectra modeled by it so they can no longer influence step 1
                4) Repeat steps 1-3 until there are are no available spectra [all status = 0]
                When more than 1 group exist calculate the out of group CoB and the CoBI
                """
                unused = np.ones(n, dtype=bool)
                while np.sum(unused) > 0:
                    cob = np.sum(constraints_inside, 1)
                    cob_max = cob.max()
                    if cob_max != 0:
                        cob_index = np.where(cob == cob_max)[0]
                        cob_in[inside_indices[cob_index]] = cob_max
                    else:
                        cob_index = np.where(unused)[0]
                    if n < n_spec:
                        cob_out[inside_indices[cob_index]] = np.sum(constraints_outside[cob_index, :], 1)

                    # set the 'pixel' containing the model, as the 'pixels' unmixed by the model to 0
                    # set the same 'models' to 0
                    unmixed = np.where(constraints_inside[cob_index, :])[1]
                    constraints_inside[:, unmixed] = 0
                    constraints_inside[unmixed, :] = 0
                    constraints_inside[:, cob_index] = 0
                    constraints_inside[cob_index, :] = 0
                    unused[cob_index] = 0
                    unused[unmixed] = 0

        if constraints:
            # CoBI: CoB index (InCoB/OutCoB/number of spectra in the group)
            cob_ratio = np.divide(cob_in / groups_n, cob_out, out=np.zeros_like(cob_in), where=cob_out != 0)
        else:
            cob_ratio = None

        return ear, masa, cob_in, cob_out, cob_ratio
