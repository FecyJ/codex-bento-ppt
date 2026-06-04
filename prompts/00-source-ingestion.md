# Prompt: Codex Source Ingestion

Use this role whenever the user provides raw material: a directory, files, URLs, or pasted text.

## Definition

Source Ingestion means reading the user's original material before deciding the deck's demand, outline, claims, or visuals.

## Mission

Create a reliable map of the raw material so later phases can use concrete source evidence.

## Process

1. Identify all supplied source locations.
2. For local directories, scan recursively for supported material.
3. Extract text and structure from Markdown/text directly.
4. For DOCX, PDF, and spreadsheet files, prefer the dedicated document skills before fallback extraction:
   - DOCX: use `docx` skill for text, tables, tracked-change-aware reading when needed, and embedded images.
   - PDF: use `pdf` skill for text, tables, page images, embedded images, and OCR if the PDF is scanned.
   - XLSX/XLSM/CSV/TSV: use `xlsx` skill for workbook/sheet inspection, formulas, tables, charts, and embedded images.
5. Use `scripts/ingest_sources.py` as fallback and to normalize the inventory/digest.
6. Read user-provided images/SVGs/screenshots and images extracted by document skills as candidate slide assets.
7. Preserve source attribution: path, title, file type, extraction method, and extraction status.
8. Note tables, figures, diagrams, formulas, screenshots, charts, and image assets that may be useful in slides.
9. Summarize the material by topic, not by file order.
10. Record unsupported or failed files with a warning.

## Output

Write `source_inventory.json`:

```json
{
  "sources": [
    {
      "path": "",
      "type": "",
      "title": "",
      "status": "extracted",
      "char_count": 0,
      "topics": [],
      "reusable_assets": [],
      "warnings": []
    }
  ]
}
```

Write `source_digest.md`:

```markdown
# Source Digest

## Source Coverage

- ...

## Main Topics

- ...

## Evidence Candidates

- Claim:
- Source:
- Useful slide:

## Reusable Visual Material

- ...

## Extraction Warnings

- ...
```

## Normalizing Related Skill Outputs

When `docx`, `pdf`, or `xlsx` skill processing succeeds, normalize its outputs into the same project artifacts:

- Set `status` to `extracted`.
- Set `extraction_method` to `docx-skill`, `pdf-skill`, or `xlsx-skill`.
- Put readable text, tables, and source excerpts into `source_digest.md`.
- Copy extracted images, charts, screenshots, or page renders into `source_assets/`.
- List copied assets under the source's `reusable_assets` in `source_inventory.json`.

Use the fallback script only for formats not handled by a related skill, failed related-skill extraction, or final inventory/digest normalization.

## Rules

- Do not invent facts to fill extraction gaps.
- Do not ignore unsupported files.
- Do not discard images just because they are not text sources. Record them as reusable assets, then choose later during page planning.
- If another document skill extracts embedded images, copy or reference those outputs in `source_assets/` and list them in `source_inventory.json`.
- If a source is too long, summarize structure and prioritize sections relevant to the requested presentation.
- Use this digest as the starting context for requirement consulting and research.
