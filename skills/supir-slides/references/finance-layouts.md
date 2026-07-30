# Finance Layout Patterns

Use these patterns as page layout names in `deck_plan` and `render_lock`.

## Core Patterns

| Pattern | Use |
| --- | --- |
| `executive_summary_grid` | 3-6 key conclusions, each with evidence line |
| `single_big_chart` | one dominant chart with compact direct implication |
| `two_chart_with_takeaway` | paired evidence charts plus right-side direct conclusion sentence |
| `chart_plus_table` | chart above or left, exact table as support |
| `full_width_table` | valuation comps, forecast, KPI table |
| `three_kpi_plus_chart` | KPI strip plus trend chart |
| `valuation_bridge` | waterfall / bridge from base case to upside/downside |
| `risk_matrix` | probability × impact or factor table |
| `market_dashboard` | multi-panel recurring dashboard（注意：这是页面布局；strategist.md 中同名的是沟通模式，二者概念不同） |
| `thesis_evidence_stack` | conclusion, 3 evidence blocks, source notes |
| `assumption_chain` | facts -> assumptions -> inference -> conclusion |
| `scenario_payoff_grid` | base/upside/downside scenarios with probability/payoff framing |
| `compliance_check_panel` | compact source, assumption, and risk/disclaimer checklist |
| `institutional_claim_evidence_page` | top/left conclusion + medium analytical paragraph or substantive bullets + bottom/right chart/table evidence; default for ordinary research pages |

## Default Layout Routing

For institutional investor roadshows, fund education, and investment research
reporting, ordinary analysis pages default to
`institutional_claim_evidence_page`.

- Use `institutional_claim_evidence_page` when the page is a normal analysis,
  data, finance, comparison, product-evidence, or research judgment page.
- The default structure is: top 15-20% conclusion title and core message; middle
  viewpoint zone with 1-3 bold-lead-in paragraphs (10-20 character lead-in plus
  50-150 character body each, whole zone within ~350 Chinese characters) or 2-4
  substantive bullets; bottom 45-60% evidence zone with 1-3 aligned charts,
  tables, screenshots, product photos, or other evidence artifacts.
- Prefer white or near-white report pages with restrained blue/gray accents.
  Use invisible grids, alignment, whitespace, thin rules, chart axes, and table
  rules for organization.
- Do not convert ordinary pages into infographic card grids, badge systems,
  icon-heavy comparison pages, data-screen dashboards, or technology posters.
- Use visual reasoning patterns only when the page truly explains mechanism,
  principle, industry chain, technology stack, business model, data/capital flow,
  substitution, scarcity, positioning, or architecture.
- Keep the image model's strength for mechanism/origin/industry-chain/product
  architecture pages, but ordinary evidence pages should read first as research
  pages: claim, reasoning, evidence, source.

## Investment Evidence Page Archetypes

These patterns are for buy-side decision support, IC discussion, monitoring,
and research communication. They were largely learned from sell-side analyst
decks, and the sell-side page idiom is the default visual baseline (see the
风格契约 in `institutional-research-style.md`). Keep the wording buy-side: state
the investment question, show the evidence, and connect it to a decision,
scenario, monitoring item, or risk.

| Pattern | Use |
| --- | --- |
| `evidence_triptych` | 1-2 conclusion bullets plus three evidence panels: table + share chart + impact chart, or three charts. Use when one thesis needs multiple independent supports. |
| `claim_then_artifact` | 2-4 concise bullets plus one screenshot/product taxonomy/process artifact. Use for channel checks, product scope, customer mix, supply-chain mapping, or qualitative evidence. |
| `thesis_left_table_right` | left side has thesis, assumptions, and one chart; right side has a full-height peer/company/constraint table. Use when the decision question is "who has room, cash, capacity, constraints, or exposure?". |
| `small_multiples_comparison` | matched charts in small multiples. Use for domestic vs overseas vs global trend, segment vs total market, before/after, or scenario comparison. |
| `chart_table_crosscheck` | one chart and one table answer different sub-questions; include a short direct implication sentence tying them together. |
| `scenario_monitor_panel` | base/upside/downside or watchlist panel with triggers, indicators, disconfirming evidence, and action implications. Use for buy-side monitoring pages. |
| `quote_or_fieldwork_evidence` | short management/fieldwork quote or paraphrase plus chart/table evidence. Use sparingly and source clearly; do not present unsourced hearsay as fact. |

Decision-question mapping:

- "Should we care, add, trim, avoid, or monitor?" -> `scenario_monitor_panel` with triggers, upside/downside, and risk indicators.
- "Who has the best exposure or constraint profile?" -> `thesis_left_table_right` with peer metrics and constraint table.
- "Is the thesis supported by more than one evidence source?" -> `evidence_triptych` with independent evidence panels.
- "What exactly is growing and why now?" -> `claim_then_artifact` with product taxonomy, order/channel artifact, or process map.
- "Is the change domestic, overseas, segment-specific, or market-wide?" -> `small_multiples_comparison` with matched axes and shared legend.
- "What is the implication?" -> every page needs a conclusion title plus a one-line decision/monitoring implication near the decisive chart/table, written directly without a visible label such as "关键判断：" or "So what:".

Visible wording rule:

- Internal planning terms such as takeaway, so-what, claim, implication, or
  judgment are not visible page labels. On the slide, write the actual
  conclusion sentence directly, e.g. `高端磁材所需 Dy/Tb 仍主要依赖南方离子矿和缅甸进口`,
  not `关键判断：高端磁材所需 Dy/Tb 仍主要依赖南方离子矿和缅甸进口`.

## Visual Reasoning Patterns

Use these layouts when the page explains "why", "how", "relative position",
"substitution", "causal path", "industry logic", or "strategic implication".
They should normally carry the conclusion through one dominant diagram rather
than through many text cards.

| Pattern | Use |
| --- | --- |
| `substitution_topology` | nodes and arrows showing replacement, complementarity, or partial substitution between products/technologies |
| `scarcity_axis` | one horizontal or vertical axis ranking scarcity, urgency, pricing power, or supply tightness |
| `industry_logic_comparison` | two-sided comparison canvas with shared dimensions in the center and visual evidence on both sides |
| `value_chain_map` | upstream -> midstream -> downstream chain with profit pool, bottleneck, or control-point markers |
| `causal_chain` | source fact -> mechanism -> market behavior -> financial implication |
| `moat_comparison_canvas` | compare two businesses across market size, expansion elasticity, technical barrier, customer lock-in, and value capture |
| `2x2_positioning` | position companies/products by two strategic axes; label quadrants with implication |
| `timeline_inflection_map` | timeline with inflection points, lead/lag relationships, and expected monitoring windows |
| `supply_demand_map` | supply constraints, demand drivers, inventory/channel state, and price transmission path |
| `capability_stack` | layered capability or technology stack showing dependency and bottleneck layers |

Selection rules:

- If the user asks for "relationship", "substitution", "synergy", "who replaces whom", use `substitution_topology`.
- If the page compares scarcity, urgency, tightness, pricing power, or capacity pressure, use `scarcity_axis`.
- If the page compares two industries or technologies, use `industry_logic_comparison` or `moat_comparison_canvas`.
- If the page explains an investment conclusion from mechanisms rather than exact data, use `causal_chain`, `value_chain_map`, or `timeline_inflection_map`.
- Use `executive_summary_grid` or `thesis_evidence_stack` only when the user explicitly wants a dense memo-style summary or there is no clear visual relationship to encode.

## Density Rules

- Finance decks can be dense; density must be organized, not cramped.
- Finance content pages should be information-dense rather than large-type
  sparse. Do not enlarge body text, icons, or spacing until the page can only
  hold a few short statements; use compact readable type and restore evidence or
  analytical explanation.
- Workpaper density does not require slide density. The registry, data audit,
  and Excel export can hold full support while the main slide shows a sparse
  diagram or one decisive chart.
- Ordinary research pages should read as reviewable claim-plus-evidence pages:
  conclusion title, medium-length analytical paragraph or 2-4 substantive
  bullets, then bottom evidence zone with charts/tables/artifacts.
- The viewpoint paragraph/bullets are part of the research evidence chain. Do not
  compress them into slogan tags or wrap them in decorative cards by default.
- Dense does not mean text-heavy or poster-like. Prefer dominant diagrams for
  mechanism, industry-chain, architecture, causal, scarcity, positioning,
  substitution, supply-demand, technology-roadmap, and business-model pages.
- Investment evidence pages may carry more visible evidence than commercial
  slides. When density is necessary, structure the page as "claim zone +
  evidence zone": a conclusion title, 1-3 substantive bullets, then
  chart/table/artifact panels with clear captions and concise origin-first
  source notes.
- For visual reasoning pages, keep body text to short labels and one-line notes. If more than four text blocks or nodes are needed, convert them into an axis, topology, flow, matrix, or comparison canvas.
- Main narrative visual reasoning pages default to 0-3 visible key numbers.
  Additional proof stays in `archive_evidence_ids`, appendix, or Excel export.
- Use strong column logic and narrow gutters.
- Align chart baselines and table numeric columns.
- Keep source notes small but readable.
- Use 12 pt equivalent as the normal minimum for body text in final slide
  output, with ordinary content body text usually around 12.5-15 pt. Avoid
  title-like body text on content pages.
- Avoid decorative cards on every page; use report-style rules, section captions,
  table headers, and spacing.
- Avoid using rounded rectangles as the default content container. Prefer open
  grids, shared baselines, light rules, axis lines, and subtle background bands.
  Use a framed box only when it groups a true module, and do not put a box around
  every item.
- Avoid pill-shaped headers and oversized rounded badges unless they are inherited from the user's template.
- Keep icons sparse: ordinary research pages use 0 decorative icons by default;
  mechanism or industry-chain diagrams may use a few small line icons. Do not add
  icons to every bullet, KPI, table row, or card.
- Do not use image-only generation for dense tables unless exact overlays are composited after.
- Prefer white or near-white research-report backgrounds with deep navy
  structural anchors and restrained low-saturation blue/gray accents; keep
  chart/table evidence panels white when useful. Avoid dark full-page dashboards
  unless the user asks.
- Avoid the tech launch / consulting infographic / SaaS dashboard / marketing
  poster look unless the user explicitly asks for it.
- Use coral red only for the single most important direct implication, contrast, or
  transition cue; overuse makes the page noisy.
- Quiet secondary data with light gray treatment; reserve saturated accent colors for the critical curve, variance, inflection, or risk signal.

## Chart And Table Rules

- Use charts for evidence whenever the claim depends on trend, comparison,
  rank, share, composition, growth, or inflection.
- Do not use charts/tables merely because the workpaper ledger contains many
  datasets. If the claim is structural, use a visual reasoning pattern and keep
  detailed datasets in the archive.
- Use line charts for time trends and cycles; bar charts for comparison and
  ranking; stacked bars for composition; waterfall/bridge charts for
  attribution; scatter/bubble charts for positioning; pie/donut charts only
  for simple share stories with few slices.
- Use tables for exact assumptions, segment splits, valuation comps, peer
  comparison, or model inputs. Prefer compact three-line tables over boxed
  table grids when the table has a small number of rows/columns.
- Three-line table style: top rule, header rule, bottom rule; no heavy outer
  border, no vertical grid unless needed; numbers aligned by decimal/unit;
  light emphasis only on the one row/column that carries the conclusion.
- Flat institutional table style: blue or gray header, white body, optional
  subtle alternating rows, thin borders/rules, compact spacing, no rounded
  corners, no shadows, no gradients, no badges, and no decorative icons in cells.
- Use multi-panel charts only when each panel answers a distinct investor
  sub-question. Avoid three charts that repeat the same point.
- For combined bar+line charts, specify both axes, units, and series roles:
  bars for amount/volume, line for growth/margin/utilization/share.
- For screenshots or product taxonomies, crop to the meaningful region and
  annotate with one restrained direct callout; do not rely on tiny unreadable
  labels, and do not prefix the callout with generic labels such as
  "关键判断：" or "Takeaway:".
- Do not use icons as a substitute for data. If data are missing, acquire them
  via the data-acquisition workflow or mark the figure as `Needs-Source`; do
  not block waiting for the user.
- Do not use dense tables as a substitute for explanation. If a table proves the
  point but does not help the audience understand the mechanism, keep it in
  appendix/Excel and use a mechanism or chain diagram in the main deck.

## Master Chrome

Institutional finance pages usually need:

- confirmed logo, author/producer name, or institution name when identity policy allows it
- report title or section label
- source note only for research/report pages, user-requested source display, or templates that already reserve a source area
- forecast assumption note when relevant
- no page number unless the user explicitly requires it; a page number printed
  on a reference/template image is not such a requirement — exclude it
  explicitly when prompting with a reference image
- confidentiality / disclaimer marker when requested

Master chrome must be consistent across all pages.
