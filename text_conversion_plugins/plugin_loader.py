import importlib
from text_conversion_plugins.interfaces import (
    HtmlPluginInterface,
    PluginConfigurationInstruction
)
from typing import List, Optional


def import_plugin_module(name: str) -> HtmlPluginInterface:
    """Imports HTML plugin module by its name."""
    return importlib.import_module(name)


def load_plugin(
    plugin_to_load: str,
    loaded_plugins_container: List,
    configuration_to_inject:
        Optional[List[PluginConfigurationInstruction]] = None
) -> None:
    """Performs single plugin initialization. Initialized plugin will be appended
    to the loaded_plugins_container object.

    Args:
        plugin_to_load (str): specific plugin script location 
            (for example: 'text_conversion_plugins.simple_regex_replacer')
        loaded_plugins_container (List): 
            reference on object that stores/aggregates plugins
        configuration_to_inject (Optional[List[PluginConfigurationInstruction]]): 
            If the plugin has configuration/instructions - pass it here,
            it will be provided at initialization stage. 
            Defaults to None.
    """
    imported_plugin = import_plugin_module(
        plugin_to_load
    )
    initialized_plugin = imported_plugin.initialize()

    if configuration_to_inject:
        initialized_plugin.set_instructions(configuration_to_inject)

    loaded_plugins_container.append(initialized_plugin)
