"""Provider-neutral domain models for story-to-visual production.

These models deliberately contain no image or language model integration. They
form the canonical memory layer that future providers must read and update.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


VALID_STATUSES = {"draft", "needs_review", "approved", "rejected", "superseded"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SourceEvidence:
    excerpt: str
    start_offset: int
    end_offset: int

    def validate(self, source_text: str) -> List[str]:
        errors: List[str] = []
        if not (0 <= self.start_offset <= self.end_offset <= len(source_text)):
            errors.append("source evidence offsets are outside the source text")
        elif source_text[self.start_offset : self.end_offset] != self.excerpt:
            errors.append("source evidence excerpt does not match its offsets")
        return errors


@dataclass
class Character:
    character_id: str
    canonical_name: str
    aliases: List[str] = field(default_factory=list)
    role: str = ""
    physical_traits: List[str] = field(default_factory=list)
    immutable_traits: List[str] = field(default_factory=list)
    allowed_variations: List[str] = field(default_factory=list)
    reference_asset_ids: List[str] = field(default_factory=list)
    evidence: List[SourceEvidence] = field(default_factory=list)
    status: str = "draft"


@dataclass
class Location:
    location_id: str
    canonical_name: str
    visual_traits: List[str] = field(default_factory=list)
    landmarks: List[str] = field(default_factory=list)
    reference_asset_ids: List[str] = field(default_factory=list)
    evidence: List[SourceEvidence] = field(default_factory=list)
    status: str = "draft"


@dataclass
class Prop:
    prop_id: str
    canonical_name: str
    owner_character_id: Optional[str] = None
    current_location_id: Optional[str] = None
    visual_traits: List[str] = field(default_factory=list)
    continuity_important: bool = False
    evidence: List[SourceEvidence] = field(default_factory=list)
    status: str = "draft"


@dataclass
class Event:
    event_id: str
    order: int
    summary: str
    participant_ids: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    state_changes: Dict[str, str] = field(default_factory=dict)
    evidence: Optional[SourceEvidence] = None


@dataclass
class Scene:
    scene_id: str
    order: int
    summary: str
    source: SourceEvidence
    objective: str = ""
    conflict: str = ""
    emotional_turn: str = ""
    character_ids: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    required_information: List[str] = field(default_factory=list)
    status: str = "draft"


@dataclass
class PanelSpec:
    panel_id: str
    scene_id: str
    order: int
    source: SourceEvidence
    story_purpose: str
    character_ids: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    prop_ids: List[str] = field(default_factory=list)
    shot: str = "medium"
    camera_angle: str = "eye_level"
    subject_action: str = ""
    lighting: str = ""
    dialogue: List[str] = field(default_factory=list)
    narration: List[str] = field(default_factory=list)
    reference_asset_ids: List[str] = field(default_factory=list)
    continuity_constraints: List[str] = field(default_factory=list)
    status: str = "draft"


@dataclass
class Asset:
    asset_id: str
    asset_type: str
    uri: str
    entity_ids: List[str] = field(default_factory=list)
    scene_id: Optional[str] = None
    panel_id: Optional[str] = None
    provider: str = "manual"
    model: str = ""
    model_version: str = ""
    prompt: str = ""
    reference_asset_ids: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    estimated_cost_usd: float = 0.0
    file_hash: str = ""
    status: str = "draft"
    created_at: str = field(default_factory=utc_now)


@dataclass
class ContinuityFinding:
    finding_id: str
    severity: str
    rule_id: str
    message: str
    object_id: str
    expected: str = ""
    observed: str = ""
    resolution: str = "open"


@dataclass
class Approval:
    approval_id: str
    object_type: str
    object_id: str
    object_version: int
    decision: str
    reviewer: str
    comment: str = ""
    created_at: str = field(default_factory=utc_now)


@dataclass
class StoryBible:
    project_id: str
    title: str
    author: str
    rights_status: str
    source_text: str
    source_version: str
    schema_version: str = "1.0"
    tone: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    visual_style: str = ""
    forbidden_changes: List[str] = field(default_factory=list)
    characters: List[Character] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    props: List[Prop] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    panels: List[PanelSpec] = field(default_factory=list)
    assets: List[Asset] = field(default_factory=list)
    approvals: List[Approval] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def entity_ids(self) -> set[str]:
        return {
            *(item.character_id for item in self.characters),
            *(item.location_id for item in self.locations),
            *(item.prop_id for item in self.props),
            *(item.event_id for item in self.events),
            *(item.scene_id for item in self.scenes),
            *(item.panel_id for item in self.panels),
            *(item.asset_id for item in self.assets),
        }

    def validate_statuses(self) -> List[str]:
        errors: List[str] = []
        for kind, items in (
            ("character", self.characters),
            ("location", self.locations),
            ("prop", self.props),
            ("scene", self.scenes),
            ("panel", self.panels),
            ("asset", self.assets),
        ):
            for item in items:
                if item.status not in VALID_STATUSES:
                    errors.append(f"{kind} has invalid status: {item.status}")
        return errors

