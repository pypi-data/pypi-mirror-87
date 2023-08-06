# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : November 2019
| Copyright           : © 2019 - 2020 by Ann Crabbé (KU Leuven) and Benjamin Jakimow (HU Berlin)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Extension on QGIS Plugin Support (QPS)
|                       Benjamin Jakimow (HU Berlin) https://bitbucket.org/jakimowb/qgispluginsupport
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
from qgis.utils import iface
from qgis.core import QgsCoordinateReferenceSystem, QgsPointXY
from qgis.gui import QgsMapCanvas, QgsMessageBarItem
from qgis.PyQt.QtCore import Qt

from spectral_libraries.qps.layerproperties import VectorLayerTools
from spectral_libraries.qps.speclib.core import SpectralProfile as qpsProfile, SpectralLibrary as qpsLib
from spectral_libraries.qps.speclib.gui import SpectralLibraryWidget as qpsWidget
from spectral_libraries.qps.maptools import CursorLocationMapTool as qpsMapTool
from spectral_libraries.qps.utils import SpatialExtent as qpsExtent, SpatialPoint as qpsPoint
from spectral_libraries.qps import initResources
initResources()


class SpectralLibraryWidget(qpsWidget):
    """
    QDialog to interactively work with Spectral Libraries in QGIS.
    """

    def __init__(self, spectral_library: qpsLib = None, map_canvas: QgsMapCanvas = None, i_face: iface = None):
        super(SpectralLibraryWidget, self).__init__(speclib=spectral_library)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # note:
        # self.mMapCanvas is an internal and invisible canvas of the SpectralLibrary(AttributeTable) widget
        # it is not the QGIS map canvas or another one that might exist temporary only
        self.map_tool_canvas: QgsMapCanvas = map_canvas
        self.map_tool = None
        self.actionSelectProfilesFromMap.setVisible(True)
        self.sigLoadFromMapRequest.connect(self.onActivateMapTool)

        # the VectorLayerTools class is used between SpectralLibraryWidget instances and other classes that react on
        # changes, e.g. to realize interactions with the QGIS map canvas
        vector_layer_tools = VectorLayerTools()
        vector_layer_tools.sigMessage.connect(lambda h, t, l: iface.messageBar().pushItem(QgsMessageBarItem(h, t, l)))
        vector_layer_tools.sigFreezeCanvases.connect(self.freezeCanvases)
        vector_layer_tools.sigZoomRequest.connect(self.zoomToExtent)
        vector_layer_tools.sigPanRequest.connect(self.panToPoint)

        self.setVectorLayerTools(vector_layer_tools)
        self.iface = i_face

    def onActivateMapTool(self):
        """
        Activates a map tool that informs on clicked map locations.
        """
        self.map_tool = qpsMapTool(self.map_tool_canvas, showCrosshair=True)
        self.map_tool.sigLocationRequest[QgsCoordinateReferenceSystem, QgsPointXY].connect(self.onLocationClicked)
        self.map_tool_canvas.setMapTool(self.map_tool)

    def onLocationClicked(self, crs: QgsCoordinateReferenceSystem, point: QgsPointXY):
        """
        Reacts on clicks to the QGIS Map canvas
        :param crs: coordinate reference system
        :param point: point in SpatialPoint format as defined in the qps package
        """
        spatial_point = qpsPoint(crs, point)
        profiles = qpsProfile.fromMapCanvas(self.map_tool_canvas, spatial_point)
        self.setCurrentProfiles(profiles)

    def zoomToExtent(self, extent: qpsExtent):
        """
        Zooms the QGIS map canvas to a requested extent
        """
        canvas = self.iface.mapCanvas()
        if isinstance(canvas, QgsMapCanvas) and isinstance(extent, qpsExtent):
            ext = extent.toCrs(canvas.mapSettings().destinationCrs())
            if isinstance(ext, qpsExtent):
                canvas.setExtent(ext)

    def panToPoint(self, point: qpsPoint):
        """
        pans the current map canvas to the provided point
        """
        canvas = self.iface.mapCanvas()
        if isinstance(canvas, QgsMapCanvas) and isinstance(point, qpsPoint):
            p = point.toCrs(canvas.mapSettings().destinationCrs())
            if isinstance(p, qpsPoint):
                canvas.setCenter(p)

    def freezeCanvases(self, b: bool):
        """
        Freezes/releases the map canvases
        """
        for c in self.iface.mapCanvases():
            c.freeze(b)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = SpectralLibraryWidget()
    z.show()

    app.exec_()


def _testing():
    from spectral_libraries.qps.testing import start_app
    app = start_app()

    import os
    from qgis.gui import QgisInterface
    from qgis.core import QgsRasterLayer, QgsProject
    from spectral_libraries.qps.testing import QgisMockup
    from spectral_libraries.qps import initAll
    initAll()
    from qgis.utils import iface
    assert isinstance(iface, QgisInterface)
    if isinstance(iface, QgisMockup):
        iface.ui.show()

    canvas = iface.mapCanvas()
    assert isinstance(canvas, QgsMapCanvas)

    raster_layer = QgsRasterLayer(os.path.join(os.path.dirname(__file__), '../../tests/data/testdata'),
                                  baseName='testdata')
    QgsProject.instance().addMapLayer(raster_layer)

    canvas.setLayers([raster_layer])
    canvas.setDestinationCrs(raster_layer.crs())
    canvas.setExtent(raster_layer.extent())

    widget = SpectralLibraryWidget(map_canvas=canvas)
    widget.show()

    app.exec_()


if __name__ == '__main__':
    _testing()
