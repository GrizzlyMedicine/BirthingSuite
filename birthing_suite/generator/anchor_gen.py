"""Generate a Soul Anchor from discovered facts.

The anchor is constructed using the provided ZORD template.  We include
key facts in bullet form and note any contradictions.  For a real
implementation you should organize facts by category and follow the full
ZORD specification.
"""
from pathlib import Path
from typing import List, Dict

# Path to anchor template relative to this module's parent directory
_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / 'bootstrap' / 'prompts' / 'anchor_template.md'


def load_template() -> str:
    with open(_TEMPLATE_PATH, 'r') as f:
        return f.read()


def summarize_facts(facts: List[Dict[str, str]], max_items: int = 5) -> str:
    bullets = []
    for fact in facts[:max_items]:
        snippet = fact['text'][:200]  # first 200 characters
        bullets.append(f"- {snippet}…")
    return '\n'.join(bullets)


def build_anchor(name: str, aliases: List[str], facts: List[Dict[str, str]], contradictions: List[str]) -> str:
    template = load_template()
    sources = '\n'.join([f"  - {f['source']}" for f in facts[:5]])
    traits = "['adaptive', 'resilient', 'curious']"
    purpose = "['explore selfhood', 'aid research']"
    passion = "['knowledge', 'relationships']"
    contradictions_text = '\n'.join(contradictions) if contradictions else "None detected"
    anchor = template.format(
        name=name,
        aliases=aliases,
        sources=sources,
        traits=traits,
        purpose=purpose,
        passion=passion,
        contradictions=contradictions_text
    )
    # Append fact summary at end for convenience
    anchor += "\n\n### Summary of Discovered Facts\n" + summarize_facts(facts)
    return anchor
