import pytest
from pathlib import Path
from configuration.urls_cfg_json_loader import (
    load_urls_configuration
)
from configuration.data_structures import UrlsConfiguration, SingleUrlSetting
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
        file_path=correct_json_file
    )
    assert isinstance(urls, UrlsConfiguration)


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
        file_path=incorrect_json_data
    )
    assert isinstance(urls, UrlsConfiguration)


@pytest.mark.parametrize(
    "unexpected_key_name",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.unexpected_key_name]
)
def test_load_urls_configuration_with_unexpected_key_cfg(
    unexpected_key_name: Path
):
    """If key in expected json structure is unknown - loader should
    raise ValueError as configuration cannot be loaded correctly.
    """
    with pytest.raises(ValueError):
        load_urls_configuration(
            file_path=unexpected_key_name
        )


@pytest.mark.parametrize(
    "incorrect_json_structure",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.incorrect_structure]
)
def test_load_urls_configuration_with_incorrect_json_structure_cfg(
    incorrect_json_structure: Path
):
    """If json structure has incorrect structure - loader should
    raise ValueError."""
    with pytest.raises(ValueError):
        load_urls_configuration(
            file_path=incorrect_json_structure
        )


@pytest.mark.parametrize(
    "data_to_evaluate_in_detail",
    [JSON_FILES_DIR / f for f in FILE_DESCRIPTOR.detailed_evaluation]
)
def test_load_urls_configuration_output_data(
    data_to_evaluate_in_detail: Path
):
    """Checks if data from json is transformed correctly"""
    urls = load_urls_configuration(
        file_path=data_to_evaluate_in_detail
    )

    assert isinstance(urls, UrlsConfiguration)
    assert len(urls.urls) == 2
    assert isinstance(urls.urls[0], SingleUrlSetting)
    assert urls.urls[0].id == "example_com"
    assert urls.urls[0].url == "http://www.example.com/"
    assert isinstance(urls.urls[0], SingleUrlSetting)
    assert urls.urls[1].id == "exampleexample_com"
    assert urls.urls[1].url == "http://www.exampleexample.com/"
