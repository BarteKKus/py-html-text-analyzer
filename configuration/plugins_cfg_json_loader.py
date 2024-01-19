from dataclasses import dataclass
from typing import List,Dict,Type
from pathlib import Path
import json

from text_conversion_plugins.data_structures import CONFIGURATION_TYPES

JSON_KEYS_MAP={
    'steps':'conversion_steps',
    'plugin':'plugin',
    'cfg_type':'configuration_type',
    'cfg':'configuration',
    'active':'active'
}   

@dataclass
class PluginConfiguration:
    name:str
    source:str
    configuration_type:str
    configuration_data:List[Dict]

def load_configuration(filepath: Path)->List[PluginConfiguration]:
    with open(filepath) as file:
        loaded_configuration=json.load(file)
    plugins=[]

    for plugin_name in loaded_configuration[JSON_KEYS_MAP['steps']]:

        plugin=loaded_configuration[JSON_KEYS_MAP['steps']][plugin_name]
        source=plugin[JSON_KEYS_MAP['plugin']]
        cfg_type=CONFIGURATION_TYPES.get(plugin[JSON_KEYS_MAP['cfg_type']])

        plugin_configuration=[]
        for config_element in plugin[JSON_KEYS_MAP['cfg']]:
            if config_element[JSON_KEYS_MAP['active']]:
                plugin_configuration.append(cfg_type.init_from_dict(
                    cfg_dict=config_element
                ))

        plugins.append(
            PluginConfiguration(
                name=plugin_name,
                source=source,
                configuration_type=cfg_type,
                configuration_data=plugin_configuration
           )
        )
    return plugins


    