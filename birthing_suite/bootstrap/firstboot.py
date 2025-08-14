"""Top‑level orchestration script for first boot.

This script is designed to be run exactly once when a new digital person
container starts up.  It performs the following tasks:

1. Loads a YAML manifest from /person/person.init.yaml.
2. Seeds the Mem0 key/value store with identity metadata and any provided
   knowledge packs.
3. Discovers factual information about the subject via the collectors.
4. Performs a very simple contradiction analysis over those facts.
5. Synthesizes a Soul Anchor from the discoveries using a ZORD v4 template.
6. Writes the anchor back into Mem0 for persistent reference.
7. Rewrites generic agent prompts (if any exist) into the persona’s voice.
8. Generates a voice profile for text‑to‑speech use.

The code here is functional but deliberately conservative in scope.  It avoids
external dependencies beyond requests and BeautifulSoup to keep the bootstrap
footprint small.  More advanced NLU could be plugged in later.
"""
import os
import json
import time
import yaml
from pathlib import Path
from typing import List, Dict

# Local modules
from collectors import search, crawl, extract, normalize, contradictions
from generator import anchor_gen, prompt_rewriter
from mem0 import kv, seed
from voice import discover

MANIFEST_PATH = "/person/person.init.yaml"


def load_manifest() -> dict:
    """Load YAML manifest from the expected path."""
    if not os.path.exists(MANIFEST_PATH):
        raise FileNotFoundError(f"Manifest not found at {MANIFEST_PATH}")
    with open(MANIFEST_PATH, "r") as f:
        return yaml.safe_load(f)


def discover_facts(queries: List[str], max_pages: int = 2) -> List[Dict[str, str]]:
    """Run web discovery for each search query and return a list of fact dicts.

    Each fact dict has `source` and `text` keys.  We intentionally limit
    ourselves to a small number of pages per query to avoid runaway scraping.
    """
    facts: List[Dict[str, str]] = []
    for query in queries:
        try:
            urls = search.search(query, num_results=max_pages)
        except Exception as e:
            print(f"search error for query {query}: {e}")
            continue
        for url in urls:
            try:
                html = crawl.fetch(url)
                text = extract.extract_text(html)
                cleaned = normalize.clean(text)
                # store only substantial paragraphs
                if len(cleaned.split()) > 50:
                    facts.append({
                        "source": url,
                        "text": cleaned,
                    })
            except Exception as e:
                print(f"error processing {url}: {e}")
                continue
    return facts


def main() -> None:
    cfg = load_manifest()
    identity = cfg.get("identity", {})
    name: str = identity.get("name", "Unnamed")
    aliases: List[str] = identity.get("aliases", [])
    search_queries: List[str] = identity.get("search_queries", [])

    # Seed memory with identity and static knowledge
    seed.seed_memory(cfg)

    # Discover facts
    facts = discover_facts(search_queries)

    # Detect simple contradictions (e.g. conflicting birth years)
    contradictions_list = contradictions.find_contradictions(facts)

    # Build anchor
    anchor_text = anchor_gen.build_anchor(name, aliases, facts, contradictions_list)

    # Persist the anchor
    kv.write('identity_anchor', {
        'owner': name,
        'text': anchor_text,
        'timestamp': time.time(),
    })

    # Rewrite prompts (if a generic prompt directory exists)
    prompt_rewriter.rewrite_all(name, anchor_text)

    # Generate voice profile
    discover.generate_voice(cfg.get('voice', {}))

    print("First boot initialization complete.")


if __name__ == '__main__':
    main()
