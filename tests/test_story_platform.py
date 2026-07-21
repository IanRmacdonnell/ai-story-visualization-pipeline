from __future__ import annotations

import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from continuity import check_continuity
from production_exporter import build_export_manifest, write_export_bundle
from scene_planner import plan_panels, segment_semantic_scenes
from story_models import Character, StoryBible
from story_production_cli import build_project
from review_queue import build_review_queue
from story_evaluation import evaluate_story_bible, merged_span_length
from build_review_app_data import build_review_payload

BENCHMARK_DIR = ROOT / "benchmarks" / "man_of_the_crowd"
sys.path.insert(0, str(BENCHMARK_DIR))
from build_benchmark import build_story_bible


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

    def test_day24_benchmark_is_canonical_and_continuity_clean(self) -> None:
        project = build_story_bible()
        findings = check_continuity(project)
        self.assertEqual(len(project.scenes), 3)
        self.assertEqual(len(project.panels), 8)
        self.assertEqual([panel.order for panel in project.panels], list(range(1, 9)))
        self.assertFalse([finding for finding in findings if finding.severity == "blocking"])
        self.assertTrue(all(panel.source.validate(project.source_text) == [] for panel in project.panels))

    def test_day24_storyboard_provenance_approvals_and_reproducibility(self) -> None:
        storyboard = BENCHMARK_DIR / "man-of-the-crowd-storyboard.png"
        project = build_story_bible(storyboard)
        findings = check_continuity(project)
        self.assertEqual(len(project.assets), 1)
        self.assertEqual(len(project.approvals), 3)
        self.assertTrue(all(panel.status == "approved" for panel in project.panels))
        self.assertEqual(project.assets[0].status, "approved")
        self.assertEqual(project.assets[0].file_hash, hashlib.sha256(storyboard.read_bytes()).hexdigest())
        self.assertEqual(build_export_manifest(project, findings), build_export_manifest(project, findings))

    def test_story_evaluation_measures_provenance_context_and_continuity(self) -> None:
        project = build_story_bible()
        report = evaluate_story_bible(project)
        self.assertEqual(report["blocking_findings"], 0)
        self.assertEqual(report["source_validity_rate"], 1.0)
        self.assertEqual(report["entity_context_rate"], 1.0)
        self.assertGreater(report["source_coverage_rate"], 0.25)
        self.assertGreaterEqual(report["quality_score"], 80)

    def test_review_queue_surfaces_unapproved_panels(self) -> None:
        project = build_project("Test Story", "Tester", SAMPLE, "internal_test", panels=2)
        queue = build_review_queue(project, check_continuity(project))
        panel_tasks = [task for task in queue if task.object_type == "panel"]
        self.assertTrue(panel_tasks)
        self.assertTrue(any("status" in task.reason.lower() for task in panel_tasks))

    def test_coverage_merges_overlapping_source_spans(self) -> None:
        self.assertEqual(merged_span_length([(0, 10), (5, 15), (20, 25)]), 20)

    def test_review_app_payload_preserves_panel_source_and_queue(self) -> None:
        payload = build_review_payload()
        self.assertEqual(payload["schemaVersion"], "1.0")
        self.assertEqual(len(payload["panels"]), 8)
        self.assertEqual(len(payload["reviewQueue"]), 8)
        self.assertTrue(all(panel["sourceExcerpt"] for panel in payload["panels"]))


if __name__ == "__main__":
    unittest.main()
