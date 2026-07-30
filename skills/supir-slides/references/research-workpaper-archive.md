# Research Workpaper Archive

Use this reference for investment, finance, company, industry, macro, market,
fund product, and institutional roadshow decks that need traceable workpapers.
The workpaper archive is the machine-readable source of truth behind
`data_audit.md`; `data_audit.md` remains a human-readable summary.

## Core Rule

Every evidence-bearing deck should maintain a workpaper ledger under
`workNN/data/registry/` before rendering. A slide should not introduce a hard
number, chart, table, source note, or main-deck claim unless the corresponding
registry record exists or the item is explicitly marked `Needs-Source`.
`Needs-Source` is an audit marker, not permission to present an unsupported
item as fact; weaken the wording, frame it as a scenario/monitoring item, move
it to appendix, or omit it from the visible slide.
This does not mean every supporting record must be visible on the slide. The
ledger is the audit layer; the slide should show only the subset needed for
clear communication.

The ledger chain is mode-aware. For quantitative or chart/table pages:

```text
page_id -> claim_id -> figure_id/table_id -> dataset_id -> source_id -> run_id
```

For qualitative, document-backed, or visual-reasoning pages:

```text
page_id -> claim_id -> source_id / archive_evidence_ids -> run_id
```

Do not create placeholder datasets, figures, or tables just to fill the
quantitative chain. Use those IDs only when the page uses structured data,
charts, tables, or displayed key numbers.

## Directory Layout

```text
workNN/
  research_memo.md
  data_audit.md
  argument_map.md
  deck_plan.md
  deck_plan.json
  data/
    registry/
      tool_run_registry.jsonl
      source_registry.jsonl
      dataset_registry.jsonl
      figure_registry.jsonl
      table_registry.jsonl
      claim_registry.jsonl
      page_evidence_registry.jsonl
      needs_source_registry.jsonl
      export_manifest.json
    raw/
    normalized/
    derived/
    charts/
    tables/
    exports/
```

- `raw/`: tool outputs, document-search exports, copied source snippets, and
  unmodified tables.
- `normalized/`: cleaned tabular data with stable columns and units.
- `derived/`: calculated ratios, peer screens, scenario outputs, and other
  transformed data.
- `charts/` and `tables/`: exact chart/table specs referenced by slides.
- `registry/`: JSONL index files. Append one JSON object per line. Use stable
  IDs; do not renumber existing records during edits.
- `exports/`: user-facing audit exports, such as `ppt_workpapers.xlsx`.

## ID Conventions

Use short stable IDs:

| Prefix | Meaning |
| --- | --- |
| `R001` | tool run |
| `S001` | source or provider artifact |
| `D001` | dataset |
| `D101` | derived dataset |
| `F001` | figure, chart, or displayed key number |
| `T001` | table |
| `C001` | claim |
| `P001` | planned page |
| `N001` | unsupported, low-confidence, or needs-source item |

Internal IDs are never rendered visibly on the slide.

## Registry Schemas

### `tool_run_registry.jsonl`

Record every material tool invocation, including failures and fallback paths.

```json
{
  "run_id": "R001",
  "tool": "search_global_data",
  "purpose": "Fetch NVDA annual revenue and net income for peer comparison",
  "query_summary": "NVIDIA NVDA annual income statement revenue and net income for the last 3 fiscal years",
  "status": "success",
  "output_paths": ["data/raw/R001_search_global_data/result.json"],
  "created_source_ids": ["S001"],
  "created_dataset_ids": ["D001"],
  "limitations": "",
  "retrieved_at": "2026-06-13T10:00:00+08:00"
}
```

### `source_registry.jsonl`

Record the provenance chain and visible source label for every source. Prefer
the most original identifiable publisher as the visible source. Keep
intermediate collectors, broker reports, platform tools, and retrieval channels
in the audit fields so the trail is still inspectable.

```json
{
  "source_id": "S001",
  "source_type": "structured_market_data",
  "provider_visible": "Company filings",
  "original_publisher": "NVIDIA",
  "intermediate_publisher": "",
  "retrieval_provider": "Alpha派",
  "provider_internal": "search_global_data",
  "title": "NVDA annual income statement",
  "publisher": "NVIDIA",
  "source_chain": ["NVIDIA", "Alpha派"],
  "publish_date": "",
  "retrieved_at": "2026-06-13T10:00:00+08:00",
  "raw_path": "data/raw/R001_search_global_data/result.json",
  "authority_level": "primary_structured",
  "freshness": "latest_available",
  "limitations": ""
}
```

Visible source selection:

1. If the tool output or referenced document identifies the original publisher
   of the data, set `original_publisher` and make `provider_visible` use that
   original source, not the platform or broker that surfaced it.
2. If a secondary source republishes, cites, or整理s the original data, keep it
   in `intermediate_publisher` and `source_chain`, for example
   `["中指院", "招商证券", "Alpha派"]`; use a concise visible note such as
   `资料来源：中指院，招商证券整理`.
3. If the original source cannot be identified after reasonable inspection of
   the tool result, report, excerpt, chart caption, or source table, fall back
   to the current provider logic: use the broker/vendor/database/platform as
   `provider_visible`.
4. For Alpha Pai / PaiWork platform data, use `provider_visible: "Alpha派"` on
   slides only when no more specific original publisher is available or when a
   platform tool such as `data_analyst`, `doc_searcher`, `search_paipai`, or a
   structured database returns synthesized data without concrete source
   attribution. Keep the exact tool and database details in
   `retrieval_provider`, `provider_internal`, `raw_path`, and
   `tool_run_registry.jsonl`.

### `dataset_registry.jsonl`

Record each normalized or derived table that can support a chart, table, or
claim.

```json
{
  "dataset_id": "D001",
  "name": "nvda_financials",
  "description": "NVDA annual revenue and net income",
  "file_path": "data/normalized/D001_nvda_financials.csv",
  "source_ids": ["S001"],
  "grain": "company-fiscal-year",
  "period_start": "2023",
  "period_end": "2025",
  "unit_policy": "USD mn",
  "verified": true,
  "limitations": ""
}
```

### `figure_registry.jsonl`

Record every chart and displayed key number.

```json
{
  "figure_id": "F001",
  "page_id": "P003",
  "figure_type": "line_chart",
  "title": "NVDA revenue and net income trend",
  "dataset_ids": ["D001"],
  "spec_path": "data/charts/F001_nvda_revenue_profit.json",
  "source_ids": ["S001"],
  "visible_source_note": "资料来源：Company filings",
  "verified": true
}
```

### `table_registry.jsonl`

Record every slide table.

```json
{
  "table_id": "T001",
  "page_id": "P004",
  "table_type": "peer_valuation",
  "title": "AI infrastructure peer valuation comparison",
  "dataset_ids": ["D002"],
  "spec_path": "data/tables/T001_peer_valuation.json",
  "source_ids": ["S002"],
  "visible_source_note": "资料来源：Alpha派",
  "verified": true
}
```

### `claim_registry.jsonl`

Record each main-deck claim and its evidence.

```json
{
  "claim_id": "C001",
  "claim": "AI infrastructure leaders keep stronger revenue growth, but valuation dispersion has widened",
  "page_ids": ["P003", "P004"],
  "evidence_ids": ["F001", "T001"],
  "source_ids": ["S001", "S002"],
  "assumptions": ["Peer set contains comparable AI infrastructure exposure"],
  "counter_evidence": ["Growth may normalize if capex digestion slows"],
  "confidence": "medium",
  "slide_treatment": "main_deck"
}
```

### `page_evidence_registry.jsonl`

Record the final evidence bundle for each page. Separate evidence that is
visible on the page from evidence that stays in the archive.

```json
{
  "page_id": "P003",
  "slide_title": "Revenue growth still separates AI infrastructure leaders",
  "slide_expression_mode": "evidence_page",
  "claim_ids": ["C001"],
  "visible_evidence_ids": ["F001"],
  "archive_evidence_ids": ["T001", "D002", "S002"],
  "figure_ids": ["F001"],
  "table_ids": [],
  "source_ids": ["S001"],
  "needs_source_ids": []
}
```

- `visible_evidence_ids`: the chart, table, key number, screenshot, or artifact
  actually shown on the slide.
- `archive_evidence_ids`: supporting workpaper evidence that proves the page but
  should not be rendered visibly.
- `slide_expression_mode`: use the modes in
  `research-to-slide-expression.md`.

### `needs_source_registry.jsonl`

Record claims or figures that cannot be fully supported.

```json
{
  "needs_source_id": "N001",
  "page_id": "P006",
  "item": "Industry share reaches 35%",
  "reason": "No authoritative industry source found",
  "treatment": "weaken_headline_or_appendix",
  "status": "open"
}
```

## Research Memo

For deep research decks, write `workNN/research_memo.md` after the initial
tool-backed scan and before final page planning. The memo must reference
registry IDs instead of free-floating citations:

```markdown
## Core Thesis
C001: Revenue growth still separates AI infrastructure leaders.
Evidence: F001, T001
Sources: S001, S002
Confidence: medium

## Debate / Counter-Evidence
N001: Capex digestion risk is not yet fully quantified.
Treatment: scenario monitor page, not a firm conclusion.

## Page Implications
- P003 uses C001 and F001.
- P006 frames N001 as a monitoring item.
```

Use `analyst_report` only after material sources and datasets have been
registered. Its output should become or update `research_memo.md`; it must not
introduce new hard numbers without a registry record.

## Excel Export Contract

When the user asks to save or export PPT workpapers as Excel, generate
`workNN/data/exports/ppt_workpapers.xlsx` from the registry and tabular files.
The workbook should include these sheets when data exist:

| Sheet | Contents |
| --- | --- |
| `00_README` | deck title, work directory, generated time, limitations |
| `01_Source_Register` | `source_registry.jsonl` |
| `02_Tool_Runs` | `tool_run_registry.jsonl` |
| `03_Dataset_Register` | `dataset_registry.jsonl` |
| `04_Figure_Register` | `figure_registry.jsonl` |
| `05_Table_Register` | `table_registry.jsonl` |
| `06_Claim_Map` | `claim_registry.jsonl` |
| `07_Page_Evidence` | `page_evidence_registry.jsonl` |
| `08_Needs_Source` | `needs_source_registry.jsonl` |
| `09_Compliance_Notes` | source display, forecast, and wording notes |
| `Dxxx_*` | normalized and derived CSV datasets |

Do not paste long report or filing text into Excel by default. Include source
metadata, short excerpts when available, and local raw paths so high-audit users
can trace back to the original workpapers.

### Use The Excel Skill

Do not implement a custom Excel writer inside `paipai-slides` for normal
workpaper export. When the user asks for an `.xlsx` export, load and use the
dedicated `xlsx` skill unless the runtime has an active Excel editor that
requires an online spreadsheet operation route.

The handoff instruction to `xlsx` should include:

- output path: `workNN/data/exports/ppt_workpapers.xlsx`
- source files: `workNN/data/registry/*.jsonl`, `workNN/data/normalized/*.csv`,
  `workNN/data/derived/*.csv`, and `workNN/data_audit.md`
- required workbook sheets from the table above
- source-tracing requirement: preserve registry IDs and raw file paths; do not
  collapse provenance into vague notes
- formatting expectation: audit workbook, not a presentation deck; make tables
  filterable/readable and keep long raw text out of the workbook by default

Suggested natural-language handoff:

```text
Use the xlsx skill to create a new offline Excel workbook at
workNN/data/exports/ppt_workpapers.xlsx from these workpaper files:
workNN/data/registry/*.jsonl, workNN/data/normalized/*.csv,
workNN/data/derived/*.csv, and workNN/data_audit.md.

Create sheets 00_README, 01_Source_Register, 02_Tool_Runs,
03_Dataset_Register, 04_Figure_Register, 05_Table_Register, 06_Claim_Map,
07_Page_Evidence, 08_Needs_Source, 09_Compliance_Notes, plus one sheet for
each normalized/derived CSV dataset. Preserve all registry IDs, source paths,
provider fields, freshness, limitations, and visible source labels. Do not paste
long report or filing text; include raw paths and short excerpts only when
available.
```
