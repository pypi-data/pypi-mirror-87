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
import argparse

from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant

from spectral_libraries.core.ear_masa_cob import EarMasaCob
from spectral_libraries.interfaces import imports


def create_parser():
    """ The parser for the CLI command parameters. """
    parser = argparse.ArgumentParser(description=str(EarMasaCob.__doc__))

    # library
    parser.add_argument('library', metavar='spectral library', help='spectral library input file')
    parser.add_argument('sp_class', metavar='class', help='metadata header with the spectrum classes')
    parser.add_argument('-r', '--reflectance-scale', metavar='\b', type=int,
                        help='in case L: reflectance scale factor (default: derived from data as 1, 1 000 or 10 000)')

    # constraints
    parser.add_argument('--min-fraction', metavar='\b', type=float, default=-0.05,
                        help='minimum allowable fraction (default -0.05), use -9999 for no constraint')
    parser.add_argument('--max-fraction', metavar='\b', type=float, default=1.05,
                        help='maximum allowable fraction (default 1.05), use -9999 for no constraint')
    parser.add_argument('--max-rmse', metavar='\b', type=float, default=0.025,
                        help='maximum allowable RMSE (default 0.025), use -9999 for no constraint')
    parser.add_argument('-u', '--unconstrained', action='store_true', default=False,
                        help='create a square array without constraints')
    parser.add_argument('-reset', '--reset-off', action='store_true', default=False,
                        help='do not reset fractions to the min/max when they surpass them, RMSE is then calculated '
                             'with these corrected values (ignored when no constraints are set) (default on)')

    # output
    parser.add_argument('-o', '--output', metavar='\b',
                        help="output library (default: same name as input library with suffix '_emc.sli'")

    return parser


def run_emc(args):
    """
    Documentation: viper-emc -h
    """

    library, names, classes = imports.import_library_as_array(args.library, spectra_names=True, metadata=args.sp_class)

    scale = args.reflectance_scale if args.reflectance_scale else imports.detect_reflectance_scale_factor(library)
    library = library / scale
    print('Reflectance scale factor: ' + str(scale))

    # get the constraints
    constraints = (-9999, -9999, -9999) if args.unconstrained else (args.min_fraction, args.max_fraction, args.max_rmse)
    use_reset = not args.reset_off

    # Run ear_masa_cob.py
    result = EarMasaCob().execute(library=library, class_list=classes, constraints=constraints, reset=use_reset)

    # Output
    output_file = args.output if args.output else '{}_emc.sli'.format(os.path.splitext(args.library)[0])

    # append metadata to spectral library
    spectral_library = imports.import_library(args.library)

    spectral_library.startEditing()
    spectral_library.addAttribute(QgsField(name="EAR", type=QVariant.Double))
    spectral_library.addAttribute(QgsField(name="MASA", type=QVariant.Double))
    if not args.unconstrained:
        spectral_library.addAttribute(QgsField(name="InCOB", type=QVariant.Int))
        spectral_library.addAttribute(QgsField(name="OutCOB", type=QVariant.Int))
        spectral_library.addAttribute(QgsField(name="COBI", type=QVariant.Double))
    spectral_library.commitChanges()

    # add extra attribute data
    fields = spectral_library.fields()
    ear_index = fields.indexFromName("EAR")
    masa_index = fields.indexFromName("MASA")
    profiles = spectral_library.profiles()
    spectral_library.startEditing()
    for (profile, ear, masa) in zip(profiles, result[0], result[1]):
        spectral_library.changeAttributeValue(profile.id(), ear_index, ear)
        spectral_library.changeAttributeValue(profile.id(), masa_index, masa)

    if not args.unconstrained:
        cob_in_index = fields.indexFromName("InCOB")
        cob_out_index = fields.indexFromName("OutCOB")
        cob_ratio_index = fields.indexFromName("COBI")
        profiles = spectral_library.profiles()
        for (profile, ci, co, cr) in zip(profiles, result[2], result[3], result[4]):
            spectral_library.changeAttributeValue(profile.id(), cob_in_index, ci)
            spectral_library.changeAttributeValue(profile.id(), cob_out_index, co)
            spectral_library.changeAttributeValue(profile.id(), cob_ratio_index, cr)

    # Export to new library
    spectral_library.write(output_file)


def main():
    """ Function called by CLI. """
    parser = create_parser()
    run_emc(parser.parse_args())


if __name__ == '__main__':
    main()
