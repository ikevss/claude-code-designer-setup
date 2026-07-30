# Template Library Workflow

Use this reference when the user asks to save, reuse, list, inspect, delete,
insert, or set defaults for uploaded slide templates. The library is a
workspace-level cache of parsed template intermediates; it does not replace the
`paipai-slides` deck bundle format.

## Library Location

The fixed library prefix is:

```text
/workspace/.paipai-slides/templates/
```

Default layout:

```text
/workspace/.paipai-slides/templates/
  index.json
  latest.json
  default.json
  tpl_YYYYMMDD_HHMMSS_ab12cd34/
    template.json
    source/
    rendered_pages/
    selected_refs/
      cover.png
      toc.png
      section.png
      content.png
      closing.png
    brand_assets/
      logo_primary.png
    overview.png
    ooxml.json
    extracted_images/
```

`index.json` lists all templates. `latest.json` points to the newest inserted
template. `default.json` exists only when the user has set a default.

## Management Tool

The library is always at `/workspace/.paipai-slides/templates/`. Resolve the skill dir **once** (deeptask injects `$PAIPAI_SLIDES_SKILL_DIR`; the `find` is a fallback for older images / local use), then always call the tool by absolute path — never `cd <guessed dir> && python3 scripts/...` (a wrong `cd` is silently swallowed by `&&`):

```bash
SD="${PAIPAI_SLIDES_SKILL_DIR:-$(find /workspace/skills -maxdepth 5 -type d -name paipai-slides -print -quit)}"
test -n "$SD" || { echo "paipai-slides skill dir not found"; exit 2; }

python3 "$SD/scripts/template_library.py" list
python3 "$SD/scripts/template_library.py" get latest
python3 "$SD/scripts/template_library.py" get default
python3 "$SD/scripts/template_library.py" get <template-id>
python3 "$SD/scripts/template_library.py" get <template-id> --assets-only
python3 "$SD/scripts/template_library.py" get <template-id> --resolve-paths
python3 "$SD/scripts/template_library.py" set-default <template-id>
python3 "$SD/scripts/template_library.py" clear-default
python3 "$SD/scripts/template_library.py" remove <template-id>
python3 "$SD/scripts/validate_template_profile.py" <template-dir-or-template.json>
```

`list` on an empty / uninitialized library prints no templates (the tool defaults to an empty index) — that is **not** an error.

**Failure semantics (important):** only say "template does not exist" when `list` ran and the name/id isn't in it. If `$SD` cannot be resolved, or a command fails to run, say "**template library query failed (retryable)**" — never "does not exist".

Insert a newly parsed template:

```bash
# resolve $SD as in "Management Tool" first:
python3 "$SD/scripts/template_library.py" insert \
  --display-name "华泰个股研究模板" \
  --deck-type "个股研究" \
  --source-file "/workspace/tmp/upload/template.pptx" \
  --rendered-dir "/workspace/tmp/upload/template.pages" \
  --overview "work01/template_overview.png" \
  --ooxml "work01/template_ooxml.json" \
  --ref cover="/workspace/tmp/upload/template.pages/slide_01.png" \
  --ref toc="/workspace/tmp/upload/template.pages/slide_02.png" \
  --ref section="/workspace/tmp/upload/template.pages/slide_03.png" \
  --ref content="/workspace/tmp/upload/template.pages/slide_05.png" \
  --brand-asset logo_primary="work01/brand_assets/logo_primary.png" \
  --style-layer-json "work01/template_style_layer.json" \
  --content-layer-json "work01/template_content_layer.json"
```

Use `--set-default` when the user explicitly asks to make the inserted template
the default. The tool deduplicates by source SHA-256: if the same source PPT/PPTX
already exists, `insert` reuses the existing archive and updates `latest.json`
instead of failing. Use `--allow-duplicate` only when the user explicitly wants a
separate copy of the same source file.

After inserting or hand-editing a template profile, run:

```bash
python3 scripts/validate_template_profile.py "<template-dir-or-template.json>"
```

The validator allows incomplete templates: missing canonical roles are warnings,
not hard failures, because many real templates lack a TOC, section divider, or
closing page. Broken asset paths, missing cropped logo files, malformed
`brand_elements`, stale soft-brand policy markers, and legacy font markers are
reported so they can be fixed before reuse. Use `--strict` only when preparing a
curated default template where warnings should block packaging.

## Natural Language Routing

When the user asks:

先按 Management Tool 解析 `$SD`，下面都用 `python3 "$SD/scripts/template_library.py" …`：

- "列出模板 / 有哪些模板 / 某模板在不在" → `list`
- "默认是哪个 / 最新是哪个" → `get default` / `get latest`
- "看看某个模板 / 获取模板信息" → `get <id|name|latest|default> --assets-only`，只向用户给出原始 PPT/PPTX 和 `overview.png`
- "查看模板完整档案 / 调试模板 manifest" → `get <id|name|latest|default>`，仅在用户明确要内部档案时使用
- "删除/移除某个模板" → `remove <id|name>`
- "把某个模板设为默认" → `set-default <id|name>`
- "取消默认模板" → `clear-default`
- "保存/插入/归档这个模板" → 解析模板后 `insert …`
- "用最新上传的模板" → `get latest --assets-only`
- "用我的默认模板" → `get default --assets-only`

For ambiguous names, list templates first and choose the best exact match by
display name, deck type, tags, and recency. Ask only if two candidates are truly
indistinguishable.

When the user asks about an archived PPT template, do not expose internal
implementation assets by default. The normal user-facing answer should include
only:

- the copied original PPT/PPTX under `source/`
- `overview.png`

Do not show `template.json`, `ooxml.json`, `rendered_pages/`, `selected_refs/`,
or `extracted_images/` unless the user explicitly asks for the full archive,
debug details, or implementation internals.

## What To Store

Archive all assets needed to reuse the template without relying on temporary
upload paths:

- source file when available, copied under `source/`
- selected representative reference images under `selected_refs/`
- rendered pages under `rendered_pages/` when size is reasonable
- confirmed cropped brand assets, such as logos, under `brand_assets/`
- `overview.png` from `tile_pages.py`
- `ooxml.json` from `parse_ooxml.py --json` when source is PPTX/PPT
- extracted image assets when `parse_ooxml.py --extract-images` was used
- `template.json`, containing structured style/content/reuse metadata

`overview.png` is for human/agent review, auditing, and re-selecting
representative pages. Do not use it directly as `reference_image` for slide
generation.

## Page Role Vocabulary

Use five canonical page roles for template references:

| Canonical role | Meaning | Common aliases |
| -------------- | ------- | -------------- |
| `cover` | Cover page | - |
| `toc` | Table of contents / agenda | `contents`, `agenda` |
| `section` | Chapter divider / section transition | `chapter`, `section_divider` |
| `content` | Ordinary content page, including text, chart, table, evidence, and diagram pages | `title_page`, `content_text`, `content_chart`, `content_table`, `content_diagram`, `diagram`, `evidence`, `chart_evidence` |
| `closing` | Closing, thank-you, contact, or disclaimer page | `end`, `thanks`, `disclaimer` |

`template_library.py insert` preserves legacy alias keys for compatibility, but
also fills the canonical key when an alias is supplied. Prefer storing and
planning with the canonical roles; use aliases only as secondary labels or
subroles in notes. If a template has multiple content variants, pick the most
generic content page for `content` and record the variants in
`style_layer.layout_features` rather than expanding the top-level role list.

Supported `content` subroles are currently:

- `title_page`: light title/content opener that is not a cover.
- `content_text`: ordinary text or viewpoint page.
- `content_chart`: chart-led evidence page.
- `content_table`: table-led evidence page.
- `content_diagram` / `diagram`: mechanism, flow, industry-chain, or reasoning diagram page.
- `evidence` / `chart_evidence`: evidence-heavy page that may contain charts,
  tables, screenshots, or compact proof panels.

These subroles may appear as alias keys in `assets.selected_refs` or
`style_layer.page_role_map` when a template genuinely provides different
content layouts. The canonical `content` key remains the general fallback for
ordinary pages. Do not create new top-level roles for every visual variant; use
`style_layer.layout_features`, `content_layer.page_slot_map`, or notes to record
additional nuance.

Templates are allowed to omit roles. When a planned role has no exact
reference, resolve in this order:

1. Exact role or alias reference, such as `content_chart` for a chart page.
2. Canonical role fallback, such as `content`.
3. Nearest visual neighbor: `toc` can fall back to `content`; `closing` can fall
   back to `content` or `cover`; `section` can fall back to `cover`; specialized
   content pages can fall back to generic `content`.
4. Skill default references or `institutional_research_default` when no usable
   template reference exists.

The fallback must be recorded in `render_lock.md` or the generation plan so QA
knows whether a page intentionally reused a nearby template role.

## Template Profile Contract

`template.json` must keep visual style and content framework separate:

```json
{
  "id": "tpl_20260611_153012_ab12cd34",
  "display_name": "华泰个股研究模板",
  "deck_type": "个股研究",
  "tags": ["research", "equity"],
  "assets": {
    "overview": "overview.png",
    "ooxml": "ooxml.json",
    "brand_assets": {
      "logo_primary": "brand_assets/logo_primary.png"
    },
    "selected_refs": {
      "cover": "selected_refs/cover.png",
      "toc": "selected_refs/toc.png",
      "section": "selected_refs/section.png",
      "content": "selected_refs/content.png",
      "closing": "selected_refs/closing.png"
    }
  },
  "style_layer": {
    "canonical_page_roles": ["cover", "toc", "section", "content", "closing"],
    "page_role_aliases": {
      "contents": "toc",
      "agenda": "toc",
      "chapter": "section",
      "section_divider": "section",
      "title_page": "content",
      "content_text": "content",
      "content_chart": "content",
      "content_table": "content",
      "content_diagram": "content",
      "diagram": "content",
      "evidence": "content",
      "chart_evidence": "content",
      "end": "closing",
      "thanks": "closing",
      "disclaimer": "closing"
    },
    "page_role_map": {
      "cover": "selected_refs/cover.png",
      "toc": "selected_refs/toc.png",
      "section": "selected_refs/section.png",
      "content": "selected_refs/content.png",
      "closing": "selected_refs/closing.png"
    },
    "brand_elements": [
      {
        "kind": "logo",
        "asset": "brand_assets/logo_primary.png",
        "source_page_role": "cover",
        "source_page": 1,
        "bbox_px": [90, 70, 260, 130],
        "padded_bbox_px": [78, 58, 272, 142],
        "position": "top-left",
        "size_ratio": "about 10% slide width",
        "visible_text": "XX证券",
        "identity": "template_brand",
        "source": "vision_crop",
        "retain_policy": "retain_by_default",
        "confidence": 0.92
      }
    ],
    "palette": [],
    "typography_tone": "",
    "typography_signature": {
      "cover_title": "",
      "section_title": "",
      "page_title": "",
      "body": "",
      "chart_axis_label": "",
      "table_cell": "",
      "caption_source_note": "",
      "avoid_substitution": ""
    },
    "typography_hierarchy": {
      "cover_title": "",
      "section_title": "",
      "page_title": "",
      "body": "",
      "chart_axis_label": "",
      "table_cell": "",
      "caption_source_note": ""
    },
    "layout_features": [],
    "chart_table_style": ""
  },
  "content_layer": {
    "deck_type": "个股研究",
    "framework": ["封面", "核心观点", "投资逻辑", "财务分析", "风险提示"],
    "writing_style": "",
    "content_expression_signature": {
      "headline_pattern": "",
      "body_rhythm": "",
      "module_semantics": "",
      "chart_narration_pattern": "",
      "summary_or_transition_pattern": ""
    },
    "page_slot_map": {
      "cover": [],
      "toc": [],
      "section": [],
      "content": [],
      "closing": []
    },
    "content_reuse_risk": "old_subject_specific"
  },
  "reuse_policy": {
    "default": "style_only",
    "use_content_framework_when": [
      "same_deck_type",
      "user_explicitly_requests_structure",
      "user_explicitly_requests_content_expression"
    ],
    "never_reuse": [
      "old_titles",
      "old_numbers",
      "old_dates",
      "old_body_text"
    ]
  }
}
```

If a field is unknown, leave it empty rather than inventing. The style layer is
usually reusable across topics. The content layer is reusable only for same-type
decks or when the user explicitly asks to reuse the structure or content
expression. `content_expression_signature` captures how the template writes and
organizes content, not the old subject matter: headline sentence pattern,
paragraph/bullet rhythm, module meaning, chart-side narration, and summary or
transition patterns. `page_slot_map` records reusable content slots by page role
without copying old titles, numbers, dates, body text, or subject-specific
claims.

For financial and institutional templates, treat logo and issuer identity as
brand elements, not content. Use the vision model to locate and judge logo
candidates on rendered representative pages, then crop the original pixels with
`scripts/crop_brand_asset.py` and archive the result under `brand_assets/`.
Logos that appear in the cover, header, footer, or master chrome and clearly
function as template / issuer branding should default to
`identity:"template_brand"` and `retain_policy:"retain_by_default"`. User
requests can override this with `retain_policy:"remove"` or `"replace"` and a
new `identity:"user_requested_brand"` asset. Record logos with position, size,
visible text, identity, confidence, and source (`vision_crop`, `slide`, `layout`,
or `master` when OOXML can be aligned). Research subject logos, data-source
marks, audience/client names, and old author stamps should not be promoted to
template brand by default. Image generation may use cropped logo assets as a
fallback enhancement reference, but generated/repainted logos are not
authoritative brand assets.

## Reuse Priority

When generating a new deck and no new template file is supplied:

1. Use the template explicitly named in the user request.
2. If user memory/context names a default template, use that template.
3. Else use `default.json` if present.
4. Else use `latest.json` if present and the user asked to use the latest or
   implied continued template use.
5. Else fall back to the existing style defaults such as
   `institutional_research_default`.

Do not silently apply the latest template to an unrelated request unless the
user has asked for template reuse, default-template behavior, or memory/context
indicates that default.

## Reuse Decision

Before generation, decide which layers to apply:

- Same deck type or explicit "沿用结构/沿用内容样式或表达方式" → style layer
  plus content framework/expression may be used.
- Cross-type reuse, such as an equity research template for an industry deck →
  use style layer only; rebuild the content framework from the new request.
- For content style, keep the skill's `institutional_research_default` research
  writing and layout discipline for finance/research pages, and keep the global
  content-expression baseline for all professional pages even when a user
  template is used: conclusion-first titles, analytical paragraphs or
  substantive bullets in the middle, and evidence charts/tables or other
  reviewable artifacts in the lower/right evidence zone. Avoid cardifying every
  point, KPI, bullet, or chart; ordinary pages should use few or no icons unless
  the template or page type truly requires them, or the user explicitly asks to
  inherit that expression.
- When the user explicitly asks to inherit the template's content style,
  translate `content_expression_signature` and `page_slot_map` into each page's
  instruction: preserve the template's headline pattern, paragraph/bullet rhythm,
  module semantics, chart narration pattern, and fixed content slots while
  replacing all old subject-specific facts, titles, dates, numbers, and source
  text with the new deck's content.
- Preserve or define a typography hierarchy in `style_layer`: same role should
  use the same font tone, size level, and weight across pages. When a PPTX
  template is available, derive this hierarchy from OOXML/representative pages;
  if uncertain, use the default compact sans hierarchy rather than inventing a
  new size system per page.
- Preserve distinctive template typography in `style_layer.typography_signature`,
  especially cover and section display titles. Record whether the title is
  high-contrast Chinese serif, Songti/Kaiti-like, calligraphic, heavy sans, or
  compact sans; record color/shadow/letter-spacing only when visually important.
  If the template uses a serif or calligraphic title, set `avoid_substitution`
  so generation does not replace it with a heavy bold sans display font.
- Template brand logos in cover/header/footer/master chrome → retain by default;
  user-requested removal or replacement overrides this. Research subject,
  data-source, audience/client, and old-author marks are not template brand by
  default.
- Old titles, old numbers, old dates, old body text, and old subject-specific
  claims are never reused.

When using archived templates with `batch-add --items-json`, map each planned
page role to `style_layer.page_role_map` / `assets.selected_refs`, resolve the
relative archive path against the template directory, and set `reference_image`
to that absolute path. `template_library.py get <template> --resolve-paths`
returns ready-to-use absolute `resolved_assets.selected_refs` paths. If the role
is missing, choose the nearest generic content reference or fall back to the
style preset.
