# Day 1–24 Execution Plan

This is a sequence of work units, not a requirement to wait 24 calendar days. Multiple units can be completed in one sustained sprint when dependencies allow.

## Phase 1 — Product and Canon (Days 1–3)

### Day 1: Lock the wedge

Deliverables:

- primary customer: independent author;
- product: one consistent illustrated pilot chapter;
- test story: one public-domain Poe story;
- written non-goals.

Acceptance: the product can be explained in one sentence without mentioning movies.

### Day 2: Define success and evaluation

Deliverables:

- story-fidelity rubric;
- visual-continuity rubric;
- author workflow metrics;
- cost and time tracking fields.

Acceptance: every test result can be recorded as a number, decision, or documented observation.

### Day 3: Define the canonical Story Bible

Deliverables:

- project, character, location, prop, event, scene, panel, asset, finding, and approval schemas;
- stable ID rules;
- source evidence requirements.

Acceptance: a project can be represented without relying on information hidden in a prompt or chat.

## Phase 2 — Source and Story Understanding (Days 4–10)

### Day 4: Source import

Preserve original text, encoding, version/hash, paragraphs, and offsets.

### Day 5: Entity extraction contract

Define required and optional fields for characters, locations, props, organizations, and aliases.

### Day 6: Timeline contract

Define events, ordering constraints, participant state changes, and uncertainty.

### Day 7: Semantic scene segmentation

Replace equal sentence chunks with scene/beat boundaries using location, time, participants, objective, conflict, and emotional change.

### Day 8: Evidence linking

Attach each extracted claim to a source excerpt and offsets.

### Day 9: Human correction workflow

Support draft, needs-review, approved, rejected, and superseded information.

### Day 10: Story Bible validation

Add deterministic validation for missing IDs, broken references, impossible chronology, and incomplete required fields.

Phase acceptance:

- one Poe story imports reproducibly;
- extracted structures are editable;
- every canonical claim cites the source;
- validation produces a clear report.

## Phase 3 — Adaptation and Visual Planning (Days 11–17)

### Day 11: Select adaptation scene

Choose one visually strong, self-contained scene and record why it was selected.

### Day 12: Scene adaptation brief

Record objective, conflict, emotional turn, must-preserve information, allowed compression, and prohibited changes.

### Day 13: Panel decomposition

Produce 8–15 ordered panel specifications with purpose and source coverage.

### Day 14: Character reference requirements

Define identity anchors, immutable traits, allowed variation, clothing, expression range, and reference views.

### Day 15: Location and prop references

Define spatial layout, landmarks, lighting states, recurring objects, and continuity-sensitive props.

### Day 16: Visual direction

Lock tone, visual style, palette, camera language, aspect ratio, lettering assumptions, and prohibited aesthetics.

### Day 17: Prompt/asset production contract

Define provider-neutral requests and save provider, model, prompt, references, settings, time, cost, and output hash.

Phase acceptance:

- every panel references canonical entity IDs;
- every visual constraint exists in structured data;
- the same panel plan can be sent to different generation providers;
- the author can approve the adaptation before assets are produced.

## Phase 4 — Production, Continuity, and Approval (Days 18–24)

### Day 18: Candidate asset workflow

Create candidate, approved, rejected, and superseded asset states.

### Day 19: Identity continuity

Check character reference usage, canonical traits, age/state, and scene-specific clothing.

### Day 20: World continuity

Check location, lighting/time, prop custody, injuries, weather, and chronology.

### Day 21: Narrative continuity

Check panel order, source coverage, dialogue attribution, required story information, and unapproved inventions.

### Day 22: Human review workflow

Record reviewer decisions, comments, revision reasons, accepted exceptions, and superseding approvals.

### Day 23: Export package

Export approved panels, reading order, original excerpts, Story Bible, continuity report, and production provenance.

### Day 24: Benchmark and decision review

Run the complete workflow on the selected Poe scene and record:

- extraction corrections;
- continuity pass rate;
- human review time;
- attempts per approved panel;
- estimated cost;
- reader and author feedback;
- blockers and next backlog.

Phase acceptance:

- one 8–15-panel chapter plan is exportable;
- no blocking continuity findings remain unresolved;
- all final assets are approved and traceable;
- the team has a written continue/change/pause decision.

## Validation Sprint After Day 24

Recruit:

- 3–5 independent authors for interviews;
- 10 readers for text-only versus illustrated comparison;
- one author willing to discuss a limited pilot license.

Do not claim product-market fit. Look for evidence that authors value creative control and will contribute a story, time, money, or distribution.

## Go/No-Go Thresholds

Continue or iterate when:

- at least three authors confirm the problem;
- at least one author agrees to a controlled pilot;
- readers understand and enjoy the illustrated format;
- most panels pass continuity with manageable human correction;
- costs and review time suggest a credible paid pilot.

Change the wedge when authors like the output but will not pay or license.

Pause expansion when continuity requires studio-level manual work, rights cannot be secured, or reader engagement does not improve.

## Immediate Next Build Order

1. Implement schema classes and validators.
2. Replace equal sentence chunking with semantic scene records.
3. Generate a deterministic panel plan from one scene.
4. Add continuity rules and approval states.
5. Export the complete structured project.
6. Only then connect a live image provider and create final visual candidates.
