import abc
from typing import List

class TextConverterPluginInterface(metaclass=abc.ABCMeta):
    """Represents plugin object interface."""

    @abc.abstractmethod
    def set_instructions(self, instructions: List)->None:
        """Allow to register replacement instructions"""
        raise NotImplementedError

    @abc.abstractmethod
    def convert(self, text: str) -> str:
        """Start conversion procedure(s) on text.
        Returns converted text"""
        raise NotImplementedError
    
class HtmlPluginInterface:
    """Represents a plugin script interface."""

    @staticmethod
    def initialize() -> TextConverterPluginInterface:
        """Initializes html modificator plugin."""