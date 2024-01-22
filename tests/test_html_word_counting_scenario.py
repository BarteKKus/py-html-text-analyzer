import filecmp
import pytest
from pathlib import Path
from analyze_scenarios.html_word_counting import HtmlWordCountingScenario

from configuration.urls_cfg_json_loader import UrlsConfiguration, SingleUrlSetting
from configuration.plugins_cfg_json_loader import (
    load_plugins_configuration
)

from url_processors.async_url_processor import process_local_urls
from text_conversion_plugins.plugin_configuration_types import CONFIGURATION_TYPES


def delete_files(
        directory_path: Path,
        file_extension: str = '*.txt'
) -> None:
    directory_path = Path(directory_path)
    txt_files = directory_path.glob(file_extension)

    for txt_file in txt_files:
        try:
            txt_file.unlink()
        except Exception as e:
            print(f"Error deleting {txt_file}: {e}")


def load_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def compare_files(file_path1: str, file_path2: str) -> bool:
    filecmp.clear_cache()
    return filecmp.cmp(file_path1, file_path2)


@pytest.fixture
def get_url_cfg():
    return UrlsConfiguration(
        urls=[SingleUrlSetting(
            id="local_webpage_A",
            url=str(Path() / 'tests' / 'data' /
                    'html_text_files' / 'page_a.html')
        )]
    )


@pytest.fixture
def get_plugins_cfg():
    return load_plugins_configuration(
        file_path=Path() / 'configuration' / 'default_configuration_files' /
        'text_converter_plugins.json',
        configuration_types=CONFIGURATION_TYPES,
    )


@pytest.fixture
def get_files_output_directory():
    return Path() / 'tests' / 'tmp_test_results' / 'html_word_counting_scenario_files'


@pytest.fixture
def get_validation_file():
    return Path() / 'tests' / 'data' / 'html_text_files' / 'expected_html_word_counter_results.txt'


def test_html_word_counting_scenario(
        get_url_cfg,
        get_plugins_cfg,
        get_files_output_directory,
        get_validation_file
):

    delete_files(directory_path=get_files_output_directory)
    assert not any(get_files_output_directory.iterdir())
    scenario = HtmlWordCountingScenario(
        urls_cfg=get_url_cfg,
        plugins_cfg=get_plugins_cfg,
        urls_handler=process_local_urls,
        override_file_output_directory=get_files_output_directory,
        override_file_name_suffix='test_results.txt',
        override_file_header_string="TEST_CASE "
    )
    expected_result_file_location = (
        Path() / get_files_output_directory /
        'local_webpage_A_test_results.txt'
    )
    if scenario.execute():
        assert expected_result_file_location.exists()

    assert compare_files(
        expected_result_file_location,
        get_validation_file
    )
