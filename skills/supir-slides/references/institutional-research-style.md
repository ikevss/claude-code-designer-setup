# Institutional Research Default Style

Use this reference when the user asks for an investment research deck, mutual
fund product launch deck, broker-style horizontal report, institutional client
roadshow, fund education material, or when no style/template is provided for a
finance-oriented deck.

The default is `institutional_research_default`: credible research material that
can be reviewed by an investment committee, institutional client, or sales
channel. It should look like a professional fund company, broker research, or
asset-management roadshow page. It is not a tech launch deck, consulting
infographic, SaaS dashboard, data screen, marketing poster, or startup pitch
deck.

默认版式基准是主流券商策略/行业研究报告和机构路演材料的横版页面范式：
普通证据页采用观点区粗体导语段 + 底部图表平铺；机制、产业链、供需传导、
技术路径、竞争格局页采用结论标题 + 主体结构图。视觉系统使用通用冷蓝/深靛蓝/
珊瑚强调色与现代无衬线字体；措辞仍遵守投研合规语言。

## 风格契约（Style Contract）

**这是唯一权威的风格描述段。** 组装任何金融/投研页面的生成或编辑
instruction 时，以此契约生成本页 Style constraints：优先写短正向目标形态，
只追加本页特有的模板、品牌、来源、页码排除或数据约束。不要在同一条
instruction 的多个字段反复转述风格规则；反面清单用于 QA 和必要的末尾短
negative block，不作为正文风格描述反复堆叠。

```text
整页是一张可送审的券商研究报告 / 机构路演风格横版页面。封面/首页使用深靛蓝或深海军蓝背景、白色现代紧凑无衬线标题、充足留白和确认过的品牌/身份信息；章节过渡页使用深蓝底白字或大号章节编号/标题。正文页使用白色或极浅冷蓝到白色的克制纸面背景，顶部放深靛蓝结论式标题和细分隔线/左侧短竖线。普通证据页采用“标题 + 观点区 + 证据区”：观点区为 1-3 个直接排在纸面上的自然段（10-20 字加粗业务导语 + 50-150 字正文）或 2-4 条实质 bullet；证据区放 1 张主图表/三线表，或最多 2 张紧凑证据图表并排，带坐标轴、单位、图例/直接标注和 provider 级来源注。视觉推理页用一个主体结构图承载结论，可采用产业链、价值链、供需传导、技术路线、因果链、稀缺度坐标、2x2 定位或竞争格局图，占页面主体 60% 以上，只放少量关键数字或短 callout。全页靠留白、对齐、细灰分隔线、分区小标题、图表轴线和表格规则组织层级；配色以深靛蓝、深蓝/亮蓝、浅蓝、少量珊瑚红和中性灰为主；中文优先使用思源黑体 / Source Han Sans SC 或等价清晰系统黑体，英文与数字使用 Helvetica/Arial/Inter 类字体。普通页标题约 22-26pt，正文约 12.5-15pt，图表标签和表格约 11-13.5pt，来源注约 8.5-10.5pt，字号与行距紧凑但清晰。
```

QA 和末尾 negative block 只保留少量必要排除项：不发明数字、作者、部门、Logo、来源或页码；不显示字体名、色号、提示词或工具说明；不把普通观点段、bullet、KPI、图表逐项包成装饰圆角卡片或图标网格；不使用深色霓虹、发光、玻璃拟态、3D、数据大屏、SaaS dashboard、营销海报或科技发布会感。参考图中已确认的 Alpha/PaiWork 标识或页脚水印是内置模板品牌元素，默认保留；用户要求去掉品牌、水印、页脚或替换 Logo 时按用户要求覆盖。

封面、章节过渡页默认采用深蓝底白字或浅蓝纸面大号章节编号/标题 + 大量留
白；正文页默认采用极浅冷蓝到白色的克制渐变纸面。机制图/产业链图页允许主图占
60% 以上，仍保持扁平克制。

## Default Preset

- Canvas: cover/section pages may use a full-bleed deep indigo or deep navy
  background with white typography. Ordinary content pages use a white or
  near-white institutional report canvas with a very subtle pale-cool-blue to
  white gradient. The gradient is a paper/background atmosphere only; avoid
  decorative gradients, glow, or poster-style lighting.
- Cover/title pages are not summary pages by default. They should show the deck
  title, optional subtitle/date, and confirmed brand/author identity with ample
  breathing room. Do not add KPI strips, three-column metric rows, large-number
  summaries, evidence conclusions, or core-viewpoint lists below the title
  unless the user explicitly asks for a metric-heavy cover or the selected
  reference template's cover/title page clearly uses this metric-summary design.
- Master: fixed header and footer. Header may use a deep navy left vertical bar,
  a thin navy title rule, or a restrained title band. Footer may use a subtle
  pale-blue or light-gray band for source note, internal-use / disclaimer text
  when required, and page number only when the user explicitly requires it (a
  page number printed on a reference/template image is not such a requirement).
- Structure: top 15-20% for conclusion title and core message; middle viewpoint
  zone for a real analytical paragraph or substantive bullets; bottom 45-60% for
  evidence. The default ordinary page layout is upper viewpoint and lower
  evidence with 1-3 aligned charts/tables/artifacts. When the evidence artifact
  is very large, use a left narrative column plus right/bottom evidence.
- Visual reasoning pages: top conclusion title plus one dominant mechanism,
  industry-chain, demand-transmission, technology-roadmap, causal-chain, or
  positioning visual occupying most of the canvas. Use sparse labels and a few
  decisive numbers; keep detailed proof in workpapers.
- Evidence zone: one main chart/table, or 2-3 aligned charts, tables,
  screenshots, product catalogs, or other artifacts.
- Separation: use whitespace, alignment, indentation, typography, light rules,
  section labels, chart axes, and table rules. Do not put every paragraph,
  number, bullet, or chart in its own card.
- Colors: generic cool-blue institutional palette by default:
  deep indigo `#01105C` for cover backgrounds, titles, rules, and structural
  anchors; dark blue `#0C30A8` for secondary title emphasis; white `#FFFFFF` for
  cover and dark-section typography; bright blue `#2A66F6` for links, active
  emphasis, and selected highlights; light blue `#7DADFF` and pale blue
  `#CFE4FF` for the subtle content-page gradient, light bands, table headers,
  and low-emphasis fills; coral red `#EF404A` for critical emphasis or contrast;
  neutral surface `#F4F5F6` and neutral gray `#5F6670` for secondary text and
  rules. Use no more than one strong accent family on a page unless a comparison
  needs it. Avoid neon, glow, heavy decorative gradients, glassmorphism, and 3D
  effects.
- Typography: use a modern compact sans system derived from the default PPT
  theme: Chinese text should use Source Han Sans SC / 思源黑体 when available,
  with Noto Sans CJK SC or an equivalent clear system CJK sans as
  fallback; Latin text and numerals should look like Helvetica/Arial/Inter.
  Ordinary page titles are bold and compact at roughly 22-26pt depending on
  length; long titles may be smaller. Body copy should sit around 12.5-15pt,
  chart labels and table cells around 11-13.5pt, and source notes around
  8.5-10.5pt. Cover and section titles may be much larger but keep the same sans
  tone. For ordinary content pages, typography must preserve information
  density: do not enlarge body text, icons, or line spacing so much that the
  slide becomes a sparse slogan list. Do not rely on WPS-only fonts as the
  default customer-facing font dependency.

## Broker Research Page Guardrails

Use these guardrails for ordinary analysis, data, finance, comparison, fund
education, and roadshow pages:

- The page should feel credible, rational, data-driven, and reviewable. Visual
  design serves the research judgment and must not overpower the content.
- Default layout: conclusion-first title at the top, a medium analytical
  paragraph or 2-4 substantive bullets below it, then an evidence zone with 1-3
  charts, tables, screenshots, product photos, or other evidence artifacts.
- Use invisible grids, alignment, whitespace, thin rules, chart axes, table
  rules, and restrained section captions for organization. Do not rely on cards,
  heavy blocks, or colored panels to separate every item.
- Do not wrap each paragraph, bullet, KPI, chart, or evidence artifact in its own
  rounded rectangle. Use at most one light divider or a very pale gray/blue band
  when a page needs extra separation.
- Obvious borders are allowed only for real tables, flow/process boundaries,
  mechanism diagrams, legends, comparison boundaries, or true grouped modules.
  Ordinary text blocks should remain unboxed.
- Keep emphasis restrained: title can be strong, but body text should be
  readable and calm. Avoid frequent bolding, oversized words, badge labels, and
  repeated red/blue emphasis.
- If a content page has only a few short statements because typography is too
  large, reduce title/body/icon scale and restore reviewable substance: causes,
  evidence, constraints, dates, units, implications, or a compact chart/table.

## Text Style

- Titles are conclusion-first research judgments, not slogans or advertising
  copy. Do not end main titles, page titles, or section titles with a Chinese
  full stop `。` or English period `.`.
- Visible conclusions should be written directly. Do not prefix titles,
  callouts, lead-ins, chart notes, or summary rows with generic meta labels such
  as `关键判断：`, `核心结论：`, `结论：`, `洞察：`, `投资启示：`, `Takeaway:`,
  or `So what:`. If emphasis is needed, make the whole sentence concise and
  prominent instead of adding a label.
- Ordinary research pages default to a viewpoint zone of 1-3 paragraphs, each
  opening with a 10-20 Chinese character bold lead-in phrase followed by a
  50-150 Chinese character body; the whole viewpoint zone should stay within
  roughly 350 Chinese characters.
- Alternatively use 2-4 bullets.
- Bullets should be complete analytical statements, typically 40-110 Chinese
  characters each, with cause, data/fact, implication, date, unit, source, or
  constraint when relevant. Do not use bullets as short labels only.
- Treat the narrative paragraph/bullets as first-class research content, not as a
  failure to make a diagram. Do not collapse them into slogan labels.
- Do not remove necessary explanation merely to make the slide look simpler.
- Do not remove necessary explanation merely to make the slide look simpler or
  to accommodate oversized type.
- Avoid advertising language, exaggerated claims, vague labels, and excessive
  emphasis color.

## Containers And Frames

- Default: no decorative rounded cards, shadow cards, glowing frames, gradient
  panels, pill headers, or card-inside-card layouts.
- Use a border only when it expresses a real grouping, table, process stage,
  legend, comparison boundary, or diagram node.
- Paragraph text and bullet groups should not be boxed by default. Use
  hierarchy, spacing, indentation, and rules instead. If the user template uses a
  text panel, keep it light and purposeful; do not add heavy colored rounded
  borders merely to decorate the viewpoint area.

## Icons

- Ordinary analysis, data, comparison, finance, fund education, and table pages
  default to 0 decorative icons.
- Do not attach an icon to every bullet, KPI, table row, or card.
- Avoid app-style, emoji-like, cute, badge-like, warning-sign, target, rocket,
  flame, people, oversized-arrow, or template-heavy icons.
- Mechanism, industry-chain, technical-architecture, product-architecture, data
  flow, capital flow, and process pages may use sparse line icons, only when
  they clarify the relationship.
- If icons are used, they must be small, consistent, linear, and subordinate to
  the logic and text.

## Tables

- Use research-report table styling: flat, audit-friendly, compact.
- Preferred style: light blue/gray header, thin gray rules, optional subtle
  alternating rows, no rounded corners, no shadows, no gradients.
- Use compact three-line or thin-grid tables: top rule, header rule, bottom rule,
  optional light row rules, and minimal vertical lines.
- Numbers align right; text aligns left; units are explicit.
- Emphasize only the few important cells with brand bright blue or a small coral
  red accent.
- Do not put decorative icons in table cells.
- Do not turn tables into colored infographics, dashboard panels, badge systems,
  or floating card grids.

## Charts

- Charts should resemble Wind, Excel, broker research, or fund roadshow
  materials: clear axes, units, time ranges, legends or direct labels, and
  source notes when required.
- Prefer flat 2D charts with 2-3 main colors.
- Do not use 3D charts, glowing bars, dashboard gauges, neon effects, huge
  floating numbers, or unnecessary arrows.
- Direct labels are preferred over complex legends when readable.
- Chart titles should be factual, e.g. `图：...`, or a concise proof statement.
- When a page includes sources, place a small bottom note such as
  `资料来源：...` / `Source: ...`.

## Mechanism Diagram Exception

When the page is about a mechanism, principle, industry chain, technology stack,
business model, product architecture, data flow, capital flow, supply-demand
transmission, or substitution relationship, use the image model's diagram
strength deliberately:

- Use nodes, arrows, layers, swimlanes, timelines, axes, and sparse line icons.
- Use restrained color blocks only to encode hierarchy, stage, or direction.
- The diagram must answer "who affects whom", "how it transmits", "what is
  upstream/downstream", or "which layer does what".
- Stay flat and institutional. Do not turn mechanism pages into tech posters or
  glowing infographics.
- Keep line weight, arrow style, icon style, and text hierarchy consistent.

## Forbidden By Default

- Dark neon technology backgrounds, cyber lines, glowing grids, data waves,
  cinematic technology scenes, decorative globes, sci-fi cars.
- Default rounded-card layouts, card grids, every module boxed, icon-per-bullet.
- Large gradients, shadows, glow, glassmorphism, 3D, glossy dashboard panels.
- Marketing slogans, launch-event visuals, SaaS dashboard look, data-screen
  look, startup pitch deck look.
- Decorative imagery that weakens source traceability or makes the page feel
  less reviewable.
- Default card-based layouts, icon-per-bullet treatments, table-as-infographic
  treatments, floating numbers, exaggerated arrows, and badge-heavy emphasis.
