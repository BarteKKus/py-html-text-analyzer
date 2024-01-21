import asyncio

from pathlib import Path
from typing import List

from .interfaces import AnalyzeScenario

from configuration.urls_cfg_json_loader import UrlConfiguration
from configuration.plugins_cfg_json_loader import PluginConfiguration

from url_processors.async_url_processor import process_urls

from text_conversion_plugins.interfaces import TextConverterPluginInterface
from text_conversion_plugins.plugin_loader import load_plugin

from text_postprocessors.words_counter import simple_words_counter
from text_postprocessors.text_tools import WordInterpreters


class HtmlWordCountingScenario(AnalyzeScenario):
    def __init__(
            self,
            urls_cfg: List[UrlConfiguration],
            plugins_cfg: List[PluginConfiguration]
    ):
        self.urls_cfg = urls_cfg
        self.plugins_cfg = plugins_cfg

    def execute(self):
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
                plugin_to_load=plugin_cfg.source,
                loaded_plugins_container=plugins_container,
                configuration_to_inject=plugin_cfg.configuration_data
            )

        loop = asyncio.get_event_loop()

        # process all url's asynchronously
        #
        results = loop.run_until_complete(process_urls(urls))

        for url, id, content in zip(urls, url_ids, results):

            for modificator in plugins_container:
                content = modificator.convert(str(content))

            counted_words = simple_words_counter(text=content)

            words_selection = WordInterpreters.select_specific_words(
                word_occurrences=counted_words,
                count=10,
                descending_order=True
            )
            WordInterpreters.print_word_occurences(
                words=words_selection,
                prefix_info=f"Words from URL '{url}' "
            )
            WordInterpreters.save_word_occurrences_to_txt_file(
                words=words_selection,
                filename=Path() / "text_processing_results" /
                f"{id}_results.txt",
                prefix_info=f"Top 10 words from URL '{url}' "
            )
