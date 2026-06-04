"""NLP pipeline helpers for text-to-visual literary storytelling.

This script turns the original exploratory notebook into a small reusable
command-line workflow:

- load Poe short story data
- clean and tokenize story text
- train a genre classifier
- generate page-level visual prompts for an image model
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


DEFAULT_DATA_PATH = Path("Short_Stories_with_Image_Descriptions.csv")

STOPWORDS = {
    "a",
    "an",
    "and",
    "any",
    "all",
    "are",
    "as",
    "at",
    "be",
    "been",
    "before",
    "but",
    "by",
    "could",
    "did",
    "does",
    "down",
    "each",
    "every",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "him",
    "her",
    "here",
    "his",
    "i",
    "in",
    "into",
    "is",
    "it",
    "its",
    "may",
    "might",
    "more",
    "most",
    "not",
    "now",
    "of",
    "on",
    "one",
    "or",
    "own",
    "she",
    "some",
    "that",
    "the",
    "them",
    "then",
    "these",
    "their",
    "there",
    "they",
    "this",
    "to",
    "upon",
    "very",
    "was",
    "were",
    "which",
    "who",
    "would",
    "with",
}


@dataclass(frozen=True)
class Story:
    title: str
    text: str
    classification: str
    publication_date: str = ""
    first_published_in: str = ""
    image_description: str = ""


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]+", text.lower())
    return [word for word in words if word not in STOPWORDS and len(word) > 2]


def load_stories(path: Path) -> List[Story]:
    if not path.exists():
        raise FileNotFoundError(f"Could not find dataset: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    stories = []
    for row in rows:
        stories.append(
            Story(
                title=clean_text(row.get("title", "")),
                text=clean_text(row.get("text", "")),
                classification=clean_text(row.get("classification", "")),
                publication_date=clean_text(row.get("publication_date", "")),
                first_published_in=clean_text(row.get("first_published_in", "")),
                image_description=clean_text(row.get("image description", "")),
            )
        )
    return stories


def find_story(stories: Iterable[Story], title: str) -> Story:
    target = normalize_title(title)
    for story in stories:
        if normalize_title(story.title) == target:
            return story
    for story in stories:
        if target in normalize_title(story.title):
            return story
    available = ", ".join(story.title for story in list(stories)[:8])
    raise ValueError(f"Could not find story matching {title!r}. Examples: {available}")


def split_into_scene_chunks(text: str, pages: int) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", clean_text(text))
    sentences = [sentence for sentence in sentences if sentence]
    if not sentences:
        return []

    pages = max(1, pages)
    chunk_size = max(1, len(sentences) // pages)
    chunks = []
    for index in range(0, min(len(sentences), chunk_size * pages), chunk_size):
        chunk = " ".join(sentences[index : index + chunk_size])
        chunks.append(chunk)
        if len(chunks) == pages:
            break
    return chunks


def summarize_keywords(text: str, limit: int = 12) -> List[str]:
    counts: dict[str, int] = {}
    for token in tokenize(text):
        counts[token] = counts.get(token, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def build_visual_prompt(story: Story, excerpt: str, page_number: int, use_existing_description: bool = False) -> str:
    keywords = ", ".join(summarize_keywords(excerpt, limit=8))
    tone = story.classification or "literary"
    visual_direction = (
        f"Prior dataset image note: {story.image_description}. "
        if use_existing_description and story.image_description
        else ""
    )
    return (
        f"Page {page_number} visual prompt for {story.title}: "
        f"Create a {tone} scene inspired by Edgar Allan Poe. "
        f"Use the following narrative excerpt as source material: {excerpt[:700]} "
        f"{visual_direction}"
        f"Important motifs/keywords: {keywords}. "
        "Keep the image atmospheric, story-faithful, and consistent with a classic literary adaptation. "
        "Prioritize setting, character continuity, lighting, mood, and narrative tension over decorative details."
    )


def print_prompts(story: Story, pages: int, use_existing_description: bool = False) -> None:
    print(f"Story: {story.title}")
    print(f"Genre label: {story.classification}")
    print(f"Published: {story.publication_date or 'unknown'}")
    print()

    chunks = split_into_scene_chunks(story.text, pages)
    for index, chunk in enumerate(chunks, start=1):
        print(f"--- Prompt {index} ---")
        print(build_visual_prompt(story, chunk, index, use_existing_description))
        print()


def train_genre_classifier(stories: List[Story]) -> None:
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics import classification_report
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
    except ImportError as exc:
        raise RuntimeError("Install scikit-learn first: pip install -r requirements.txt") from exc

    rows = [story for story in stories if story.text and story.classification]
    labels = [story.classification for story in rows]
    common_labels = {label for label in labels if labels.count(label) >= 2}
    rows = [story for story in rows if story.classification in common_labels]

    if len(rows) < 10:
        raise ValueError("Not enough labeled rows to train a classifier.")

    x_train, x_test, y_train, y_test = train_test_split(
        [story.text for story in rows],
        [story.classification for story in rows],
        test_size=0.25,
        random_state=42,
        stratify=[story.classification for story in rows],
    )

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(max_features=1200, stop_words="english", ngram_range=(1, 2))),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions, zero_division=0))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate literary scene prompts and train a Poe story genre classifier.")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH, help="CSV file with Poe story data.")
    parser.add_argument("--story", default="THE MAN OF THE CROWD", help="Story title or partial title to generate prompts for.")
    parser.add_argument("--pages", type=int, default=4, help="Number of visual prompts to generate.")
    parser.add_argument("--train-classifier", action="store_true", help="Train and evaluate a TF-IDF + Random Forest genre classifier.")
    parser.add_argument(
        "--use-existing-description",
        action="store_true",
        help="Include the dataset's existing image description in generated prompts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stories = load_stories(args.data)

    if args.train_classifier:
        train_genre_classifier(stories)
        return

    story = find_story(stories, args.story)
    print_prompts(story, args.pages, args.use_existing_description)


if __name__ == "__main__":
    main()
