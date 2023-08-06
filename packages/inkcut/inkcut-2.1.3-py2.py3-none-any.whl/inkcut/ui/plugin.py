"""
Copyright (c) 2017-2019, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jul 12, 2015

@author: jrm
"""
import sys
import enaml
import pkg_resources
from datetime import datetime
from atom.api import Atom, Int, List, Str, Instance, Bool, Enum, Dict
from enaml.qt.q_resource_helpers import get_cached_qicon
from enaml.layout.api import AreaLayout, DockBarLayout, HSplitLayout
from enaml.widgets.api import MenuBar
from enaml.application import timed_call

from inkcut.core.api import Plugin, DockItem, log
from inkcut.core.utils import load_icon
from . import extensions

with enaml.imports():
    from enaml.stdlib.dock_area_styles import available_styles


ALL_STYLES = sorted(['system']+available_styles())


class Clock(Atom):
    """ A clock so widgets can observe each field as required. """
    year = Int()
    month = Int()
    day = Int()
    hour = Int()
    minute = Int()
    second = Int()
    running = Bool(True)
    now = Instance(datetime, factory=lambda: datetime.now())

    def _observe_running(self, change):
        if self.running:
            timed_call(0, self.tick)

    def _observe_now(self, change):
        t = self.now
        self.year, self.month, self.day = t.year, t.month, t.day
        self.hour, self.minute, self.second = t.hour, t.minute, t.second
        if self.running:
            timed_call(1000, self.tick)

    def tick(self):
        self.now = datetime.now()


class InkcutPlugin(Plugin):
    #: Project site
    wiki_page = Str("https://www.codelv.com/projects/inkcut")

    #: For anything that needs to update every second
    clock = Instance(Clock, ())

    #: Dock items to add
    dock_items = List(DockItem)
    dock_layout = Instance(AreaLayout)
    dock_style = Enum(*reversed(ALL_STYLES)).tag(config=True)

    #: Settings pages to add
    settings_pages = List(extensions.SettingsPage)

    #: Current settings page
    settings_page = Instance(extensions.SettingsPage)

    #: Internal settings models
    settings_typemap = Dict()
    settings_model = Instance(Atom)

    def start(self):
        """ Load all plugins, refresh the dock area and then
        restore state from the disk (if any).

        """
        self.set_app_name()
        self.set_window_icon()
        if sys.platform == 'darwin':
            self.fix_menubar()
        self.load_plugins()
        self._refresh_dock_items()
        self._refresh_settings_pages()
        super(InkcutPlugin, self).start()

    def load_plugins(self):
        """ Load all the plugins Inkcut is dependent on """
        w = self.workbench
        plugins = []
        with enaml.imports():
            #: TODO autodiscover these
            from inkcut.preview.manifest import PreviewManifest
            from inkcut.job.manifest import JobManifest
            from inkcut.device.manifest import DeviceManifest
            from inkcut.joystick.manifest import JoystickManifest
            from inkcut.console.manifest import ConsoleManifest
            from inkcut.monitor.manifest import MonitorManifest
            plugins.append(PreviewManifest)
            plugins.append(JobManifest)
            plugins.append(DeviceManifest)
            plugins.append(JoystickManifest)
            plugins.append(ConsoleManifest)
            plugins.append(MonitorManifest)

            #: Load any plugins defined as extension points
            for entry_point in pkg_resources.iter_entry_points(
                    group='inkcut.plugin', name=None):
                plugins.append(entry_point.load())

        #: Install all of them
        for Manifest in plugins:
            w.register(Manifest())

    def _bind_observers(self):
        """ Setup the observers for the plugin.
        """
        super(InkcutPlugin, self)._bind_observers()
        workbench = self.workbench
        point = workbench.get_extension_point(extensions.DOCK_ITEM_POINT)
        point.observe('extensions', self._refresh_dock_items)

        point = workbench.get_extension_point(extensions.SETTINGS_PAGE_POINT)
        point.observe('extensions', self._refresh_settings_pages)

    def _unbind_observers(self):
        """ Remove the observers for the plugin.
        """
        super(InkcutPlugin, self)._unbind_observers()
        workbench = self.workbench
        point = workbench.get_extension_point(extensions.DOCK_ITEM_POINT)
        point.unobserve('extensions', self._refresh_dock_items)

        point = workbench.get_extension_point(extensions.SETTINGS_PAGE_POINT)
        point.unobserve('extensions', self._refresh_settings_pages)

    # -------------------------------------------------------------------------
    # Dock item extension API
    # -------------------------------------------------------------------------
    def create_new_area(self):
        """ Create the dock area
        """
        with enaml.imports():
            from .dock import DockView
        area = DockView(
            workbench=self.workbench,
            plugin=self
        )
        return area

    def _refresh_dock_items(self, change=None):
        """ Reload all DockItems registered by any Plugins

        Any plugin can add to this list by providing a DockItem
        extension in their PluginManifest.

        """
        workbench = self.workbench
        point = workbench.get_extension_point(extensions.DOCK_ITEM_POINT)

        #: Layout spec
        layout = {
            'main': [],
            'left': [],
            'right': [],
            'bottom': [],
            'top': []
        }

        dock_items = []
        for extension in sorted(point.extensions, key=lambda ext: ext.rank):
            for declaration in extension.get_children(extensions.DockItem):

                # Load the plugin
                plugin_id = declaration.plugin_id
                log.info("Loading plugin {}".format(plugin_id))
                plugin = workbench.get_plugin(plugin_id)

                # Check if it's known dependencies are met
                if not plugin.is_supported():
                    log.warning("Plugin {} reported unsupported".format(
                        plugin_id))
                    continue

                # Create the item
                DockItem = declaration.factory()
                item = DockItem(
                    plugin=plugin,
                    closable=False
                )

                # Add to our layout
                layout[declaration.layout].append(item.name)

                # Save it
                dock_items.append(item)

        #: Update items
        log.debug("Updating dock items: {}".format(dock_items))
        self.dock_items = dock_items
        self._refresh_layout(layout)

    def _refresh_layout(self, layout):
        """ Create the layout for all the plugins


        """
        items = layout.pop('main')
        main = HSplitLayout(*items) if len(items) > 1 else items[0]

        dockbars = [DockBarLayout(*items, position=side)
                    for side, items in layout.items() if items]

        #: Update layout
        self.dock_layout = AreaLayout(
            main,
            dock_bars=dockbars
        )

    # -------------------------------------------------------------------------
    # Settings page extension API
    # -------------------------------------------------------------------------
    def _default_settings_page(self):
        return self.settings_pages[0]

    def _observe_settings_page(self, change):
        log.debug("Settings page: {}".format(change))

    def _refresh_settings_pages(self, change=None):
        """ Reload all SettingsPages registered by any Plugins

        Any plugin can add to this list by providing a SettingsPage
        extension in their PluginManifest.

        """
        workbench = self.workbench
        point = workbench.get_extension_point(extensions.SETTINGS_PAGE_POINT)

        settings_pages = []
        typemap = {}
        for extension in sorted(point.extensions, key=lambda ext: ext.rank):
            for d in extension.get_children(extensions.SettingsPage):
                #: Save it
                settings_pages.append(d)

                #: Update the type map
                plugin = self.workbench.get_plugin(d.plugin_id)
                t = type(getattr(plugin, d.model) if d.model else plugin)
                typemap[t] = d.factory()

        #: Update items
        log.debug("Updating settings pages: {}".format(settings_pages))

        self.settings_typemap = typemap
        self.settings_pages = sorted(settings_pages, key=lambda p: p.name)

    # -------------------------------------------------------------------------
    # Utility methods
    # -------------------------------------------------------------------------
    def set_app_name(self):
        """ Set the application name

        """
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        try:
            qt_app = ui._application._qapp
            qt_app.setApplicationName('inkcut')
            if hasattr(qt_app, 'setApplicationDisplayName'):
                qt_app.setApplicationDisplayName('Inkcut')
        except Exception as e:
            log.error('Failed to set app name: {}'.format(e))

    def set_window_icon(self):
        """ Set the main application window icon

        """
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        try:
            icon = get_cached_qicon(load_icon('logo'))
            ui.window.proxy.widget.setWindowIcon(icon)
        except Exception as e:
            log.error('Failed to set window icon: {}'.format(e))

    def fix_menubar(self):
        """ Disable native menu on OSX

        """
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        for c in ui.window.children:
            if isinstance(c, MenuBar):
                c.proxy.widget.setNativeMenuBar(False)
                break
