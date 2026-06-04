# Agent Portability

This skill is agent-neutral even though its stable skill name remains `codex-bento-ppt`. The active agent performs every role in the workflow and maps the capabilities below to whatever tools, skills, MCP servers, shell access, or user-provided preprocessing are available in its environment.

## Capability Contract

Required:

- `read_markdown`: read Markdown and plain text files. This is the minimum portable input path.
- `run_python`: execute the bundled Python scripts from this skill directory with dependencies from `requirement.txt`.
- `render_svg`: render SVG to PNG for visual validation.
- `export_editable_pptx`: export SVG primitives to native PowerPoint DrawingML objects. This is required for final delivery.

Optional:

- `read_docx`: extract Word document text, tables, comments/tracked-change context when relevant, and embedded images.
- `read_pdf`: extract PDF text, tables, page images, embedded images, and OCR output for scanned PDFs.
- `read_xlsx`: inspect spreadsheet sheets, tables, formulas, charts, and embedded images.
- `extract_images`: place user-provided and document-extracted images in `source_assets/`.
- `web_research`: search or browse current sources when local material is insufficient or facts may have changed.

## Adapter Rules

- Prefer first-party document skills/tools when the active agent has them. Record successful outputs with an explicit `extraction_method`, such as `docx-skill`, `pdf-tool`, `xlsx-mcp`, or another environment-specific label.
- Use `scripts/ingest_sources.py` for Markdown/text ingestion, asset inventory, and fallback extraction when document-specific tools are unavailable or incomplete.
- If DOCX/PDF/XLSX extraction is unavailable and the deck cannot be produced from Markdown/text coverage alone, ask the user for Markdown/text exports or extracted source material.
- If web research is unavailable, proceed only when local sources are sufficient or the user accepts a local-only deck.
- If `export_editable_pptx` is unavailable, stop. A snapshot or PNG-only PPTX is not a successful final deliverable for this skill.

## Environment Check

Run this before serious work in a new environment:

```bash
python3 <skill_dir>/scripts/check_environment.py
```

The check reports required capabilities, optional document fallback packages, native converter availability, and likely CJK font support. Treat missing required capabilities as blockers and missing optional capabilities as input-format limits.
