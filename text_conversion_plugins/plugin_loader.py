import importlib
from text_conversion_plugins.interfaces import (
    HtmlPluginInterface
)
from typing import List, Optional, Any


def import_plugin_module(name: str) -> HtmlPluginInterface:
    """Imports HTML plugin module by its name."""
    return importlib.import_module(name)


def load_plugin(
        plugin_to_load: str, 
        loaded_plugins_container: List,
        configuration_to_inject: Optional[Any] = None
    ) -> None:
    """Performs complete plugin import with initialization."""
    imported_plugin = import_plugin_module(plugin_to_load)
    initialized_plugin = imported_plugin.initialize()
    if configuration_to_inject:
        initialized_plugin.set_instructions(configuration_to_inject)
    loaded_plugins_container.append(initialized_plugin)