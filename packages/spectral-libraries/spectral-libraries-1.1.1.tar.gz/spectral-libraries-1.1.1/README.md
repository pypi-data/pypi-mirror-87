###############################
About The Spectral Library Tool
###############################

The Spectral Library Tool software package is both a QGIS plugin and stand-alone python package that provides a suite of
processing tools for multi- and hyperspectral spectral libraries.

The software is based on VIPER Tools: code written for ENVI/IDL and released in 2007.
Several updates have been released since and now it has been ported to PyQGIS in the period 2017 - 2020.
The original VIPER Tools is now split over two python/QGIS tools: Spectral Library Tools and MESMA.

**Spectral Library Tool** provides the following:
 - Creating spectral libraries interactively (selecting spectra from an image or using regions of interest) and managing
   the metadata (developed by HU Berlin)
 - Optimizing spectral libraries with Iterative Endmember Selection, Ear-Masa-Cob, CRES, MUSIC or AMUSES
 - Website: <https://spectral-libraries.readthedocs.io>
 - Repository: https://bitbucket.org/kul-reseco/spectral-libraries

**MESMA** provides the following:
 - Running SMA and MESMA (with multi-level fusion, stable zone unmixing, ...)
 - Post-processing of the MESMA results (visualisation tool, shade normalisation, ...)
 - Website: <https://mesma.readthedocs.io>
 - Repository: https://bitbucket.org/kul-reseco/mesma

The software has now been developed in the open source environment to encourage further development of the tool.

**PLEASE GIVE US CREDIT**

When using The Spectral Library Tool, please use the following citation:

*Crabbé, A. H., Jakimow, B., Somers, B., Roberts, D. A., Halligan, K., Dennison, P., Dudley, K. (2020).*
*Spectral Library QGIS Plugin (Version x) [Software]. Available from https://bitbucket.org/kul-reseco/spectral-libraries.*

**ACKNOWLEDGEMENTS**

The software and user guide are based on VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab):
Roberts, D. A., Halligan, K., Dennison, P., Dudley, K., Somers, B., Crabbe, A., 2018, Viper Tools User Manual,
Version 2, 91 pp.

The software also makes use of the QGISPluginSupport python packages developed by Benjamin Jakimow  (HU Berlin):
https://bitbucket.org/jakimowb/qgispluginsupport.

The MUSIC and AMUSES algorithms are based on work and code by Jeroen Degerickx (KU Leuven):
https://doi.org/10.3390/rs9060565.

This revision is funded primarily through BELSPO (the Belgian Science Policy Office) in the framework
of the STEREO III Programme – Project LUMOS - SR/01/321.

Logo's were created for free at https://logomakr.com.

**SOFTWARE LICENSE**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.


