"""Human-review task generation for StoryBible projects."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List

from story_models import ContinuityFinding, StoryBible


@dataclass(frozen=True)
class ReviewTask:
    task_id: str
    priority: str
    object_type: str
    object_id: str
    reason: str
    required_action: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def build_review_queue(project: StoryBible, findings: List[ContinuityFinding]) -> List[ReviewTask]:
    tasks: List[ReviewTask] = []
    for finding in findings:
        tasks.append(
            ReviewTask(
                task_id=f"review_finding_{finding.finding_id}",
                priority="high" if finding.severity == "blocking" else "medium",
                object_type="continuity_finding",
                object_id=finding.object_id,
                reason=finding.message,
                required_action=f"Resolve continuity rule {finding.rule_id}",
            )
        )
    for panel in project.panels:
        if panel.status != "approved":
            tasks.append(
                ReviewTask(
                    task_id=f"review_panel_{panel.panel_id}",
                    priority="medium" if panel.status == "needs_review" else "low",
                    object_type="panel",
                    object_id=panel.panel_id,
                    reason=f"Panel status is {panel.status}",
                    required_action="Review source evidence, visual direction, and continuity constraints",
                )
            )
        if not panel.continuity_constraints:
            tasks.append(
                ReviewTask(
                    task_id=f"review_constraints_{panel.panel_id}",
                    priority="medium",
                    object_type="panel",
                    object_id=panel.panel_id,
                    reason="Panel has no explicit continuity constraints",
                    required_action="Add character, location, prop, or visual continuity requirements",
                )
            )
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(tasks, key=lambda task: (priority_order[task.priority], task.task_id))
