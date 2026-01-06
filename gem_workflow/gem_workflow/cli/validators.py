from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from .constants import ALPHA_STAGE, BETA_STAGE, CHARTER_VERSION, HANDOFF_VERSION
from .errors import ConfigMismatchError


SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"


def _load_schema(filename: str) -> dict[str, Any]:
    schema_path = SCHEMA_DIR / filename
    return json.loads(schema_path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        error_messages = "; ".join(_format_error(error) for error in errors)
        raise ValidationError(error_messages)


def _format_error(error: ValidationError) -> str:
    path = "/".join(str(item) for item in error.path)
    if path:
        return f"{path}: {error.message}"
    return error.message


def _check_version_lock(payload: dict[str, Any]) -> None:
    charter = payload.get("charter_version")
    handoff = payload.get("handoff_version")
    if charter != CHARTER_VERSION:
        raise ConfigMismatchError(
            f"Expected charter_version {CHARTER_VERSION}; received {charter or 'missing'}."
        )
    if handoff != HANDOFF_VERSION:
        raise ConfigMismatchError(
            f"Expected handoff_version {HANDOFF_VERSION}; received {handoff or 'missing'}."
        )


def validate_alpha_handoff(payload: dict[str, Any]) -> None:
    _check_version_lock(payload)
    if payload.get("stage") != ALPHA_STAGE:
        raise ConfigMismatchError(
            f"Expected stage {ALPHA_STAGE}; received {payload.get('stage') or 'missing'}."
        )
    schema = _load_schema("alpha_to_beta_handoff_schema_v1.4.1.json")
    validate_json(payload, schema)


def validate_beta_handoff(payload: dict[str, Any]) -> None:
    _check_version_lock(payload)
    if payload.get("stage") != BETA_STAGE:
        raise ConfigMismatchError(
            f"Expected stage {BETA_STAGE}; received {payload.get('stage') or 'missing'}."
        )
    schema = _load_schema("22_beta_to_gamma_handoff_schema_v1.4.1.json")
    validate_json(payload, schema)
