"""Deterministic quality metrics for StoryBible production bundles."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from continuity import check_continuity
from story_models import StoryBible


def merged_span_length(spans: Iterable[Tuple[int, int]]) -> int:
    merged: List[List[int]] = []
    for start, end in sorted(spans):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return sum(end - start for start, end in merged)


def ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def evaluate_story_bible(project: StoryBible) -> Dict[str, object]:
    findings = check_continuity(project)
    blocking = [finding for finding in findings if finding.severity == "blocking"]
    valid_sources = [panel for panel in project.panels if not panel.source.validate(project.source_text)]
    contextualized = [panel for panel in project.panels if panel.character_ids and panel.location_id]
    approved = [panel for panel in project.panels if panel.status == "approved"]
    covered = merged_span_length((panel.source.start_offset, panel.source.end_offset) for panel in valid_sources)
    source_coverage = ratio(covered, len(project.source_text))
    source_validity = ratio(len(valid_sources), len(project.panels))
    entity_context_rate = ratio(len(contextualized), len(project.panels))
    approval_rate = ratio(len(approved), len(project.panels))
    continuity_score = 1.0 if not blocking else max(0.0, 1.0 - len(blocking) / max(1, len(project.panels)))
    quality_score = round(
        30 * continuity_score
        + 25 * source_validity
        + 20 * entity_context_rate
        + 15 * approval_rate
        + 10 * min(1.0, source_coverage / 0.5),
        1,
    )
    return {
        "project_id": project.project_id,
        "scenes": len(project.scenes),
        "panels": len(project.panels),
        "blocking_findings": len(blocking),
        "warning_findings": sum(finding.severity == "warning" for finding in findings),
        "source_validity_rate": source_validity,
        "source_coverage_rate": source_coverage,
        "entity_context_rate": entity_context_rate,
        "approval_rate": approval_rate,
        "quality_score": quality_score,
    }
