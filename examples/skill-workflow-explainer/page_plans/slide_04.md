# slide_04 - Source Ingestion：先读材料，再谈需求

## Page Role

Implementation detail.

## Core Message

用户材料、嵌入图片和表格先被归档，后续决策都回到证据。

## Content Blocks

1. Inputs: Markdown/text, DOCX, PDF, XLSX/CSV, images.
2. Priority: dedicated skills first, fallback script second.
3. Outputs: source_inventory.json, source_digest.md, source_assets/.
4. Benefit: reduce hallucination and preserve reusable visuals.

## Designer Handoff Draft

- Plain wireframe intent: input cards feed into three output cards.
- Exact element placement: left input stack, center processing bridge, right outputs.
- What must be emphasized: docx/pdf/xlsx skill priority and image asset pool.
- What may be omitted if crowded: CSV/TSV details.
- What should stay visually quiet: file icons.

## Evidence To Show

- `prompts/00-source-ingestion.md`
- `scripts/ingest_sources.py`

## Bento Layout Plan

- Canvas: 1280x720
- Grid: asymmetric main/support split
- Card A: x=72, y=152, w=365, h=420, purpose=input types
- Card B: x=468, y=152, w=344, h=420, purpose=priority routing
- Card C: x=844, y=152, w=364, h=420, purpose=normalized outputs
- Card D: x=72, y=604, w=1136, h=62, purpose=why it matters
- Gutters: at least 20px

## Visual Direction

- palette: teal inputs, violet routing, orange outputs
- typography: Noto Sans CJK SC stack
- icon/image needs: document chips and arrows
- avoid: actual file screenshots
- reference image/style cue: dashboard flow cards

## Speaker Notes Seed

解释为什么第 0 阶段很重要：先把材料读清楚，后面才有资格做需求判断和内容取舍。
