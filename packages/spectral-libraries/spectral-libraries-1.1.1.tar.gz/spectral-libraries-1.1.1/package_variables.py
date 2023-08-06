# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : March 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
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
dense_name = 'spectral-libraries'  # used for distributing your package on pip or qgis, no spaces
long_name = 'Spectral Library Tool'  # what users see in the QGIS plugin repository and on the RTD toc
pdf_title = 'Spectral Library Tool Documentation'  # the front page title on the read the docs PDF version

author = 'Ann Crabbé'  # your name
author_email = 'acrabbe.foss@gmail.com'  # your contact information
author_copyright = '© 2018 - 2020 by Ann Crabbé'  # a copyright, typical "© [start year] - [end year] by [your name]"
short_version = '1.1'  # 2 numbers, update with each new release
long_version = '1.1.1'  # 3 numbers, update with each new release

bitbucket_home = 'https://bitbucket.org/kul-reseco/spectral-libraries'
bitbucket_src = 'https://bitbucket.org/kul-reseco/spectral-libraries/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/spectral-libraries/issues'

read_the_docs = 'https://spectral-libraries.readthedocs.io'

keywords = ['ies', 'ear', 'masa', 'cob', 'emc', 'cres', 'square array', 'spectral library', 'remote sensing', 'viper',
            'endmember', 'spectral signal', 'music', 'amuses']

qgis_min_version = '3.14'

short_description = 'The Spectral Library Tool is a suite of processing tools for multi- and hyperspectral libraries.'
long_description = 'Creating spectral libraries interactively (selecting spectra from an image or using regions of ' \
                   'interest); visualizing the library on a plot and managing the metadata (developed by HU Berlin); ' \
                   'Optimizing spectral libraries with IES, Ear-Masa-Cob, CRES, MUSIC, AMUSES.'

qgis_metadata_icon = 'images/profile.png'
qgis_category = 'Raster'
processing_provider = False
