import pytest
from pathlib import Path
from configuration.plugins_cfg_json_loader import (
    load_plugins_configuration,
)
from configuration.data_structures import ConversionStep, SinglePluginData
from tests.files_descriptor import JSONPluginFilesDescriptor
from text_conversion_plugins.plugin_configuration_types import (
    CONFIGURATION_TYPES
)
from text_conversion_plugins.data_structures import ReplacementInstruction


FILE_DESCRIPTOR = JSONPluginFilesDescriptor()
JSON_FILES_DIR = FILE_DESCRIPTOR.get_files_directory


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.correct]
)
def test_load_plugins_configuration_with_correct_cfg(
    correct_json_file: Path
):
    """Correct configuration should allow to create list of
    ConversionStep(s) - that are used further by plugin
    loader module"""
    plugins_configurations = load_plugins_configuration(
        file_path=correct_json_file,
        configuration_types=CONFIGURATION_TYPES
    )
    assert all(
        isinstance(plugin, ConversionStep)
        for plugin in plugins_configurations)


@pytest.mark.parametrize(
    "non_existent_plugin",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.non_existent_resource]
)
def test_load_plugins_configuration_with_correct_cfg(
    non_existent_plugin: Path
):
    """If for example plugin source do not exists - loader should stil
    return ConversionSteps as it is not responsible for checking if
    plugin exists at all"""
    plugins_configurations = load_plugins_configuration(
        file_path=non_existent_plugin,
        configuration_types=CONFIGURATION_TYPES
    )
    assert all(
        isinstance(plugin, ConversionStep)
        for plugin in plugins_configurations)


@pytest.mark.parametrize(
    "unexpected_key_name_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.unexpected_key_name]
)
def test_load_plugins_configuration_with_unknow_cfg_keys(
        unexpected_key_name_json_file: Path
):
    """Unexpected of misspelled key names in cfg should raise ValueError
    as module cannot load data in correct/expected way"""
    with pytest.raises(ValueError):
        load_plugins_configuration(
            file_path=unexpected_key_name_json_file,
            configuration_types=CONFIGURATION_TYPES
        )


@pytest.mark.parametrize(
    "detailed_evaluation_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.detailed_evaluation]
)
def test_load_plugins_configuration_with_correct_cfg(
    detailed_evaluation_json_file: Path
):
    """Checks if data from json is transformed correctly"""
    pc = load_plugins_configuration(
        file_path=detailed_evaluation_json_file,
        configuration_types=CONFIGURATION_TYPES
    )
    assert all(
        isinstance(plugin, ConversionStep)
        for plugin in pc)
    assert len(pc) == 1
    assert pc[0].step_name == "regex_replace"
    assert isinstance(pc[0].step_instructions, SinglePluginData)
    assert pc[0].step_instructions.plugin == "ab.cd"
    assert pc[0].step_instructions.configuration_type == "replacement"
    assert len(pc[0].step_instructions.configuration) == 2
    assert all(
        isinstance(cfg, ReplacementInstruction)
        for cfg in pc[0].step_instructions.configuration
    )

    assert pc[0].step_instructions.configuration[0].find == '\\s+'
    assert pc[0].step_instructions.configuration[0].replace_to == ' '
    assert pc[0].step_instructions.configuration[0].info == (
        "remove extra whitespaces"
    )
    assert pc[0].step_instructions.configuration[1].active == True

    assert pc[0].step_instructions.configuration[1].find == '&\\w+;(?!<\\/\\w+>)'
    assert pc[0].step_instructions.configuration[1].replace_to == ' '
    assert pc[0].step_instructions.configuration[1].info == (
        "remove entities"
    )
    assert pc[0].step_instructions.configuration[1].active == True
