import pytest

from text_conversion_plugins.simple_string_replacer import (
    ReplacementInstruction,
    SimpleStringReplacer
)


@pytest.fixture
def replacer_with_instructions():
    replacer = SimpleStringReplacer()
    instructions = [
        ReplacementInstruction(find='apple', replace_to='orange'),
        ReplacementInstruction(find='banana', replace_to='grape')
    ]
    replacer.set_instructions(instructions)
    return replacer


def test_convert_with_instructions(replacer_with_instructions):
    result = replacer_with_instructions.convert(
        "Apple and a banana.")
    assert result == "Apple and a grape."


def test_convert_without_instructions():
    replacer = SimpleStringReplacer()
    result = replacer.convert("Text without instructions.")
    assert result == "Text without instructions."


def test_convert_with_empty_instructions():
    replacer = SimpleStringReplacer()
    replacer.set_instructions([])
    result = replacer.convert("Text with empty instructions.")
    assert result == "Text with empty instructions."


def test_convert_with_special_characters():
    replacer = SimpleStringReplacer()
    instructions = [
        ReplacementInstruction(find='@', replace_to='at'),
        ReplacementInstruction(find='!', replace_to='exclamation')
    ]
    replacer.set_instructions(instructions)
    result = replacer.convert("Hello @world!.")
    assert result == "Hello atworldexclamation."
