from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
import json

from text_conversion_plugins.data_structures import CONFIGURATION_TYPES
from text_conversion_plugins.interfaces import PluginConfigurationInstruction

# JSON_KEYS_MAP contains mapping between in-code references
# and json file keys naming
#
JSON_KEYS_MAP = {
    'steps': 'conversion_steps',
    'plugin': 'plugin',
    'cfg_type': 'configuration_type',
    'cfg': 'configuration',
    'active': 'active'
}


@dataclass
class PluginConfiguration:
    """Represents a single plugin configuration"""
    name: str
    source: str
    configuration_type: str
    configuration_data: List[Dict]


def load_configuration(filepath: Path) -> List[PluginConfiguration]:
    """Load json file with conversion steps and plugins configuration

    Args:
        filepath (Path): path with filename to load

    Raises:
        FileNotFoundError: if file was not found
        ValueError: on any decoding errors

    Returns:
        List[PluginConfiguration]: list with all plugins with configuration
    """
    try:
        with filepath.open() as file:
            loaded_configuration = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON file '{filepath}': {e}")

    return [create_plugin_configuration(plugin_name, plugin)
            for plugin_name, plugin in loaded_configuration[
                JSON_KEYS_MAP['steps']].items()]


def create_plugin_configuration(
    name: str,
    plugin: Dict,
    cfg_key_map: Dict[str, str] = JSON_KEYS_MAP,
    cfg_types: Dict[str, PluginConfigurationInstruction] = CONFIGURATION_TYPES
) -> PluginConfiguration:
    """Handles configuration assembly process for particular plugin.

    Args:
        name (str): plugin name (this is not script name that implements plugin!)
        plugin (Dict): plugin script name
        cfg_key_map (Dict[str, str], optional):keys map between code and json. 
            Defaults to JSON_KEYS_MAP.
        cfg_types (Dict[str, PluginConfigurationInstruction], optional): 
            known/registered types of configuration. Defaults to CONFIGURATION_TYPES.

    Returns:
        PluginConfiguration: initialized single plugin configuration.
    """

    source = plugin.get(cfg_key_map['plugin'])

    configuration_type = cfg_types.get(plugin.get(cfg_key_map['cfg_type']))

    active_configurations = prepare_configuration(
        plugin.get(cfg_key_map['cfg']),
        configuration_type
    )

    return PluginConfiguration(
        name=name,
        source=source,
        configuration_type=configuration_type,
        configuration_data=active_configurations
    )


def prepare_configuration(
    config_elements: List[Dict],
    cfg_type: PluginConfigurationInstruction,
    cfg_key_map: Dict[str, str] = JSON_KEYS_MAP
) -> List[PluginConfigurationInstruction]:
    """Prepares configuration part for specific plugin if
    marked as 'active'.

    Args:
        config_elements (List[Dict]): container with all configuration elements
        cfg_type (PluginConfigurationInstruction): selected configuration type
        cfg_key_map (Dict[str, str], optional): keys map between code and json.
            Defaults to JSON_KEYS_MAP.

    Returns:
        List[PluginConfigurationInstruction]: 
            all initialized plugin configuration elements
    """

    return [
        cfg_type.init_from_dict(cfg_dict=element)
        for element in config_elements
        if element.get(cfg_key_map['active'])
    ]
