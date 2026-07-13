"""Build the canonical Day-24 benchmark for Poe's The Man of the Crowd."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from continuity import check_continuity
from production_exporter import write_export_bundle
from story_models import (
    Approval,
    Asset,
    Character,
    Event,
    Location,
    PanelSpec,
    Prop,
    Scene,
    SourceEvidence,
    StoryBible,
)
from story_visual_pipeline import find_story, load_stories


STORY_TITLE = "THE MAN OF THE CROWD"
SCENE_START = "As the night deepened, so deepened to me the interest of the scene;"
SCENE_END = "These observations heightened my curiosity, and I resolved to follow the stranger whithersoever he should go."
BENCHMARK_TIMESTAMP = "2026-07-12T21:00:00-07:00"


def evidence(text: str, excerpt: str) -> SourceEvidence:
    start = text.index(excerpt)
    return SourceEvidence(excerpt=excerpt, start_offset=start, end_offset=start + len(excerpt))


def build_story_bible(storyboard: Path | None = None) -> StoryBible:
    story = find_story(load_stories(ROOT / "Short_Stories_with_Image_Descriptions.csv"), STORY_TITLE)
    full_start = story.text.index(SCENE_START)
    full_end = story.text.index(SCENE_END) + len(SCENE_END)
    source_text = story.text[full_start:full_end]

    old_man_intro = (
        "With my brow to the glass, I was thus occupied in scrutinizing the mob, when suddenly there came into view a "
        "countenance (that of a decrepid old man, some sixty-five or seventy years of age,)—a countenance which at once "
        "arrested and absorbed my whole attention, on account of the absolute idiosyncrasy of its expression."
    )
    narrator_reaction = (
        "I felt singularly aroused, startled, fascinated. “How wild a history,” I said to myself, “is written within that bosom!”"
    )
    pursuit_decision = (
        "Hurriedly putting on an overcoat, and seizing my hat and cane, I made my way into the street, and pushed through "
        "the crowd in the direction which I had seen him take; for he had already disappeared."
    )
    old_man_description = (
        "He was short in stature, very thin, and apparently very feeble. His clothes, generally, were filthy and ragged; "
        "but as he came, now and then, within the strong glare of a lamp, I perceived that his linen, although dirty, was "
        "of beautiful texture; and my vision deceived me, or, through a rent in a closely-buttoned and evidently second-handed "
        "roquelaire which enveloped him, I caught a glimpse both of a diamond and of a dagger."
    )

    project = StoryBible(
        project_id="story_the_man_of_the_crowd_day24",
        title="The Man of the Crowd — Coffeehouse Encounter",
        author="Edgar Allan Poe",
        rights_status="public_domain",
        source_text=source_text,
        source_version=hashlib.sha256(story.text.encode("utf-8")).hexdigest(),
        tone=["gothic", "psychological", "urban", "mysterious"],
        themes=["anonymity", "obsession", "the unknowability of others", "the modern crowd"],
        visual_style=(
            "Cinematic historical graphic novel realism; 1840 London; smoky amber gaslight against blue-black rain; "
            "fine ink texture; restrained color; expressive but anatomically natural faces"
        ),
        forbidden_changes=[
            "Do not modernize clothing, architecture, lighting, or props",
            "Do not reveal a definitive supernatural identity for the old man",
            "Do not romanticize the pursuit",
            "Keep the narrator visually distinct from the old man",
        ],
    )

    project.characters = [
        Character(
            character_id="char_narrator",
            canonical_name="The Narrator",
            role="Convalescent observer who becomes an obsessive pursuer",
            physical_traits=["adult man", "pale from recent illness", "dark 1840s overcoat", "hat and cane"],
            immutable_traits=["observant", "physically recovering", "never presented as omniscient"],
            allowed_variations=["seated in coffeehouse", "overcoat and hat in street", "handkerchief at mouth in rain"],
            evidence=[evidence(source_text, narrator_reaction), evidence(source_text, pursuit_decision)],
            status="approved",
        ),
        Character(
            character_id="char_old_man",
            canonical_name="The Old Man",
            aliases=["the stranger", "the man of the crowd"],
            role="Enigmatic figure whose expression compels the narrator to follow",
            physical_traits=[
                "sixty-five or seventy years old",
                "short, very thin, apparently feeble",
                "filthy ragged outer clothing",
                "fine but dirty linen",
                "closely buttoned second-hand roquelaire",
                "diamond and dagger glimpsed through a tear",
            ],
            immutable_traits=["unreadable contradictory expression", "physically slight", "period-accurate clothing"],
            allowed_variations=["face caught in gaslight", "partly hidden by crowd", "seen from behind during pursuit"],
            evidence=[evidence(source_text, old_man_intro), evidence(source_text, old_man_description)],
            status="approved",
        ),
    ]

    project.locations = [
        Location(
            location_id="loc_coffeehouse_window",
            canonical_name="D—— Coffee-House Bow Window",
            visual_traits=["large bow window", "smoky panes", "warm interior", "newspaper and cigar", "crowded London street beyond"],
            landmarks=["bow window", "street-facing table", "gas lamps outside"],
            evidence=[evidence(source_text, SCENE_START)],
            status="approved",
        ),
        Location(
            location_id="loc_london_thoroughfare",
            canonical_name="London Thoroughfare at Night",
            visual_traits=["dense crowd", "gas lamps", "humid fog", "wet stone", "blue-black night"],
            landmarks=["coffeehouse frontage", "continuous streams of pedestrians"],
            status="approved",
        ),
    ]

    project.props = [
        Prop("prop_newspaper", "Newspaper", owner_character_id="char_narrator", current_location_id="loc_coffeehouse_window", status="approved"),
        Prop("prop_cigar", "Cigar", owner_character_id="char_narrator", current_location_id="loc_coffeehouse_window", status="approved"),
        Prop("prop_hat", "Narrator's Hat", owner_character_id="char_narrator", continuity_important=True, status="approved"),
        Prop("prop_cane", "Narrator's Cane", owner_character_id="char_narrator", continuity_important=True, status="approved"),
        Prop("prop_diamond", "Hidden Diamond", owner_character_id="char_old_man", continuity_important=True, status="approved"),
        Prop("prop_dagger", "Hidden Dagger", owner_character_id="char_old_man", continuity_important=True, status="approved"),
    ]

    scene_specs = [
        (
            "scene_001",
            "The narrator studies the nighttime crowd through the coffeehouse window.",
            SCENE_START,
            old_man_intro,
            "Observe the crowd until one face breaks the pattern.",
            "The crowd is visually overwhelming and anonymous.",
            "Detached fascination becomes personal fixation.",
            ["char_narrator"],
            "loc_coffeehouse_window",
        ),
        (
            "scene_002",
            "The old man's contradictory expression arrests the narrator's attention.",
            old_man_intro,
            narrator_reaction,
            "Understand the stranger's unreadable history.",
            "The face suggests mutually incompatible qualities and resists interpretation.",
            "Curiosity becomes startled obsession.",
            ["char_narrator", "char_old_man"],
            "loc_coffeehouse_window",
        ),
        (
            "scene_003",
            "The narrator enters the street and discovers the stranger's hidden signs of wealth and violence.",
            pursuit_decision,
            SCENE_END,
            "Keep the old man in view and learn who he is.",
            "The crowd conceals him while his appearance creates deeper contradictions.",
            "Observation becomes action and pursuit.",
            ["char_narrator", "char_old_man"],
            "loc_london_thoroughfare",
        ),
    ]
    for order, (scene_id, summary, start_phrase, end_phrase, objective, conflict, turn, chars, location) in enumerate(scene_specs, 1):
        start = source_text.index(start_phrase)
        end = source_text.index(end_phrase) + len(end_phrase)
        project.scenes.append(
            Scene(
                scene_id=scene_id,
                order=order,
                summary=summary,
                source=SourceEvidence(source_text[start:end], start, end),
                objective=objective,
                conflict=conflict,
                emotional_turn=turn,
                character_ids=chars,
                location_id=location,
                required_information=[summary],
                status="approved",
            )
        )

    panel_rows = [
        ("scene_001", SCENE_START, "All was dark yet splendid—as that ebony to which has been likened the style of Tertullian.", "Establish the gaslit London crowd and the narrator framed behind glass.", ["char_narrator"], "loc_coffeehouse_window", ["prop_newspaper", "prop_cigar"], "establishing", "high_angle"),
        ("scene_001", "The wild effects of the light enchained me to an examination of individual faces;", "the history of long years.", "Move from the anonymous crowd toward individual faces under flickering gaslight.", ["char_narrator"], "loc_coffeehouse_window", [], "wide", "eye_level"),
        ("scene_002", old_man_intro, "Any thing even remotely resembling that expression I had never seen before.", "Reveal the old man's face for the first time through the moving crowd.", ["char_old_man"], "loc_london_thoroughfare", [], "close_up", "eye_level"),
        ("scene_002", "As I endeavored, during the brief minute of my original survey,", "of intense—of supreme despair.", "Show contradictory emotions crossing the old man's face without resolving his identity.", ["char_old_man"], "loc_london_thoroughfare", [], "extreme_close_up", "eye_level"),
        ("scene_002", narrator_reaction, "Then came a craving desire to keep the man in view—to know more of him.", "Return to the narrator as fascination becomes an irresistible need to follow.", ["char_narrator"], "loc_coffeehouse_window", ["prop_newspaper"], "close_up", "eye_level"),
        ("scene_003", pursuit_decision, "With some little difficulty I at length came within sight of him,", "The narrator throws on his coat, takes hat and cane, and enters the crowd.", ["char_narrator", "char_old_man"], "loc_london_thoroughfare", ["prop_hat", "prop_cane"], "dynamic_wide", "low_angle"),
        ("scene_003", "I had now a good opportunity of examining his person.", "of beautiful texture;", "Follow behind the old man and contrast ragged outer clothes with fine linen in gaslight.", ["char_narrator", "char_old_man"], "loc_london_thoroughfare", [], "medium", "over_shoulder"),
        ("scene_003", "and my vision deceived me, or, through a rent", SCENE_END, "End on the fleeting diamond and dagger beneath the torn roquelaire as the pursuit continues.", ["char_old_man"], "loc_london_thoroughfare", ["prop_diamond", "prop_dagger"], "detail", "low_angle"),
    ]
    for order, (scene_id, start_phrase, end_phrase, purpose, chars, location, props, shot, angle) in enumerate(panel_rows, 1):
        start = source_text.index(start_phrase)
        end = source_text.index(end_phrase) + len(end_phrase)
        project.panels.append(
            PanelSpec(
                panel_id=f"panel_{order:03d}",
                scene_id=scene_id,
                order=order,
                source=SourceEvidence(source_text[start:end], start, end),
                story_purpose=purpose,
                character_ids=chars,
                location_id=location,
                prop_ids=props,
                shot=shot,
                camera_angle=angle,
                subject_action=purpose,
                lighting="Flickering amber gaslight, smoky interior or blue-black wet street as appropriate",
                reference_asset_ids=["asset_storyboard_day24"] if storyboard else [],
                continuity_constraints=[
                    "1840 London only",
                    "Narrator and old man must remain visually distinct",
                    "Old man's roquelaire, fine dirty linen, diamond, and dagger remain canonical",
                ],
                status="approved" if storyboard else "needs_review",
            )
        )

    project.events = [
        Event("event_001", 1, "Narrator observes the nighttime crowd.", ["char_narrator"], "loc_coffeehouse_window"),
        Event("event_002", 2, "The old man's face arrests the narrator's attention.", ["char_narrator", "char_old_man"], "loc_london_thoroughfare"),
        Event("event_003", 3, "Narrator leaves the coffeehouse and begins following.", ["char_narrator", "char_old_man"], "loc_london_thoroughfare", {"char_narrator": "pursuing"}),
        Event("event_004", 4, "Diamond and dagger are glimpsed beneath the old man's coat.", ["char_old_man"], "loc_london_thoroughfare", {"char_old_man": "more mysterious"}),
    ]

    if storyboard:
        storyboard = storyboard.resolve()
        asset = Asset(
            asset_id="asset_storyboard_day24",
            asset_type="eight_panel_storyboard",
            uri=storyboard.relative_to(ROOT).as_posix(),
            entity_ids=["char_narrator", "char_old_man", "loc_coffeehouse_window", "loc_london_thoroughfare"],
            provider="OpenAI built-in image generation",
            model="built-in",
            prompt="See benchmarks/man_of_the_crowd/visual-direction.md",
            settings={"panels": 8, "orientation": "portrait", "human_review": True},
            file_hash=hashlib.sha256(storyboard.read_bytes()).hexdigest(),
            status="approved",
            created_at=BENCHMARK_TIMESTAMP,
        )
        project.assets.append(asset)
        project.approvals.extend(
            [
                Approval("approval_story_bible", "story_bible", project.project_id, 1, "approved", "prototype_team", "Canonical public-domain benchmark.", BENCHMARK_TIMESTAMP),
                Approval("approval_panel_plan", "panel_plan", "panels_001_008", 1, "approved", "prototype_team", "Faithful adaptation of the coffeehouse encounter.", BENCHMARK_TIMESTAMP),
                Approval("approval_storyboard", "asset", asset.asset_id, 1, "approved", "prototype_team", "Approved as benchmark storyboard, not final publication art.", BENCHMARK_TIMESTAMP),
            ]
        )
    return project


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "benchmarks/man_of_the_crowd/day24-production-bundle.json")
    args = parser.parse_args()
    project = build_story_bible(args.storyboard)
    findings = check_continuity(project)
    output = write_export_bundle(project, findings, args.output)
    report = {
        "project_id": project.project_id,
        "scenes": len(project.scenes),
        "panels": len(project.panels),
        "assets": len(project.assets),
        "approvals": len(project.approvals),
        "findings": len(findings),
        "blocking_findings": sum(item.severity == "blocking" for item in findings),
        "output": output.relative_to(ROOT).as_posix(),
    }
    (output.parent / "day24-review.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
