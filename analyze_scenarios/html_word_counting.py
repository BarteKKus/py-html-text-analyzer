import asyncio

from pathlib import Path
from typing import List, Callable, Optional

from analyze_scenarios.interfaces import AnalyzeScenario

from configuration.urls_cfg_json_loader import UrlsConfiguration
from configuration.plugins_cfg_json_loader import ConversionStep

from url_processors.async_url_processor import (
    process_network_urls
)

from text_conversion_plugins.interfaces import TextConverterPluginInterface
from text_conversion_plugins.plugin_loader import load_plugin

from text_postprocessors.words_counter import simple_words_counter
from text_postprocessors.text_tools import WordInterpreters


class HtmlWordCountingScenario(AnalyzeScenario):
    """Html human-readable text word counting scenario implementation"""

    def __init__(
            self,
            urls_cfg: UrlsConfiguration,
            plugins_cfg: List[ConversionStep],
            urls_handler: Callable[[List[str]], List[str]] = (
                process_network_urls
            ),
            max_results_number: int = 10,
            descending_results_order: bool = True,
            enable_console_output: bool = True,
            override_console_output_header: Optional[str] = None,
            enable_file_output: bool = True,
            override_file_name_suffix: Optional[str] = None,
            override_file_header_string: Optional[str] = None,
            override_file_output_directory: Optional[Path] = None,
    ):
        self.urls_cfg = urls_cfg.urls
        self.plugins_cfg = plugins_cfg
        self.urls_handler = urls_handler

        self.max_results_number = max_results_number
        self.descending_results_order = descending_results_order

        self.enable_console_output = enable_console_output
        self.enable_file_output = enable_file_output

        self.console_output_header = "Words from URL "
        if override_console_output_header:
            self.console_output_header = override_console_output_header

        self.file_name_suffix = "results.txt"
        if override_file_name_suffix:
            self.file_name_suffix = override_file_name_suffix

        self.file_header_string = (
            f"Top {self.max_results_number} from URL "
        )
        if override_file_header_string:
            self.file_header_string = override_file_header_string

        self.file_output_directory = Path() / "text_processing_results"
        if override_file_output_directory:
            self.file_output_directory = override_file_output_directory

    def execute(self) -> bool:
        """Executes scenario"""
        # Extract urls and url_ids from config.
        # Url names are used for file creation in case of
        # multiple url provided
        #
        urls, url_ids = zip(*[(config.url, config.id)
                              for config in self.urls_cfg])

        # Initialize empty text conversion plugins container
        #
        plugins_container: List[TextConverterPluginInterface] = []

        # Load and initialize text conversion plugins
        #
        for plugin_cfg in self.plugins_cfg:
            load_plugin(
                plugin_to_load=plugin_cfg.step_instructions.plugin,
                loaded_plugins_container=plugins_container,
                configuration_to_inject=plugin_cfg.step_instructions.configuration
            )

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.urls_handler(urls)
        )

        for url, url_id, text_content in zip(urls, url_ids, results):

            for modificator in plugins_container:
                text_content = modificator.convert(str(text_content))

            counted_words = simple_words_counter(text=text_content)

            words_selection = WordInterpreters.select_specific_words(
                word_occurrences=counted_words,
                count=self.max_results_number,
                descending_order=self.descending_results_order
            )
            if self.enable_console_output:
                WordInterpreters.print_word_occurences(
                    words=words_selection,
                    prefix_info=(
                        f"{self.console_output_header}'{url}' "
                    )
                )
            if self.enable_file_output:
                WordInterpreters.save_word_occurrences_to_txt_file(
                    words=words_selection,
                    filename=Path() / self.file_output_directory /
                    f"{url_id}_{self.file_name_suffix}",
                    prefix_info=f"{self.file_header_string}'{url}' "
                )
            return True
