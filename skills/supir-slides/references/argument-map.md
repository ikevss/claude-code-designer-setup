# Argument Map

Use this reference for financial research decks where content quality, logic,
and evidence matter more than visual polish. The argument map is the bridge
between research workpapers and slide design.

## Purpose

Every core claim should be traceable to evidence, assumptions, counter-evidence,
and confidence. Do this before rendering slides. If a claim cannot be mapped,
it should be weakened, moved to appendix, marked `Needs-Source`, or removed.
For finance/research decks, mirror or export every main-deck claim into
`workNN/data/registry/claim_registry.jsonl` using the schema in
`research-workpaper-archive.md`.

## Claim Record

Use this structure in `workNN/deck_plan.md`, `workNN/deck_plan.json`, or a separate
`workNN/argument_map.md` when the deck is complex.

```markdown
## Claim ID: C01

- Claim:
- Role in deck: thesis / evidence / model / valuation / risk / appendix
- Page(s):
- Evidence:
  - E01: fact, metric, interview note, filing excerpt, dataset, or chart spec
  - E02:
- Sources:
  - source file, URL, database, working paper, user-provided note, or
    `source_id` from `source_registry.jsonl`
- Registry links:
  - claim_id:
  - page_ids:
  - evidence_ids: figure_id / table_id / dataset_id
  - source_ids:
- Assumptions:
  - A01:
  - A02:
- Inference:
  - How the evidence and assumptions lead to the claim.
- Counter-evidence / disconfirming signals:
  - What would weaken or falsify this claim?
- Confidence:
  - high / medium / low
- Confidence rationale:
  - Explain source quality, triangulation, sample size, freshness, and model sensitivity.
- Slide treatment:
  - main deck visual reasoning / main deck evidence page / summary page /
    appendix data page / omit / Needs-Source
- Visible evidence plan:
  - visible_evidence_ids:
  - archive_evidence_ids:
  - visible data budget:
```

## Confidence Guidance

- `high`: multiple independent sources, recent data, low model sensitivity, and
  clear causal or accounting link.
- `medium`: credible evidence but limited triangulation, moderate sensitivity,
  or a timing / attribution uncertainty.
- `low`: single-source, anecdotal, stale, highly model-sensitive, or dependent
  on unverified assumptions.

Low-confidence claims may still appear in research decks, but they should be
framed as monitoring items, scenarios, or risks rather than firm conclusions.

## Page-Level Rule

Every main-deck page needs at least one mapped claim. Evidence-heavy pages may
map several claims, but avoid mixing unrelated claims on the same page. If a
page contains only context, background, or education for an expert audience,
move it to appendix unless the user explicitly asks for it.

Each evidence-bearing main-deck page should also have a
`page_evidence_registry.jsonl` record linking visible page content to
`claim_id`, visible evidence, archive evidence, and `source_id`. If a page has
a hard number or sourced claim but no registry link, it should not pass QA. Do
not require every evidence item for a claim to appear visibly on the slide.

## Red Flags

- Claim has evidence but no explicit assumption.
- Claim has assumptions but no evidence.
- Claim has no counter-evidence or falsification signal.
- Claim confidence is high but depends on one source.
- Page headline is stronger than the mapped claim.
- Visual emphasis makes a low-confidence claim look definitive.
- A main-deck claim has no `claim_registry.jsonl` entry.
- A page contains a chart/table but no `figure_id` / `table_id` or spec path.
- A structural claim is forced into a dense chart/table page when a visual
  reasoning treatment would explain it better.
