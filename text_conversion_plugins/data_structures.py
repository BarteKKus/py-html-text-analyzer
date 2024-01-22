from dataclasses import dataclass, field
from typing import Optional
from text_conversion_plugins.interfaces import PluginConfigurationInstruction


@dataclass
class ReplacementInstruction(PluginConfigurationInstruction):
    """Represents 'replacement' plugin configuration type"""
    find: str
    replace_to: str
    info: Optional[str] = field(default=None)
    active: Optional[bool] = field(default=True)

# Add here new plugin instructions definition for new types
