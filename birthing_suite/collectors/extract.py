"""Extract readable text from HTML.

We use BeautifulSoup to strip scripts, styles and other non‑content tags.
This function returns a single whitespace‑normalized string.
"""
from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'form']):
        tag.decompose()
    text = ' '.join(soup.stripped_strings)
    return text
