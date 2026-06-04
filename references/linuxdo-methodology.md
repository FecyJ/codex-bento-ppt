# Linux.do PPT Agent Methodology

Source: https://linux.do/t/topic/1782304  
Static local archive: `references/source/linuxdo-1782304/article.md`  
Archived attachments: `references/source/linuxdo-1782304/images/` and `references/source/linuxdo-1782304/manifest.json`

## Adapted Principle

The workflow is not "topic in, template out." It treats a deck as a consultant and design-team deliverable:

0. Read the user's raw material when files, directories, URLs, or pasted source text are provided. For DOCX/PDF/spreadsheets, prefer the dedicated document skills and use fallback extraction only when needed.
1. Clarify demand before creating a deck.
2. Gather factual material before building the outline.
3. Build the outline as digital sticky notes.
4. Create a planning draft for every page before visual design.
5. Use Bento Grid card layouts for information-heavy pages.
6. Generate full-page SVG designs at 1280x720.
7. Export PPTX while preserving editability. In this skill, native DrawingML export is the required final path, with an SVG snapshot deck as a visual reference.

The original post uses multiple AI products for different jobs. In this skill, every role is performed by the active agent. When a step calls for search, use the active agent's web or local-source tools; when a step calls for design, write editable SVG primitives directly.

## Phase Notes

### Source Ingestion

Before consulting or researching, read the user's original material. Build a source inventory and digest so every later phase can point back to concrete evidence rather than relying on a loose impression of the files.

For directories, scan recursively. Markdown/text reading is the required baseline. DOCX/PDF/spreadsheet reading is an optional enhancement: prefer available document-processing tools first, then use fallback extraction if available. For each source, record path, file type, title or inferred title, extraction status, high-level topics, reusable figures/tables/images if known, and any extraction warning. Do not silently discard unsupported files. User-provided images and images extracted from documents become candidate visual assets for page planning.

### Demand Clarification

The first useful output is not a slide. It is a requirement brief. Identify:

- audience and decision maker
- presentation occasion
- desired action or impression
- page count and time budget
- must-use sources, data, logos, or visuals
- style/tone
- forbidden messages or risky claims

Do not ask questions that can be answered from supplied files or the conversation.

### Research

The outline should be grounded in facts. For each section, gather current context, evidence, examples, and counterpoints. Prefer primary sources. Keep enough citation detail for the final deck creator to avoid unsupported claims.

The source article emphasizes large-scale information retrieval after outline planning. Use the approved outline or likely section titles as research targets, then return slide-level evidence packets. Do not let outdated or contradicted claims become core slide messages.

### Sticky Notes

Each slide is a movable planning unit:

- slide id
- page role
- one-sentence message
- supporting evidence
- audience value
- likely visual treatment

This makes structure easy to review and reorder before design.

The article's open structure prompt uses a "顶级的PPT结构架构师" role, a context-aware profile, and the pyramid principle. Replicate that behavior in `prompts/03-outline-architect.md`: conclusion first, parent-child summarization, logical grouping, and research-aware outline decisions.

### Planning Draft

The planning draft is a plain blueprint handed from planner to designer. It fixes the content and layout intention before styling. It should say what belongs in each visual block, what is emphasized, and what can be omitted if space is tight.

This phase should deliberately look unpolished. The source article shows a simple planning draft before the final styled page: clean blocks, exact placement intent, and minimal decoration. Use it to review and refine content before SVG design.

### Bento Grid Design

Bento Grid is the default content-page design language because it is flexible, information-dense, and easy for an agent to reason about. Use card sizes to show hierarchy. Maintain at least 20px gutters between cards. Important content gets the largest card.

Common patterns:

- one large focus card
- symmetric two-column cards
- asymmetric main/support split
- three equal comparison cards
- top hero card with smaller cards below
- mixed grid with one dominant card plus supporting cards

The article's open Bento prompt stresses that the layout is driven by content, not a rigid template. Card count can be 1, 2, 3, 4, 5, or more. The designer should choose among single focus, symmetric two-column, asymmetric two-column, three-column, main-plus-sides, top hero, and mixed-grid patterns according to the information.

Visual cues from the archived attachments:

- Technical/business analysis examples use deep navy or black backgrounds, translucent dark cards, cyan/teal strokes, subtle glows, and occasional violet/orange metric highlights.
- Pages are information-dense but modular: large headline/claim area, KPI chips, comparison cards, architecture lanes, side panels, and small diagram nodes.
- Planning examples are much lighter and quieter: pale background, grey cards, and wireframe-like modules before final design.
- The desired final effect is a dashboard-like slide built from separate editable primitives, not a flattened screenshot.

### SVG Output

Generate full-page SVG, not HTML screenshots. Required canvas:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
```

Use safe SVG only: shapes, text, paths, gradients, clipping, masks, and embedded simple symbols. Avoid scripts, foreignObject, remote images, and layout that depends on browser-only CSS.

The source article's direct SVG prompt begins from an "information architecture and SVG coding expert" role and asks for a high-quality, structured, premium, clean, professional SVG page. In this skill, keep those design goals while also preserving native PPTX editability:

- wrap major content units in top-level semantic groups;
- build cards, metrics, diagrams, and labels from native-convertible SVG primitives;
- keep images as separate local `<image>` elements;
- avoid flattening a slide into one full-page bitmap.

### PPT Export

Keep the SVG files as the canonical slide designs. Export to PPTX through the native editable path so PowerPoint users can directly select text, cards, shapes, groups, lines, paths, and images. Also emit an SVG snapshot deck for visual comparison. A PNG fallback is acceptable only for the snapshot deck or when explicitly requested; it is not a successful final deliverable when native editability is required.

## Replication Checklist

- Requirement brief exists before outline.
- Source inventory and digest exist before requirement brief when source material is provided.
- Research exists before outline for factual topics.
- Sticky notes exist before page planning.
- Page planning exists before SVG.
- Content pages use Bento Grid unless their page role justifies another layout.
- SVG pages are 1280x720 and validate.
- SVG pages pass native editable validation before assembly.
- Editable PPTX output exists, has the expected slide count, and contains multiple native editable objects per slide.
- Snapshot PPTX output exists for visual comparison and source SVGs are preserved.
