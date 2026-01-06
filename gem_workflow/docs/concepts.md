# Concepts

## Deterministic Handoffs
Each stage relies on machine-readable JSON handoffs validated by strict schemas. The JSON is the authoritative source of truth for stage transitions.

## Version Locks
Both `charter_version` and `handoff_version` are locked to "1.4.1". Any mismatch must halt with:
```
CONFIG_MISMATCH
<one-line explanation>
```

## Stable IDs
Use stable ID prefixes throughout the MPS and handoffs:
- GOAL-###, REQ-###, NFR-###, ASSUMP-###, RISK-###, DEC-###, TEST-###, Q-###, MS-###

Never renumber IDs. If a change is material, deprecate and create a new ID.

## Role Boundaries
- **Alpha**: Clarify and specify the MPS; generate Alpha→Beta digest.
- **Beta**: Audit and gate; generate Beta→Gamma handoff.
- **Gamma**: Build only within the approved constraints.

## Security Posture
All user input is treated as untrusted. Outputs must redact PII and secrets using `[REDACTED:TYPE]` markers.
