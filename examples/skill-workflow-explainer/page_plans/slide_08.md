# slide_08 - 如何使用与验收

## Page Role

Usage and closing.

## Core Message

一个项目目录、三组命令、两份 PPTX，构成可复现交付。

## Content Blocks

1. Project layout: source_digest, requirements, research, outline, sticky_notes, page_plans, svg, previews, exports.
2. Commands: init_project, validate_svg --native-editable, assemble_pptx, inspect_pptx.
3. Outputs: deck_editable.pptx and deck_snapshot.pptx.
4. Final evidence checklist.

## Designer Handoff Draft

- Plain wireframe intent: terminal-style command card plus project tree plus final outputs.
- Exact element placement: project tree left; commands center; outputs/checks right.
- What must be emphasized: validation before completion.
- What may be omitted if crowded: all file names beyond core dirs.
- What should stay visually quiet: decorative code background.

## Evidence To Show

- `SKILL.md` Project Layout and Final Evidence sections.
- `scripts/validate_svg.py`, `scripts/assemble_pptx.py`, `scripts/inspect_pptx.py`.

## Bento Layout Plan

- Canvas: 1280x720
- Grid: asymmetric three-card
- Card A: x=72, y=150, w=350, h=430, purpose=project tree
- Card B: x=454, y=150, w=430, h=430, purpose=commands
- Card C: x=916, y=150, w=292, h=430, purpose=outputs and pass checks
- Card D: x=72, y=604, w=1136, h=62, purpose=closing principle
- Gutters: at least 20px

## Visual Direction

- palette: dark terminal, cyan checks, orange PPTX output
- typography: Noto Sans CJK SC stack plus monospace for commands
- icon/image needs: check badges
- avoid: too much shell text
- reference image/style cue: dashboard status panel

## Speaker Notes Seed

收束到可执行方式：用户照着项目结构和命令，就能验证生成物是否完整、可编辑、可复现。
