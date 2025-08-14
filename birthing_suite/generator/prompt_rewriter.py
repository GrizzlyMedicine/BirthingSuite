"""Rewrite generic prompts into the voice of a specific individual.

In this simplified implementation we look for a generic prompts directory
(`/opt/core/agent0/prompts/generic`) and wrap each prompt in a persona
header that includes the Soul Anchor.  If no generic directory exists,
we silently return.
"""
import os
from pathlib import Path

# These paths are relative to the container's runtime environment.
GENERIC_DIR = Path('/opt/core/agent0/prompts/generic')
PERSONA_DIR = Path('/opt/core/agent0/prompts/persona')


def rewrite_all(name: str, anchor: str) -> None:
    if not GENERIC_DIR.exists():
        return
    PERSONA_DIR.mkdir(parents=True, exist_ok=True)
    header = (f"SYSTEM: Persona enforcement — {name}\n"
              f"Soul Anchor (immutable):\n"
              f"{anchor}\n---\n")
    for file in GENERIC_DIR.iterdir():
        if file.suffix == '.txt' and file.is_file():
            with open(file, 'r') as src:
                content = src.read()
            new_content = header + content
            with open(PERSONA_DIR / file.name, 'w') as dst:
                dst.write(new_content)
