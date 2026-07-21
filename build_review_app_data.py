"""Build the static data contract consumed by the local Story review app."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "benchmarks" / "man_of_the_crowd"))

from build_benchmark import build_story_bible
from continuity import check_continuity
from review_queue import build_review_queue
from story_evaluation import evaluate_story_bible


def build_review_payload() -> Dict[str, object]:
    project = build_story_bible()
    findings = check_continuity(project)
    queue = build_review_queue(project, findings)
    return {
        "schemaVersion": "1.0",
        "project": {"id": project.project_id, "title": project.title, "author": project.author},
        "evaluation": evaluate_story_bible(project),
        "panels": [
            {
                "panelId": panel.panel_id,
                "sceneId": panel.scene_id,
                "order": panel.order,
                "storyPurpose": panel.story_purpose,
                "sourceExcerpt": panel.source.excerpt,
                "sourceOffsets": [panel.source.start_offset, panel.source.end_offset],
                "characterIds": panel.character_ids,
                "locationId": panel.location_id,
                "propIds": panel.prop_ids,
                "shot": panel.shot,
                "cameraAngle": panel.camera_angle,
                "continuityConstraints": panel.continuity_constraints,
                "status": panel.status,
            }
            for panel in project.panels
        ],
        "reviewQueue": [task.to_dict() for task in queue],
    }


def main() -> None:
    output = ROOT / "review-app" / "data.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_review_payload(), indent=2), encoding="utf-8")
    print(f"Review data written to {output}")


if __name__ == "__main__":
    main()
