# slide_05 - 提示词工程：结构架构师 + 研究上下文

## Page Role

Prompt engineering.

## Core Message

大纲必须被研究上下文约束，避免凭空编故事。

## Content Blocks

1. Research packets capture facts, dates, caveats, slide uses.
2. Structure architect uses pyramid principle.
3. Guardrail: outdated or contradicted facts cannot become core recommendations.
4. Output: outline.json and sticky_notes.md.

## Designer Handoff Draft

- Plain wireframe intent: pyramid in center; research context shield on left; output schema card on right.
- Exact element placement: central pyramid 45% width.
- What must be emphasized: context-aware outline.
- What may be omitted if crowded: schema details.
- What should stay visually quiet: code-like micro labels.

## Evidence To Show

- `prompts/02-researcher.md`
- `prompts/03-outline-architect.md`
- `references/source/linuxdo-1782304/prompt-extracts.md`

## Bento Layout Plan

- Canvas: 1280x720
- Grid: main central card plus two side cards
- Card A: x=72, y=164, w=288, h=390, purpose=research context
- Card B: x=388, y=132, w=504, h=454, purpose=pyramid logic
- Card C: x=920, y=164, w=288, h=390, purpose=outputs
- Gutters: at least 20px

## Visual Direction

- palette: dark, cyan shield, violet pyramid, orange output
- typography: Noto Sans CJK SC stack
- icon/image needs: pyramid triangles, guardrail line
- avoid: long code blocks
- reference image/style cue: structured technical explanation

## Speaker Notes Seed

把原帖“顶级 PPT 结构架构师”的提示词思想解释清楚：不是只要 JSON 格式，更重要是调研上下文约束和金字塔原理。
