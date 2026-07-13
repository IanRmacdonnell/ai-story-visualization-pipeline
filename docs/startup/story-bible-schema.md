# Story Bible and Production Schema

The Story Bible is the canonical memory layer used by every format. Images, comics, video, animation, games, and future film assets should reference the same stable entities.

## Top-Level Project

```json
{
  "project_id": "story_001",
  "title": "Example Story",
  "source": {
    "author": "Author Name",
    "rights_status": "public_domain|licensed|internal_test",
    "source_version": "sha256-or-version",
    "language": "en"
  },
  "creative_direction": {
    "tone": [],
    "themes": [],
    "visual_style": "",
    "palette": [],
    "cinematography_rules": [],
    "forbidden_changes": []
  },
  "characters": [],
  "locations": [],
  "props": [],
  "events": [],
  "scenes": [],
  "assets": [],
  "approvals": []
}
```

## Character

Required fields:

- `character_id`: stable identifier;
- `canonical_name` and aliases;
- narrative role;
- age range and physical traits;
- personality and mannerisms;
- relationships;
- default and scene-specific clothing;
- injuries or state changes with timeline positions;
- visual reference asset IDs;
- immutable traits and allowed variations;
- source evidence and approval status.

## Location

Required fields:

- `location_id` and canonical name;
- geography and spatial relationships;
- architecture, materials, weather, lighting, and time rules;
- recurring landmarks and props;
- visual reference asset IDs;
- scene appearances;
- source evidence and approval status.

## Prop

Required fields:

- `prop_id`, name, owner, appearance, and function;
- location and custody across the timeline;
- state changes;
- visual references;
- continuity importance.

## Event and Timeline

Each event records:

- `event_id`;
- story time and ordering constraints;
- participants;
- location;
- actions and consequences;
- entity state changes;
- source excerpt and offsets.

## Semantic Scene

Each scene records:

- `scene_id`;
- source start/end offsets;
- summary;
- objective and conflict;
- emotional turn;
- participating entity IDs;
- required story information;
- time and location;
- preceding/following scene IDs;
- adaptation status and approval.

## Panel Specification

```json
{
  "panel_id": "panel_001",
  "scene_id": "scene_001",
  "order": 1,
  "source_excerpt": "",
  "story_purpose": "",
  "characters": ["char_001"],
  "location": "loc_001",
  "props": [],
  "composition": {
    "shot": "medium",
    "camera_angle": "eye_level",
    "subject_action": "",
    "lighting": "",
    "palette": []
  },
  "dialogue": [],
  "narration": [],
  "reference_asset_ids": [],
  "continuity_constraints": [],
  "status": "draft"
}
```

## Asset and Provenance

Every generated or uploaded asset records:

- stable `asset_id`;
- entity, scene, and panel relationships;
- provider and model version;
- prompt and negative constraints;
- reference asset IDs and generation settings;
- created timestamp, duration, and estimated cost;
- candidate, approved, rejected, or superseded status;
- reviewer and revision reason;
- file hash and storage location.

## Continuity Finding

A finding contains:

- severity: info, warning, or blocking;
- rule ID;
- affected entity/panel/scene;
- expected and observed values;
- source and Story Bible evidence;
- suggested correction;
- resolution and approver.

## Approval

Approvals are append-only production records:

- object type and ID;
- object version;
- decision;
- reviewer;
- timestamp;
- comment;
- superseding approval, if any.

## Minimum Deterministic Checks

- referenced IDs exist;
- scenes follow valid chronology;
- characters are not present before introduction or after confirmed death without an exception;
- clothing and injuries match the timeline;
- required props are in the correct custody/location;
- panels cite source excerpts;
- blocking Story Bible fields are approved before final export;
- only approved assets appear in a final package.
