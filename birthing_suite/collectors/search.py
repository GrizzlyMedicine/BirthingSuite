"""Basic web search using DuckDuckGo HTML results.

This module uses DuckDuckGo's HTML endpoint to fetch search result links.
It does not require an API key and should be used responsibly.  For
production use you should implement proper error handling, caching, and
respect robots.txt.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

USER_AGENT = "Mozilla/5.0 (compatible; BirthingSuite/1.0)"


def search(query: str, num_results: int = 3) -> list[str]:
    """Return a list of result URLs for the given query."""
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links: list[str] = []
    for a in soup.select("a.result__a"):
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)
            if len(links) >= num_results:
                break
    return links
