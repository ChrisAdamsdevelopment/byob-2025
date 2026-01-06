# Gem Workflow (ai-scrum-master)

A deterministic, version-locked, multi-agent idea-to-execution engine. This repository provides the prompts, schemas, CLI tooling, and documentation for the Gem Alpha → Beta → Gamma pipeline.

## What’s Included
- **Prompts** for Alpha, Beta, Gamma, and orchestration roles.
- **JSON Schemas** for Alpha→Beta and Beta→Gamma handoffs.
- **CLI** (`gemflow`) for scaffolding artifacts, validating handoffs, and redacting PII/secrets.
- **Tests** for schema validation, version lock enforcement, redaction, and output discipline.
- **Docs** covering quickstart, concepts, operator SOP, and artifact storage.

## Install
```bash
cd gem_workflow
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Core Commands
```bash
gemflow init <project_slug>
gemflow validate alpha-digest <path.json>
gemflow validate beta-handoff <path.json>
gemflow smoketest beta
gemflow redact <input> <output>
```

## Test
```bash
pytest
```

## Version Locks
The workflow enforces `charter_version` and `handoff_version` at `1.4.1`. Any mismatch must halt with:
```
CONFIG_MISMATCH
<one-line explanation>
```

## License
MIT
