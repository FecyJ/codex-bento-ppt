# Source Digest

## Source Coverage

- `SKILL.md` defines the complete workflow: source ingestion, requirement consulting, research, sticky-note outline, page planning, SVG design, visual review, PPTX assembly, and final evidence.
- `references/linuxdo-methodology.md` explains why the skill rejects one-click template generation and instead treats a deck as a consultant plus design-team deliverable.
- `prompts/` contains role-specific operating instructions for each phase.
- `scripts/` contains deterministic helpers for project setup, source extraction, SVG validation, native editable PPTX export, and PPTX inspection.

## Key Takeaways

- The core idea is separation of concerns: content logic is solved before visual design.
- The skill turns every slide into an inspectable planning unit before SVG generation.
- Bento Grid is used because AI can reason about cards, hierarchy, spacing, and information density.
- The export path is no longer a flat SVG picture by default; it converts SVG primitives into editable PowerPoint DrawingML objects.
- Validation is part of the workflow, not an afterthought: SVG rendering and native conversion are checked before the deck is accepted.

## Reusable Evidence

- Main workflow order and non-negotiables: `SKILL.md`.
- Original methodology and style cues: `references/linuxdo-methodology.md`.
- Direct prompt design: `prompts/03-outline-architect.md`, `prompts/04-page-planner.md`, `prompts/05-svg-designer.md`.
- Editable PPTX implementation: `scripts/assemble_pptx.py`, `scripts/ppt_master_bridge.py`, `scripts/inspect_pptx.py`.
