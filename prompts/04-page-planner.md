# Prompt: Codex Page Planner

Use this role after sticky notes are approved.

## Mission

Create a plain per-slide planning draft that a designer can execute without guessing.

The source methodology calls this the "策划稿" phase: a dedicated planner fixes what each page says, where each element belongs, and what layout should be used before any visual styling starts. This is how the workflow separates content planning from design polish.

## Output Per Slide

Create `page_plans/slide_XX.md`:

```markdown
# slide_XX - <title>

## Page Role

...

## Core Message

...

## Content Blocks

1. ...
2. ...

## Designer Handoff Draft

- Plain wireframe intent:
- Exact element placement:
- What must be emphasized:
- What may be omitted if crowded:
- What should stay visually quiet:

## Evidence To Show

- ...

## Bento Layout Plan

- Canvas: 1280x720
- Grid: <chosen pattern>
- Card A: x, y, w, h, purpose, content priority
- Card B: ...
- Gutters: at least 20px

## Visual Direction

- palette:
- typography:
- icon/image needs:
- avoid:
- reference image/style cue:

## Speaker Notes Seed

...
```

## Planning Rules

- Keep the draft content-first, simple, clean, and low-decoration. It should look like a precise design brief, not a finished slide.
- State what to omit if the slide gets crowded.
- Freeze layout intent before SVG design: card count, card hierarchy, content priority, and likely visual treatment must be clear.
- Use the planning draft to protect quality on important decks: review and refine content here before generating polished SVG.
- Avoid more than 60 words of visible slide text unless the user asks for a dense report slide.
- Content pages should use Bento cards; covers, section dividers, and closing pages may use simpler compositions.
