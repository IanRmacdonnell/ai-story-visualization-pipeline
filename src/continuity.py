"""Deterministic continuity validation for StoryBible projects."""

from __future__ import annotations

from typing import List

from story_models import ContinuityFinding, StoryBible


def check_continuity(project: StoryBible) -> List[ContinuityFinding]:
    findings: List[ContinuityFinding] = []
    counter = 1

    def add(severity: str, rule: str, message: str, object_id: str) -> None:
        nonlocal counter
        findings.append(
            ContinuityFinding(
                finding_id=f"finding_{counter:04d}",
                severity=severity,
                rule_id=rule,
                message=message,
                object_id=object_id,
            )
        )
        counter += 1

    seen: set[str] = set()
    for entity_id in project.entity_ids():
        if entity_id in seen:
            add("blocking", "unique_id", f"Duplicate ID: {entity_id}", entity_id)
        seen.add(entity_id)

    character_ids = {item.character_id for item in project.characters}
    location_ids = {item.location_id for item in project.locations}
    prop_ids = {item.prop_id for item in project.props}
    scene_ids = {item.scene_id for item in project.scenes}
    asset_ids = {item.asset_id for item in project.assets}

    expected_scene_orders = list(range(1, len(project.scenes) + 1))
    observed_scene_orders = sorted(item.order for item in project.scenes)
    if observed_scene_orders != expected_scene_orders:
        add("blocking", "scene_order", "Scene order must be contiguous and start at 1", project.project_id)

    for scene in project.scenes:
        for error in scene.source.validate(project.source_text):
            add("blocking", "source_evidence", error, scene.scene_id)
        for character_id in scene.character_ids:
            if character_id not in character_ids:
                add("blocking", "character_reference", f"Unknown character: {character_id}", scene.scene_id)
        if scene.location_id and scene.location_id not in location_ids:
            add("blocking", "location_reference", f"Unknown location: {scene.location_id}", scene.scene_id)

    panel_orders: dict[str, List[int]] = {}
    for panel in project.panels:
        panel_orders.setdefault(panel.scene_id, []).append(panel.order)
        if panel.scene_id not in scene_ids:
            add("blocking", "scene_reference", f"Unknown scene: {panel.scene_id}", panel.panel_id)
        for error in panel.source.validate(project.source_text):
            add("blocking", "source_evidence", error, panel.panel_id)
        for character_id in panel.character_ids:
            if character_id not in character_ids:
                add("blocking", "character_reference", f"Unknown character: {character_id}", panel.panel_id)
        if panel.location_id and panel.location_id not in location_ids:
            add("blocking", "location_reference", f"Unknown location: {panel.location_id}", panel.panel_id)
        for prop_id in panel.prop_ids:
            if prop_id not in prop_ids:
                add("blocking", "prop_reference", f"Unknown prop: {prop_id}", panel.panel_id)
        for asset_id in panel.reference_asset_ids:
            if asset_id not in asset_ids:
                add("blocking", "asset_reference", f"Unknown asset: {asset_id}", panel.panel_id)

    all_panel_orders = sorted(panel.order for panel in project.panels)
    if all_panel_orders != list(range(1, len(project.panels) + 1)):
        add("blocking", "panel_order", "Chapter panel order must be contiguous and start at 1", project.project_id)
    for scene_id, orders in panel_orders.items():
        if orders != sorted(orders) or len(orders) != len(set(orders)):
            add("blocking", "scene_panel_order", "Panels within a scene must be strictly increasing", scene_id)

    for status_error in project.validate_statuses():
        add("blocking", "status", status_error, project.project_id)

    approved_asset_ids = {item.asset_id for item in project.assets if item.status == "approved"}
    for panel in project.panels:
        if panel.status == "approved" and panel.reference_asset_ids:
            unapproved = set(panel.reference_asset_ids) - approved_asset_ids
            if unapproved:
                add(
                    "warning",
                    "unapproved_reference",
                    f"Approved panel uses unapproved references: {sorted(unapproved)}",
                    panel.panel_id,
                )
    return findings
