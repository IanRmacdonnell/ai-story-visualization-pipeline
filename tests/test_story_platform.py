Exit code: 0
Wall time: 0.4 seconds
Output:
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from continuity import check_continuity
from production_exporter import write_export_bundle
from scene_planner import plan_panels, segment_semantic_scenes
from story_models import Character, StoryBible
from story_production_cli import build_project


SAMPLE = (
    "At dusk, Mara entered the abandoned observatory. The brass telescope pointed east. "
    "She heard footsteps below and hid the silver key inside her coat.\n\n"
    "Later that night, the storm broke over the hill. Mara returned to the telescope, "
    "but the silver key was gone. A shadow crossed the doorway."
)


class StoryPlatformTests(unittest.TestCase):
    def test_semantic_scenes_preserve_exact_source_offsets(self) -> None:
        scenes = segment_semantic_scenes(SAMPLE, min_scene_chars=50)
        self.assertGreaterEqual(len(scenes), 2)
        for scene in scenes:
            self.assertEqual(
                SAMPLE[scene.source.start_offset : scene.source.end_offset],
                scene.source.excerpt,
            )

    def test_panel_plan_is_ordered_and_source_linked(self) -> None:
        scene = segment_semantic_scenes(SAMPLE, min_scene_chars=50)[0]
        panels = plan_panels(scene, target_panels=3)
        self.assertEqual([panel.order for panel in panels], list(range(1, len(panels) + 1)))
        for panel in panels:
            self.assertEqual(SAMPLE[panel.source.start_offset : panel.source.end_offset], panel.source.excerpt)

    def test_valid_generated_project_has_no_blocking_findings(self) -> None:
        project = build_project("Test Story", "Tester", SAMPLE, "internal_test", panels=4)
        findings = check_continuity(project)
        self.assertFalse([finding for finding in findings if finding.severity == "blocking"])

    def test_unknown_character_is_blocking(self) -> None:
        project = build_project("Test Story", "Tester", SAMPLE, "internal_test", panels=2)
        project.characters.append(Character("char_mara", "Mara", status="approved"))
        project.panels[0].character_ids = ["char_missing"]
        findings = check_continuity(project)
        self.assertTrue(any(finding.rule_id == "character_reference" for finding in findings))

    def test_export_is_json_and_contains_hash(self) -> None:
        project: StoryBible = build_project("Test Story", "Tester", SAMPLE, "internal_test", panels=2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle.json"
            write_export_bundle(project, check_continuity(project), output)
            data = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(data["project"]["title"], "Test Story")
        self.assertEqual(len(data["project_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()

