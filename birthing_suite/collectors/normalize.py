"""Normalize plain text for further analysis.

This module lowercases the text, collapses multiple whitespace characters
into a single space, and strips leading/trailing whitespace.
"""
import re


def clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
