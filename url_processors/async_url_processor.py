import aiohttp
import asyncio
from typing import List

async def fetch_url(session: aiohttp.ClientSession, url: str, timeout: int = 10) -> str:
    """
    Fetches the content of a given URL using aiohttp lib.

    Args:
        session (aiohttp.ClientSession): Aiohttp session object.
        url (str): URL to fetch.
        timeout (int): Timeout for the HTTP request in seconds (default: 10 secs).

    Returns:
        str: Text content of the response.
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

async def process_urls(urls: List[str], timeout: int = 10) -> List[str]:
    """
    Processes a list of URLs concurrently using aiohttp.

    Args:
        urls (List[str]): List of URLs to process.
        timeout (int): Timeout for each HTTP request in seconds (default: 10 secs).

    Returns:
        List[str]: List of text contents for each URL.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, timeout) for url in urls]
        return await asyncio.gather(*tasks)