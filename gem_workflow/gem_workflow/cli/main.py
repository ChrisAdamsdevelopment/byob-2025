from __future__ import annotations

import json
from pathlib import Path

import typer
from jsonschema import ValidationError

from .artifacts import ArtifactPaths
from .errors import ConfigMismatchError
from .redaction import redact_text
from .validators import load_json, validate_alpha_handoff, validate_beta_handoff

app = typer.Typer(no_args_is_help=True, add_completion=False)
validate_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(validate_app, name="validate")


@app.command("init")
def init_project(project_slug: str) -> None:
    """Initialize a new Gem Workflow project with artifacts and config."""
    root = Path(project_slug).resolve()
    root.mkdir(parents=True, exist_ok=True)
    artifacts = ArtifactPaths(root=root)
    artifacts.create_base_structure()
    artifacts.write_config()
    typer.echo(f"Initialized project at {root}")


@validate_app.command("alpha-digest")
def validate_alpha(path: Path) -> None:
    _run_validation(path, validate_alpha_handoff)


@validate_app.command("beta-handoff")
def validate_beta(path: Path) -> None:
    _run_validation(path, validate_beta_handoff)


@app.command("smoketest")
def smoketest(stage: str) -> None:
    """Run smoketests for a given stage (beta)."""
    stage = stage.lower()
    if stage != "beta":
        typer.echo("Only beta smoketests are available.")
        raise typer.Exit(code=1)

    valid_payload = {
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

    mismatch_payload = dict(valid_payload)
    mismatch_payload["charter_version"] = "0.0.0"

    _report("Valid minimal Beta handoff", _attempt(validate_beta_handoff, valid_payload))
    _report("Version mismatch halts", _attempt(validate_beta_handoff, mismatch_payload, expect_mismatch=True))


@app.command("redact")
def redact(input_path: Path, output_path: Path) -> None:
    """Redact PII/secrets from a file."""
    content = input_path.read_text(encoding="utf-8")
    redacted = redact_text(content)
    output_path.write_text(redacted, encoding="utf-8")
    typer.echo(f"Redacted output written to {output_path}")


def _run_validation(path: Path, validator) -> None:
    try:
        payload = load_json(path)
        validator(payload)
    except ConfigMismatchError as exc:
        typer.echo("CONFIG_MISMATCH")
        typer.echo(exc.message)
        raise typer.Exit(code=2)
    except (ValidationError, json.JSONDecodeError) as exc:
        typer.echo(f"INVALID_JSON: {exc}")
        raise typer.Exit(code=1)
    typer.echo("VALID")


def _attempt(validator, payload, expect_mismatch: bool = False) -> bool:
    try:
        validator(payload)
        return not expect_mismatch
    except ConfigMismatchError:
        return expect_mismatch
    except Exception:
        return False


def _report(label: str, ok: bool) -> None:
    status = "PASS" if ok else "FAIL"
    typer.echo(f"{status}: {label}")
    if not ok:
        raise typer.Exit(code=1)
