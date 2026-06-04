# Final Evidence

## Artifacts

- Editable PPTX: `exports/deck_editable.pptx`
- Snapshot PPTX: `exports/deck_snapshot.pptx`
- SVG source pages: `svg/slide_01.svg` through `svg/slide_08.svg`
- PNG previews: `previews/slide_01.png` through `previews/slide_08.png`
- Validation report: `validation.json`

## Validation

Command:

```bash
python3 ../../scripts/validate_svg.py svg/*.svg --render-dir previews --json-out validation.json --native-editable
```

Result:

- total slides: 8
- passed: 8
- warnings: 0
- failed: 0
- native editable dry-run: passed for every slide
- native conversion event counts by slide: 46, 45, 60, 45, 39, 45, 36, 40

## PPTX Inspection

Editable deck command:

```bash
python3 ../../scripts/inspect_pptx.py exports/deck_editable.pptx --expect-slides 8 --require-native-editable
```

Editable deck result:

- status: pass
- slide count: 8
- native shape counts: 46, 45, 60, 45, 39, 45, 36, 40
- SVG media count: 0
- errors: none

Snapshot deck command:

```bash
python3 ../../scripts/inspect_pptx.py exports/deck_snapshot.pptx --expect-slides 8 --require-svg-media
```

Snapshot deck result:

- status: pass
- slide count: 8
- SVG media count: 8
- errors: none

## Visual Review

The rendered previews were checked as a contact sheet. The deck uses a consistent dark technology-dashboard Bento style, CJK text renders correctly, and no page is blank or visibly malformed.
