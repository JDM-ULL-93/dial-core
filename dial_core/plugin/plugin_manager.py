# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from typing import Optional

import dependency_injector.providers as providers

from dial_core.plugin import Plugin
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


# How are plugins going to be stored?
# * Structure that can be stored per project and per installation.
# * List of installed plugins (downloaded), list of active pluglins.
# * Active plugins are activated depending on the active project.
# * Don't unload plugin completely, just put in on hold.

# * -> OR, always show all installed projects, saving on the project only the used ones.
# * So, only have an unique list of all the installed plugins, and list which ones are
# loaded or not.
# * Loaded plugins are loaded on start.

# Have a superior structure that can be used to query for version, name, path, and more
# necessary attributes.

# Also has a reference to the inner module


# TODO FOR TOMORROW
# * Load/Save plugins to a list
# * Show loaded nodes on the gui


class PluginManager:
    def __init__(self):
        self.__installed_plugins = {}

    @property
    def installed_plugins(self):
        return self.__installed_plugins

    def install_plugin(self, plugin_path: str):
        if not os.path.exists(plugin_path):
            raise FileNotFoundError("Can't import this plugin")

        plugin = Plugin(plugin_path)
        self.__installed_plugins[plugin.name] = plugin

    def load_plugin(self, plugin_name: str) -> Optional["Plugin"]:
        plugin = self.__get_plugin_by_name(plugin_name)
        plugin.load()

        return plugin

    def unload_plugin(self, plugin_name: str):
        plugin = self.__get_plugin_by_name(plugin_name)
        plugin.unload()

    def __get_plugin_by_name(self, plugin_name):
        try:
            return self.__installed_plugins[plugin_name]

        except KeyError as err:
            LOGGER.warning("Can't load a plugin called %s", plugin_name)
            raise err


PluginManagerSingleton = providers.Singleton(PluginManager)
