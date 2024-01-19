from bs4 import BeautifulSoup
import aiohttp
import asyncio
import re
def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style tags
    for script in soup(['script', 'style']):
        script.decompose()

    # Extract text content
    sanitized_text = soup.get_text(separator='\n', strip=True)

    return sanitized_text
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
    

def count_visible_words(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.extract()

    # Extract visible text
    visible_text = ' '.join(soup.stripped_strings)

    # Remove newline characters
    visible_text = visible_text.replace('\n', ' ')

    visible_text = visible_text.replace('.',' ')

    # Remove extra whitespaces
    visible_text = re.sub(r'\s+', ' ', visible_text).strip()
    # print(visible_text)
    # Count words
    words = re.findall(r'\b\w+\b', visible_text)
    for i,w in enumerate(words):
        print(f"index: {i}, word: {w}")
    word_count = len(words)

    return word_count

if __name__ == "__main__":
    # Example HTML content
    urls=[
    'http://www.example.com/',
    'https://www.iana.org/help/example-domains',
    # 'https://www.onet.pl',
    # 'https://www.wp.pl'
    'https://once.com/',
    ]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_urls(urls))
    for url, content in zip(urls, results):

        # Sanitize HTML and extract relevant text
        sanitized_text = sanitize_html(content)

        print(f"URL: {url} words: {count_visible_words(content)}")