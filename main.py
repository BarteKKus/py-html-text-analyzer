import aiohttp
import asyncio
import json
from typing import List
from pathlib import Path
import re
####################################################################
from text_conversion_plugins.data_structures import (
    CONFIGURATION_TYPES,
)
from text_conversion_plugins.interfaces import TextConverterPluginInterface
from text_conversion_plugins.plugin_loader import (
    load_plugin
)

# hardcoded list of url's for now
# TODO allow to pass txt file where each row = url link
# TODO allow to pass list of urls as command line argument

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
    
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
    with open(Path() / 'html_converter_plugins.json') as file:
        config=json.load(file)

    for plugin in config['conversion_steps']:
        step=config['conversion_steps'][str(plugin)]['plugin']
        plugin_config=CONFIGURATION_TYPES.get(
                config['conversion_steps'][str(plugin)]['configuration_type'],None)
        total_cfg=[]
        for single_cfg in config['conversion_steps'][str(plugin)]['configuration']:
            c=plugin_config.init_from_dict(cfg_dict=single_cfg)
            total_cfg.append(c)
        load_plugin(
            plugin_to_load=config['conversion_steps'][str(plugin)]['plugin'],
            loaded_plugins_container=plugins_container,
            configuration_to_inject=total_cfg
            )

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_urls(urls))

    def count_words(text):
        # Extract words (assuming words are separated by spaces)
        words = re.findall(r'\b\w+\b', text)
        # for i,w in enumerate(words):
            # print(f"index: {i}, word: {w}")
        return len(words)

    for url, content in zip(urls, results):
        
        for modificator in plugins_container:
            content=modificator.convert(str(content))
        words_count=count_words(content)
        print(f"URL: {url} words: {words_count}")