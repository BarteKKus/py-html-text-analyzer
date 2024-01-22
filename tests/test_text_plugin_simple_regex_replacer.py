import pytest
from text_conversion_plugins.simple_regex_replacer import SimpleRegexReplacer
from text_conversion_plugins.data_structures import ReplacementInstruction


@pytest.fixture
def replacer_with_instructions():
    replacer = SimpleRegexReplacer()
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
    replacer = SimpleRegexReplacer()
    result = replacer.convert("Text without instructions.")
    assert result == "Text without instructions."


def test_convert_with_empty_instructions():
    replacer = SimpleRegexReplacer()
    replacer.set_instructions([])
    result = replacer.convert("Text with empty instructions.")
    assert result == "Text with empty instructions."


def test_convert_with_regex_expression():
    replacer = SimpleRegexReplacer()
    instructions = [
        ReplacementInstruction(find=r'\d+', replace_to='NUMBER')
    ]
    replacer.set_instructions(instructions)
    result = replacer.convert("123 apples and 000 bananas.")
    assert result == "NUMBER apples and NUMBER bananas."
