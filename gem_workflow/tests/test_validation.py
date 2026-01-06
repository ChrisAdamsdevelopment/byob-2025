from pathlib import Path

import pytest

from gem_workflow.cli.errors import ConfigMismatchError
from gem_workflow.cli.validators import validate_alpha_handoff, validate_beta_handoff


def alpha_payload() -> dict:
    return {
        "handoff_version": "1.4.1",
        "charter_version": "1.4.1",
        "stage": "ALPHA_TO_BETA",
        "timestamp_local": "2025-01-01T09:00",
        "mps_version": "v1.0",
        "clarity_gates": {
            "objective": "Ship a deterministic workflow CLI",
            "primary_user": "Operators",
            "scope_in": ["CLI", "Schemas", "Prompts"],
            "scope_out": ["Hosting", "Billing", "Analytics"],
            "constraints": ["Offline-friendly"],
            "success_metrics": ["All handoffs validate"],
        },
        "requirements": [
            {"id": "REQ-001", "statement": "Provide a CLI validator", "priority": "Must"}
        ],
        "nfrs": [
            {"id": "NFR-001", "statement": "Validation is deterministic", "metric": "No warnings"}
        ],
        "tests": [
            {"id": "TEST-001", "description": "Validate schema", "covers": ["REQ-001", "NFR-001"]}
        ],
        "assumptions": [
            {"id": "ASSUMP-001", "statement": "Users can run Python 3.11", "impact": "CLI usable"}
        ],
        "risks": [
            {"id": "RISK-001", "statement": "Missing dependencies", "mitigation": "Pin versions"}
        ],
        "decisions": [
            {"id": "DEC-001", "summary": "Use Typer for CLI"}
        ],
        "questions": [
            {"id": "Q-001", "question": "Do we need API mode?"}
        ],
    }


def beta_payload() -> dict:
    return {
        "handoff_version": "1.4.1",
        "charter_version": "1.4.1",
        "stage": "BETA_TO_GAMMA",
        "timestamp_local": "2025-01-01T12:00",
        "mps_version": "v1.0",
        "gating_status": "APPROVED",
        "summary": {
            "what_was_audited": ["Alpha digest"],
            "top_blockers": [],
            "ready_for_gamma": True,
        },
        "must_fix": [],
        "recommended_fixes": [],
        "coverage_gaps": [],
        "discrepancies": [],
        "implementation_constraints": {
            "gamma_must_do": ["Follow handoff constraints"],
            "gamma_must_not_do": ["Change scope"],
        },
        "changed_ids": [],
        "impacted_sections": [],
    }


def test_alpha_schema_validates():
    validate_alpha_handoff(alpha_payload())


def test_beta_schema_validates():
    validate_beta_handoff(beta_payload())


def test_version_mismatch_halts_beta():
    payload = beta_payload()
    payload["charter_version"] = "0.0.0"
    with pytest.raises(ConfigMismatchError):
        validate_beta_handoff(payload)


def test_invalid_stage_halts():
    payload = alpha_payload()
    payload["stage"] = "BETA_TO_GAMMA"
    with pytest.raises(ConfigMismatchError):
        validate_alpha_handoff(payload)
