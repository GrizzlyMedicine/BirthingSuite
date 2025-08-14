"""Seed the memory store with identity metadata and initial knowledge.

This module is responsible for writing the initial state of the digital
person into Mem0.  It stores the name, aliases, and any knowledge records
provided directly in the manifest under `knowledge.packs`.  Each record
should be a JSON file path.
"""
import json
import time
from typing import Dict
from . import kv


def seed_memory(cfg: Dict) -> None:
    identity = cfg.get('identity', {})
    name = identity.get('name', 'Unknown')
    aliases = identity.get('aliases', [])
    kv.write('identity', {
        'owner': name,
        'aliases': aliases,
        'timestamp': time.time(),
    })
    records = []
    for pack in cfg.get('knowledge', {}).get('packs', []):
        path = pack.get('path')
        if not path:
            continue
        try:
            with open(path, 'r') as f:
                if pack.get('type') == 'json':
                    data = json.load(f)
                    records.extend(data if isinstance(data, list) else [data])
        except Exception:
            continue
    kv.write('knowledge', {
        'owner': name,
        'records': records,
        'timestamp': time.time(),
    })
