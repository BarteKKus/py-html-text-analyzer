from typing import Dict

from text_conversion_plugins.interfaces import PluginConfigurationInstruction
from text_conversion_plugins.data_structures import ReplacementInstruction

# Add/register here new configuration types for new plugin types
#
CONFIGURATION_TYPES: Dict[str, PluginConfigurationInstruction] = {
    "replacement": ReplacementInstruction,
}
