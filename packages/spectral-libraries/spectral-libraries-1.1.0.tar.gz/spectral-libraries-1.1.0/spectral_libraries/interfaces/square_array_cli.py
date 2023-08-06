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
import os
import time
import numpy as np
import argparse

from spectral_libraries.core.square_array import SquareArray
from spectral_libraries.interfaces import exports, imports


def create_parser():
    """ The parser for the CLI command parameters. """
    parser = argparse.ArgumentParser(description=str(SquareArray.__doc__))

    # library
    parser.add_argument('library', metavar='input', help='spectral library file')
    parser.add_argument('--reflectance-scale', metavar='\b', type=int,
                        help='reflectance scale factor (default: derived from data as 1, 1 000 or 10 000)')

    # constraints
    parser.add_argument('--min-fraction', metavar='\b', type=float, default=-0.05,
                        help='minimum allowable fraction (default -0.05), use -9999 for no constraint')
    parser.add_argument('--max-fraction', metavar='\b', type=float, default=1.05,
                        help='maximum allowable fraction (default 1.05), use -9999 for no constraint')
    parser.add_argument('--max-rmse', metavar='\b', type=float, default=0.025,
                        help='maximum allowable RMSE (default 0.025), use -9999 for no constraint')
    parser.add_argument('-u', '--unconstrained', action='store_true', default=False,
                        help='create a square array without constraints')
    parser.add_argument('-r', '--reset-off', action='store_true', default=False,
                        help='do not reset fractions to the min/max when they surpass them, RMSE is then calculated '
                             'with these corrected values (ignored when no constraints are set) (default on)')

    # output
    parser.add_argument('-o', '--output', metavar='\b',
                        help="output ENVI file with square array (default: in same folder with extension '_sq.sqr'")

    # bands
    parser.add_argument('--exclude-rmse', action='store_true', default=False,
                        help='exclude rmse band (default: included)')
    parser.add_argument('--exclude-constraints', action='store_true', default=False,
                        help='exclude constraints band (default: included, ignored no constraints are set)')
    parser.add_argument('--include-fractions', action='store_true', default=False,
                        help='include fractions band (default: excluded)')
    parser.add_argument('--include-shade', action='store_true', default=False,
                        help='include shade band (default: excluded)')
    parser.add_argument('--include-angle', action='store_true', default=False,
                        help='include spectral angle band (default: excluded)')

    return parser


def run_square_array(args):
    """
    Documentation: viper-square -h
    """

    library, spectra_names, _ = imports.import_library_as_array(args.library, spectra_names=True)

    # divide the library by the reflectance scale
    scale = args.reflectance_scale if args.reflectance_scale else imports.detect_reflectance_scale_factor(library)
    library = library / scale
    print('Reflectance scale factor: ' + str(scale))

    # get the constraints
    constraints = (-9999, -9999, -9999) if args.unconstrained else (args.min_fraction, args.max_fraction, args.max_rmse)
    use_reset = not args.reset_off

    # output preferences
    out_rmse = not args.exclude_rmse
    out_constraints = False if sum(constraints) == -29997 else not args.exclude_constraints
    out_angle = args.include_angle
    out_fractions = args.include_fractions
    out_shade = args.include_shade

    # Run square_array.py
    start = time.time()
    square_array = SquareArray().execute(library=library, constraints=constraints, reset=use_reset, out_rmse=out_rmse,
                                         out_constraints=out_constraints, out_fractions=out_fractions,
                                         out_shade=out_shade, out_angle=out_angle)
    duration = np.float16(time.time() - start)

    # output name
    if args.output:
        output_base, ext = os.path.splitext()
        output_file = output_base if ext.lower() in ['.tiff', '.tif'] else args.output
    else:
        output_file = '{}_sq.sqr'.format(os.path.splitext(args.library)[0])

    exports.save_square_to_envi(square_array=square_array, outfile_path=output_file, spectra_names=spectra_names,
                                library_name=os.path.basename(args.library), constraints=constraints, reset=use_reset,
                                duration=duration, ngb=library.shape[0])


def main():
    """ Function called by CLI. """
    parser = create_parser()
    run_square_array(parser.parse_args())


if __name__ == '__main__':
    main()
