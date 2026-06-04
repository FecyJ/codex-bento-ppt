---
name: codex-bento-ppt
description: "Build presentation decks with the Linux.do PPT Agent workflow: source ingestion, requirement consulting, agent-led research, sticky-note outlines, per-slide planning, Bento Grid SVG design, validation, and native editable SVG-to-PPTX export. Use when the user asks for a new PPT, slide deck, presentation, AI PPT workflow, editable PPTX/SVG slides, or wants to replicate the linux.do topic 1782304 approach."
metadata:
  source_url: https://linux.do/t/topic/1782304
  short-description: Bento Grid PPT workflow
---

# Bento PPT Agent Workflow

## Purpose

This skill creates PowerPoint decks through a consultant-style workflow inspired by linux.do topic `1782304`: read the user's raw material, clarify demand, research deeply, plan the deck as sticky notes, produce a page planning draft, generate each page as a full-slide Bento Grid SVG, validate it, then export to PPTX.

Use this for high-quality decks where content logic and slide planning matter. Do not use it for quick template filling, image-only decks, or cases where the user requires real PowerPoint chart data objects or strict corporate template layouts.

## Non-Negotiables

- Start from questions and source context, not from a template.
- When the user provides files, directories, URLs, or pasted source text, perform Source Ingestion before requirement consulting or research.
- Markdown/text reading is required. If the active agent cannot read Markdown or plain text, stop and ask for an environment that can.
- DOCX, PDF, and spreadsheet reading are optional enhancement capabilities. Use the active agent's dedicated document-processing skills/tools first when available; use `scripts/ingest_sources.py` as a normalization and fallback path.
- Use the active agent for every role. If the source workflow names a specific AI product, map that role to the current agent and its available tools.
- Research before outline when the topic is current, market-facing, technical, legal, financial, medical, or otherwise fact-sensitive.
- Treat each slide as one digital sticky note before design. The sticky note must state role, message, evidence, and visual intent.
- Create a planning draft before SVG. The draft fixes what appears where, without decorative polish.
- Generate final pages as SVG with `viewBox="0 0 1280 720"`.
- Use Bento Grid card layouts for content pages unless a slide role clearly calls for another structure.
- Validate every SVG before exporting. Broken, blank, unsafe, wrong-size, or unreadable SVGs must be repaired before assembly.
- Export with `scripts/assemble_pptx.py`. The final deliverable must be a native editable PPTX built from SVG elements, with a snapshot PPTX kept for visual comparison. If native editable export is unavailable, fail with a fix path rather than delivering a flattened substitute. Keep source SVGs with the deck.

## Portability Model

Read `references/agent-portability.md` when running this skill in a new agent environment or when native editable export/document ingestion capability is uncertain.

Minimum required capabilities:

- `read_markdown`: read Markdown or plain text source material directly.
- `run_python`: run the bundled scripts with Python and dependencies from `requirement.txt`.
- `render_svg`: render SVG previews through CairoSVG/Pillow.
- `export_editable_pptx`: convert SVG primitives into native editable PowerPoint elements.

Optional enhancement capabilities:

- `read_docx`, `read_pdf`, `read_xlsx`: extract richer structure, tables, OCR, comments, formulas, charts, and embedded images through environment-specific document tools.
- `extract_images`: gather user-provided and document-embedded images into `source_assets/`.
- `web_research`: browse or search when local material is insufficient or facts may have changed.

When optional document capabilities are absent, continue only if Markdown/text source coverage is enough for the requested deck. Otherwise ask the user to provide Markdown/text exports or extracted source material.

## Workflow

### 0. Source Ingestion

Read `prompts/00-source-ingestion.md`.

Read the user's original material before deciding what the presentation should say. Source material can be a directory, one or more files, URLs, or pasted text. For local directories, scan recursively for supported source files and extract enough structure to understand the topic, coverage, evidence, and reusable visuals.

Priority:

- Markdown/text: required baseline; read directly or through the fallback script.
- DOCX: optional enhancement; use an available DOCX-processing skill/tool first to extract text, tables, and embedded images. If unavailable or insufficient, use the fallback script. Normalize successful related-skill outputs with `extraction_method: docx-skill` or another clear environment-specific method name.
- PDF: optional enhancement; use an available PDF-processing skill/tool first to extract text, tables, page images, embedded images, or OCR when needed. If unavailable or insufficient, use the fallback script. Normalize successful related-skill outputs with `extraction_method: pdf-skill` or another clear environment-specific method name.
- XLSX/XLSM/CSV/TSV: optional enhancement; use an available spreadsheet-processing skill/tool first to inspect sheets, tables, formulas, charts, and embedded images. If unavailable or insufficient, use the fallback script. Normalize successful related-skill outputs with `extraction_method: xlsx-skill` or another clear environment-specific method name.
- User-provided images, SVGs, screenshots, and images extracted by other document skills must be recorded as reusable visual material for later slide planning and design.

For fallback extraction and inventory normalization, run:

```bash
python3 <skill_dir>/scripts/ingest_sources.py <source_path...> --project-dir <project_dir>
```

Supported fallback text extraction formats are Markdown/text, DOCX, PDF, XLSX/XLSM, CSV, and TSV. Images and SVGs are copied into `source_assets/` and recorded. Unsupported files are recorded in the inventory with an extraction warning instead of ignored.

Output:

- `source_inventory.json`
- `source_digest.md`
- `source_assets/` when images or extracted embedded media are available

### 1. Requirement Consulting

Read `references/linuxdo-methodology.md` and `prompts/01-requirement-consultant.md`.

Use `source_digest.md` and `source_inventory.json` as context. Ask only the questions needed to remove real ambiguity. Default questions cover audience, purpose, occasion, page count, tone, must-use material, and forbidden content. If the user already supplied enough context, write the requirement brief without asking.

Output:

- `requirements.md`
- optional `requirements.json`

### 2. Research

Read `prompts/02-researcher.md`.

Start from `source_digest.md`, `source_inventory.json`, and the original local source files. Use web access only when the local material is insufficient, current facts matter, or the user asks for external research. For each planned section, capture source title, URL or file path, date if available, and the takeaway. Do not cite search-result snippets as evidence when a primary source is available.

Output:

- `research.md`
- optional `sources.json`

### 3. Sticky-Note Outline

Read `prompts/03-outline-architect.md`.

Build the deck with the pyramid principle: conclusion first, grouped arguments, logical progression. Represent every slide as a sticky note, not as a polished slide.

Output:

- `outline.json`
- `sticky_notes.md`

Stop for user approval when the user has not already authorized full autonomous generation.

### 4. Page Planning Draft

Read `prompts/04-page-planner.md`.

For each sticky note, define title, main point, evidence, content blocks, visual hierarchy, Bento card allocation, and any image/chart/icon needs. This is the "策划稿" phase; keep it plain and precise.

Output:

- `page_plans/slide_XX.md`

### 5. SVG Design

Read `prompts/05-svg-designer.md`.

Create one SVG per page under `svg/slide_XX.svg`. Each page must be a complete 1280x720 composition. Use `data-role="card"` on Bento card rectangles so validators can detect card structure. Use semantic top-level `<g id="...">` groups for major content units; these become selectable PowerPoint groups and optional animation targets in the native export.

When the user asks to replicate the linux.do article style, inspect `references/source/linuxdo-1782304/article.md` and the archived attachments under `references/source/linuxdo-1782304/images/` before designing. Use them for style cues only; generate new editable SVG primitives rather than tracing or flattening the images.

For the first non-cover content slide, generate a sample and inspect it before continuing. If the style misses the brief, revise the prompt and regenerate the sample before making the rest.

Output:

- `svg/slide_XX.svg`

### 6. Visual Review And Repair

Read `prompts/06-visual-reviewer.md`.

Run:

```bash
python3 <skill_dir>/scripts/validate_svg.py <project_dir>/svg/*.svg --render-dir <project_dir>/previews --json-out <project_dir>/validation.json
```

For decks that will be delivered as editable PowerPoint, add the native conversion dry-run:

```bash
python3 <skill_dir>/scripts/validate_svg.py <project_dir>/svg/*.svg --render-dir <project_dir>/previews --json-out <project_dir>/validation.json --native-editable
```

Inspect the rendered PNG previews. Repair severe issues: blank rendering, bad size, clipped text, incoherent overlap, unreadable contrast, missing required evidence, a page that does not match its sticky note, or a native conversion failure.

### 7. PPTX Assembly

Run:

```bash
python3 <skill_dir>/scripts/assemble_pptx.py <project_dir>/svg <project_dir>/exports/deck_editable.pptx --snapshot-output <project_dir>/exports/deck_snapshot.pptx --title "<deck title>"
```

The primary exported PPTX converts SVG elements into native PowerPoint DrawingML objects, so text, shapes, groups, lines, paths, and images can be selected directly in PowerPoint. The snapshot PPTX embeds each SVG as a full-slide object for visual comparison only. Use `--png-fallback` when the snapshot deck should be rasterized PNG pages.

Default text mode preserves layout: positioned `tspan` lines may become separate PowerPoint text frames. Add `--merge-paragraphs` only when the user explicitly prefers larger editable paragraph boxes and accepts possible PowerPoint text reflow.

Inspect the package:

```bash
python3 <skill_dir>/scripts/inspect_pptx.py <project_dir>/exports/deck_editable.pptx --expect-slides <N> --require-native-editable
python3 <skill_dir>/scripts/inspect_pptx.py <project_dir>/exports/deck_snapshot.pptx --expect-slides <N> --require-svg-media
```

If using LibreOffice as an external open/render check, run conversions serially. Parallel LibreOffice conversions can fail from profile locking and should not be treated as deck corruption without a serial retry.

### 8. Final Evidence

Before calling the deck complete, verify:

- `source_inventory.json` and `source_digest.md` exist when the user provided source material.
- user-provided or extracted images are listed under reusable visual material and stored in `source_assets/` when available.
- `requirements.md`, `research.md`, `outline.json`, and `sticky_notes.md` exist.
- every `page_plans/slide_XX.md` exists for the expected slide count.
- every `svg/slide_XX.svg` validates with the script.
- native editable validation passes for every deliverable SVG.
- previews are nonblank and visually coherent.
- `deck_editable.pptx` exists, has the expected slide count, and contains multiple native editable objects per slide.
- `deck_snapshot.pptx` exists as the visual comparison file.
- sources are listed for factual claims.

## Project Layout

Use this structure:

```text
<project>/
├── source_inventory.json
├── source_digest.md
├── source_assets/
├── requirements.md
├── research.md
├── outline.json
├── sticky_notes.md
├── page_plans/
│   └── slide_01.md
├── svg/
│   └── slide_01.svg
├── previews/
├── exports/
│   ├── deck_editable.pptx
│   └── deck_snapshot.pptx
└── validation.json
```

Initialize it with:

```bash
python3 <skill_dir>/scripts/init_project.py <project_dir> --title "<deck title>"
```

## Reference Map

- `references/agent-portability.md`: capability contracts and environment adapters for non-Codex agents.
- `references/linuxdo-methodology.md`: source-derived methodology, adapted for the active agent.
- `references/source/linuxdo-1782304/article.md`: static local archive of the original linux.do post with local image references.
- `references/source/linuxdo-1782304/manifest.json`: source URL, image metadata, and local paths for the archived attachments.
- `references/source/linuxdo-1782304/prompt-extracts.md`: direct open prompt/code-block extracts from the archived post.
- `prompts/00-source-ingestion.md`: read user-provided raw material.
- `prompts/01-requirement-consultant.md`: demand clarification.
- `prompts/02-researcher.md`: agent research pass.
- `prompts/03-outline-architect.md`: sticky-note outline.
- `prompts/04-page-planner.md`: per-page planning draft.
- `prompts/05-svg-designer.md`: Bento Grid SVG generation.
- `prompts/06-visual-reviewer.md`: review and repair rubric.
- `scripts/init_project.py`: create project folders and manifest.
- `scripts/ingest_sources.py`: scan and extract user-provided raw material.
- `scripts/check_environment.py`: report required and optional runtime capabilities.
- `scripts/ppt_master_bridge.py`: locate and load the native SVG-to-PPTX conversion code.
- `scripts/validate_svg.py`: parse, render, lint, and optionally dry-run native SVG conversion.
- `scripts/assemble_pptx.py`: export SVG pages to native editable PPTX plus a snapshot PPTX.
- `scripts/inspect_pptx.py`: inspect slide count, packaged media, and native editable object counts.
