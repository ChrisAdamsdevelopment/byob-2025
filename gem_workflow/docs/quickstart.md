# Gem Workflow Quickstart

## Overview
Gem Workflow provides a deterministic, version-locked pipeline for multi-agent execution:
Alpha → Beta → Gamma. The CLI helps you scaffold artifacts, validate handoffs, and redact PII/secrets.

## Install
```bash
cd gem_workflow
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Initialize a Project
```bash
gemflow init demo_project
```
This creates a project directory with `/artifacts` and a version-locked config.

## Manual Paste Mode (Recommended)
1. Run Alpha with the prompts in `prompts/alpha/`.
2. Save the Alpha→Beta digest JSON as `artifacts/alpha/runs/<timestamp>_mps_vX.Y/alpha_to_beta_digest.json`.
3. Validate the digest:
   ```bash
   gemflow validate alpha-digest artifacts/alpha/runs/<timestamp>_mps_vX.Y/alpha_to_beta_digest.json
   ```
4. Paste the digest into Beta with `prompts/beta/20_gem_beta_system_instructions_v1.4.1.md`.
5. Save the critique output and the final Beta→Gamma JSON.
6. Validate the handoff:
   ```bash
   gemflow validate beta-handoff artifacts/beta/runs/<timestamp>_mps_vX.Y/beta_to_gamma_handoff.json
   ```
7. Provide the validated handoff to Gamma with `prompts/gamma/gamma_system_instructions_alignment_snippet_v1.4.1.md`.

## Smoke Tests
```bash
gemflow smoketest beta
```

## Redaction
```bash
gemflow redact input.txt output.txt
```
