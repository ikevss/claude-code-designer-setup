# Investment Research PPT SOP

Use this reference when the deck is for financial research, investment
committee discussion, roadshow support, earnings review, strategy research, or
any other audience that expects traceable investment logic.

## Pre-Deck Logic Gate

Do this before choosing templates, layouts, or image style.

1. **300-word thesis brief**
   - Audience: name the decision maker and what they care about.
   - Takeaways: write a small set of conclusions the audience should remember
     after the meeting. As a default, use 2-4; for complex reports, group more
     takeaways under a few higher-level pillars.
   - Decision context: specify whether the deck supports screening, monitoring,
     valuation, allocation, risk review, or client education.
2. **Forward reasoning chain**
   - Source fact / field research -> assumption -> inference -> conclusion.
   - Do not start with a preferred conclusion and backfill evidence.
   - For each major claim, record the weakest link in the chain.
   - For each core claim, create or update an argument-map entry with evidence,
     assumptions, counter-evidence, confidence, and source trail.
   - For finance/research decks, create or update the matching
     `claim_registry.jsonl` record and connect it to applicable workpaper
     records from `research-workpaper-archive.md`: always `source_id` and
     `page_id`, plus `dataset_id`, `figure_id`, or `table_id` when the claim
     uses quantitative data, charts, tables, or displayed key numbers.
3. **Content subtraction pass**
   - Remove material unrelated to the core takeaways.
   - Remove industry common knowledge for expert audiences.
- Remove claims without source support, cross-checks, or working papers.
- Reframe low-confidence claims as scenarios, monitoring items, or risks unless
  the user explicitly wants them as hypotheses.
   - Target: only the strongest 20% of available research should reach the
     main deck; move useful but nonessential detail to appendix.
   - Exception: when the deck content mainly comes from user-provided reference
     material (Word/PDF/Markdown reports, attachments, or pasted context),
     subtraction removes only duplicates, off-topic passages, and
     document-only sections (table of contents, disclaimers, back cover). Do
     not cut the facts, data, and reasoning chain carried by the user's
     material — preserve its information density by default, add pages or move
     secondary detail to appendix instead of deleting, unless the user
     explicitly asks for a condensed deck.

## Outline Lock Before Rendering

After the logic gate and data preparation, follow the Strategy Lock in
`production-deck-workflow.md`: lock the page-by-page outline from
`deck_plan.md` together with the research logic / compliance policy and the
data audit summary (sources, gaps, `Needs-Source` items) and workpaper ledger
status, then generate directly — do not wait for user confirmation; report
these together with the final result.

## Minimum Evidence Gate

Apply this gate before rendering any main-deck investment/research page.
This is a workpaper gate, not a requirement to show all evidence visibly. Use
`research-to-slide-expression.md` to decide what appears on the slide.

### Main conclusion / thesis pages

- Require at least one `claim_id` in `claim_registry.jsonl`.
- Require at least two evidence items when feasible. Prefer one structured
  dataset/chart/table evidence item plus one document, filing, announcement,
  meeting-minutes, or research-view source.
- These evidence items may be archive-only. The slide should show only the
  evidence needed for audience comprehension.
- Require explicit assumptions and at least one counter-evidence or
  disconfirming signal.
- Require a confidence level. If confidence is low, frame the page as scenario,
  monitoring, risk, or appendix rather than a firm conclusion.

### Data chart / table pages

- Require a `figure_id` or `table_id` and a chart/table spec before rendering.
- Require each figure/table to point to `dataset_id` or source records in the
  workpaper ledger.
- Require units, period, frequency where relevant, and visible origin-first
  source policy.
- Use this page type only when the chart/table is the best way to understand
  the claim. If the page is about mechanism, industry chain, causal logic, or
  positioning, keep the table/chart in the workpapers or appendix and render a
  visual reasoning page.

### Analyst view / document-evidence pages

- `search_paipai` can support semantic scan and thematic framing.
- Claims such as "all recent reports", "market consensus", "most institutions",
  or date/institution-filtered coverage require `doc_searcher` or another
  exhaustive retrieval route.
- Separate company/official facts, management commentary, broker views, market
  commentary, and user-provided material in the ledger and slide wording.

If the evidence gate fails, weaken the headline, move the item to appendix,
record a `Needs-Source` item, or ask the user only when the missing evidence
blocks a reasonable professional result.

If the evidence gate passes but the planned page is visually crowded, do not add
more visible data. Move excess evidence to archive/appendix and choose a more
explanatory slide expression mode.

## Research Narrative Spine

Use this sequence as the default story spine unless the user provides another
structure:

1. Decision question, expectation gap, or monitoring problem.
2. Thesis and key assumptions.
3. Evidence by driver: demand, supply, price, margin, capital cycle, policy,
   competitive position, or customer/channel signal.
4. Scenario / payoff / valuation / risk-reward framing.
5. Tracking indicators, disconfirming evidence, and risk factors.

Every page should declare its role in this spine. If a page cannot be mapped to
the spine, it is probably appendix material.

## Buy-Side Page Roles

Page content defaults to decision support. Note the deliberate split: the
**visual layout** defaults to the sell-side research-report page idiom (the
style contract in `institutional-research-style.md`), while the **wording and
page roles** stay buy-side:

- `decision_question`: what portfolio, monitoring, screening, or risk question
  this page answers.
- `thesis_evidence`: one claim with the specific evidence needed to support or
  weaken it.
- `scenario_monitor`: base/upside/downside, triggers, indicators, and what would
  change the view.
- `crosscheck`: chart/table/fieldwork comparison that tests whether a signal is
  real or isolated.
- `positioning`: peer, factor, valuation, or exposure comparison.
- `risk_disconfirming`: what could break the thesis and what to watch.

The sell-side strategy/industry research report page is the default **visual**
benchmark: conclusion-first headline, bold lead-in viewpoint paragraphs, and
1-3 flat charts/tables tiled in the lower evidence zone. Adopt that layout
language by default; what must remain buy-side is the wording — convert
recommendation language into scenario, monitoring, valuation, and risk
language per the Compliance Gate below.

When the user does not provide a template or special style, use
`institutional_research_default` from `institutional-research-style.md`: a
deep-blue cover with white typography plus white/near-white broker-research
content pages using a subtle pale-blue-to-white gradient, generic cool-blue
palette (deep indigo structure, dark/bright blue emphasis, pale-blue light
bands, small coral-red critical accents), and Source Han Sans SC / 思源黑体 plus
Helvetica/Arial/Inter-like compact sans typography. In each page instruction,
summarize this as a short positive Style constraints paragraph and add only the
page-specific constraints.
It is suitable for
investment committee review, mutual fund product launch materials, broker-style
horizontal reports, institutional roadshows, and sales-channel review.

## Dense Finance Page Rules

- Dense pages are allowed; confused pages are not.
- Use conclusion-first headlines that can be read as a complete story when
  scanned page by page.
- Ordinary research pages may use a medium-length analytical paragraph or 2-4
  substantive bullets. Do not over-compress necessary explanation into slogans
  just to make the page look clean.
- Do not solve layout by making body text, icons, or spacing oversized. If a
  content page becomes sparse, reduce scale and restore analytical substance:
  evidence, dates, units, constraints, causal links, or a compact chart/table.
- Use charts for trends, comparisons, market share, and distribution.
- Use tables for nested assumptions, segment breakdowns, valuation comps, and
  forecast models where readers need the calculation grain.
- Evidence panels should answer distinct investor questions. Avoid adding three
  charts that all prove the same point; use panels to triangulate a thesis or
  separate demand, supply, price, margin, and risk drivers.
- Buy-side pages should show the implication: add/trim/watch/avoid language is
  converted into objective scenario, trigger, risk-reward, valuation, or
  monitoring language.
- Prefer compact three-line tables for concise research tables: top rule,
  header rule, bottom rule, no heavy outer border, and numeric alignment by
  unit/decimal.
- Avoid rounded-card grids as the default structure. Use open grid, light
  section rules, axis lines, chart panels, and whitespace for separation.
- Use icons sparingly as semantic anchors; do not attach an icon to every row,
  bullet, or KPI.
- Ordinary analysis/data/table pages default to 0 decorative icons; reserve
  sparse line icons for mechanism, industry-chain, architecture, data-flow,
  capital-flow, or process diagrams.
- De-emphasize background grids, historical reference series, and secondary
  rows with light gray treatment.
- Reserve saturated accent color for the one most important curve, variance,
  inflection point, or risk signal.
- Ordinary content body text usually sits around 12.5-15 pt equivalent at final
  slide size, with 12 pt as the normal minimum; source notes may be smaller only
  if still readable after black-and-white printing. Avoid body text so large
  that it forces the page into a low-information slogan layout.

## Compliance Gate

For financial research pages, default to conservative language and source
discipline.

- Every chart, table, macro number, forecast, and externally sourced statement
  needs an audit trail in `workNN/data_audit.md` and, for finance/research
  decks, the workpaper registry before rendering.
- Visible source notes are required on research/report pages when external
  data appear, but they should be concise and origin-first: company filing,
  government agency, exchange, industry association, original data vendor, or
  user-provided data when those are identifiable. For secondary reports that
  cite or整理 original data, show the original source plus the整理/转引方 when
  useful, e.g. `资料来源：中指院，招商证券整理`. Do not put long report titles,
  URLs, page numbers, query text, or retrieval metadata on the slide unless the
  user/template explicitly asks.
- When the evidence comes from Alpha Pai / PaiWork platform databases,
  structured data, or platform search tools, inspect the source chain before
  rendering. Use `Alpha派` as the visible provider only when no more specific
  original source is available or when tools such as `data_analyst`,
  `doc_searcher`, `search_paipai`, or platform structured databases return
  synthesized data without concrete attribution. Keep exact database, tool,
  document type, source chain, and retrieval metadata in `workNN/data_audit.md`;
  do not write `Alpha派数据库`, `PaiWork数据库`, `内部数据库`, or tool names on the
  slide.
- Forecast pages need visible key assumptions or a reference to the assumptions
  table.
- Avoid absolute or promotional language: guaranteed profit, must rise, risk
  free, all-in, certain buy, no downside, or equivalents in any language.
- Convert action language into objective probability, payoff, valuation,
  monitoring, or scenario language.
- Use "关注", "配置思路", "情景测算", "胜率/赔率", "跟踪指标", and "风险提示"
  when making investment implications.
- Keep an audit trail of final deck, working papers, data extracts, prompt
  metadata, and compliance notes. If a number changes before delivery, update
  both the deck and the supporting source record.

## AI Image Policy For Research Decks

- AI-generated images may improve abstraction, texture, and transition pages,
  but may not create facts, chart values, table values, logos, citations, or
  source notes.
- Generated visuals must be emotionally neutral. Avoid rockets, crashes,
  cliffs, flames, euphoric bull imagery, panic imagery, or any visual that
  implies a trade recommendation.
- For abstract concepts such as compute topology or synthetic biology
  mechanisms, use restrained institutional visuals and exact deterministic text
  overlays.
- When the model cannot preserve text or numbers exactly, composite deterministic
  chart/table/text layers over the generated page.

## Go / No-Go Checklist

Before export, answer all items:

- Logic: are the core takeaways explicit and appropriately grouped?
- Logic: does each conclusion follow from sourced facts and stated assumptions?
- Logic: does each main-deck claim have evidence, assumptions, counter-evidence, and confidence?
- Logic: can each main-deck claim be traced through the applicable workpaper
  chain: quantitative pages through `page_id -> claim_id ->
  figure/table/dataset/source/run`, and qualitative or visual-reasoning pages
  through `page_id -> claim_id -> source/archive_evidence/run`? If it uses a
  documented `Needs-Source` record, is the visible wording weakened, moved to
  monitoring/scenario/risk, or placed in appendix?
- Logic: has expert-audience common knowledge been removed or moved to appendix?
- Layout: are all headlines conclusion-first assertions?
- Layout: do main titles, page titles, and section titles avoid a trailing
  Chinese full stop `。` or English period `.`?
- Layout: are secondary data and grids visually quiet?
- Layout: is the page readable when printed in grayscale?
- Compliance: does every data point have an audit source or `Needs-Source` marker?
- Compliance: if visible source notes are present, do they prefer the original
  source when identifiable and stay concise rather than long citations?
- Compliance: do all forecasts show or reference assumptions?
- Compliance: has absolute / promotional wording been removed?
- Audit: can every displayed number be found in the working files or source log?
