import aiohttp
import asyncio
from http_to_text_filters.text_only_extractors import (
    extract_visible_text,
    count_words,
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

    # Run the event loop
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_urls(urls))

    for url, content in zip(urls, results):
        custom_c=extract_visible_text(str(content))
        words=count_words(custom_c)
        
        print(f"URL: {url} words: {words}")