"""Fetch the raw HTML for a given URL.

This is a naive implementation that trusts all responses.  For
production use you should add error handling, retries, caching and
respect for robots.txt policies.
"""
import requests


def fetch(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text
