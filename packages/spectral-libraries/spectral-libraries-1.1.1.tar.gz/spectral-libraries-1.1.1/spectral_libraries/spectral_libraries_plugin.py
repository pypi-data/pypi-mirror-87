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
from os import path
from sip import isdeleted
from typing import Dict

from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QWidget

from spectral_libraries.interfaces.spectral_library_gui import SpectralLibraryWidget
from spectral_libraries.interfaces.square_array_gui import SquareArrayWidget
from spectral_libraries.interfaces.ies_gui import IesWidget
from spectral_libraries.interfaces.ear_masa_cob_gui import EarMasaCobWidget
from spectral_libraries.interfaces.cres_gui import CresWidget
from spectral_libraries.interfaces.music_gui import MusicWidget
from spectral_libraries.interfaces.amuses_gui import AmusesWidget
from spectral_libraries.qps.speclib.core import SpectralLibrary
from spectral_libraries.images.speclib_resources_rc import qInitResources as Resources

Resources()


class SpectralLibrariesPlugin:
    """ QGIS Plugin Implementation """

    def __init__(self, iface):
        """
        :param QgsInterface iface: the interface instance which provides the hook to manipulate the QGIS GUI at run time
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)

        # List of actions added by this plugin
        self.actions = []

        from spectral_libraries.qps import initAll
        initAll()

        # Add an empty menu to the Raster Menu
        self.menu = QMenu(title='Spectral Libraries', parent=self.iface.rasterMenu())
        self.menu.setIcon(QIcon(':/profile'))
        self.iface.rasterMenu().addMenu(self.menu)

        # Add an empty toolbar
        self.toolbar = self.iface.addToolBar('Spectral Library Toolbar')

        # Reference to all open Library Widgets
        self.opened_library_widgets: Dict[str, SpectralLibraryWidget] = dict()
        self.count = 0

        # Permanent reference needed for cres widget, otherwise auto-closes
        self.cres_widget = None

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        # add actions to menu and/or toolbar
        action = QAction(QIcon(':/profile'), 'Create Library', self.iface.mainWindow())
        action.triggered.connect(self.start_library_widget)
        action.setStatusTip('Create Library')
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/cube'), 'Square Array', self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('sqa'))
        action.setStatusTip('Square Array')
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/iteration'), 'IES', self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('ies'))
        action.setStatusTip('IES')
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/average'), "Ear, Masa, Cob", self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('emc'))
        action.setStatusTip("Ear, Masa, Cob")
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/music'), "MUSIC", self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('music'))
        action.setStatusTip("MUSIC")
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/prune'), "AMUSES", self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('amuses'))
        action.setStatusTip("AMUSES")
        self.toolbar.addAction(action)
        self.menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/percentage'), 'CRES', self.iface.mainWindow())
        action.triggered.connect(self.run_cres)
        action.setStatusTip('CRES')
        self.menu.addAction(action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.rasterMenu().removeAction(self.menu.menuAction())

        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        # remove the toolbar
        del self.toolbar

    def start_library_widget(self, *args, **kwds):
        self.count += 1

        new_widgets = []
        # search in LayerTree/TOC for checked (visible in canvas) and unchecked (not in canvas but layer tree) libraries
        # (https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/cheat_sheet.html#table-of-contents)
        for layerNode in self.iface.layerTreeView().model().rootGroup().findLayers():
            layer_id: str = layerNode.layerId()
            speclib = layerNode.layer()
            speclib: SpectralLibrary

            if str(layerNode.customProperty('nodeHidden')).lower() == 'true':
                continue
            if not isinstance(speclib, QgsVectorLayer):
                continue

            if ('SpectralLibrary' in layer_id) and (layer_id not in self.opened_library_widgets.keys()):
                widget = SpectralLibraryWidget(map_canvas=self.iface.mapCanvas(), spectral_library=speclib)
                new_widgets.append(widget)

        widget = SpectralLibraryWidget(map_canvas=self.iface.mapCanvas(), i_face=self.iface)
        widget.speclib().setName("Spectral Library " + str(self.count))
        QgsProject.instance().addMapLayer(widget.speclib())
        new_widgets.append(widget)

        for widget in new_widgets:
            widget: SpectralLibraryWidget
            layer_id = widget.speclib().id()
            # ensure that opened_library_widgets removes the widget reference immediately
            widget.destroyed.connect(lambda *args, id=layer_id: self.remove_library_layer(id))
            # speclib deleted? close and remove widget too
            widget.speclib().willBeDeleted.connect(lambda *args, id=layer_id: self.remove_library_layer(id))
            self.opened_library_widgets[layer_id] = widget
            widget.show()

    def remove_library_layer(self, layer_id: str):

        if layer_id in self.opened_library_widgets.keys():
            widget = self.opened_library_widgets.pop(layer_id)
            if isinstance(widget, QWidget) and not isdeleted(widget):
                widget.close()

    @staticmethod
    def run_widget(plugin: str):
        switcher = {
            'sqa': SquareArrayWidget(),
            'ies': IesWidget(),
            'emc': EarMasaCobWidget(),
            'music': MusicWidget(),
            'amuses': AmusesWidget()
        }

        widget = switcher[plugin]
        widget.show()
        widget.exec_()

    def run_cres(self):
        self.cres_widget = CresWidget()
        self.cres_widget.show()
