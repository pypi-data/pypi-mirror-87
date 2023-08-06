import os
import yaml
import logging
from copy import deepcopy
from typing import Dict, List, Optional, Iterable

import meltano.core.bundle as bundle
from meltano.core.utils import nest, NotFound
from .project import Project
from .setting_definition import SettingDefinition
from .plugin import PluginDefinition, ProjectPlugin, PluginType, PluginRef
from .plugin.factory import plugin_factory
from .plugin.error import PluginMissingError

logger = logging.getLogger(__name__)


class PluginAlreadyAddedException(Exception):
    def __init__(self, plugin: PluginRef):
        self.plugin = plugin
        super().__init__()


class ConfigService:
    def __init__(self, project: Project):
        self.project = project

        self._settings = None
        self._current_config = None

    @property
    def settings(self):
        if self._settings is None:
            with bundle.find("settings.yml").open() as settings_yaml:
                settings = yaml.safe_load(settings_yaml)
            self._settings = list(map(SettingDefinition.parse, settings["settings"]))

        return self._settings

    @property
    def current_config(self):
        if self._current_config is None:
            self._current_config = self.project.meltano.extras
        return self._current_config

    def update_config(self, config):
        with self.project.meltano_update() as meltano:
            meltano.extras = config

        self._current_config = None

    def make_meltano_secret_dir(self):
        os.makedirs(self.project.meltano_dir(), exist_ok=True)

    def add_to_file(self, plugin: ProjectPlugin):
        plugin = plugin_factory(plugin.type, plugin.canonical())

        if not plugin.should_add_to_file(self.project):
            return plugin

        with self.project.meltano_update() as meltano_yml:
            if plugin in self.plugins():
                raise PluginAlreadyAddedException(plugin)

            if not plugin.type in meltano_yml.plugins:
                meltano_yml.plugins[plugin.type] = []

            meltano_yml.plugins[plugin.type].append(plugin)

        return plugin

    def has_plugin(self, plugin_name: str):
        try:
            self.find_plugin(plugin_name)
            return True
        except PluginMissingError:
            return False

    def find_plugin(
        self,
        plugin_name: str,
        plugin_type: Optional[PluginType] = None,
        invokable=None,
        configurable=None,
    ) -> ProjectPlugin:
        if "@" in plugin_name:
            plugin_name, profile_name = plugin_name.split("@", 2)
            logger.warning(
                f"Plugin configuration profiles are no longer supported, ignoring `@{profile_name}` in plugin name."
            )

        try:
            plugin = next(
                plugin
                for plugin in self.plugins()
                if (
                    plugin.name == plugin_name
                    and (plugin_type is None or plugin.type == plugin_type)
                    and (invokable is None or plugin.is_invokable() == invokable)
                    and (
                        configurable is None or plugin.is_configurable() == configurable
                    )
                )
            )

            return plugin
        except StopIteration as stop:
            raise PluginMissingError(plugin_name) from stop

    def get_plugin(self, plugin_ref: PluginRef) -> ProjectPlugin:
        try:
            plugin = next(plugin for plugin in self.plugins() if plugin == plugin_ref)

            return plugin
        except StopIteration as stop:
            raise PluginMissingError(plugin_ref.name) from stop

    def get_plugins_of_type(self, plugin_type):
        return self.project.meltano.plugins[plugin_type]

    def plugins_by_type(self):
        return {
            plugin_type: self.get_plugins_of_type(plugin_type)
            for plugin_type in PluginType
        }

    def plugins(self) -> Iterable[ProjectPlugin]:
        yield from (
            plugin
            for plugin_type, plugins in self.plugins_by_type().items()
            for plugin in plugins
        )

    def get_extractors(self):
        return self.get_plugins_of_type(PluginType.EXTRACTORS)

    def get_loaders(self):
        return self.get_plugins_of_type(PluginType.LOADERS)

    def get_transforms(self):
        return self.get_plugins_of_type(PluginType.TRANSFORMS)

    def get_models(self):
        return self.get_plugins_of_type(PluginType.MODELS)

    def get_dashboards(self):
        return self.get_plugins_of_type(PluginType.DASHBOARDS)

    def get_transformers(self):
        return self.get_plugins_of_type(PluginType.TRANSFORMERS)

    def get_files(self):
        return self.get_plugins_of_type(PluginType.FILES)

    def update_plugin(self, plugin: ProjectPlugin):
        with self.project.meltano_update() as meltano:
            # find the proper plugin to update
            idx, outdated = next(
                (i, it)
                for i, it in enumerate(meltano.plugins[plugin.type])
                if it == plugin
            )

            meltano.plugins[plugin.type][idx] = plugin

            return outdated
