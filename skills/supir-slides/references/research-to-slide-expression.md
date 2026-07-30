# Research To Slide Expression

Use this reference after `data-acquisition.md` and
`research-workpaper-archive.md`, before `strategist.md` and
`slide-generation-guide.md`, when a deck is investment, finance, company,
industry, macro, market, fund product, or institutional roadshow oriented.

The core principle is:

```text
Workpapers prove the claim. Slides explain the claim.
```

Do not confuse audit completeness with visible slide density. A page can be
fully traceable in the workpaper ledger while showing only one number, one
diagram, or no visible chart at all.

## Three Evidence Layers

| Layer | Purpose | Where it lives |
| --- | --- | --- |
| `workpaper_evidence` | Full proof trail: tool runs, sources, datasets, calculations, claims, counter-evidence | `workNN/data/registry/`, `data_audit.md`, Excel export |
| `visible_evidence` | The small subset shown on a slide: 0-5 key numbers, one chart/table/artifact, or one short source note | slide image |
| `visual_reasoning` | The diagram, topology, chain, map, matrix, or pathway that helps the audience understand the claim | slide image |

Every main-deck claim should have `workpaper_evidence`. Only the evidence needed
for audience comprehension should become `visible_evidence`.

## Slide Expression Modes

Assign every planned page one `slide_expression_mode` before writing the prompt.

| Mode | Use when | Visible data budget |
| --- | --- | --- |
| `visual_reasoning_page` | Mechanism, industry chain, supply-demand path, technology roadmap, causal logic, substitution, competitive position, business model | 0-3 key numbers; no dense table; source note optional unless required |
| `evidence_page` | A precise trend, comparison, ranking, or forecast is the point of the page | 1 main chart/table or 2 small panels; 3-8 key numbers |
| `summary_page` | Executive summary, section summary, takeaways, roadshow story page | 0-4 key numbers; evidence stays in workpapers |
| `appendix_data_page` | Audit detail, full peer table, model assumptions, detailed data dump | Dense tables allowed; not preferred for main narrative |
| `transition_page` | Cover, TOC, section divider, closing | No data unless user/template requires |

Default mix for a professional 20-30 page research deck:

- 25-40% `visual_reasoning_page`
- 25-40% `evidence_page`
- 10-20% `summary_page`
- 10-20% `transition_page`
- appendix pages only when needed

If most pages are `evidence_page`, the deck will feel like a report screenshot.
Rebalance toward `visual_reasoning_page` unless the user explicitly asked for a
data book or dashboard.

## Visible Data Budget

For main-deck pages, default to:

- one dominant visual argument per page
- one primary claim
- 0-5 visible numbers
- at most one main chart/table/artifact, or two compact evidence panels
- one concise origin-first source note only when required
- no long citations, query details, registry IDs, or source trails on the slide

Move extra data to:

- `workNN/data/registry/`
- `data_audit.md`
- exported Excel workpapers
- appendix data pages

## Mode Selection Rules

Use `visual_reasoning_page` when the page answers:

- How does the industry chain work?
- Why does demand transmit to this supplier or segment?
- Where is the bottleneck?
- Which technology path is upgrading?
- How do upstream, midstream, downstream, customer, and product layers connect?
- What is the causal path from capex/policy/price/supply to financial impact?
- How do competitors differ by capability, exposure, or constraint?

Use `evidence_page` when the page answers:

- How large is the market?
- How fast is it growing?
- Who ranks higher?
- How does valuation compare?
- What trend or inflection supports the claim?

Use `summary_page` when the page synthesizes:

- takeaways
- monitoring framework
- risks
- scenario implications
- decision context

Use `appendix_data_page` when completeness matters more than persuasion.

## Visual Reasoning Patterns

Prefer these forms over dense text/table pages when the claim is structural:

- industry chain map
- demand transmission path
- supply-demand-price mechanism
- technology roadmap
- value-chain profit pool
- capability stack
- substitution topology
- scarcity axis
- 2x2 positioning map
- causal chain
- timeline inflection map
- peer capability matrix with sparse labels

Visual reasoning pages are still research pages. Their claims must link to
`claim_registry.jsonl` and source records, but the full proof stays in the
workpapers.

## Page Evidence Registry Fields

When maintaining `page_evidence_registry.jsonl`, separate visible from archive
evidence:

```json
{
  "page_id": "P015",
  "slide_title": "AI服务器PCB产业链：上游材料到下游应用呈金字塔结构",
  "slide_expression_mode": "visual_reasoning_page",
  "claim_ids": ["C006"],
  "visible_evidence_ids": ["F012"],
  "archive_evidence_ids": ["F013", "T004", "D008", "S021"],
  "figure_ids": ["F012", "F013"],
  "table_ids": ["T004"],
  "source_ids": ["S021", "S022"],
  "needs_source_ids": []
}
```

`archive_evidence_ids` prove the page but should not all appear on the slide.

## Prompt Translation Rule

When turning research into a slide prompt:

1. Start from the claim and audience question.
2. Choose `slide_expression_mode`.
3. Select one dominant visual argument.
4. Select only the visible evidence needed for comprehension.
5. Put every other supporting source in workpapers or appendix.

Bad prompt:

```text
Show all data supporting AI server PCB demand: market size, CAGR, CCL prices,
GPU model table, peer valuations, company shares, and five source notes.
```

Better prompt:

```text
Create a visual reasoning page showing the AI server PCB demand transmission
path from GPU accelerator platforms to high-layer PCB, high-speed CCL, copper
foil, and equipment suppliers. Use one small callout with the registered market
size figure F012. Keep supporting peer and material price evidence in the
workpaper ledger, not visibly on this slide.
```

## QA Principle

Do not fail a page because it has few visible numbers. Fail it only when:

- its claim is unsupported in the workpaper ledger
- the visible data it does show is wrong
- the visual reasoning does not explain the claim
- the page is decorative but not explanatory
- the page omits a required source note for externally sourced visible data
