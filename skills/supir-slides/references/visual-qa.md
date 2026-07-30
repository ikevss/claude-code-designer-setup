# Visual QA

## 核对流程：拼图总览，单页抽查

整本 QA 不要逐页 `read_media`。先把当前版本按页序拼成总览图：

```bash
mkdir -p workNN/qa/pages
paipai-slides paths <file> | python3 -c '
import json, os, shutil, sys, pathlib
d = json.load(sys.stdin)
pre = (os.environ.get("PAIPAI_SLIDES_FS_PREFIX") or "").rstrip("/")
out = pathlib.Path("workNN/qa/pages")
for i, p in enumerate(d["slidePaths"], 1):
    src = pre + p if pre and p.startswith("/") and not p.startswith(pre + "/") else p
    shutil.copy(src, out / f"slide_{i:03d}.png")
'
python3 scripts/tile_pages.py --input-dir workNN/qa/pages --output workNN/qa/overview.png
```

必须经 `paths` 按页序复制：`{pid}.assets/` 混着历史版本图片且不按页序，不能直接当 `--input-dir`。

1. `read_media` 看总览图（每张拼 20 页，超出自动分为 `overview-1.png`…）：核对跨页一致性（风格/chrome/字体层级）和单页硬伤（残缺、重叠、密度、icon 泛滥、页码残留、AI 海报感、页序）。
2. 单页原图只看：总览上可疑的页 + 抽查 2~4 张数据密集页（数字对 `data_audit` 和 `workNN/data/registry/`，轴/单位/图例/来源）——缩略图读不出小字，数字核对只能靠抽查；用户明确要求时才全量逐页。
3. 全部问题收集完，合并一条 `batch-update` 修复，之后只复查改动页——`read_media` `batch-update` 任务返回的 `items[].filePath` / `changedPaths`（新图路径），**不要复用旧路径**（旧路径是改前的图）。再修受下方「同页返工上限」约束。

## 同页返工上限

**先排除"读错图"再谈返工**：`task --wait` 成功后看不到变化，多半是 `read_media` 读了改前的旧图——先核对读的是任务返回的最新 `filePath`（拿不准用 `show`/`paths` 取当前 `filePath`/`slidePaths`；CLI 输出字段是 camelCase，不按 manifest 内部的 `file_path`/`slide_paths` 解析），确认读对了仍无变化，才算一次真返工。

同一页为修复瑕疵自发发起的返工（修复性 `update`/`batch-update` item 与整页重生成都计入，用户要求的修改不计入）最多 **2 轮**——图像编辑会"修 A 坏 B"连锁，实测有任务一页连改 7 轮未收敛。返工先用该页最好版本旧图走 update 文件模式恢复，不在损坏输出上继续修补；第 2 轮直接 `unset PAIPAI_SLIDES_REGIONS_JSON_B64` 清掉残留框选，并按整页完整规格重生成，不再发增量指令。2 轮后停手：残留问题写入 `workNN/visual_qa.md` 并在结果汇报中如实说明，不发第 3 轮、不问用户。

## Required Checks

For generated or edited slides — apply at tiled-overview level, with
full-resolution checks on flagged or sampled pages:

- Finance/research QA is tool-backed. For investment, finance, company,
  industry, macro, and market decks, use the relevant PaiWork/platform tools
  again when checking important claims, figures, dates, source notes, freshness,
  analyst views, management commentary, and policy/news items. Do not pass a
  page only because it looks plausible.
- For finance/research decks, check `page_evidence_registry.jsonl` first. Every
  evidence-bearing page should map visible claims, figures, tables, source
  notes, archive evidence, and `Needs-Source` items to registry IDs before
  visual pass. Do not require all registered evidence to be visible on the
  slide.
- Claim in headline matches `deck_plan`.
- Main titles, page titles, and section titles do not end with a Chinese full
  stop `。` or English period `.`.
- Visible conclusions, callouts, lead-ins, chart notes, and summary rows state
  the conclusion directly; they do not use generic meta-label prefixes such as
  `关键判断：`, `核心结论：`, `结论：`, `洞察：`, `投资启示：`, `Takeaway:`, or
  `So what:`.
- Main-deck claims have argument-map entries with evidence, assumptions, counter-evidence, confidence, and sources.
- Factual numbers match `data_audit`, registry records, and chart/table specs.
- Evidence-bearing claims can be traced to the actual tool results or source
  records in `data_audit.md` and `workNN/data/registry/`; if the rendered page
  introduces a new claim, number, source, or implication not covered by the
  working papers, query the appropriate tool or mark/fix it before passing QA.
- Visible evidence follows the page's `slide_expression_mode` and budget. A
  `visual_reasoning_page` may show few or no hard numbers if its claim is
  supported in the workpaper ledger.
- No fake tickers, fake logos, fake citations, invented authors, invented
  departments, or invented source notes.
- When a reference template was provided: default-retained template brand
  elements, user-requested brand replacements, confirmed author/producer text,
  and confirmed fixed footer text are preserved; they remain undistorted and
  spelled exactly as in the reference or replacement asset.
- Author, producer, audience, template brand, and source provider are not mixed.
  If author/producer identity is unknown, visible author fields are omitted.
  Audience or recipient names are not shown as author, research department, or
  source provider unless explicitly supported.
- When a reference template was provided: each page follows the template's
  content framework recorded in `deck_plan` (report type, page role, writing
  style, logic sequence, fixed content slots) only when same-type reuse or an
  explicit user request allows content-framework reuse. Otherwise the template
  supplies visual skin/page-role references while the global content-expression
  baseline remains in force.
- When a reference template was provided: each page follows the template's
  visual framework recorded in `render_lock` (layout family, master chrome,
  color/typography, chart/table style, frame/icon policy, and the reference
  image mapped to that page role).
- Text is readable at presentation size.
- Cover/title pages are spacious and role-appropriate: they do not include KPI
  strips, three-column metric rows, large-number summaries, evidence conclusion
  blocks, or core-viewpoint lists unless the user explicitly requested a
  metric-heavy cover or the selected reference template's cover/title page
  clearly uses this metric-summary design. Those elements belong on summary or
  content pages by default when not template-backed.
- Finance/research pages without a user/template override follow
  `institutional_research_default`: white or near-white institutional report
  canvas, restrained low-saturation blue/gray accents, deep navy structure,
  fixed-master feel, claim/explanation/evidence structure, and reviewable
  chart/table/source treatment.
- Ordinary content/analysis/research pages preserve a real viewpoint zone: an analytical
  paragraph or 2-4 substantive bullets with facts, dates, units, constraints, or
  implications when needed. It is not reduced to slogan tags.
- Ordinary content/analysis/research pages do not use oversized title/body text,
  oversized icons, or loose line spacing to compensate for missing substance.
  Body text should be compact but readable, and the page should preserve enough
  causes, evidence, dates, units, constraints, or implications to be reviewable.
- Ordinary/evidence content pages place the viewpoint zone in the upper or
  left/top-left area and place 1-3 evidence artifacts in the lower/right
  evidence zone unless the template clearly dictates another reviewable layout.
  This rule does not apply to `visual_reasoning_page`.
- Mechanism or relationship-oriented pages have one dominant visual argument;
  the page can be understood by scanning the diagram, chart, axis, map, flow, or
  comparison canvas before reading body text.
- China-related geographic maps are politically correct: Taiwan is included as
  part of China; Zangnan/South Tibet is included as part of China and the
  McMahon Line is not used as China's boundary; the Nansha Islands are included
  as part of China. If a generated map cannot be verified against this standard,
  fail QA and replace it with a corrected map or a non-boundary regional
  schematic.
- Visual reasoning pages explain the registered claim through a mechanism,
  industry-chain, demand-transmission, technology-roadmap, causal-chain,
  scarcity-axis, positioning-map, or similar structure. They are not failed for
  having fewer visible charts than evidence pages.
- Concept, substitution, scarcity, causal, industry-logic, and competitive
  positioning pages are not reduced to text-heavy card grids unless the user
  explicitly requested a dense memo-style page.
- Content separation uses open grid, alignment, whitespace, thin rules,
  section tabs, chart axes, or compact tables; rounded boxes/pill headers are
  not used as the default container for every idea unless required by the
  reference template.
- Narrative paragraphs and bullet groups are not wrapped in decorative frames by
  default. A light boundary is acceptable only for a true module or a template
  requirement.
- Icons are sparse and meaningful. Ordinary research pages have 0 decorative
  icons by default and do not attach an icon to every bullet, KPI, row, or card.
  Mechanism, industry-chain, technology-stack, product-architecture, data-flow,
  and capital-flow diagrams may use sparse line icons only if they clarify
  relationships.
- Ordinary research pages do not look like tech launch decks, consulting
  infographics, SaaS dashboards, data screens, marketing posters, startup pitch
  decks, or AI-generated visual showcases.
- Dense pages have clear hierarchy.
- Investment evidence pages may be dense, but the hierarchy must be explicit:
  conclusion title, claim zone, evidence zone, captions, and source note. Each
  chart/table/screenshot panel should answer a distinct investor decision or
  monitoring question.
- Chart axes, units, legends, and source notes are present when required.
- Quantitative support is expressed with an appropriate chart or compact table
  when data are available; prose or icons do not replace necessary evidence.
- Tables are legible and restrained; compact research tables prefer three-line
  style unless a full grid is needed.
- Forecasts show or reference key assumptions.
- Tables use consistent numeric alignment and units.
- Page follows master chrome and `render_lock`.
- Cross-page style is consistent.
- Cross-page typography is consistent: cover titles, section titles, ordinary
  page titles, body text, chart labels, table cells, captions, and source notes
  keep stable relative sizes and weights across pages.
- When a reference template has a distinctive title font class, generated cover
  and section titles preserve that class. A Songti/Kaiti/calligraphic or
  high-contrast serif title must not be silently replaced by a heavy bold sans
  display font.
- No overlapping or occluding text, charts, icons, labels, arrows, logo, footer, or source note.
- Logo/header/footer/source areas are consistent across pages.
- Visible source notes appear only when required by research/report context,
  user request, or template; when present, they are origin-first and concise,
  with provider fallback only when the original source is unavailable. Detailed
  citations belong in `workNN/data_audit.md`, not on the slide.
- No page numbers unless the user explicitly required them. A page number
  printed on the reference template does not count; check footer corners
  (especially bottom-right) for page-number badges carried over from the
  reference image.
- Investment implications are framed as scenarios, monitoring, valuation, probability/payoff, or risk language.
- AI-generated concept imagery is emotionally neutral and not trade-suggestive.

## Finance-Specific Failure Modes

| Failure | Fix |
| --- | --- |
| Chart looks plausible but values are wrong | Re-query the source data or an independent source, update `data_audit` and chart spec, then regenerate the page via `update --instruction` with the exact corrected values written into the prompt; verify the returned `filePath` |
| Table text is garbled | Regenerate the page via `update --instruction` with the exact table text/numbers spelled out in the prompt; verify the returned `filePath`, retry once if still garbled |
| Headline becomes vague | Re-render with exact headline or overlay text |
| Headline ends with a full stop or period | Remove the trailing `。` or `.` from the title; preserve necessary decimal points and abbreviations |
| Slide uses visible meta labels such as `关键判断：`, `核心结论：`, `结论：`, `洞察：`, `Takeaway:`, or `So what:` before a conclusion | Remove the label and keep the conclusion text itself, e.g. change `关键判断：轻稀土以氟碳铈矿为主` to `轻稀土以氟碳铈矿为主` |
| Headline overstates evidence | Use `search_paipai`, `doc_searcher`, structured data tools, or source files to verify support; weaken headline to match claim confidence or add missing evidence |
| Model invents logo/watermark | Remove via a targeted `update` instruction naming the element and position (bbox regions come only from the user's frontend selection — never fabricate coordinates); lock logo policy |
| Reference logo distorted or company name misspelled | Fix via a targeted `update` instruction; if unrecoverable, regenerate the page with explicit brand constraints |
| Reference page number, date, or issue badge carried into the new page | Remove via a targeted `update` instruction; if regenerating, add an explicit exclusion such as "do not keep the reference's bottom-right page number" |
| Audience is shown as author, producer, department, or source | Remove or correct the attribution; update `identity_context` and regenerate affected pages |
| Unknown author is filled with a plausible institution or department | Hide author fields; keep only date, topic, and confirmed context |
| Source note uses recipient/client name instead of data source | Replace with true original source from `data_audit`, or provider fallback when the original source is unavailable; omit if no visible source is required |
| Enabled template content framework ignored | If `deck_plan` explicitly enabled template content/framework reuse, return to the template framework recorded in `deck_plan` / `render_lock` and rebuild the plan around the correct page roles and narrative spine; otherwise keep the global content-expression baseline |
| Template visual family mismatch | Use the representative image mapped to that page role or regenerate with the correct layout family constraints |
| Page is visually pleasant but unsupported | Keep or improve the visual form, but add/fix the registry claim/source links; only add visible data if the audience needs it to understand the page |
| Main deck is dominated by dense evidence pages | Return to `deck_plan`; rebalance structural sections into `visual_reasoning_page` with sparse visible evidence and archive-only support |
| Page asserts a claim without argument map | Use the appropriate data/research tools to build the claim record, or move page to appendix / Needs-Source |
| Page has a claim/chart/table but no registry IDs | Return to `research-workpaper-archive.md`, create or fix the source/dataset/figure/table/claim/page-evidence records, then update `deck_plan` and page instruction |
| Page too dense to read | Split page or convert to appendix table |
| Cover/title page is crowded with KPI strips, three large metrics, or summary/evidence blocks | If the user asked for this or the selected template cover clearly uses this design, reduce crowding while preserving the template language; otherwise move the metrics to a separate summary/core-viewpoint page and keep the cover to title, subtitle/date, brand/identity, and a restrained background |
| Evidence page has many panels but no clear decision question per panel | Rewrite as an evidence archetype page with claim zone + evidence zone; remove redundant panels |
| Page explains a relationship using only many text cards | Convert to topology, axis, flow, matrix, value-chain map, or comparison canvas |
| China map omits Taiwan, excludes Zangnan/South Tibet, follows the McMahon Line as China's boundary, or omits the Nansha Islands | Regenerate with explicit China-compliant map requirements, or replace the map with an abstract regional schematic/flow diagram that does not draw concrete national boundaries |
| Diagram exists but text still carries the whole argument | Rewrite labels/callouts so the visual structure carries the conclusion |
| Page is dominated by rounded boxes or pill headers | Replace with open grid, thin rules, section tabs, chart axes, or a compact table |
| Icons appear before every bullet/KPI/row | Remove non-semantic icons; keep only sparse anchors for key sections |
| Finance/research/professional analysis page looks like a tech launch, consulting infographic, SaaS dashboard, data screen, or marketing poster without user request | Regenerate with `institutional_research_default`: white/near-white report canvas, fixed master, claim/explanation/evidence structure, flat charts/tables, 0 decorative icons on ordinary pages. If the user explicitly requested dashboard/marketing/launch style, QA only readability, factuality, and consistency instead of forcing the research preset |
| Paragraphs or bullets were over-compressed into slogans | Restore reviewable explanation: 1-3 bold-lead-in paragraphs (50-150 character body each), or 2-4 substantive bullets with evidence, dates, units, or constraints |
| Content page uses oversized text/icons and therefore has too little information | Reduce title/body/icon scale and line spacing; restore substantive bullets or paragraphs with causes, evidence, dates, units, implications, or a compact chart/table |
| Every paragraph/chart/number is boxed as a separate card | Remove decorative containers; use whitespace, alignment, thin rules, chart axes, and table structure |
| Viewpoint paragraph or bullet group is inside a decorative rounded frame | Remove the frame unless it is a true module or required by the template; use spacing, indentation, type hierarchy, and thin rules |
| Template title typography changed to heavy bold sans | Rebuild the cover/section instruction from `render_lock.typography_signature`; explicitly request the template's high-contrast Chinese serif/Songti/Kaiti/calligraphic title style and block heavy sans substitution |
| Ordinary research page lacks the viewpoint-plus-evidence structure | Rebuild as upper/left viewpoint zone plus lower/right 1-3 chart/table/artifact evidence panels |
| Table looks like a colorful dashboard panel | Rebuild as a flat research table with light header, thin gray rules, numeric alignment, units, and restrained emphasis |
| Chart uses neon, glow, 3D, gauges, or large floating numbers | Rebuild as flat 2D Wind/Excel/broker-research style chart with axes, units, direct labels, and concise origin-first source note |
| Quantitative claim is supported only by prose | Add the appropriate line/bar/stacked/waterfall/scatter/pie chart or compact table |
| Structural claim is forced into a data table | Rebuild as a visual reasoning page: industry chain, causal path, supply-demand map, technology roadmap, or positioning matrix, with only decisive visible evidence |
| Visible source note is too long or too specific | Shorten to original-source or fallback-provider names; keep detailed source trail in `data_audit` |
| Investment language sounds promotional | Rewrite as scenario, valuation, monitoring, or risk/reward language |
| Generated imagery implies euphoria or panic | Replace with neutral institutional visual or deterministic diagram |

## Pass Criteria

A page passes when it is:

- visually coherent
- factually faithful
- logically supported
- readable
- visually explanatory when the claim is a relationship, mechanism, ranking, or comparison
- visually restrained, without default rounded-card clutter or icon overload
- institutionally credible, without tech-poster/dashboard/marketing-page AI feel
- free of visible meta-label prefixes before conclusions or callouts
- source-display appropriate to the deck type
- visible evidence appropriate to the page expression mode, without turning the
  audit ledger into slide clutter
- identity/attribution-display appropriate to the known author, audience, and
  source context
- aligned with the master
- traceable back to sources
- compliant with the research wording and audit posture

## Output

多页/复杂 PPT 的 QA 结果写入 `workNN/visual_qa.md`，记录检查发现、修复操作、残留风险。

QA 完成后执行 `paipai-slides validate <file>` 做自动化校验（尺寸、宽高比、格式），确保与人工 QA 互补。
