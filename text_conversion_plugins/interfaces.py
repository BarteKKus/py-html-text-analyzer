import abc
from typing import List, Dict


class TextConverterPluginInterface(metaclass=abc.ABCMeta):
    """Represents plugin object interface."""

    @abc.abstractmethod
    def set_instructions(self, instructions: List) -> None:
        """Allow to register replacement instructions"""
        raise NotImplementedError

    @abc.abstractmethod
    def convert(self, text: str) -> str:
        """Start conversion procedure(s) on text.
        Returns converted text"""
        raise NotImplementedError


class HtmlPluginInterface(metaclass=abc.ABCMeta):
    """Represents a plugin script interface."""

    @abc.abstractstaticmethod
    def initialize() -> TextConverterPluginInterface:
        """Initializes html modificator plugin."""
        raise NotImplementedError


class PluginConfigurationInstruction(metaclass=abc.ABCMeta):
    """Represents a single plugin configuration object.
    This type of object should contains single config
    structure for particular type."""
