# From Text to Visuals: AI Pipeline for Immersive Storytelling

[![CI](https://github.com/IanRmacdonnell/ai-story-visualization-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/IanRmacdonnell/ai-story-visualization-pipeline/actions/workflows/ci.yml)
[![Case study](https://img.shields.io/badge/live-case_study-8f3e31)](https://ianrmacdonnell.github.io/ai-story-visualization-pipeline/)

**Research and prototype pipeline for turning literary text into visual scene prompts using NLP, genre classification, prompt engineering, and image generation.**

This project grew out of a 31-page research paper exploring how AI could make classic literature more immersive and accessible. Using Edgar Allan Poe's short stories as a test case, the project experiments with a workflow that analyzes narrative text, identifies genre and tone, and produces visual descriptions that can guide image generation.

## At a Glance

| Area | Details |
| --- | --- |
| Project type | NLP and generative AI research prototype |
| Main objective | Explore how literary text can be translated into visual scenes |
| Dataset | 70 Edgar Allan Poe short story records with metadata and image descriptions |
| Core workflow | Text cleaning -> tokenization -> genre classification -> prompt generation -> image generation |
| Tech stack | Python, Jupyter Notebook, scikit-learn, NLP preprocessing, OpenAI-style prompt workflows |
| Best portfolio signal | Combines research writing, machine learning, prompt design, and human-centered AI thinking |

## About / Examples

The project asks a practical question: if a reader struggles to visualize a dense literary scene, can AI help turn the text into a useful visual aid?

Example situations this pipeline supports:

- Convert a short story passage into a concise scene prompt for an image model.
- Classify stories by genre so prompts can preserve tone and visual style.
- Extract useful context such as title, genre, setting, and narrative text.
- Compare how different preprocessing choices affect downstream model performance.
- Discuss limitations such as visual consistency, prompt drift, rate limits, and preserving literary nuance.

## Why I Built It

I wanted to connect two interests: classic literature and AI. The research paper focused on Edgar Allan Poe because his stories are visually rich, emotionally intense, and varied across genres such as horror, satire, detective fiction, adventure, and science fiction.

The larger idea is that AI-generated visuals could support:

- Engagement for readers used to visual media.
- Accessibility for readers who struggle to visualize text.
- New digital reading formats that combine literature and interactive media.
- Better understanding of the limits of text-to-image systems.

## What Is in This Repo

```text
.
|-- Copy_of_Ai_Project_v2.ipynb                 # Original exploratory notebook
|-- src/story_visual_pipeline.py                # Clean reusable pipeline script
|-- Short_Stories_with_Image_Descriptions.csv   # Story data with image descriptions
|-- preprocessed_data.csv                       # Preprocessed story metadata/text
|-- docs/linkedin_project_entry.md              # Portfolio/LinkedIn wording
|-- requirements.txt
`-- .gitignore
```

## Skills Demonstrated

- Natural language processing and text preprocessing.
- Dataset design with story text, metadata, genre labels, and generated image descriptions.
- Classification workflow using TF-IDF features and a Random Forest classifier.
- Prompt engineering for text-to-image generation.
- Research communication through a full-length technical paper.
- Human-centered AI thinking around accessibility, engagement, and creative tools.
- Critical evaluation of model limitations, including consistency across scenes and narrative nuance.

## Run the Clean Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate visual prompts for a story:

```bash
python src/story_visual_pipeline.py --story "THE MAN OF THE CROWD" --pages 4
```

Train and evaluate the genre classifier:

```bash
python src/story_visual_pipeline.py --train-classifier
```

Use a different dataset file:

```bash
python src/story_visual_pipeline.py --data preprocessed_data.csv --story "A DESCENT INTO THE MAELSTROM"
```

## Build a Story Production Benchmark

The provider-neutral production foundation can turn any UTF-8 TXT or Markdown
file into a versioned Story Bible export with semantic scenes, panel plans, and
deterministic continuity findings. It does not require an API key:

```bash
python src/story_production_cli.py path/to/story.txt \
  --title "Story Title" \
  --author "Author Name" \
  --rights-status public_domain \
  --panels 8 \
  --output output/story-production.json
```

Run the standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

The product and startup plan is in [`docs/startup/`](docs/startup/README.md).

The completed public-domain Day-24 benchmark, including its eight-panel visual
storyboard, canonical Story Bible, continuity report, approvals, and decision
review, is in [`benchmarks/man_of_the_crowd/`](benchmarks/man_of_the_crowd/README.md).

## Evaluation and Human Review

Run the canonical benchmark evaluation and generate its review queue:

```bash
python evaluate_story_benchmark.py
```

The report measures source-offset validity, source coverage, entity context, approvals, and blocking continuity findings. It converts unresolved findings, unapproved panels, and missing continuity constraints into prioritized review tasks. This provides a deterministic boundary for a future visual review interface without coupling the story model to an image provider.

## Research Summary

The original research paper explored a pipeline with:

- Text normalization and tokenization.
- Stopword removal and feature extraction.
- Genre classification using machine learning.
- GPT-style summarization and scene description generation.
- DALL-E-style image generation.
- Evaluation of strengths and limitations.

The strongest finding was that AI can generate visuals aligned with a story's tone and setting, but maintaining consistent characters, mood, and narrative continuity across multiple pages remains difficult.

## What I Would Highlight

Resume version:

> Wrote a 31-page research paper and built an NLP/generative AI prototype that analyzes Edgar Allan Poe short stories, classifies genre, generates visual scene prompts, and explores how AI-generated imagery could make literature more immersive and accessible.

Technical version:

> Built a text-to-visual storytelling pipeline using NLP preprocessing, TF-IDF features, Random Forest genre classification, and prompt engineering for image generation workflows.

Product version:

> Explored how AI could support future digital reading experiences by turning dense literary passages into accessible, personalized visual scenes.

## Limitations and Next Steps

- The original notebook is exploratory and research-focused, not a production application.
- Generated visuals can drift across pages when character and setting details are not carried forward.
- The dataset is small and focused on one author, so model results should be interpreted as a prototype.
- Future work could add a web interface, stronger evaluation metrics, richer prompt memory, and modern multimodal models.
