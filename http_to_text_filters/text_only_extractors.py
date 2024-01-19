import re
from html import unescape

def extract_visible_text2(html):
    # Remove script, style, iframe, and iscript elements
    cleaned_html = re.sub(r'<(script|style|iframe|iscript)\b[^<]*(?:(?!</\1>)<[^<]*)*</\1>', '', html, flags=re.DOTALL)
    
    # Remove HTML comments
    cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)

    # Decode HTML entities
    cleaned_html = unescape(cleaned_html)

    # Remove other HTML tags
    cleaned_text = re.sub(r'<.*?>', '', cleaned_html)

    # Remove dots
    cleaned_text = cleaned_text.replace('.', ' ')

    # Remove extra whitespaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Remove newline characters
    cleaned_text = cleaned_text.replace('\\n', ' ')
    cleaned_text = cleaned_text.replace('\n', ' ')

    # Remove /t characters
    cleaned_text = cleaned_text.replace('\\t', '')

    # Remove special characters
    cleaned_text = cleaned_text.replace('&nbsp;', ' ')
    cleaned_text = cleaned_text.replace('&rarr;', '')
    cleaned_text = cleaned_text.replace('P.S', 'PS')
    cleaned_text = cleaned_text.replace('P.P.S', 'PPS')
    cleaned_text = cleaned_text.replace('&mdash;', '')
    cleaned_text = cleaned_text.replace('&ndash;', '')

    return cleaned_text

# def extract_visible_text(html):
#     # Remove script and style elements
#     cleaned_html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.DOTALL)
#     cleaned_html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', cleaned_html, flags=re.DOTALL)
#     cleaned_html = re.sub(r'<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>', '', cleaned_html, flags=re.DOTALL)
#     cleaned_html = re.sub(r'<iscript\b[^<]*(?:(?!<\/iscript>)<[^<]*)*<\/iscript>', '', cleaned_html, flags=re.DOTALL)
#     # Remove HTML comments
#     cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)
#     # Remove other HTML tags
#     cleaned_text = re.sub(r'<.*?>', '', cleaned_html)
#     # Add a space after each </div>
#     cleaned_text = cleaned_text.replace('</div>', ' </div>')

#     # Add a space after each </a>
#     cleaned_text = cleaned_text.replace('</a>', ' </a>')

#     # Remove extra whitespaces
#     cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

#     # Split the text using the marker
#     # cleaned_html = html_with_marker.split('<!--ANCHOR_SEPARATOR-->')
    
#     # Remove newline characters
#     cleaned_text = cleaned_text.replace('\\n', ' ')
#     # Remove newline characters
#     cleaned_text = cleaned_text.replace('\n', ' ')
#     # handle dots
#     cleaned_text = cleaned_text.replace('.', ' ')
#     # Remove /t characters
#     cleaned_text = cleaned_text.replace('\\t', '')
#     # remove nbsp
#     cleaned_text = cleaned_text.replace('nbsp','')
#     # remove right arrow
#     cleaned_text = cleaned_text.replace('rarr','')
#     # handle post scriptum
#     cleaned_text = cleaned_text.replace('P.S','PS')
#     # handle post scriptum2
#     cleaned_text = cleaned_text.replace('P.P.S','PPS')
#     # handle em dash
#     cleaned_text = cleaned_text.replace('mdash', '')
#     # handle en dash
#     cleaned_text = cleaned_text.replace('ndash', '')
#     # print(cleaned_text)
#     return cleaned_text
def extract_visible_text(html):
    # Remove script and style elements
    cleaned_html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', cleaned_html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>', '', cleaned_html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<iscript\b[^<]*(?:(?!<\/iscript>)<[^<]*)*<\/iscript>', '', cleaned_html, flags=re.DOTALL)
    # Remove HTML comments
    cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)
    
    # Remove other HTML tags
    cleaned_text = re.sub(r'<.*?>', '', cleaned_html)
    
    # Add a space after each </div>
    cleaned_text = cleaned_text.replace('</div>', '</div> ')

    # Add a space after each </a>
    cleaned_text = cleaned_text.replace('</a>', '</a> ')

    # Remove extra whitespaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Remove newline characters
    cleaned_text = cleaned_text.replace('\\n', ' ')
    cleaned_text = cleaned_text.replace('\n', ' ')

    # handle dots
    cleaned_text = cleaned_text.replace('.', ' ')

    # Remove /t characters
    cleaned_text = cleaned_text.replace('\\t', '')

    # remove nbsp
    cleaned_text = cleaned_text.replace('nbsp', '')

    # remove right arrow
    cleaned_text = cleaned_text.replace('rarr', '')

    # handle post scriptum
    cleaned_text = cleaned_text.replace('P.S', 'PS')

    # handle post scriptum2
    cleaned_text = cleaned_text.replace('P.P.S', 'PPS')

    # handle em dash
    cleaned_text = cleaned_text.replace('mdash', '')

    # handle en dash
    cleaned_text = cleaned_text.replace('ndash', '')

    # Add a space before each uppercase letter that follows a lowercase letter
    cleaned_text = re.sub(r'([a-ząćęłńóśźż])([A-ZĄĆĘŁŃÓŚŹŻ])', r'\1 \2', cleaned_text)
    
    return cleaned_text
def count_words(text):
    # Extract words (assuming words are separated by spaces)
    words = re.findall(r'\b\w+\b', text)
    for i,w in enumerate(words):
        print(f"index: {i}, word: {w}")
    return len(words)