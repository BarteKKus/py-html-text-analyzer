import pytest
from pydantic import ValidationError
from pathlib import Path
from configuration.json_file_loader import load_json_file
from configuration.urls_cfg_json_loader import (
    load_urls_configuration,
    UrlConfiguration
)
from tests.files_descriptor import JSONUrlFilesDescriptor

FILE_DESCRIPTOR = JSONUrlFilesDescriptor()
JSON_FILES_DIR = FILE_DESCRIPTOR.get_files_directory


@pytest.mark.parametrize(
    "correct_json_file",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.correct]
)
def test_load_urls_configuration_with_correct_cfg(
    correct_json_file: Path
):
    """Correct configuration should allow to create list of
    UrlConfiguration objects"""
    urls = load_urls_configuration(
        filepath=correct_json_file
    )
    assert all(isinstance(url, UrlConfiguration) for url in urls)


@pytest.mark.parametrize(
    "incorrect_json_data",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.incorrect_data]
)
def test_load_urls_configuration_with_incorrect_data_cfg(
    incorrect_json_data: Path
):
    """If data is corrupted - for example incorrect http address - 
    loader will still load that data - loader is not responsible for
    data interpretation"""
    urls = load_urls_configuration(
        filepath=incorrect_json_data
    )
    assert all(isinstance(url, UrlConfiguration) for url in urls)


@pytest.mark.parametrize(
    "unexpected_key_name",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.unexpected_key_name]
)
def test_load_urls_configuration_with_unexpected_key_cfg(
    unexpected_key_name: Path
):
    """If key in expected json structure is unknown - loader should
    raise RuntimeError as configuration cannot be loaded correctly.
    """
    # NOTE - RuntimeError here was introduced intentionally to match with
    # other loaders (like json plugins), perhaps in the future code should
    # relay on Pydantic validation fully
    #
    with pytest.raises(RuntimeError):
        load_urls_configuration(
            filepath=unexpected_key_name
        )


@pytest.mark.parametrize(
    "incorrect_json_structure",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.incorrect_structure]
)
def test_load_urls_configuration_with_incorrect_json_structure_cfg(
    incorrect_json_structure: Path
):
    """If json structure has incorrect structure - loader should
    ... .
    """
    with pytest.raises(RuntimeError):
        load_urls_configuration(
            filepath=incorrect_json_structure
        )
