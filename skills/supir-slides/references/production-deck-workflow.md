# Multi-Page / Complex Deck Workflow

## Contents

- Backend Contract
- Core Pipeline
- Reference Loading Order
- Strategy Lock
- workNN Artifacts
- CLI Generation Pattern
- Edit Loop
- Pass Criteria

Use this reference when the user asks for a professional, research, finance,
executive, client-facing, multi-page, data-heavy, or style-consistent
image-based deck.
For quick single-slide generation or small edits, use the lightweight
generation/editing guides instead.

## Backend Contract

`paipai-slides` is the only slide image generation and editing backend for this
skill.

- Do not create a separate image-slide project directory.
- Do not call a raw image model API directly.
- Do not introduce a second `slides/`, `drafts/`, or `exports/` runtime
  structure. Complex edit workpapers may go under `workNN/edits/`.
- Write final pages only through `paipai-slides` CLI commands.

For multi-page or complex tasks, planning artifacts are written under the current
`{pid}/workNN/` directory. Simple single-page generation and simple edits do not
create a work directory.

## Product Page Limit

The product supports at most **80 slides in one deck**. Every multi-page plan,
`deck_plan.md`, `deck_plan.json`, and generation batch sequence must stay at or
below 80 pages for a single deck. If the user asks for more than 80 pages, do
not generate an over-limit deck; explain the 80-page product limit and propose
splitting the work into multiple decks, such as a main report plus appendix,
volume 1/2, or chapter-based decks. For long source documents, preserve
information within this cap by merging, prioritizing, moving details into
appendix pages, or recommending a split.

## Core Pipeline

`Source Material -> PaiWork/Platform Research Scan -> Workpaper Ledger -> Data/Fact Preparation -> Research Memo -> Research-To-Slide Expression -> Strategist -> Render Lock -> Strategy Lock -> Page-Level Evidence Completion -> CLI Generation -> Tool-Backed Visual QA -> CLI Edit Loop -> Validate`

1. Normalize user intent and materials. If the user provided files, run the
   role triage in `pptx-reference-workflow.md` first: style templates →
   per-role sample PNGs for `--ref-image`; content sources → parsed as
   text/data with code, never bulk-rendered to images.
2. For finance or research decks, run the research logic gate and mandatory
   PaiWork/platform data acquisition before page planning. Use `search_paipai`
   and the appropriate structured data tools to ground the outline in real
   investment research, disclosures, roadshow/meeting minutes, macro/industry
   data, and recent commentary unless the user explicitly restricts the work to
   provided materials.
3. For finance or research decks, create the workpaper ledger described in
   `research-workpaper-archive.md`: every material tool call, source, dataset,
   chart/table spec, claim, and page evidence bundle gets a stable registry ID.
   Choose the applicable research pack from `investment-research-packs.md`.
4. Create or continue the current `workNN/`; write `manifest.md`,
   `research_memo.md` when the deck is research-deep, `deck_plan.md`,
   `render_lock.md`, and any needed data/argument files.
5. Before locking the page outline, apply `research-to-slide-expression.md`:
   decide each page's `slide_expression_mode`, visible evidence budget, and
   whether the claim is better explained by a diagram/map/pathway than by
   another chart/table.
6. Lock the page-by-page outline and strategy bundle in `deck_plan.md` /
   `render_lock.md`, then continue directly into generation. Do not stop for a
   user confirmation step unless the user explicitly asked to review the outline
   before generation or the task is blocked by missing critical information.
7. Assemble page prompts from locked facts, layout, and style constraints. For
   each evidence-bearing page, revisit the data acquisition workflow to complete
   missing chart/table specs, qualitative evidence, counter-evidence, and source
   notes before rendering. Each evidence-bearing page must have a
   `page_evidence_registry.jsonl` record or explicit `Needs-Source` treatment;
   only `visible_evidence_ids` need to appear on the slide.
8. Generate pages with `paipai-slides batch-add` when producing multiple pages.
9. Wait for the async task with `paipai-slides task <file> <taskId> --wait`.
10. Run visual QA via the tiled-overview flow in `visual-qa.md` — inspect
   overview sheets, zoom into flagged/sampled pages only, never every page.
   For finance/research pages, QA is tool-backed: cross-check key figures,
   claims, source notes, and freshness against the workpaper registry,
   `data_audit.md`, and the relevant PaiWork/platform tools, not visual
   plausibility alone.
   Write `visual_qa.md`.
11. Fix all collected issues in one `batch-update`; re-check changed pages
    only. Self-initiated rework per slide is capped at two rounds, then keep
    the best version and record residual risk.
12. Run `paipai-slides validate <file>`.

## Reference Loading Order

For a new multi-page or complex deck:

1. If the user provided files (template, old deck, report/document, data),
   read `pptx-reference-workflow.md` and triage each file's role first.
2. If it is an investment, finance, company, industry, macro, or market deck,
   read `data-acquisition.md` before deciding the outline.
3. For investment/research decks, read `investment-research-packs.md` to choose
   the minimum evidence pack and `research-workpaper-archive.md` to create the
   ledger.
4. Read `research-to-slide-expression.md` before page planning so the deck does
   not turn the ledger into dense visible tables on every page.
5. Then read `investment-research-sop.md`.
6. If data is missing or must be traceable, continue the same
   `data-acquisition.md` workflow through page-level evidence completion and QA.
7. Read `strategist.md` and prepare the recommendation bundle.
8. Read `render-lock-template.md` and write `render_lock.md` in the current
   `workNN/`.
9. If the deck is finance-heavy, read `argument-map.md` and
   `finance-layouts.md`.
10. Read `image-renderer.md` before converting page plans into CLI
   `--instruction` strings.
11. Read `slide-generation-guide.md` before submitting generation commands.
12. Read `visual-qa.md` after each generation task completes.
13. Read `bbox-editing.md` and `slide-editing-guide.md` before localized edits.

## Strategy Lock

Before rendering any image, create **one** internal strategy bundle and write it
to `workNN/deck_plan.md` / `workNN/render_lock.md`. This is a planning lock, not
a user approval checkpoint. Continue directly to `batch-add` / `add` after the
bundle is written, unless the user explicitly asked to review the outline before
generation, asked for per-page approval, or critical information is missing.

The internal bundle must contain:

- the page-by-page outline from `deck_plan.md` (each page's role,
  conclusion-first headline/claim, and key content blocks), in readable form
- canvas and aspect ratio
- page count and page roles
- product page limit check: planned pages <= 80, or split recommendation
- audience and use occasion
- identity context: author/producer, audience/recipient, template brand role,
  and visible attribution/source policy
- communication mode
- brand/master/style policy, including whether `institutional_research_default`
  applies as the default preset or a user/template style overrides it
- global content-expression baseline: ordinary content pages default to
  conclusion-first title + middle substantive viewpoint paragraphs/bullets +
  bottom/right evidence artifacts; this baseline applies across templates and
  non-template generation unless the user explicitly asks for another expression
  mode
- default visual reference policy: when `institutional_research_default` applies
  and no user template overrides it, resolve the built-in assets under
  `assets/default-template/` and map page roles to reference images
  (`pptx-slide-01-cover.png`, `pptx-slide-02-contents.png`,
  `pptx-slide-03-section.png`, and `pptx-slide-04-title-page.png`) so image generation is reference-backed rather than prompt-only.
  Existing Alpha/PaiWork marks in the reference screenshots are built-in
  template brand elements: retain them by default, and remove or replace them
  when the user requests brand-free output or a different logo.
- typography signature and hierarchy: font family/tone, distinctive display-title
  class, same-role size levels, and substitution rules for cover, section, page
  title, body, chart labels, table cells, captions, and source notes
- visible wording policy: conclusion/callout text is written directly, without
  visible meta-label prefixes such as `关键判断：`, `核心结论：`, `结论：`,
  `洞察：`, `Takeaway:`, or `So what:`
- density and page rhythm
- chart/table policy
- image rendering/editing policy
- research logic, compliance posture, and data gaps when relevant
- PaiWork/platform research actions already performed before outline lock, plus
  the remaining page-level evidence and QA checks that must use tools later
- workpaper ledger status for finance/research decks: selected research pack,
  registry files created, key `claim_id` / `source_id` links and applicable
  `dataset_id` / `figure_id` / `table_id` links, open `Needs-Source` items,
  and any unavailable data
- research-to-slide expression policy: page-level `slide_expression_mode`, mix
  of visual reasoning vs evidence pages, visible evidence budgets, and which
  evidence stays in archive/Excel rather than on slides

If the user later requests changes, update `deck_plan.md` / `render_lock.md` and
execute against the revised plan. Do not pause repeatedly for every page unless
the user explicitly asked for per-page review.

## workNN Artifacts

Create `work01/` for the first multi-page or complex task on a `{pid}`. Continue the
current `workNN/` for the same request, retries, QA, local fixes, and bbox edit
refinements. Create the next directory (`work02/`, `work03/`, ...) for a new
goal, new multi-page generation, major rewrite, changed audience/theme/data
policy, or explicit re-planning request.

Before reading prior work, inspect each candidate `manifest.md` and load only
the current relevant `workNN/` unless the user asks to compare or restore
history.

Default files for multi-page or complex decks:

- `manifest.md`: task purpose, created/updated time when known, status,
  related task IDs, and whether this work directory is current for the request.
- `deck_plan.md`: page-by-page role, claim, headline, content blocks, chart/table
  needs, source notes, identity context, visual intent, and registry IDs for
  evidence-bearing pages.
- `render_lock.md`: canvas, style preset, palette, typography tone,
  typography signature and hierarchy, master chrome, density, page rhythm,
  identity policy, and data policy.
- `visual_qa.md`: page-level and cross-page QA findings, fixes applied, and
  residual risks.

Scenario files:

- `deck_plan.json`: use for complex multi-page decks, chart/table-heavy decks,
  or when structured tracking is useful.
- `data_audit.md`: source trail, figure registry, chart/table claims,
  `Needs-Source` items, and compliance notes.
- `research_memo.md`: use for deep investment/research decks after the initial
  tool-backed scan; cite `claim_id` and `source_id`, plus applicable
  `figure_id`, `table_id`, and `dataset_id`, instead of free-floating
  citations.
- `argument_map.md`: claim, evidence, assumptions, counter-evidence, confidence,
  and slide treatment for research decks.
- `workNN/data/registry/`: machine-readable workpaper ledger for tool runs,
  sources, datasets, figures, tables, claims, page evidence, and needs-source
  items.
- `workNN/data/raw/`, `workNN/data/normalized/`, `workNN/data/derived/`,
  `workNN/data/charts/`, `workNN/data/tables/`: use when the deck contains data
  extracts, chart specs, or table specs.
- `workNN/data/exports/`: generated user-facing workpaper exports such as
  `ppt_workpapers.xlsx`.
- `edits/`: use for complex bbox/local edit records.
- `qa/`: ordered page copies and tiled overview sheets for whole-deck visual QA.

Do not create `prompts.md` by default. Create `prompt_metadata.md` only if the
user explicitly asks for a full audit pack.

## CLI Generation Pattern

Initialize the bundle first. Always pass `--id` with a short Chinese name
derived from the title (≤16 chars, no dates/timestamps — the runtime appends a
timestamp suffix for uniqueness):

```bash
paipai-slides init --id 贵州茅台投资概览 --title "Deck title"
```

For several pages, use `batch-add` with the canonical batch-size rule from
`SKILL.md`: submit <=30 pages in one batch; for 31-80 pages, split into batches
as close to 30 pages as possible and wait for each batch before submitting the
next. Do not split by chapter or other natural content boundaries when that
would create smaller batches, and do not pass `--concurrency`. Submit
`batch-add` only after `deck_plan` and `render_lock` are ready and each planned
page has a complete, self-contained instruction. Do not use vague placeholders
such as "same style as previous page" or "continue the outline" inside batch
items. Never submit generation for more than 80 pages in one deck.

```bash
paipai-slides batch-add <file> \
  --instruction "Cover structured page instruction..." \
  --instruction "Summary structured page instruction..." \
  --instruction "Analysis structured page instruction..."
paipai-slides task <file> <taskId> --wait --timeout 560
```

Use individual `add --instruction` when:

- the user wants to approve each page before the next one
- one page requires a materially different source/context setup
- retrying or replacing a failed page
- inserting a page into a specific position

After the task finishes, inspect the result fields and run QA. If the output is
`running` after timeout, call `task --wait` again with enough shell timeout.

## Edit Loop

Use `paipai-slides update --instruction` for a single page fix. Use
`batch-update` when several pages need fixes in one pass — put **all** the
edits into **one** `batch-update --items-json`; do not split into small batches
and do not pass `--concurrency` (splitting rules: see the batch-update section
in `SKILL.md`). With editor region context, read `bbox-editing.md`; the Agent
writes only the edit intent and never invents or passes pixel coordinates.

For a local edit:

1. Identify the page and intended region from editor context or user wording.
2. Preserve everything outside the requested scope.
3. If the region contains facts, chart values, or table values, consult the
   current plan/data constraints before editing.
4. Submit `update --instruction`.
5. Wait with `task --wait`.
6. Run local QA on the changed page only; at most one more targeted edit
   (self-initiated rework is capped at two rounds per slide, regeneration
   included), then keep the best version and record the residual issue.

For `batch-update`, create a per-slide fix list before submitting:

- target `slideId`
- current issue or current content
- exact target content or visual state
- preservation constraints
- whether the item is bbox/local, local plus style, or whole-page

Each item instruction must be self-contained. Merge multiple small fixes on the
same slide into one item, then QA every returned item against `visual_qa.md`.

## Pass Criteria

A multi-page or complex deck is complete only when:

- each page has a clear role and conclusion-first headline
- main titles, page titles, and section titles do not end with a Chinese full
  stop `。` or English period `.`
- visible conclusions, callouts, lead-ins, and summary rows use direct wording
  without generic meta-label prefixes such as `关键判断：` or `So what:`
- the final deck has at most 80 pages, or the user was guided to split the work
- generated text, numbers, charts, visible source notes, and logos are not invented
- finance/research pages can trace every displayed hard number, chart, table,
  source note, and main-deck claim through `page_evidence_registry.jsonl` or a
  documented `Needs-Source` record; `Needs-Source` items are not presented as
  firm facts in visible slide wording
- author/producer/department names are shown only when explicitly supported;
  audience or recipient names are not reused as author or data source
- visible source notes follow the deck policy: concise origin-first labels on
  research/report pages, provider fallback only when the original source is
  unavailable, omitted on non-research pages unless requested, with detailed
  provenance retained in `workNN/data_audit.md`
- when a template was provided, pages follow the visual framework recorded in
  `render_lock` (brand, master chrome, layout family, chart/table style); they
  follow the template content framework recorded in `deck_plan` only for
  same-type reuse or when the user explicitly asked to inherit structure,
  writing style, logic sequence, or fixed content slots
- when a template was provided but the user did not explicitly ask to inherit its
  content expression, ordinary content pages still follow the global
  content-expression baseline instead of becoming card grids, icon-per-bullet
  layouts, SaaS dashboards, or marketing infographics
- when no template/style was provided for finance, fund product, broker
  research, or institutional roadshow decks, pages follow
  `institutional_research_default` rather than a tech launch, consulting
  infographic, SaaS dashboard, or marketing poster style
- dense pages remain readable and organized
- cross-page style, chrome, rhythm, and source notes are consistent
- cross-page typography is consistent: same role uses the same font tone, size
  level, and weight across pages
- investment language is framed conservatively when relevant
- `paipai-slides validate <file>` passes
