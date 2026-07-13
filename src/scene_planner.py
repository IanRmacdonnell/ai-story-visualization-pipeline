"""Deterministic semantic-scene and panel planning helpers."""

from __future__ import annotations

import re
from typing import List

from story_models import PanelSpec, Scene, SourceEvidence


SCENE_BREAK_PATTERNS = re.compile(
    r"(?:\n\s*\n|(?<=[.!?])\s+(?=(?:Later|Meanwhile|The next|That night|At dawn|At last|Suddenly)\b))",
    flags=re.IGNORECASE,
)


def _sentences_with_offsets(text: str, base_offset: int = 0) -> List[SourceEvidence]:
    evidence: List[SourceEvidence] = []
    for match in re.finditer(r"\S(?:.*?\S)?(?:[.!?](?=\s|$)|$)", text, flags=re.DOTALL):
        excerpt = match.group(0).strip()
        if not excerpt:
            continue
        local_start = match.start() + len(match.group(0)) - len(match.group(0).lstrip())
        start = base_offset + local_start
        evidence.append(SourceEvidence(excerpt, start, start + len(excerpt)))
    return evidence


def segment_semantic_scenes(text: str, min_scene_chars: int = 300) -> List[Scene]:
    """Split on paragraphs and explicit time/transition language, then merge tiny beats."""
    chunks: List[SourceEvidence] = []
    cursor = 0
    for match in SCENE_BREAK_PATTERNS.finditer(text):
        raw = text[cursor : match.start()]
        stripped = raw.strip()
        if stripped:
            start = cursor + len(raw) - len(raw.lstrip())
            chunks.append(SourceEvidence(stripped, start, start + len(stripped)))
        cursor = match.end()
    raw = text[cursor:]
    stripped = raw.strip()
    if stripped:
        start = cursor + len(raw) - len(raw.lstrip())
        chunks.append(SourceEvidence(stripped, start, start + len(stripped)))

    merged: List[SourceEvidence] = []
    for chunk in chunks:
        if merged and len(chunk.excerpt) < min_scene_chars:
            previous = merged[-1]
            combined = text[previous.start_offset : chunk.end_offset]
            merged[-1] = SourceEvidence(combined, previous.start_offset, chunk.end_offset)
        else:
            merged.append(chunk)

    if not merged and text.strip():
        start = len(text) - len(text.lstrip())
        excerpt = text.strip()
        merged = [SourceEvidence(excerpt, start, start + len(excerpt))]

    scenes: List[Scene] = []
    for index, source in enumerate(merged, start=1):
        first_sentence = _sentences_with_offsets(source.excerpt, source.start_offset)
        summary = first_sentence[0].excerpt if first_sentence else source.excerpt[:180]
        scenes.append(
            Scene(
                scene_id=f"scene_{index:03d}",
                order=index,
                summary=summary[:240],
                source=source,
                objective="Review and define the scene objective",
                conflict="Review and define the scene conflict",
                emotional_turn="Review and define the emotional turn",
                required_information=[summary[:160]],
                status="needs_review",
            )
        )
    return scenes


def plan_panels(scene: Scene, target_panels: int = 8) -> List[PanelSpec]:
    sentences = _sentences_with_offsets(scene.source.excerpt, scene.source.start_offset)
    if not sentences:
        return []
    count = max(1, min(target_panels, len(sentences)))
    groups: List[List[SourceEvidence]] = [[] for _ in range(count)]
    for index, sentence in enumerate(sentences):
        bucket = min(count - 1, index * count // len(sentences))
        groups[bucket].append(sentence)

    panels: List[PanelSpec] = []
    shots = ["establishing", "wide", "medium", "close_up", "detail"]
    for index, group in enumerate(groups, start=1):
        start = group[0].start_offset
        end = group[-1].end_offset
        excerpt = scene.source.excerpt[start - scene.source.start_offset : end - scene.source.start_offset]
        panels.append(
            PanelSpec(
                panel_id=f"{scene.scene_id}_panel_{index:03d}",
                scene_id=scene.scene_id,
                order=index,
                source=SourceEvidence(excerpt, start, end),
                story_purpose=f"Represent beat {index} of {count}: {group[0].excerpt[:120]}",
                character_ids=list(scene.character_ids),
                location_id=scene.location_id,
                shot=shots[min(index - 1, len(shots) - 1)],
                subject_action=group[0].excerpt[:180],
                continuity_constraints=["Preserve approved character and location canon"],
                status="needs_review",
            )
        )
    return panels

