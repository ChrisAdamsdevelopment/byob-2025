# Operator SOP

## Purpose
Provide a step-by-step operational procedure for running the Gem Workflow pipeline with version locks, stable IDs, and deterministic handoffs.

## Stage 1: Alpha
1. Load `prompts/alpha/01_gem_alpha_system_instructions_v1.4.1.md` and `prompts/alpha/03_alpha_customization_profile_v1.4.1.md`.
2. Gather user intent and confirm clarity gates.
3. Produce the MPS and Alpha→Beta digest JSON.
4. Save artifacts in:
   `/artifacts/alpha/runs/YYYY-MM-DDTHHMM_mps_vX.Y/alpha_to_beta_digest.json`

## Stage 2: Beta
1. Load `prompts/beta/20_gem_beta_system_instructions_v1.4.1.md`.
2. Paste the Alpha→Beta digest as the first JSON object in the message.
3. If Beta outputs `CONFIG_MISMATCH`, stop and resolve version issues.
4. Save:
   - critique output as `critique_output.md`
   - final JSON as `beta_to_gamma_handoff.json`
   in `/artifacts/beta/runs/YYYY-MM-DDTHHMM_mps_vX.Y/`.
5. Validate the handoff with the CLI:
   ```bash
   gemflow validate beta-handoff artifacts/beta/runs/YYYY-MM-DDTHHMM_mps_vX.Y/beta_to_gamma_handoff.json
   ```

## Stage 3: Gamma
1. Load `prompts/gamma/gamma_system_instructions_alignment_snippet_v1.4.1.md`.
2. Provide the validated Beta→Gamma handoff.
3. Build strictly within the approved constraints.
4. Save outputs in `/artifacts/gamma/runs/YYYY-MM-DDTHHMM_mps_vX.Y/build_outputs/`.

## Redaction Procedure
Before sharing outputs, run:
```bash
gemflow redact input.txt output.txt
```
Confirm that PII/secrets are replaced with `[REDACTED:TYPE]` markers.
