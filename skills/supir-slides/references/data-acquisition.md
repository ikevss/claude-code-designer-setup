# Data Acquisition for Investment Research Decks

This reference governs how image-slides leverages the platform's financial data
infrastructure and PaiWork research tools to collect professional-grade data and
materials. Use it as a **throughout-the-deck research workflow**, not as a
one-time optional lookup. Run it **before** the Strategist phase whenever the
deck involves financial research, company analysis, industry study, macro
themes, or any content requiring traceable quantitative data, then revisit it
during page-level instruction assembly and QA whenever a claim, chart, source,
or data freshness question appears.

Unless the user explicitly says to use only the provided materials or forbids
external/tool research, do not plan an investment/research deck from model
memory alone. Use PaiWork/platform tools to ground the content framework,
outline, page claims, evidence choices, and final QA in real research material.

## Guiding Principles

1. **Active acquisition, not passive intake** — do not rely solely on
   user-provided files. Proactively identify data gaps from the thesis brief
   and fill them using platform tools.
2. **Primary sources first** — company announcements and filings are the
   highest-authority source; roadshow/meeting minutes are first-hand; broker
   reports and commentary are secondary analysis.
3. **Cross-verify key figures** — critical numbers (revenue, margins, guidance)
   must be confirmed from at least 2 independent sources.
4. **Structured + unstructured** — combine quantitative time-series data with
   qualitative research insights for a complete picture.
5. **Freshness matters** — always check the latest available data; stale
   numbers undermine credibility.
6. **Tool-backed planning** — use `search_paipai` and the appropriate structured
   data tools before locking the outline, so the page framework reflects real
   investment debates, recent disclosures, management commentary, and available
   quantitative evidence rather than a generic report template.
7. **Lifecycle coverage** — use tools at three checkpoints: before outline
   planning, before rendering each evidence-bearing page, and during QA.
8. **Ledger first** — for finance/research decks, record material tool calls,
   sources, datasets, figures, tables, claims, and page evidence in the
   workpaper registry described in `research-workpaper-archive.md`. Treat
   `data_audit.md` as a readable summary of that ledger, not the only source of
   truth.
9. **Archive-heavy, slide-light** — complete the evidence trail in workpapers,
   but expose only the visible evidence needed to explain a page. Use
   `research-to-slide-expression.md` to decide which data stay in the archive.

## Data Acquisition Workflow

### Phase 0: Pre-Outline Research Scan

Before writing `deck_plan.md` or deciding the final content framework, run a
research scan using the relevant PaiWork/platform tools:

- Use `search_paipai` for thematic framing, analyst views, roadshow/meeting
  minutes, announcements, and recent commentary relevant to the topic.
- Use `quick_fetch_stock_financials`, `search_cn_marketdata`, or
  `search_global_data` when the topic needs company financials, valuation,
  macro, industry, market, commodity, FX, or global market data.
- Use `doc_searcher` when the outline depends on comprehensive coverage of a
  document set, such as all recent reports on a company, all roadshow minutes,
  or full announcement history.
- Use `data_analyst` when the framing requires screening, ranking, joins,
  calculated ratios, peer groups, or other computed evidence.
- Choose the applicable research pack in `investment-research-packs.md`
  (company, industry/theme, macro/market, overseas/cross-market, fund/roadshow)
  and use it as the minimum evidence checklist.

The pre-outline scan should produce:

- candidate thesis directions and what evidence supports or weakens each one
- recent events, policy changes, disclosures, or management comments that should
  affect the story spine
- likely page roles and evidence pages grounded in available data
- likely visual reasoning pages where a mechanism, industry chain, causal path,
  supply-demand map, technology route, or competitive position explains the
  research better than another visible chart/table
- data gaps, low-confidence claims, and items that should be marked
  `Needs-Source`

Write the resulting research summary into `workNN/research_memo.md` for
research-deep decks and `workNN/data_audit.md` for human-readable audit. Feed
the registered `claim_id`, `source_id`, applicable `dataset_id` / `figure_id`
/ `table_id`, and `needs_source_id` links into `deck_plan.md` /
`argument_map.md` before the Strategist locks the outline.

### Phase 1: Scope Analysis

After receiving the user's topic/thesis, identify the data requirements:

```markdown
## Data Requirements Checklist
- [ ] Target companies (name, ticker, market: A-share/HK/US)
- [ ] Key financial metrics needed (revenue, profit, margins, cash flow, etc.)
- [ ] Valuation metrics needed (PE, PB, PS, EV/EBITDA, etc.)
- [ ] Time series range (quarters/years of historical data)
- [ ] Industry/macro context needed
- [ ] Peer/comparable companies for benchmarking
- [ ] Qualitative research (analyst views, management commentary, catalysts)
- [ ] Charts/tables to be rendered (what data feeds each visual)
```

### Phase 2: Tool Selection And Invocation

PaiWork Agent context already contains detailed tool descriptions, schemas, and
usage examples. This skill should not duplicate those manuals. Select and call
the appropriate available tool according to the evidence need, following the
tool's own current instructions.

Use this routing logic:

- **A-share / domestic standard data** → `search_cn_marketdata` for A-share
  company financials, A-share quotes, A-share indices, and China macro standard
  time series.
- **Global / overseas structured data** → `search_global_data` for HK/US and
  other overseas stocks, global indices, ETFs/funds, FX, crypto, commodities,
  Treasury rates, overseas quote/price/history/financials/valuation/analyst
  data, ETF holdings, SEC filing metadata, 13F summaries, and similar
  standardized tables. Use one clear English query per tool call, split
  different data domains into separate calls, and record limitations when the
  result is a quick standardized snapshot rather than official filing text.
- **Financial snapshot / multi-company comparison** →
  `quick_fetch_stock_financials` for quick valuation, statements, and estimates
  snapshots. Results should become datasets, chart specs, table specs, or source
  records.
- **Macro, industry, market, commodity, FX, index, and time-series data** →
  structured market/macro data tools. Record indicator name, unit, frequency,
  freshness, and provider.
- **Analyst views, announcements, roadshow or meeting minutes, commentary, fund
  reports, thematic research** → `search_paipai` or the relevant PaiWork
  research/search tool.
- **Comprehensive document coverage** → exhaustive document retrieval tools or
  a document-search agent, especially when the outline depends on "all recent"
  reports, minutes, or announcements.
- **Screening, ranking, joins, ratios, custom calculations, peer-group
  construction** → data-analysis tools or a data-analysis agent.
- **Policy, regulatory, overseas company, or public news items outside PaiWork's
  professional databases** → public web search/fetch tools.

Fallback rules:

- If direct `search_cn_marketdata` or `search_global_data` attempts fail twice,
  return incomplete data, or reveal that screening/joins/calculation are needed,
  delegate to `data_analyst`.
- If `search_paipai` is not enough to support "all recent", institution/date
  filters, exact announcement/report/minutes coverage, or consensus/dispersion
  claims, delegate to `doc_searcher`.
- Do not use `search_global_data` as the primary path for A-share data, China
  macro mainline, SEC filing original text/high-granularity XBRL, HKEX
  announcement originals, HK local specialty disclosures, or long-form research
  interpretation.

For large result sets, save structured results to `workNN/data/` or a working
file and summarize only the decision-relevant findings in the main context.
Record the actual tool used, provenance chain, source/provider, freshness, and
any limitations in `workNN/data_audit.md`.

For finance/research decks, also append each material invocation to
`workNN/data/registry/tool_run_registry.jsonl`, register resulting sources in
`source_registry.jsonl`, and register normalized tables in
`dataset_registry.jsonl`. Empty results and fallback decisions should be
registered so audit users can see what was attempted.

For any data obtained through Alpha Pai / PaiWork platform databases or
platform search tools, inspect the result metadata, document caption/source
line, chart/table footnote, report excerpt, or retrieved file to find the
earliest attributable source. Use that original source as the **visible slide
source label** when it is identifiable, and keep Alpha派/PaiWork only as
`retrieval_provider` or `provider_internal` in `source_registry.jsonl` and
`workNN/data_audit.md`. If the original source is not identifiable after
reasonable inspection, or a tool such as `data_analyst`, `doc_searcher`,
`search_paipai`, or a structured platform database returns synthesized data
without concrete attribution, fall back to `资料来源：Alpha派`. Do not render
phrases such as `Alpha派数据库`, `PaiWork数据库`, `平台数据库`, `内部数据库`,
`search_paipai`, or `doc_searcher` in a slide footer.

### Phase 3: Data Organization & Audit

After collection, organize all data into the project structure:

#### `workNN/data/` directory structure

```
workNN/data/
├── registry/
│   ├── tool_run_registry.jsonl
│   ├── source_registry.jsonl
│   ├── dataset_registry.jsonl
│   ├── figure_registry.jsonl
│   ├── table_registry.jsonl
│   ├── claim_registry.jsonl
│   ├── page_evidence_registry.jsonl
│   └── needs_source_registry.jsonl
├── raw/                 # original tool outputs and retrieved document exports
├── normalized/          # cleaned tabular data
├── derived/             # calculated ratios, screens, scenarios
├── charts/              # chart specification files
├── tables/              # table specification files
└── exports/             # generated audit exports, e.g. ppt_workpapers.xlsx
```

#### Chart/Table Spec Format

Every chart or table that will appear in the deck must have a spec file
**before** image rendering begins and a matching `figure_registry.jsonl` or
`table_registry.jsonl` entry:

```json
{
  "page": "P03",
  "type": "line_chart",
  "title": "营收增速持续放缓，但绝对规模仍在扩张",
  "data": {
    "x_axis": ["2021Q1", "2021Q2", "...", "2025Q4"],
    "series": [
      {"name": "营业收入(亿元)", "values": [280.5, 312.8, "..."]},
      {"name": "同比增速(%)", "values": [25.3, 18.7, "..."], "secondary_axis": true}
    ]
  },
  "source": "公司公告，Alpha派",
  "source_ids": ["S012", "S034"],
  "unit": "亿元 / %",
  "so_what": "增速从25%回落至个位数，规模增长进入平台期",
  "visual_notes": "highlight the inflection point in 2024Q2 with the coral-red critical accent"
}
```

#### `workNN/data_audit.md` — Enhanced Format

`data_audit.md` summarizes the machine-readable registry for human review.

```markdown
# Data Audit

## Data Sources Summary
| Source ID | Source Type | Description | Tool Used | Freshness |
|---|-----------|-------------|-----------|-----------|
| S001 | 公司财报 | 目标公司近3年季度财务数据 | quick_fetch_stock_financials | 2025Q4 |
| S002 | 券商研报 | 近3个月深度研报核心观点 | search_paipai (report) | 2025-12 |
| S003 | 路演纪要 | 最新业绩会管理层指引 | search_paipai (roadShow) | 2025-11 |
| S004 | 行业数据 | 行业产销量月度数据 | search_cn_marketdata | 2025-11 |
| S005 | 海外数据 | 美股同业历史价格和分析师目标价 | search_global_data | latest |

## Figure Registry
| Figure ID | Value/Visual | Unit | Period | Source IDs | Verified |
|-----------|-------|------|--------|--------|----------|
| F001 | 3,261.8 | 亿元 | 2025Q4 | S001  | yes |
| F002 | 21.3 | % | 2025Q4 | S001  | yes |
| F003 | ~25 | % | 2026E | S002  | forecast |

## Chart/Table Claims
| Internal Page ID | Visual Type | Data Source IDs | Spec File | Status |
|------|-----------|-------------|-----------|--------|
| P003 | 双轴折线图 | D001 + D004 | workNN/data/charts/F001_revenue.json | Ready |
| P005 | 估值对比表 | D005 | workNN/data/tables/T001_valuation.json | Ready |

## Unsupported / Needs-Source
| Item | Claim | Status | Action |
|------|-------|--------|--------|
| N01 | "市占率提升至35%" | ❌ Needs-Source | 需从行业报告验证 |

## Compliance Notes
- All forecasts marked with "E" suffix and assumption references
- No promotional language in data annotations
- Source trails recorded for every chart/table in `data_audit.md`; visible
  source notes are prepared only for research/report pages, user-requested
  source display, or templates with a source area. Use the most original
  identifiable source when available; otherwise use the concise provider label.
- Alpha Pai / PaiWork platform database or search results are displayed on
  slides as "Alpha派" only when no more specific original source is available;
  detailed database/tool names stay in `data_audit.md`.
- Audience, recipient, or client organizations are not source providers unless
  the user explicitly says they supplied the data. Do not turn "for XX fund" into
  "Source: XX fund research department".
```

For detailed schemas, ID conventions, and Excel export contract, read
`research-workpaper-archive.md`.

### Phase 4: Page-Level Evidence Completion

Before assembling each `batch-add --items-json` item or individual
`--instruction`, inspect the planned page claim and visual. If the page contains
a factual assertion, chart/table, ranking, peer comparison, forecast, management
view, policy reference, market data point, or source note:

- verify that the claim has an argument-map entry and source trail
- fetch or compute the exact data required for the chart/table
- save chart/table specs before rendering
- update the workpaper ledger: `claim_registry.jsonl`,
  `figure_registry.jsonl` / `table_registry.jsonl`, and
  `page_evidence_registry.jsonl`
- separate `visible_evidence_ids` from `archive_evidence_ids`; do not put every
  supporting dataset/source on the slide
- use `search_paipai` / `doc_searcher` to fill missing qualitative evidence,
  counter-evidence, and recent commentary
- use structured data tools for exact numeric values instead of asking the image
  model to invent or infer numbers

If the required evidence cannot be obtained, weaken the headline, mark the item
`Needs-Source`, move it to appendix, or ask the user only when the missing
information blocks a reasonable professional result.

### Phase 5: Tool-Backed QA

During visual QA, use the relevant tools again for factual and freshness checks,
not only visual inspection:

- re-query key figures with the same structured data source or an independent
  source when a rendered value looks wrong or unusually important
- use `search_paipai` / `doc_searcher` to confirm analyst views, management
  commentary, event dates, and document-backed claims
- use `search_global_data` again for overseas/global quotes, prices,
  financials, valuation, analyst data, ETFs, FX, crypto, commodities, or global
  indices when those figures appear on slides
- use public web tools for policy/regulatory/news items outside PaiWork's
  professional databases
- update registry files, `data_audit.md`, chart/table specs, and
  `argument_map.md` when QA finds mismatches, stale data, unsupported claims,
  or missing counter-evidence

No evidence-bearing page should pass QA solely because it "looks plausible".

## Tool Selection Decision Tree

```
User topic / thesis received
│
├─ Involves specific companies?
│  └─ Use structured financial / valuation / quote tools
│
├─ Needs macro / industry time-series?
│  └─ Use structured market, macro, industry, or global data tools
│
├─ Needs analyst views / qualitative research?
│  ├─ Thematic / semantic scan → search_paipai or equivalent PaiWork search
│  ├─ Exhaustive coverage → document-search tools or agent
│  └─ Public news / policy → web search/fetch tools
│
├─ Needs complex computation / screening / ranking?
│  └─ Use data-analysis tools or agent
│
└─ Needs peer comparison data?
   └─ Combine structured peer data with qualitative research search
```

## Integration with Downstream Phases

### → Strategist Phase
Data acquisition results inform:
- **Page count**: more data dimensions = more pages needed
- **Chart/table policy**: structured data availability determines hybrid vs
  deterministic rendering
- **Density strategy**: rich quantitative data supports dense institutional pages
- **Argument map**: each claim now has traceable data backing
- **Identity context**: source providers remain separate from author, producer,
  audience, recipient, and template brand

### → Render Lock
Add to `workNN/render_lock.md`:
```markdown
## data_sources
- primary: company announcements, financial statements
- secondary: broker reports, meeting minutes
- tertiary: news, social media
- data_tool_chain: actual PaiWork/platform tools used for this deck
```

### → Image Rendering
- Chart specs in `workNN/data/charts/` provide exact values for deterministic rendering
- Table specs in `workNN/data/tables/` provide exact cell values
- No chart or table should be rendered without a completed spec file
- Image model prompts reference spec files, not raw data

### → Visual QA
Enhanced QA checks when platform data was used:
- Every rendered number traces back to a Figure Registry entry
- Every chart matches its spec file exactly
- `data_audit.md` records actual data provenance (retrieval tool + source chain
  + original source when identifiable)
- Visible source notes, when used, prefer original-source labels and remain
  concise rather than full citations
- Visible source notes normalize Alpha Pai / PaiWork database-backed evidence
  to "Alpha派" only when the underlying original source is unavailable or the
  result is platform-synthesized without concrete attribution
- Cross-verified figures show consistent values across sources
