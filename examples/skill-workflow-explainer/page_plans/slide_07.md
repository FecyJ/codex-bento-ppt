# slide_07 - Bento SVG 到可编辑 PPTX

## Page Role

Design and export implementation.

## Core Message

Bento Grid 负责表达，native DrawingML 转换负责可编辑。

## Content Blocks

1. SVG design constraints: 1280x720, safe elements, semantic groups, CJK font stack.
2. Native export: `assemble_pptx.py` calls `ppt-master` converter.
3. Editable objects: text, cards, groups, lines, paths, images.
4. Snapshot deck: visual comparison only.

## Designer Handoff Draft

- Plain wireframe intent: left SVG primitive panel, center converter, right PPT object panel.
- Exact element placement: SVG card left, conversion arrow center, PPTX card right.
- What must be emphasized: not a full-slide bitmap.
- What may be omitted if crowded: converter internals.
- What should stay visually quiet: background grid.

## Evidence To Show

- `prompts/05-svg-designer.md`
- `scripts/assemble_pptx.py`
- `scripts/ppt_master_bridge.py`

## Bento Layout Plan

- Canvas: 1280x720
- Grid: three-stage conversion diagram
- Card A: x=72, y=156, w=330, h=420, purpose=SVG primitives
- Card B: x=474, y=196, w=332, h=340, purpose=native conversion
- Card C: x=878, y=156, w=330, h=420, purpose=PPT objects
- Card D: x=72, y=604, w=1136, h=62, purpose=editable promise
- Gutters: at least 20px

## Visual Direction

- palette: cyan SVG, violet converter, orange PPTX
- typography: Noto Sans CJK SC stack
- icon/image needs: object chips, arrows
- avoid: embedded screenshot
- reference image/style cue: technical architecture slide

## Speaker Notes Seed

解释当前实现的关键变化：PPTX 不是把整页 SVG 当图片塞进去，而是转换成 native DrawingML 对象。
