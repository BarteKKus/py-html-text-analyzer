import pytest
from pathlib import Path
from configuration.plugins_cfg_json_loader import (
    JsonKeysMap,
    PluginConfiguration,
    load_plugins_configuration,
    create_plugin_configuration,
    prepare_configuration
)
from configuration.json_file_loader import load_json_file
from tests.files_descriptor import JSONPluginFilesDescriptor
from text_conversion_plugins.data_structures import ReplacementInstruction
from text_conversion_plugins.interfaces import PluginConfigurationInstruction

JSON_FILES_DIR = Path() / 'tests' / 'data' / 'json_plugins_files'
FILE_DESCRIPTOR = JSONPluginFilesDescriptor()


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.correct]
)
def test_load_plugins_configuration_with_correct_cfg(
    correct_json_file: Path
):
    """Correct configuration should allow to create list of
    PluginConfiguration object - that are used firther by plugin
    loader module"""
    plugins_configurations = load_plugins_configuration(
        filepath=correct_json_file)
    assert all(
        isinstance(plugin, PluginConfiguration)
        for plugin in plugins_configurations)


@pytest.mark.parametrize(
    "unexpected_key_name_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.unexpected_key_name]
)
def test_load_plugins_configuration_with_unknow_cfg_keys(
        unexpected_key_name_json_file: Path
):
    """Unexpected of misspelled key names in cfg should raise RuntimeError
    as module cannot continue working in correct/expected way"""
    with pytest.raises(RuntimeError):
        load_plugins_configuration(
            filepath=unexpected_key_name_json_file)


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / FILE_DESCRIPTOR.correct[0]]
)
def test_create_plugin_configuration(correct_json_file):
    """Correct input data should generate PluginConfiguration object
    with expected data"""
    data = load_json_file(correct_json_file)
    plugin_data = data['conversion_steps']['regex_replace']
    json_keys = JsonKeysMap().model_dump()
    cfg_types = {'replacement': ReplacementInstruction}

    plugin_configuration = create_plugin_configuration(
        plugin_data, json_keys, cfg_types
    )
    assert isinstance(plugin_configuration, PluginConfiguration)
    assert plugin_configuration.source == 'text_conversion_plugins.simple_regex_replacer'
    assert plugin_configuration.configuration_type == ReplacementInstruction
    assert len(plugin_configuration.configuration_data) == 2


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / FILE_DESCRIPTOR.correct[0]]
)
def test_prepare_configuration(correct_json_file):
    """Correct input data should generate PluginConfigurationInstruction object
    with expected data"""
    data = load_json_file(correct_json_file)
    config_elements = data['conversion_steps']['regex_replace']['configuration']
    cfg_type = ReplacementInstruction
    json_keys = JsonKeysMap().model_dump()

    result = prepare_configuration(config_elements, cfg_type, json_keys)

    assert len(result) == 2
    for single_result in result:
        assert isinstance(single_result, cfg_type)
        assert isinstance(single_result, PluginConfigurationInstruction)
