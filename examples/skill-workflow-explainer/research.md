# Research

## Executive Takeaways

- `codex-bento-ppt` 的价值来自工作流，而不是某个单一提示词：它把 PPT 任务拆成顾问、研究员、结构架构师、策划师、SVG 设计师和质量检查员。
- Source Ingestion 是新加入的第 0 阶段，保证用户材料先被读取、归档和摘要化。
- 结构阶段复现原帖开源的“顶级 PPT 结构架构师”思想：Context-aware、金字塔原理、调研事实约束。
- Bento Grid 提示词被移植到 SVG 设计阶段，并增加 native editable 安全规则。
- PPTX 输出通过 `ppt-master` 的 native DrawingML 转换器实现可编辑对象，而不是整页图片。

## Source Notes

### Source 1: SKILL.md

- URL/path: `/home/fecyj/.agents/skills/codex-bento-ppt/SKILL.md`
- Date: local current state
- Relevant facts: workflow stages, non-negotiables, project layout, validation and export commands
- Slide uses: workflow overview, source ingestion, final evidence
- Confidence: high
- Caveats: deck explains current local implementation only

### Source 2: linuxdo-methodology.md

- URL/path: `/home/fecyj/.agents/skills/codex-bento-ppt/references/linuxdo-methodology.md`
- Date: local static archive based on linux.do topic 1782304
- Relevant facts: consultant workflow, sticky notes, planning draft, Bento Grid, SVG-first design
- Slide uses: design philosophy, role chain, Bento design
- Confidence: high
- Caveats: adapted to Codex and native editable export

### Source 3: scripts

- URL/path: `/home/fecyj/.agents/skills/codex-bento-ppt/scripts/`
- Date: local current state
- Relevant facts: `validate_svg.py --native-editable`, `assemble_pptx.py`, `inspect_pptx.py --require-native-editable`
- Slide uses: export and verification
- Confidence: high
- Caveats: native export depends on sibling `ppt-master` converter being available

## Slide Evidence Packets

### Workflow

- claim: The skill is a staged workflow, not one-click templating.
- evidence: `SKILL.md` lists phases 0-8 with artifacts.
- source: `SKILL.md`
- visualizable detail: horizontal pipeline with artifact chips.

### Editable Export

- claim: Final PPTX remains human-editable.
- evidence: `assemble_pptx.py` calls `ppt-master` native conversion; `inspect_pptx.py` checks native object counts.
- source: `scripts/assemble_pptx.py`, `scripts/inspect_pptx.py`
- visualizable detail: SVG primitives fan into PowerPoint text/shapes/groups/images.
