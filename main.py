import aiohttp
import asyncio
import re
from pathlib import Path
from typing import List

from text_conversion_plugins.interfaces import TextConverterPluginInterface
from text_conversion_plugins.plugin_loader import (
    load_plugin
)
from url_processors.async_url_processor import process_urls
from configuration.plugins_cfg_json_loader import load_configuration
# hardcoded list of url's for now
# TODO allow to pass txt file where each row = url link
# TODO allow to pass list of urls as command line argument

    
if __name__ == "__main__":
    # List of URLs to fetch
    urls=[
        'http://www.example.com/',
        'https://www.iana.org/help/example-domains',
        'https://www.onet.pl',
        'https://www.wp.pl',
        'https://once.com/',
    ]
    plugins_container: List[TextConverterPluginInterface] = []

    # load config:
    # TODO clean this up
    text_converting_plugins_cfg=load_configuration(
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

    def count_words(text):
        # Extract words (assuming words are separated by spaces)
        words = re.findall(r'\b\w+\b', text)
        # for i,w in enumerate(words):
        #     print(f"index: {i}, word: {w}")
        return len(words)

    for url, content in zip(urls, results):
        # print("content: ",content)
        for modificator in plugins_container:
            content=modificator.convert(str(content))
        words_count=count_words(content)
        print(f"URL: {url} words: {words_count}")