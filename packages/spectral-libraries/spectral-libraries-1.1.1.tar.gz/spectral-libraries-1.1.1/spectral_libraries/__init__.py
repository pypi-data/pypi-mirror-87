# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):
    """
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from spectral_libraries.spectral_libraries_plugin import SpectralLibrariesPlugin
    return SpectralLibrariesPlugin(iface)
