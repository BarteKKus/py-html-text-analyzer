from dataclasses import dataclass, field
from typing import Optional, Dict, Type
from text_conversion_plugins.interfaces import PluginConfigurationInstruction


@dataclass
class ReplacementInstruction(PluginConfigurationInstruction):
    """Represents 'replacement' plugin configuration type"""
    find: str
    replace_to: str
    info: Optional[str] = field(default=None)
    active: Optional[bool] = field(default=True)

    @classmethod
    def init_from_dict(cls, cfg_dict: Dict) -> Type['ReplacementInstruction']:
        """Allows to initialize dataclass using configuration dictionary fragment"""
        return cls(
            find=cfg_dict['find'],
            replace_to=cfg_dict['replace_to'],
            info=cfg_dict.get('info', None),
            active=cfg_dict.get('active', True)
        )
