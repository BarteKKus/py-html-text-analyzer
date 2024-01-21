import argparse
from analyze_scenarios import (
    HtmlWordCountingScenario,
    AnalyzeScenario
)
from pydantic import BaseModel, validator
from pathlib import Path
from typing import Dict

# Add here any new analyze scenario
# or disable existing
#
AVAILABLE_ANALYZE_SCENARIOS: Dict[str, AnalyzeScenario] = {
    'html_word_counting': HtmlWordCountingScenario
}


class DefaultConfiguration:
    """Stores default settings for module arguments"""

    DEFAULT_URLS_CFG_FILE: Path = Path() / 'configuration' / \
        'default_configuration_files' / 'urls.json'
    DEFAULT_TEXT_CONV_PLUGIN_CFG_FILE: Path = Path() / 'configuration' / \
        'default_configuration_files' / 'text_converter_plugins.json'
    DEFAULT_SCENARIO: str = 'html_word_counting'


class ArgumentParserOutput(BaseModel):
    """Arg parser output structure"""
    urls_cfg_file: Path
    text_conversion_plugins_cfg_file: Path
    scenario: str

    @validator('scenario')
    def validate_scenario(cls, value):
        valid_scenarios = AVAILABLE_ANALYZE_SCENARIOS.keys()
        if value not in valid_scenarios:
            raise ValueError(
                f"Invalid scenario: {value}. "
                "Allowed scenarios are: "
                f"{', '.join(valid_scenarios)}")
        return value


def setup_argument_parser() -> ArgumentParserOutput:
    """Function aggregates all possible cmd line args and
    return ArgumentParserOutput data structure"""

    arg_parser = argparse.ArgumentParser(
        description='http_text_analyzer launching script'
    )
    arg_parser.add_argument(
        '--urls_cfg_file',
        default=DefaultConfiguration.DEFAULT_URLS_CFG_FILE,
        help=(
            "Filepath pointing to file "
            "with urls to get text from"
        )
    )
    arg_parser.add_argument(
        '--text_conversion_plugins_cfg_file',
        default=DefaultConfiguration.DEFAULT_TEXT_CONV_PLUGIN_CFG_FILE,
        help=(
            "Filepath pointing to file "
            "with text conversion plugins configuration"
        )
    )
    arg_parser.add_argument(
        '--scenario',
        default=DefaultConfiguration.DEFAULT_SCENARIO,
        choices=AVAILABLE_ANALYZE_SCENARIOS.keys(),
        help=(
            "Choose analysis scenario - avaiable options: "
            "'html_word_counting', "
        )
    )
    parsed_args = arg_parser.parse_args()
    return ArgumentParserOutput(
        urls_cfg_file=parsed_args.urls_cfg_file,
        text_conversion_plugins_cfg_file=(
            parsed_args.text_conversion_plugins_cfg_file
        ),
        scenario=parsed_args.scenario
    )
