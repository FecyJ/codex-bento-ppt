# Prompt: Codex Visual Reviewer

Use this after generating SVG pages and before PPTX assembly.

## Review Rubric

For each slide, inspect the SVG source and rendered preview.

Mark as `pass`, `repair`, or `regenerate`.

## Must Repair

- wrong canvas size
- XML parse error
- blank or nearly blank render
- unsafe SVG elements
- remote images that will not package reliably
- text visibly clipped or overlapping
- card grid lacks hierarchy
- content contradicts research or sticky note
- required image, metric, or evidence is missing
- color contrast is unreadable

## Acceptable

- minor copy edits
- small spacing refinements
- optional decorative changes

## Output

Write a short QA note per slide:

```markdown
## slide_XX

- status:
- evidence:
- fixes made:
- residual risk:
```
