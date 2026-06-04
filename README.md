# codex-bento-ppt

`codex-bento-ppt` 是一套面向任意 agent 的 PPT 生成 skill，受 Linux.do 原帖 [《一套完整的 AI PPT Agent 工作流》](https://linux.do/t/topic/1782304) 启发。原帖提出了从需求澄清、资料研究、结构规划、逐页策划到 SVG 设计的完整思路，本项目在此基础上整理为可复用的 skill，并补齐 source ingestion、跨 agent 能力契约和 native editable PPTX 导出。

具体工作流、角色分工和设计方法可以对照原帖理解：它不是“输入主题后套模板”，而是把 PPT 当作咨询交付物和设计交付物来生产。`codex-bento-ppt` 延续这个方向，从用户提供的原始材料出发，经过 source ingestion、需求澄清、研究、便利贴式大纲、逐页策划稿、Bento Grid SVG 设计、视觉校验，最终导出可逐元素编辑的 PowerPoint。

这个仓库保留 `codex-bento-ppt` 作为 skill 名称，但运行定位不是 Codex-only。任何具备本地文件读取、Python 脚本执行和基础文档处理能力的 agent 都可以按 `SKILL.md` 执行这套工作流。

## 核心目标

- 先读材料，再做需求和结构，不做“主题进、模板出”。
- Markdown/纯文本读取是最低必需能力。
- DOCX、PDF、XLSX 等读取是可选增强能力：有专用 skill/tool 时优先调用，没有时走本地 fallback。
- 用户提供的图片、文档内嵌图片、表格和截图会进入 `source_assets/`，作为后续页面设计素材。
- 最终交付必须是 native editable PPTX，而不是整页截图式 PPTX。

## 工作流

这一节是对原帖方法的工程化拆解。原帖中的多角色、多阶段协作被整理成固定产物链，方便不同 agent 在本地文件系统中持续推进和校验。

1. Source Ingestion：读取用户给出的原始材料，生成 `source_inventory.json` 和 `source_digest.md`。
2. Requirement Consulting：明确受众、场景、目标、页数、风格、必须使用或禁止出现的内容。
3. Research：基于本地材料和必要的外部研究，整理 slide-level evidence。
4. Sticky-Note Outline：用金字塔原则把每页表示成可调整的数字便利贴。
5. Page Planning：为每页生成内容优先的策划稿，确定信息层级和 Bento card 分配。
6. SVG Design：每页生成 1280x720 的完整 SVG，使用可转成 PowerPoint 原生对象的图形、文本、路径和图片。
7. Visual Review：渲染 SVG 预览并做 native conversion dry-run。
8. PPTX Assembly：导出 `deck_editable.pptx`，同时生成 `deck_snapshot.pptx` 作为视觉对照。

## 安装依赖

```bash
cd /path/to/codex-bento-ppt
python3 -m pip install -r requirement.txt
```

核心依赖包括 `python-pptx`、`cairosvg`、`Pillow`。DOCX/PDF/XLSX fallback 依赖也列在同一个 `requirement.txt` 中。

## 环境检查

```bash
python3 scripts/check_environment.py
```

检查项包括：

- Markdown/文本读取能力
- Python 运行时和关键包
- DOCX/PDF/XLSX fallback 包
- CJK 字体可用性
- native editable PPTX converter 来源

正常情况下，native converter 来源应显示为 `bundled-vendor`。这表示不需要额外安装 `ppt-master`。

## 常用命令

初始化项目目录：

```bash
python3 scripts/init_project.py ./my-deck --title "演示标题"
```

读取原始材料：

```bash
python3 scripts/ingest_sources.py ./source-docs --project-dir ./my-deck
```

校验 SVG，并执行 native editable dry-run：

```bash
python3 scripts/validate_svg.py ./my-deck/svg/*.svg \
  --render-dir ./my-deck/previews \
  --json-out ./my-deck/validation.json \
  --native-editable
```

导出 PPTX：

```bash
python3 scripts/assemble_pptx.py ./my-deck/svg ./my-deck/exports/deck_editable.pptx \
  --snapshot-output ./my-deck/exports/deck_snapshot.pptx \
  --title "演示标题"
```

检查输出是否真正可编辑：

```bash
python3 scripts/inspect_pptx.py ./my-deck/exports/deck_editable.pptx \
  --expect-slides 8 \
  --require-native-editable
```

## 为什么 PPTX 可以逐元素编辑

本项目不是把 SVG 整页截图塞进 PowerPoint。它使用 bundled `vendor/svg_to_pptx` converter 和 `vendor/svg_finalize` helper，把 SVG 中的文本、矩形、路径、线条、图片和语义分组转换为 PowerPoint DrawingML 对象。

因此在 PowerPoint 中可以直接选中和修改：

- 文本框
- Bento 卡片
- 图形和路径
- 线条和节点
- 图片对象
- 语义分组

`deck_snapshot.pptx` 只用于视觉对照，不是最终交付物。

## 跨 Agent 设计

跨 agent 可用性的核心是能力契约，而不是绑定某个 agent 的专用工具名。最低要求是：

- 能读取 Markdown/纯文本。
- 能执行本仓库的 Python 脚本。
- 能安装并使用 `requirement.txt` 中的依赖。
- 能用 bundled native converter 导出 editable PPTX。

DOCX、PDF、XLSX、联网研究、OCR、图片生成等都属于可选增强能力。缺少这些能力时，agent 应要求用户提供 Markdown/文本化材料，或使用本地 fallback 提取。

## 目录结构

仓库目录既包含 agent 执行所需的 skill 文件，也包含可重复运行的脚本、参考材料、示例输出和内置 converter。常见入口如下：

```text
codex-bento-ppt/
├── SKILL.md              # agent 读取的核心工作流说明
├── README.md             # GitHub 仓库说明，面向人类使用者
├── requirement.txt       # Python 依赖清单
├── agents/               # agent UI metadata
├── prompts/              # 各阶段角色提示词
├── references/           # 方法论、跨 agent 说明、原帖静态归档和附图
├── scripts/              # source ingestion、校验、导出、检查脚本
├── vendor/               # 内置 native converter，解除对外部 ppt-master 的硬依赖
│   ├── svg_finalize/     # SVG 后处理 helper
│   └── svg_to_pptx/      # SVG 到 DrawingML/PPTX 的转换实现
└── examples/             # 示例项目和已生成的可编辑 PPTX
```

实际生成 PPT 时，建议把每个任务放在独立项目目录下，项目目录会包含 `source_inventory.json`、`source_digest.md`、`requirements.md`、`research.md`、`outline.json`、`page_plans/`、`svg/`、`previews/` 和 `exports/` 等产物。

## 许可

`vendor/svg_to_pptx` 和 `vendor/svg_finalize` 来自 `ppt-master` 的 MIT licensed native SVG-to-PPTX 相关实现，并随本仓库一起分发，以解除运行时对外部 `ppt-master` skill 的硬依赖。

原始 Linux.do 方法论材料和附图作为本 skill 的参考归档保存在 `references/source/linuxdo-1782304/`，用于理解工作流来源和设计风格，不作为需要复刻的固定模板。

## 参考链接

- Linux.do 原帖：[https://linux.do/t/topic/1782304](https://linux.do/t/topic/1782304)
- `ppt-master` 原仓库：[https://github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)
