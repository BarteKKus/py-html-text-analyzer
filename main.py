import argparse
from pathlib import Path
from typing import Dict, Type

from configuration.plugins_cfg_json_loader import load_plugin_configuration
from configuration.urls_cfg_json_loader import load_urls_configuration
from analyze_scenarios import (
    HtmlWordCountingScenario,
    AnalyzeScenario
)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description='http_text_analyzer launching script'
    )
    arg_parser.add_argument(
        '--urls_cfg_file',
        default=Path() / 'configuration' / 'default_configuration' / 'urls.json',
        help=(
            "Filepath pointing to file "
            "with urls to get text from"
        )
    )
    arg_parser.add_argument(
        '--text_conversion_plugins_cfg_file',
        default=Path() / 'configuration' / 'default_configuration' /
        'text_converter_plugins.json',
        help=(
            "Filepath pointing to file "
            "with text conversion plugins configuration"
        )
    )
    arg_parser.add_argument(
        '--scenario',
        default='html_word_counting',
        help=(
            "Choose analysis scenario - avaiable options: "
            "'html_word_counting', "
        )
    )
    args = arg_parser.parse_args()

    # define avaiable scenarios
    #
    analyze_scenarios: Dict[str, AnalyzeScenario] = {
        'html_word_counting': HtmlWordCountingScenario
    }
    # Get list of URL's to get words from
    #
    urls_config = load_urls_configuration(
        filepath=args.urls_cfg_file
    )
    # Load text conversion plugins configuation
    #
    text_converting_plugins_cfg = load_plugin_configuration(
        filepath=args.text_conversion_plugins_cfg_file
    )
    # Launch selected analyze scenario
    #
    choosen_scenario: AnalyzeScenario = analyze_scenarios[args.scenario](
        urls_cfg=urls_config,
        plugins_cfg=text_converting_plugins_cfg
    )
    choosen_scenario.execute()
