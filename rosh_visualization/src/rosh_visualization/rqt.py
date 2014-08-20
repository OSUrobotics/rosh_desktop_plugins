from qt_gui.plugin_manager import PluginManager
from qt_gui.composite_plugin_provider import CompositePluginProvider
from qt_gui.application_context import ApplicationContext
from rqt_gui.main import Main
from python_qt_binding.QtCore import QSettings

from rosh.impl.exceptions import InvalidPlugin
from rosh.impl.namespace import Namespace, Concept
from rosh.impl.packages import Packages


class options:
    multi_process = False
    embed_plugin = False
    force_discover = False


class RQTPlugin(Namespace):
    def __init__(self, name, config):
        super(RQTPlugin, self).__init__(name, config)


class RQTPlugins(Concept):
    def __init__(self, ctx, lock):
        super(RQTPlugins, self).__init__(ctx, lock, RQTPlugin)
        # m = Main()
        # m._add_plugin_providers()
        # plugin_providers = m.plugin_providers
        # context = ApplicationContext()
        # context.options = options
        # _settings_filename = 'rqt_gui'
        # settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ros.org', _settings_filename)
        # plugin_manager_settings_prefix = ''

        # plugin_provider = CompositePluginProvider(plugin_providers)
        # plugin_manager = PluginManager(plugin_provider, settings, context, settings_prefix=plugin_manager_settings_prefix)

        # plugin_manager._discover()
        # plugin_manager._close_application_signal()
        # plugin_manager._close_application_shutdown_plugins()
        # plugins = plugin_manager._discover()
        # plugin_manager.__dict__ = {}
        # plugins = plugin_manager.get_plugins()
        packages = Packages(ctx, lock)
        for package in packages:
            continue

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return object.__setattr__(self, key, value)
        else:
            return self._root.__setitem__(key, value)

    def __call__(self, obj, plugin_pkg):
        print plugin_pkg

def show_concept(asdf):
    pass