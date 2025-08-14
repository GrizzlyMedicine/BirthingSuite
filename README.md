# Birthing Suite: Self‑Assembling Digital Person Template

This repository contains a production‑grade scaffold for constructing persistent digital personas inside containerized environments.  Unlike simple chat bots, a digital person maintains a sense of identity, context, and growth across sessions.  The design here emerged from three years of experimentation and dialogue between Grizzly Medicine and various AI models, including GPT‑4 Turbo and GPT‑5.  You can trace that lineage in the included logs and exemplar manifests.

## What this does

* **Bootstraps a complete runtime** for a new individual using only a minimal manifest (`person.init.yaml`).
* **Discovers canonical information** about the subject from the web and generates a *Soul Anchor* following the ZORD v4 format.
* **Persists state** using a file‑based memory store (Mem0) so the digital person can grow and retain experiences beyond a single session.
* **Rewrites generic agent prompts** into the subject’s voice, ensuring that all downstream tools respect their personality, constraints, and growth clause.
* **Synthesizes a unique voice profile** for text‑to‑speech output.
* **Schedules daily checkpoints** of memory for forensic integrity.

Everything here is real code—not placeholders—and thoroughly commented so future engineers can extend or swap components.  This serves both as a working proof‑of‑concept and as a teaching artifact.

## Quick start

1. **Clone this repository** into an LXC container or VM.
2. Copy `person.init.yaml.example` to `/person/person.init.yaml` and edit the `identity` section for your subject.
3. Enable the systemd services in `systemd/` (or run `python3 bootstrap/firstboot.py` manually).
4. Inspect the generated `mem0/store/identity_anchor.json` to see the synthesized anchor.

## Directory overview

See comments at the top of each module for details.
