from text_conversion_plugins.data_structures import ReplacementInstruction
from text_conversion_plugins.interfaces import TextConverterPluginInterface
from typing import List


class SimpleStringReplacer(TextConverterPluginInterface):
    "This is a simple string replace-based plugin for replacing text fragments."

    def __init__(self):
        self._instructions = None

    def set_instructions(self, instructions: List[ReplacementInstruction]) -> None:
        self._instructions = instructions

    def convert(self, text: str) -> str:
        if not self._instructions:
            return text
        for action in self._instructions:
            text = text.replace(action.find, action.replace_to)
        return text


def initialize() -> TextConverterPluginInterface:
    return SimpleStringReplacer()
