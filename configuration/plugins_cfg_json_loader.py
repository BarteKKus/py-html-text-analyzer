from dataclasses import dataclass
from typing import List, Dict, Callable
from pathlib import Path

from text_conversion_plugins.data_structures import CONFIGURATION_TYPES
from text_conversion_plugins.interfaces import PluginConfigurationInstruction
from configuration.json_file_loader import load_json_file
# _JSON_KEYS_MAP contains mapping between in-code references
# and json file keys naming
#
_JSON_KEYS_MAP = {
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


def load_plugin_configuration(
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

    return [create_plugin_configuration(plugin_name, plugin)
            for plugin_name, plugin in loaded_configuration[
                _JSON_KEYS_MAP['steps']].items()]


def create_plugin_configuration(
    name: str,
    plugin: Dict,
    cfg_key_map: Dict[str, str] = _JSON_KEYS_MAP,
    cfg_types: Dict[str, PluginConfigurationInstruction] = CONFIGURATION_TYPES
) -> PluginConfiguration:
    """Handles configuration assembly process for particular plugin.

    Args:
        name (str): plugin name (this is not script name that implements plugin!)
        plugin (Dict): plugin script name
        cfg_key_map (Dict[str, str], optional):keys map between code and json. 
            Defaults to _JSON_KEYS_MAP.
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
    cfg_key_map: Dict[str, str] = _JSON_KEYS_MAP
) -> List[PluginConfigurationInstruction]:
    """Prepares configuration part for specific plugin if
    marked as 'active'.

    Args:
        config_elements (List[Dict]): container with all configuration elements
        cfg_type (PluginConfigurationInstruction): selected configuration type
        cfg_key_map (Dict[str, str], optional): keys map between code and json.
            Defaults to _JSON_KEYS_MAP.

    Returns:
        List[PluginConfigurationInstruction]: 
            all initialized plugin configuration elements
    """

    return [
        cfg_type.init_from_dict(cfg_dict=element)
        for element in config_elements
        if element.get(cfg_key_map['active'])
    ]
