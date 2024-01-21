from typing import List, Dict, Callable, Type
from pathlib import Path
from pydantic import BaseModel, ConfigDict

from text_conversion_plugins.interfaces import PluginConfigurationInstruction
from configuration.json_file_loader import load_json_file
from text_conversion_plugins.plugin_configuration_types import CONFIGURATION_TYPES


class JsonKeysMap(BaseModel):
    steps: str = 'conversion_steps'
    plugin: str = 'plugin'
    cfg_type: str = 'configuration_type'
    cfg: str = 'configuration'
    active: str = 'active'


class PluginConfiguration(BaseModel):
    """Represents a single plugin configuration"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: str
    configuration_type: Type[PluginConfigurationInstruction]
    configuration_data: List[PluginConfigurationInstruction]


def load_plugins_configuration(
        filepath: Path,
        loader: Callable[[Path], Dict] = load_json_file) -> List[PluginConfiguration]:
    """Load file with conversion steps and plugins configuration

    Args:
        filepath (Path): path with filename to load
        loader (Callable[[Path], Dict], optional): file loader. 
            Defaults to load_json_file.

    Returns:
        List[PluginConfiguration]: list of plugins with theirs configuration
    """
    loaded_configuration = loader(filepath=filepath)
    json_keys = JsonKeysMap(**loaded_configuration).model_dump()

    return [
        create_plugin_configuration(plugin, json_keys, CONFIGURATION_TYPES)
        for plugin in loaded_configuration[json_keys['steps']].values()
    ]


def create_plugin_configuration(
    plugin: Dict,
    json_keys: Dict[str, str],
    cfg_types: Dict[str, PluginConfigurationInstruction]
) -> PluginConfiguration:
    """Handles configuration assembly process for particular plugin.

    Args:
        plugin (Dict): plugin script name
        cfg_key_map (Dict[str, str]):keys map between code and json. 
        cfg_types (Dict[str, PluginConfigurationInstruction]): 
            known/registered types of configuration.

    Returns:
        PluginConfiguration: initialized single plugin configuration.
    """
    try:
        source = plugin.get(json_keys['plugin'])

        configuration_type = cfg_types.get(plugin.get(json_keys['cfg_type']))

        active_configurations = prepare_configuration(
            plugin.get(json_keys['cfg']),
            configuration_type,
            json_keys
        )
    except (AttributeError, TypeError):
        raise RuntimeError(
            f"Failed to configure plugin {source} - check configuration!"
        )
    return PluginConfiguration(
        source=source,
        configuration_type=configuration_type,
        configuration_data=active_configurations
    )


def prepare_configuration(
    config_elements: List[Dict],
    cfg_type: PluginConfigurationInstruction,
    json_keys: Dict[str, str]
) -> List[PluginConfigurationInstruction]:
    """Prepares configuration part for specific plugin if
    marked as 'active'.

    Args:
        config_elements (List[Dict]): container with all configuration elements
        cfg_type (PluginConfigurationInstruction): selected configuration type
        cfg_key_map (Dict[str, str]): keys map between code and json.

    Returns:
        List[PluginConfigurationInstruction]: 
            all initialized plugin configuration elements
    """

    return [
        cfg_type.init_from_dict(cfg_dict=element)
        for element in config_elements
        if element.get(json_keys['active'])
    ]
