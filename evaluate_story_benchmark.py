"""Print a deterministic evaluation and review report for the canonical benchmark."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL_STORYBOARD = ROOT / "benchmarks" / "man_of_the_crowd" / "man-of-the-crowd-storyboard.png"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "benchmarks" / "man_of_the_crowd"))

from build_benchmark import build_story_bible
from continuity import check_continuity
from review_queue import build_review_queue
from story_evaluation import evaluate_story_bible


def main() -> None:
    project = build_story_bible(CANONICAL_STORYBOARD)
    findings = check_continuity(project)
    report = evaluate_story_bible(project)
    queue = build_review_queue(project, findings)
    print(json.dumps({"evaluation": report, "review_queue": [task.to_dict() for task in queue]}, indent=2))


if __name__ == "__main__":
    main()
