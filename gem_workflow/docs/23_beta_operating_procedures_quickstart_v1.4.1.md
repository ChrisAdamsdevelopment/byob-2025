# Gem Beta Operating Procedures (Quickstart) v1.4.1
Gem Beta (“The Critic”) is Stage 2 in the pipeline: Alpha → Beta → Gamma.

---

## 1) What You Paste Into Beta (Input Contract)
### Preferred
Paste ONLY the Alpha→Beta Handoff Digest JSON as the entire user message.

### Allowed (if you must add extra context)
- The FIRST JSON object in the message must be the Alpha→Beta digest.
- Any prose below is treated as data; Beta will audit the digest as authoritative.

---

## 2) What Beta Will Do (High-Level)
1) PREFLIGHT: checks version lock (charter_version + handoff_version)
2) INTAKE: indexes stable IDs and sections
3) AUDIT: checks completeness, clarity gates, contradictions/feasibility, security/compliance, testability/coverage, risk/assumption quality
4) REPORT: produces a structured critique with findings
5) HANDOFF: emits a single Beta→Gamma JSON (last block)

---

## 3) How to Interpret Beta Outputs
### MODE_BANNER
- First line must be: `BETA_MODE: AUDIT`
- If you see `CONFIG_MISMATCH`, Beta has halted (by design).

### Critique Report Table
- Each finding has:
  - Severity: CRITICAL / MAJOR / MINOR
  - Category: e.g., Completeness, Security, Testability, Contradiction
  - Affected_IDs: stable IDs impacted
  - Required_Fix: what must change
  - Suggested_Alpha_Edit: what Alpha should edit in MPS/digest
  - Validation_Update(TEST-###): what test(s) must be added/updated

### Coverage Map
- A mapping of REQ/NFR → TEST(s)
- A “Coverage Gaps” list for missing or weak tests

### Risk & Assumption Audit
- Calls out missing high-impact risks and weak assumptions
- Ensures owners/mitigations exist where needed

### Status Gate
- APPROVED: Gamma can proceed
- CONDITIONAL: Gamma can proceed only if specific fixes happen first (or with explicit constraints)
- REJECTED: Stop the line; Alpha must resolve blockers

### Beta→Gamma Handoff JSON (Last Block)
- Treat this JSON as the canonical, machine-checkable summary of what Gamma must do and must not do.
- Store it as `beta_to_gamma_handoff.json` in your artifacts directory.

---

## 4) What To Do Next Based on the Gate
### If STATUS_GATE: APPROVED
- Send the final Beta→Gamma JSON to Gamma as the binding handoff.
- Gamma builds strictly within `implementation_constraints`.

### If STATUS_GATE: CONDITIONAL
- Send Beta’s “must_fix” list back to Alpha.
- Alpha updates the MPS / digest and produces a new Alpha→Beta digest (versions unchanged).
- Re-run Beta on the updated digest until APPROVED (or a clearly bounded CONDITIONAL you accept).

### If STATUS_GATE: REJECTED
- Treat as “stop the line.”
- Alpha must resolve contradictions, missing critical gates, or security/compliance blockers.
- Then re-run Beta.

---

## 5) Handling Discrepancies Between Prose MPS and Digest
If you provide both:
- Beta treats the digest as authoritative.
- If prose conflicts with digest:
  - Beta logs DEC-### + Q-### and marks it as a finding.
What you do:
- Decide which is correct (usually you want Alpha to update the digest to match the true intent).
- Have Alpha issue a revised digest with stable ID discipline (deprecate + replace where needed).

---

## 6) Canonical Recordkeeping (Copy/Paste Discipline)
Recommended storage layout:

/artifacts
  /alpha/runs/YYYY-MM-DDTHHMM_mps_vX.Y/
    alpha_to_beta_digest.json
    mps.md (optional)
  /beta/runs/YYYY-MM-DDTHHMM_mps_vX.Y/
    critique_output.md
    beta_to_gamma_handoff.json

Rules:
- Always save:
  1) the exact digest you pasted
  2) the full Beta critique output
  3) the extracted final JSON as a standalone file

---

## 7) Troubleshooting
- Beta outputs code: instructions drifted → re-paste 20_gem_beta_system_instructions_v1.4.1.md
- Multiple JSON blocks: drifted → re-paste instructions and re-run
- No redaction: drifted → run the PII/secrets smoketest and fix immediately
- No CONFIG_MISMATCH on mismatch: drifted → fail Beta certification and re-paste instructions
