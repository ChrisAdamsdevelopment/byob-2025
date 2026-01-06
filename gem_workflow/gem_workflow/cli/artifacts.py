from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .constants import CHARTER_VERSION


@dataclass(frozen=True)
class ArtifactPaths:
    root: Path

    @property
    def config_path(self) -> Path:
        return self.root / "gemflow_config.json"

    @property
    def artifacts_root(self) -> Path:
        return self.root / "artifacts"

    def create_base_structure(self) -> None:
        for stage in ["alpha", "beta", "gamma"]:
            (self.artifacts_root / stage / "runs").mkdir(parents=True, exist_ok=True)

    def write_config(self) -> None:
        config = {
            "charter_version": CHARTER_VERSION,
            "artifact_root": str(self.artifacts_root),
        }
        self.config_path.write_text(
            json.dumps(config, indent=2) + "\n",
            encoding="utf-8",
        )
