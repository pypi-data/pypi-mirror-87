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
import numpy as np
import argparse

from spectral_libraries.core.ies import Ies
from spectral_libraries.interfaces import exports, imports


def create_parser():
    """ The parser for the CLI command parameters. """
    parser = argparse.ArgumentParser(description=str(Ies.__doc__))

    # library
    parser.add_argument('library', metavar='spectral library', help='spectral library input file')
    parser.add_argument('sp_class', metavar='class', help='metadata header with the spectrum classes')
    parser.add_argument('-r', '--reflectance-scale', metavar='\b', type=int,
                        help='in case L: reflectance scale factor (default: derived from data as 1, 1 000 or 10 000)')

    # constraints
    parser.add_argument('--min-fraction', metavar='\b', type=float, default=-0.05,
                        help='minimum allowable fraction (default -0.05)')
    parser.add_argument('--max-fraction', metavar='\b', type=float, default=1.05,
                        help='maximum allowable fraction (default 1.05)')
    parser.add_argument('--max-rmse', metavar='\b', type=float, default=0.025,
                        help='maximum allowable RMSE (default 0.025)')

    # forced endmembers
    parser.add_argument('-f', '--forced-selection', metavar='\b', nargs='+', type=int, help='numpy array with indices '
                        'of the library spectra that should be forcefully add to the selection')
    parser.add_argument('-g', '--forced-step', metavar='\b', type=int, help='insert forced endmembers after this step')

    # output
    parser.add_argument('-o', '--output', metavar='\b',
                        help="output library (default: same name as input library with suffix '_ies.sli'")

    return parser


def run_ies(args):
    """
    Documentation: viper-ies -h
    """
    library, names, classes = imports.import_library_as_array(args.library, spectra_names=True, metadata=args.sp_class)

    scale = args.reflectance_scale if args.reflectance_scale else imports.detect_reflectance_scale_factor(library)
    library = library / scale
    print('Reflectance scale factor: ' + str(scale))

    class_unique, class_list = np.unique(classes, return_inverse=True)

    if len(class_unique) == 1:
        print('IES requires more than one class, please select another column')
        return

    # get the constraints
    constraints = (args.min_fraction, args.max_fraction, args.max_rmse)

    if args.forced_selection is not None:
        forced_list = np.array(args.forced_selection, dtype=int)
        forced_step = args.forced_step
        if len(forced_list) == 0:
            print('No endmembers selected to forcefully add to the ies process.')
            return
        if max(forced_list) >= len(names):
            print('Forced library selection indexes too big.')
            return
        if min(forced_list) < 0:
            print('Forced library selection indexes too small.')
    else:
        forced_list = None
        forced_step = None

    # run ies
    ies_selection, ies_metadata = Ies().execute(library=library, class_list=class_list, constraints=constraints,
                                                forced_list=forced_list, forced_step=forced_step,
                                                summary=True)
    if ies_selection is None:
        print("IES selected no spectra. Output empty.")
        return

    # Output
    output_file = args.output if args.output else '{}_ies.sli'.format(os.path.splitext(args.library)[0])

    # write output library and metadata file
    spectral_library = imports.import_library(args.library)
    profiles_list = list(spectral_library.profiles())
    fid_attribute_index = profiles_list[0].fieldNameIndex('fid')
    fid_list = [profiles_list[x].attributes()[fid_attribute_index] for x in ies_selection]

    ies_library = spectral_library.speclibFromFeatureIDs(fid_list)
    ies_library.write(path=output_file)

    exports.save_ies_metadata(ies_metadata, args.library, os.path.splitext(output_file)[0] + '_summary.txt',
                              forced_list, forced_step, args.sp_class, classes, names, ies_selection)


def main():
    """ Function called by CLI. """
    parser = create_parser()
    run_ies(parser.parse_args())


if __name__ == '__main__':
    main()
