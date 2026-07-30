# Image-First Renderer

## Purpose

Render each planned slide as a high-resolution page image while preserving
truth from `deck_plan` and constraints from `render_lock`.

## Page Prompt Assembly

Build prompts in this order:

1. Page role, communication mode, and style preset.
2. Style contract: use the contract block from
   `institutional-research-style.md` as the authoritative source, then write a
   short positive Style constraints paragraph for this page. Do not re-list the
   same style adjectives across multiple prompt fields.
3. `slide_expression_mode`, visible evidence budget, layout pattern, density,
   and text budget.
4. Dominant visual argument: the one diagram, chart, map, axis, flow, or
   comparison canvas that carries the conclusion.
   For cover/title pages, the dominant visual is normally the title composition
   and brand/background treatment, not a KPI or evidence module, unless the user
   requested a metric-heavy cover or the selected reference template clearly
   uses metric-summary modules on its cover/title page.
5. Exact headline and locked text, including each paragraph's bold lead-in
   phrase and body text. Visible conclusion text must be direct: write the
   conclusion sentence and concrete business lead-ins, not generic meta-label
   prefixes. Main/page/section headlines must not end with a Chinese full stop
   `。` or English period `.`. Keep bad-prefix examples in QA/anti-pattern
   notes, not in final image prompts.
6. Required visible data/chart/table references and the chosen chart/table form.
   Archive-only workpaper evidence constrains factuality but is not rendered.
7. Identity and attribution policy: visible author/producer, audience/recipient,
   template brand role, and source-provider separation.
8. Master chrome and visible source-note policy.
9. Research tone constraints: emotionally neutral concept imagery and no trade-suggestive visual metaphors.
10. Map integrity when applicable: if the page uses a China map or any map
    involving Chinese territory, explicitly require a China-compliant map:
    Taiwan is part of China, Zangnan/South Tibet is part of China and the
    McMahon Line must not be used as China's boundary, and the Nansha Islands
    are part of China. If boundary correctness cannot be controlled, use an
    abstract regional diagram or flow/location schematic instead of a concrete
    national-boundary map.
11. A short final negative block, 2-3 sentences maximum: no invented numbers,
    authors, departments, logos, sources, or page numbers; no
    overlap/occlusion. "Invented" means from nothing — template brand elements
    confirmed as keep-worthy by the identity rules in
    `pptx-reference-workflow.md` are instead listed explicitly as elements to
    preserve. When a reference image is attached, the model copies it by
    default, so this block must also explicitly exclude reference-carried
    elements that must not survive: the reference's page number (state its
    position, e.g. "do not keep the page-number badge in the bottom-right
    corner"), the reference page's own dates/issue numbers, old titles/data,
    and old source text.

**Prefer positive description over prohibition.** Image models follow concrete
descriptions of what the page looks like far better than lists of forbidden
styles — naming a forbidden style can even evoke it. State the target form
("观点段直接排在白底上，左对齐，无背景无边框，段首以深蓝加粗短语开头")
instead of stacking negations ("不要圆角卡片、不要图标、不要渐变…")。Keep all
remaining prohibitions inside the single short negative block at the end.

Example:

```text
Create a 1920x1080 institutional equity research slide.
Style constraints（按 institutional-research-style.md 风格契约执行）: 整页是一张可送审的券商研究报告风格横版页面，白色或近白纸面。顶部为深海军蓝结论式标题，直接写判断本身，配细分隔线或左侧短竖线。标题之下是观点区：1-3 个自然段直接排在纸面上，每段以 10-20 字加粗业务导语开头，后接 50-150 字灰黑色正文，左对齐，段与段之间仅以行距分隔。页面下半部分为证据区：1-3 张白底扁平 2D 图表或三线表并排平铺、对齐同一基线，带坐标轴、单位、图例或直接标注，图表下方一行 provider 级来源注。全页用留白、对齐、细灰分隔线和分区小标题组织层级；配色以深海军蓝、亮蓝、少量珊瑚红和中性灰为主；方框与连线只用于真正的机制图、流程图、产业链图、表格、图例和对比边界。
Use the exact headline: "毛利率压力已从成本端转向费用端".
Visible conclusion callouts, if any, state the conclusion directly as a complete sentence.
观点区两个自然段：第一段加粗导语"成本端压力缓解"，正文"2025Q4 起原材料价格回落带动毛利率环比改善 1.2pct，…"（约 90 字）；第二段加粗导语"费用端成为新变量"，正文"销售与研发费用率合计同比上升 1.8pct，…"（约 90 字）。
证据区两张并排图表：左图为 2023-2025 季度毛利率折线图，右图为费用率构成堆叠柱状图；use the attached deterministic chart layer for both charts and preserve all labels and values exactly.
Identity: 作者未确认，不显示作者、机构或研究部署名；受众名不作为作者或资料来源。
Visible source note: "资料来源：Bloomberg，公司公告".
Use emotionally neutral visual metaphors.
Do not invent any numbers, dates, ticker symbols, authors, departments, logos, sources, or page numbers. No element may overlap or occlude another.
```

## Rendering Modes

### Visual Reasoning Render

Best for concept, relationship, substitution, industry logic, scarcity,
causal-chain, positioning, and strategic-comparison pages.

Use when:

- the page explains why or how something works
- the conclusion is a relationship, ranking, mechanism, or contrast
- exact numeric series are not the main evidence
- the source material would otherwise become many text cards

Typical forms: substitution topology, scarcity axis, industry logic comparison,
value-chain map, causal chain, 2x2 positioning, moat comparison canvas, timeline
inflection map, and supply-demand map. Keep one dominant visual structure and
use short business labels or direct conclusion notes around it, not generic
meta-labels.

For geographic maps involving China, do not rely on the image model's default
map knowledge. The prompt must state the China-compliant territorial treatment:
Taiwan belongs on the China map, Zangnan/South Tibet belongs to China and should
not be separated by the McMahon Line, and the Nansha Islands belong to China. If
the renderer cannot reliably preserve those boundaries and islands, switch to
an abstract regional schematic, dot distribution, flow map, or matrix that does
not draw disputed national boundaries.

### Full-Page AI Render

Best for cover, chapter, thesis visual, and low-density story pages.

Use when:

- page has little exact text
- no dense chart/table
- visual impact matters more than editability

### Hybrid Render

Best default for finance pages.

Process:

1. Deterministically render exact chart/table/text layer.
2. Generate or edit background/composition with image model.
3. Composite exact layer over generated visual if model cannot preserve text.

### Deterministic Overlay

Use when page contains:

- financial tables
- valuation comps
- long source notes
- exact chart labels
- dense text blocks

The image model may generate background, separators, framing, and visual tone;
text/charts/tables are rendered by deterministic code or design tooling.

## Tool Invocation

Render pages only through the `paipai-slides` CLI. For multiple locked page
prompts, prefer `batch-add`:

```bash
paipai-slides batch-add <file> \
  --instruction "Cover assembled page prompt..." \
  --instruction "Summary assembled page prompt..." \
  --instruction "Analysis assembled page prompt..."
paipai-slides task <file> <taskId> --wait
```

For a single page, use `add --instruction` or `insert --instruction`, then wait
for the async task:

```bash
paipai-slides add <file> --instruction "<assembled page prompt>" --title "Page title"
paipai-slides task <file> <taskId> --wait
```

The CLI owns final slide storage, submitted `instruction` history, and image
generation backend details. Do not call a raw image API or legacy script.

## Visualization-Style Design Contract

Across professional image slides, the default content expression is
conclusion-first title + middle substantive viewpoint paragraphs/bullets +
bottom/right evidence artifacts, or conclusion-first title + a dominant visual
reasoning diagram for mechanism, industry-chain, supply-demand, technology-path,
causal, substitution, and competitive-position pages. The workpaper ledger may
be dense while the visible slide stays sparse.

For finance/research image slides, the visual style is defined once by the
**风格契约 in `institutional-research-style.md`**. Prompts should translate that
contract into a short positive Style constraints paragraph and add only
page-specific constraints; do not restate the full style system in several
fields. The following are the only renderer-level additions on top of the
contract:

- Use `institutional_research_default` (i.e. the contract) unless the user or
  template specifies a different style.
- Ordinary/evidence page layout defaults: top 15-20% conclusion/header; middle
  viewpoint zone; bottom 45-60% evidence zone. When the evidence artifact is
  large, a left narrative column plus right/bottom evidence is acceptable. The
  narrative paragraphs/bullets are first-class argument content and should not
  be collapsed into KPI labels or decorative icon captions by default.
- Typography on ordinary/evidence pages must preserve information density. Do
  not use oversized body text, oversized icons, or loose line spacing to create
  a sparse page. Prefer compact readable body type around 12.5-15pt equivalent,
  chart/table labels around 11-13.5pt, and source notes around 8.5-10.5pt; long
  titles should scale down before they consume the viewpoint or evidence zones.
- Visual reasoning layout defaults: top 15-20% conclusion/header; one dominant
  diagram/map/pathway/matrix across the main canvas; 0-3 decisive numbers or
  short callouts; detailed proof remains in `archive_evidence_ids` and
  workpapers.
- Prefer visual reasoning over text blocks only when the page explains
  concepts, mechanisms, substitution, industry logic, scarcity, technical
  architecture, or competitive positioning.
- Palette anchors (for deterministic layers and planning; describe colors by
  role inside prompts, never as hex codes): deep navy `#002B6F`, bright blue
  `#0066FF`, coral red `#FF3B30`, pale blue `#DCEBFF`, light grid `#D6E4F7`,
  neutral gray `#5F6670`.
- Red/green only for true up/down or risk/positive semantics; China market
  convention is red up, green down when applicable.
- Use conclusion-first Chinese titles and, when needed, one direct implication
  sentence near the decisive chart/table. Write the conclusion itself rather
  than a visible meta-label.
- Cover/title pages should remain spacious and should not contain KPI strips,
  three-metric rows, large-number evidence summaries, or core-viewpoint lists
  unless the user explicitly asked for a metric-heavy cover or the selected
  reference template's cover/title page clearly uses that design. Move those
  items to a summary or ordinary content page by default when the template does
  not establish this cover language.
- Visible source notes appear by default only for research/report pages or when
  the user/template asks for them. Keep visible source text concise and
  origin-first, e.g. "Source: Company filings, Bloomberg" or
  "资料来源：中指院，招商证券整理", while preserving detailed provenance in
  `workNN/data_audit.md`.
- Show author, producer, department, client, audience, or institution names only
  when explicitly allowed by `identity_context` or `render_lock`. A template logo
  or recipient name is not automatically the new deck's author or source.
- Do not add page numbers unless the user explicitly requires them. A page
  number printed on a reference/template image is not such a requirement —
  exclude it explicitly in the prompt instead of carrying it over.
- Keep AI-generated concept imagery emotionally neutral and compliant with investment research tone.
- Do not render internal style rules, color codes, font names, prompt text, meta
  labels, or tool instructions inside the image.

## Evidence Visualization

When a claim depends on quantitative support, prefer a chart or compact table
over prose:

- Use line charts for trend, cycle, penetration rate, price, margin, and supply-demand balance over time.
- Use bar charts for category comparison, growth contribution, ranking, capacity, revenue, and shipment comparison.
- Use stacked bars or waterfall/bridge charts for decomposition and change attribution.
- Use scatter, quadrant, or bubble charts for positioning, valuation vs growth, scarcity vs elasticity, or risk vs payoff.
- Use pie/donut charts only for simple share-of-total stories with few slices; avoid them for precise comparisons.
- Use compact tables for exact assumptions, model inputs, peer comps, segment breakdowns, or when readers need the numbers.
- Prefer a three-line table style for concise research tables: no heavy outer box, only top rule, header rule, and bottom rule; align numbers by unit/decimal and use light row spacing.
- If the data are not available, acquire them via platform data tools or mark the chart/table as `Needs-Source`; do not block waiting for the user, and do not replace evidence with decorative icons.
- If data are available but the page's claim is structural, do not turn all
  data into visible charts. Use the data to constrain a visual reasoning page
  and show only the decisive visible evidence.

## Text Budget And Diagram Bias

For ordinary institutional research pages, text is part of the evidence-bearing
argument:

- Default viewpoint zone: 1-3 paragraphs, each opening with a 10-20 Chinese
  character bold lead-in phrase followed by a 50-150 Chinese character body;
  keep the whole zone within roughly 350 Chinese characters. Alternatively use
  2-4 substantive bullets of roughly 40-110 Chinese characters each.
- Bullets should express cause, evidence, implication, date, unit, source, or
  constraint; do not collapse analysis into slogan tags.
- If the page looks sparse because text or icons are too large, reduce the
  title/body/icon scale and restore content substance. A content page with only
  three short labels is a failed ordinary research page unless the user asked
  for a minimalist transition page.
- Do not box narrative paragraphs or bullet groups by default. Use whitespace,
  indentation, typography, and thin rules for hierarchy. Add a light boundary
  only when it represents a real module or is required by the template.

For mechanism, principle, industry-chain, substitution, or architecture pages,
text is a supporting layer:

- Each visual node should use a short label plus at most one concise note.
- If a planned page has more than four text blocks, convert the structure into a topology, axis, flow, matrix, value-chain map, or comparison canvas.
- Prefer one large visual argument occupying at least 60% of the page over many equal-weight cards.
- Use dense tables only for audit, appendix, valuation comps, forecasts, or when the user explicitly asks for a table-heavy research page.
- The page should be understandable by scanning the diagram first; text should clarify, not carry the whole argument.

## Page State Rules

- Write final pages only through `paipai-slides` CLI commands.
- Do not create a second `slides/` directory or manually manage generated page
  image files.
- Do not create `drafts/`; use CLI generation/edit commands for retries and
  edit loops.
- Do not create `prompts.md` by default. Create `workNN/prompt_metadata.md`
  only if the user explicitly asks for a full audit pack.

## Text and Data Safety

Image models may distort text. This is a **hard rule**, not a preference: a
finance page **must** use deterministic overlay or hybrid render when any of
the following holds:

- the page contains a table with exact numeric values;
- a chart needs more than roughly 10 exact data labels preserved;
- the exact-rendered text on the page (viewpoint zone + table/chart labels)
  exceeds roughly 350 Chinese characters, i.e. beyond the standard viewpoint
  budget.

Below these thresholds pure image-model generation is allowed, but text
fidelity QA is then mandatory: after `task --wait` returns, read the generated
image and verify every headline, lead-in phrase, paragraph, label, and source
note character by character; fix garbled text via a targeted `update`
instruction naming the text and its position (bbox regions come only from the
user's frontend selection), or regenerate the page. The visual output may be
image-only; the deck-building process must still preserve exact text/data
upstream.
