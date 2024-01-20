import asyncio
from datetime import datetime
from pathlib import Path
from typing import List

from text_conversion_plugins.interfaces import TextConverterPluginInterface
from text_conversion_plugins.plugin_loader import (
    load_plugin
)
from url_processors.async_url_processor import process_urls
from configuration.plugins_cfg_json_loader import load_configuration
from text_postprocessors.words_counter import simple_words_counter
from text_postprocessors.text_tools import WordInterpreters
# hardcoded list of url's for now
# TODO allow to pass txt file where each row = url link
# TODO allow to pass list of urls as command line argument


if __name__ == "__main__":
    # List of URLs to fetch
    urls = [
        'http://www.example.com/',
        'https://www.iana.org/help/example-domains',
        'https://www.onet.pl',
        'https://www.wp.pl',
        'https://once.com/',
    ]
    plugins_container: List[TextConverterPluginInterface] = []

    text_converting_plugins_cfg = load_configuration(
        filepath=Path() / 'html_converter_plugins.json'
    )
    for plugin_cfg in text_converting_plugins_cfg:
        load_plugin(
            plugin_to_load=plugin_cfg.source,
            loaded_plugins_container=plugins_container,
            configuration_to_inject=plugin_cfg.configuration_data
        )

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_urls(urls))

    for url, content in zip(urls, results):
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
            filename=f"results.txt",
            # prefix_info=f"Top 10 words from URL '{url}' "
        )
