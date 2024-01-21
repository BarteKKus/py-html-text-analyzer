from configuration.plugins_cfg_json_loader import load_plugins_configuration
from configuration.urls_cfg_json_loader import load_urls_configuration
from configuration.launch_configuration import (
    ArgumentParserOutput,
    setup_argument_parser,
    AVAILABLE_ANALYZE_SCENARIOS
)
from analyze_scenarios import (
    AnalyzeScenario
)


def main():
    parser_output: ArgumentParserOutput = setup_argument_parser()

    urls_configuration = load_urls_configuration(
        filepath=parser_output.urls_cfg_file
    )
    text_converting_plugins_configuration = \
        load_plugins_configuration(
            filepath=parser_output.text_conversion_plugins_cfg_file
        )
    chosen_scenario_class: AnalyzeScenario = (
        AVAILABLE_ANALYZE_SCENARIOS[parser_output.scenario](
            urls_cfg=urls_configuration,
            plugins_cfg=text_converting_plugins_configuration
        ))
    chosen_scenario_class.execute()


if __name__ == "__main__":
    main()
