# Sticky Notes

## slide_01

- Role: cover
- Title: codex-bento-ppt
- One-sentence message: 这不是模板填充，而是一条可审计的 PPT 生产线。
- Evidence: `SKILL.md` workflow 0-8.
- Audience value: 建立整体心智模型。
- Visual intent: 深色科技封面，管线节点，强调 editable PPTX。

## slide_02

- Role: method
- Title: 核心思想：把 PPT 当作专家团队交付物
- One-sentence message: 质量来自角色拆分和阶段产物，而不是一次性生成。
- Evidence: `linuxdo-methodology.md`, `prompts/*`.
- Audience value: 理解为什么需要多阶段。
- Visual intent: 反模板卡片 + 专家角色矩阵。

## slide_03

- Role: workflow
- Title: 工作流地图：0 到 8 的串行闭环
- One-sentence message: 每一阶段都把不确定性转化为可检查文件。
- Evidence: `SKILL.md` workflow.
- Audience value: 知道每步输入、产物和顺序。
- Visual intent: 横向管线 + artifact chips。

## slide_04

- Role: implementation
- Title: Source Ingestion：先读材料，再谈需求
- One-sentence message: 用户材料、嵌入图片和表格先被归档，后续决策都回到证据。
- Evidence: `prompts/00-source-ingestion.md`, `scripts/ingest_sources.py`.
- Audience value: 理解第 0 阶段如何提升准确性。
- Visual intent: 多类型文件流入 inventory、digest、assets 三个输出。

## slide_05

- Role: prompt-engineering
- Title: 提示词工程：结构架构师 + 研究上下文
- One-sentence message: 大纲必须被研究上下文约束，避免凭空编故事。
- Evidence: `prompts/02-researcher.md`, `prompts/03-outline-architect.md`.
- Audience value: 理解 prompt 设计如何约束结构质量。
- Visual intent: 金字塔结构 + context guardrail。

## slide_06

- Role: planning
- Title: 便利贴与策划稿：设计前先冻结意图
- One-sentence message: 每页先是可移动的 sticky note，再成为给设计师的策划稿。
- Evidence: `prompts/03-outline-architect.md`, `prompts/04-page-planner.md`.
- Audience value: 理解设计前的内容锁定机制。
- Visual intent: 便利贴墙 + wireframe draft。

## slide_07

- Role: design-export
- Title: Bento SVG 到可编辑 PPTX
- One-sentence message: Bento Grid 负责表达，native DrawingML 转换负责可编辑。
- Evidence: `prompts/05-svg-designer.md`, `scripts/assemble_pptx.py`.
- Audience value: 理解视觉和工程之间的约束。
- Visual intent: SVG primitives 分解为 PPT objects。

## slide_08

- Role: usage
- Title: 如何使用与验收
- One-sentence message: 一个项目目录、三组命令、两份 PPTX，构成可复现交付。
- Evidence: `SKILL.md` final evidence and scripts.
- Audience value: 能照着复用或改造。
- Visual intent: 项目目录 + 命令检查清单。
