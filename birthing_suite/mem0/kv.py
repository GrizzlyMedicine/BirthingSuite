"""Simple JSON file key/value store.

This module implements minimal persistence for the digital person using a

directory of JSON files.  Keys become filenames, and the values are JSON
serializable dictionaries.  It is synchronous and safe for single‑threaded
use.  For concurrent use, replace with a proper database.
"""
import json
import os
from typing import Any, Dict

# Default store path.  Overridden by manifest if needed.
STORE_DIR = '/opt/core/mem0/store'


def _ensure_store() -> None:
    os.makedirs(STORE_DIR, exist_ok=True)


def _path(key: str) -> str:
    return os.path.join(STORE_DIR, f"{key}.json")


def write(key: str, value: Dict[str, Any]) -> None:
    _ensure_store()
    with open(_path(key), 'w') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def read(key: str) -> Dict[str, Any]:
    with open(_path(key), 'r') as f:
        return json.load(f)
