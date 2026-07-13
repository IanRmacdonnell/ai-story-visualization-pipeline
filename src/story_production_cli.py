"""Create a free, deterministic StoryBible benchmark from a text file."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from continuity import check_continuity
from production_exporter import write_export_bundle
from scene_planner import plan_panels, segment_semantic_scenes
from story_models import StoryBible


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return result or "story"


def build_project(title: str, author: str, text: str, rights_status: str, panels: int) -> StoryBible:
    source_version = hashlib.sha256(text.encode("utf-8")).hexdigest()
    project = StoryBible(
        project_id=f"story_{slug(title)}",
        title=title,
        author=author,
        rights_status=rights_status,
        source_text=text,
        source_version=source_version,
    )
    project.scenes = segment_semantic_scenes(text)
    if project.scenes:
        project.panels = plan_panels(project.scenes[0], target_panels=panels)
    return project


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a deterministic story-production benchmark bundle.")
    parser.add_argument("source", type=Path, help="UTF-8 TXT or Markdown story file")
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="Unknown")
    parser.add_argument(
        "--rights-status",
        choices=("public_domain", "licensed", "internal_test"),
        default="internal_test",
    )
    parser.add_argument("--panels", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("output/story-production.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    text = args.source.read_text(encoding="utf-8")
    project = build_project(args.title, args.author, text, args.rights_status, args.panels)
    findings = check_continuity(project)
    output = write_export_bundle(project, findings, args.output)
    blocking = sum(finding.severity == "blocking" for finding in findings)
    print(f"Exported {len(project.scenes)} scenes and {len(project.panels)} panels to {output}")
    print(f"Continuity findings: {len(findings)} total, {blocking} blocking")


if __name__ == "__main__":
    main()

