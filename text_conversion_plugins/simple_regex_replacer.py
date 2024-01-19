import re
from text_conversion_plugins.data_structures import ReplacementInstruction
from text_conversion_plugins.interfaces import TextConverterPluginInterface
from typing import List

class SimpleRegexReplacer(TextConverterPluginInterface):
    def __init__(self):
        self._instructions=None

    def set_instructions(
            self, instructions:List[ReplacementInstruction])->None:
        self._instructions=instructions

    def convert(self, text: str) -> str:
        if not self._instructions:
            return text
        for action in self._instructions:
            text = re.sub(
                pattern=str(action.find), 
                repl=str(action.replace_to), 
                string=text,
                flags=re.DOTALL
                )
        return text

def initialize()->TextConverterPluginInterface:
    return SimpleRegexReplacer()