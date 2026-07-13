Exit code: 0
Wall time: 0.4 seconds
Output:
"""Reproducible export utilities for story-production projects."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable

from story_models import ContinuityFinding, StoryBible


def build_export_manifest(project: StoryBible, findings: Iterable[ContinuityFinding]) -> Dict[str, Any]:
    project_data = project.to_dict()
    payload = json.dumps(project_data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {
        "schema_version": project.schema_version,
        "project": project_data,
        "continuity_findings": [finding.__dict__ for finding in findings],
        "project_sha256": hashlib.sha256(payload).hexdigest(),
        "approved_panel_ids": [panel.panel_id for panel in project.panels if panel.status == "approved"],
        "approved_asset_ids": [asset.asset_id for asset in project.assets if asset.status == "approved"],
    }


def write_export_bundle(
    project: StoryBible, findings: Iterable[ContinuityFinding], output_path: Path
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = build_export_manifest(project, findings)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path

