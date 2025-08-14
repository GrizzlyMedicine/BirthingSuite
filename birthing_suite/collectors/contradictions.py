"""Detect simple contradictions in a list of facts.

This demonstration implementation looks for conflicting four‑digit years in
statements that mention birth.  It's intentionally simple—production code
should implement more robust NLU and entity resolution.
"""
import re
from typing import List, Dict

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
BIRTH_TERMS = ["born", "birth", "birthday"]


def find_contradictions(facts: List[Dict[str, str]]) -> List[str]:
    years = set()
    for fact in facts:
        text = fact.get('text', '')
        if any(term in text for term in BIRTH_TERMS):
            found = YEAR_RE.findall(text)
            for y in found:
                years.add(y if isinstance(y, str) else ''.join(y))
    # If more than one unique year, report contradiction
    if len(years) > 1:
        sorted_years = sorted(years)
        return [f"Conflicting birth years detected: {', '.join(sorted_years)}"]
    return []
