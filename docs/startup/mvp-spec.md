# MVP Specification: Consistent Illustrated Chapter

## Objective

Demonstrate that one written story chapter can become a coherent, human-approved 8–15-panel visual adaptation with measurable character, world, and narrative consistency.

## Primary User

An independent author adapting one chapter of a short story or web novel.

## Core User Journey

1. Create a project and import plain text or Markdown.
2. Review extracted characters, locations, props, timeline events, and tone.
3. Correct and approve the Story Bible.
4. Select a chapter or scene for adaptation.
5. Review scene beats and proposed panels.
6. Approve reference sheets and visual rules.
7. Generate or attach panel candidates.
8. Review continuity warnings.
9. Approve, reject, reorder, or revise panels.
10. Export a vertical comic or image package with production metadata.

## Functional Requirements

### Source and structure

- import TXT and Markdown;
- preserve the original source text and offsets;
- split text by semantic scenes/beats rather than equal sentence counts;
- attach every scene and panel to source excerpts.

### Story Bible

- stable IDs for all characters, locations, props, organizations, and events;
- editable canonical attributes;
- relationships and chronology;
- visual rules and forbidden changes;
- version history and approval status.

### Adaptation planning

- scene objective, conflict, emotional turn, and required information;
- panel-level composition, action, dialogue, narration, camera, lighting, and references;
- panel order and source coverage;
- explicit deviations from the source requiring approval.

### Visual assets

- reference assets attached by stable ID;
- candidate and approved asset states;
- prompt, model/provider, model version, seed/reference settings, timestamp, and cost metadata;
- provider-neutral asset interface.

### Continuity

- rules for identity, age, clothing, injuries, props, locations, time of day, and chronology;
- automated warnings with severity and evidence;
- human resolution: fix, accept exception, or mark false positive.

### Approval and export

- draft, needs-review, approved, rejected, and superseded states;
- comments and revision reason;
- export selected approved panels as PNG/ZIP;
- export structured project JSON and a simple web reading manifest.

## Architecture Boundary

The existing Python pipeline remains the research core. Add provider-neutral domain modules before adding a full web application:

- `story_bible.py`: schemas, validation, and versioning;
- `scene_planner.py`: semantic beats and panel specifications;
- `continuity.py`: deterministic rules and report;
- `production.py`: assets, jobs, provenance, and approval states;
- `exporter.py`: project JSON and reading-package export.

A later web layer can use React/Next.js, FastAPI, Postgres, object storage, and a background job queue. The MVP should avoid infrastructure that does not improve the demonstration.

## Evaluation Rubric

### Story fidelity

- important characters and locations are represented correctly;
- panels cover the selected scene’s essential beats;
- invented details do not contradict canon.

### Visual continuity

- recurring character identity remains recognizable;
- clothing, props, time, injuries, and environment remain coherent;
- reference usage is recorded.

### Workflow usefulness

- an author can correct extracted information;
- an author understands why a warning appeared;
- an author can approve or revise every creative decision.

### Efficiency

Track:

- minutes from import to panel plan;
- minutes of human correction;
- generation attempts per approved panel;
- estimated cost per approved panel/chapter;
- percentage of panels passing continuity review;
- author and reader satisfaction.

## Definition of Done

The MVP is complete when one Poe story can produce:

- a valid editable Story Bible;
- at least three semantic scenes;
- one approved 8–15-panel adaptation plan;
- reference-linked panel records;
- a continuity report;
- an approval history;
- a reproducible export bundle.

Live image generation is useful but not required to validate the structure. Placeholder or manually supplied assets may be used until API credentials and a provider are deliberately selected.
