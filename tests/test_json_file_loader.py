import pytest
from typing import Dict
from pathlib import Path
from configuration.json_file_loader import load_json_file
from tests.files_descriptor import JSONPluginFilesDescriptor

JSON_FILES_DIR = Path() / 'tests' / 'data' / 'json_plugins_files'
FILE_DESCRIPTOR = JSONPluginFilesDescriptor()


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.correct]
)
def test_load_json_file_success(correct_json_file: Path):
    """Loader should return dict if file is loaded"""
    result = load_json_file(correct_json_file)
    assert isinstance(result, Dict)


@pytest.mark.parametrize(
    "wrong_struct_json_file",
    [
        JSON_FILES_DIR / f
        for f in FILE_DESCRIPTOR.unexpected_key_name
    ]
)
def test_load_json_file_success_with_unexpected_key(
        wrong_struct_json_file: Path):
    """Loader should not care about specific keys"""
    result = load_json_file(wrong_struct_json_file)
    assert isinstance(result, Dict)


@pytest.mark.parametrize(
    "wrong_struct_json_file",
    [
        JSON_FILES_DIR / f
        for f in FILE_DESCRIPTOR.non_existent_resource
    ]
)
def test_load_json_file_success_with_non_existent_resourse(
        wrong_struct_json_file: Path):
    """Loader should not care about resource existence
    like specific plugin provided in config"""
    result = load_json_file(wrong_struct_json_file)
    assert isinstance(result, Dict)


@pytest.mark.parametrize(
    "file_not_found",
    [JSON_FILES_DIR / 'this_file_cannot_exists.json']
)
def test_load_json_file_not_found(file_not_found: Path):
    """Loader should raise FileNotFound when file cannot be located"""
    assert not file_not_found.exists()
    with pytest.raises(FileNotFoundError):
        load_json_file(file_not_found)


@pytest.mark.parametrize(
    "invalid_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.incorrect_file_format]
)
def test_load_json_file_json_decode_error(invalid_json_file: Path):
    """Loader should raise Value Error on incorrect file structure
    like - not closed brackets"""
    with pytest.raises(ValueError):
        load_json_file(invalid_json_file)
