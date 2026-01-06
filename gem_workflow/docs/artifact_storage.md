# Artifact Storage

## Canonical Layout
```
/artifacts
  /alpha/runs/YYYY-MM-DDTHHMM_mps_vX.Y/
    alpha_to_beta_digest.json
    mps.md
  /beta/runs/YYYY-MM-DDTHHMM_mps_vX.Y/
    critique_output.md
    beta_to_gamma_handoff.json
  /gamma/runs/YYYY-MM-DDTHHMM_mps_vX.Y/
    build_outputs/
```

## Rules
- The JSON handoff is the authoritative record.
- Never overwrite existing runs. Create a new timestamped directory for each run.
- Store the full critique output alongside the extracted JSON handoff.
- If a version lock fails, record the failure in a new run directory and halt.
