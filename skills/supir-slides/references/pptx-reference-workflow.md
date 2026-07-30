# PPTX/PDF 参考稿工作流

Agent 在用户提供参考稿/模板（上传附件或工作区已有文件）并要求按其版式、配色或视觉
风格生成新 PPT 时加载此文件。最常见形态：用户只给一个模板文件，说"按这个模板/风格
做一份 XX 的 PPT"。

若用户要求保存、复用、列出、查看、删除、插入、设置默认模板，或要求使用最新上传/
默认模板，同时加载 `template-library.md`。模板库固定在
`/workspace/.paipai-slides/templates/`。

如果用户没有提供可用视觉模板，或提供的是内容资料而非风格模板，所有专业/研究/业务汇报类
PPT 默认先采用全局内容表达基线；金融/投研/基金产品/
机构路演类 PPT 同时回落到 `institutional_research_default`（见
`institutional-research-style.md`）。如果参考稿本身有强烈 AI 信息图、科技发布会、
SaaS dashboard 或营销海报感，也用该 preset 做风格抑制。

## 触发条件

- 用户提供 .ppt/.pptx/.pdf/图片等模板，要求"按这个风格/模板出新内容"
- 用户要求仿制/复刻某份 PPT 的视觉系统，或提供品牌样稿要求统一视觉
- 用户提供制式化报告（新股分析、行业深度、路演材料等），希望新 PPT 沿用其内容框架
- 用户同时提供模板 + 内容文档（"按 A 的风格，把 B 的内容做成 PPT"）——内容文档的处理见文末
- 用户要求保存/归档上传模板，后续用最新模板或默认模板生成 PPT
- 用户上传 PPT/PPTX 且意图明显是作为模板使用（例如"按这个模板/风格/版式做"）

## Step -1：复用模板库（没有新模板文件时）

如果用户没有提供新的模板文件，但说"用默认模板"、"用最新上传的模板"、"继续用上次模板"、
或明确命名某个已保存模板，先按 `template-library.md` 读取模板档案：

```bash
python3 scripts/template_library.py get default
python3 scripts/template_library.py get latest
python3 scripts/template_library.py get <template-id-or-name>
```

读取 `template.json` 后先判断复用层：

- 同类任务或用户明确说"沿用结构/沿用栏目/沿用内容样式或表达方式" → 可使用 `style_layer` + `content_layer`
- 跨类型任务（如个股研究模板用于行业分析） → 默认只使用 `style_layer`
- 使用任何用户模板时，内容组织默认仍采用全局内容表达基线；金融/投研页同时采用 `institutional_research_default` 的研究写法和反 AI 味规则。模板负责视觉皮肤/版式角色，不默认负责把内容做成卡片化、图标化或营销化表达
- 旧标题、旧数据、旧正文、旧日期、旧主体特定观点永不复用
- 明显属于模板品牌系统的 Logo/机构名/页眉页脚（出现在封面、页眉、页脚、母版固定区，且承担出品方/模板品牌识别）默认随模板继承；用户明确要求移除或替换时覆盖默认。研究对象、数据来源、客户/受众、旧稿署名不默认继承为模板品牌

生成时先把目标页面角色归一到五个 canonical role：`cover`、`toc`、`section`、
`content`、`closing`，再用 `style_layer.page_role_map` / `assets.selected_refs`
挂 `reference_image`。`contents/agenda` 归到 `toc`，`content_text/content_chart/
content_table/content_diagram/evidence/diagram/title_page` 归到 `content`，
`thanks/disclaimer/end` 归到 `closing`。若目标页面角色没有匹配参考图，选最接近的
通用内容页或回落到 `institutional_research_default`。

## Step 0：多个文件时先定角色（只有一个模板文件时跳过）

按用户措辞判定每个文件的角色，与格式无关：

- **模板**（"按这个风格/模板/配色"）→ 需要的是**图片**，走下面 Step 1-4 主线
- **内容**（"把这篇报告/文档做成 PPT"）→ 需要的是**文字/数据**，只提取内容（见文末"用户还提供了内容文件时"），**不要渲染成图片**
- 旧稿翻新（"把这份旧稿更新成 XX"）= 同一文件兼两角色，两条都做

## Step 1：渲染参考稿为 PNG

统一用 `scripts/render_png.py`，**不要手搓 `pdftoppm` / `soffice`**——脚本按扩展名自动路由，
且封装了正确的 DPI / 分页参数。

**PPTX/PPT（走后端接口，一次转出全部页）：**

```bash
python3 scripts/render_png.py --pptx-path "<模板路径>"
```

- 成功时逐行输出 PNG 路径，如 `tmp/upload/reference.pages/slide_01.png`
- 依赖环境变量 `$PPTX_TO_PNG_API_URL` 和 `$PAIPAI_USER_ID`（由运行环境注入）；缺失则停止并告知用户联系管理员
- PPTX 还应默认尝试读取 OOXML 结构，用于辅助识别母版元素、Logo/页眉页脚候选、字号、颜色、坐标、表格与图片资产；解析失败不阻塞流程，但要在 `render_lock` 标注 OOXML 低置信：

```bash
python3 scripts/parse_ooxml.py --pptx-path "<模板路径>" --json
```

解析后优先查看 `design_summary.top_font_signatures` 和
`design_summary.largest_text_runs`，识别封面/章节大标题的字体族、字号、粗细和颜色；这些字段要进入
`style_layer.typography_signature` 与 `render_lock.typography_signature`。

**PDF（本地渲染，无需上述环境变量）——只渲要用的页，不渲整本：**

```bash
python3 scripts/render_png.py --pdf-path "<模板路径>" --first-page 1 --last-page 1
python3 scripts/render_png.py --pdf-path "<模板路径>" --first-page 3 --last-page 3
```

- 渲哪几页由 Step 2 的预分类结果决定，不要机械抽固定页码
- 复用同一 `<stem>_pages/` 输出目录，按真实页码命名，分批调用不冲突
- **DPI 用默认 120**（选图 90-120 足够清晰）；不要 `--dpi 200`，更不要整本高 DPI 渲染（卡死/超时的根因）
- 如不在技能根目录，使用 `scripts/render_png.py` 的绝对路径

**图片模板**（png/jpg/webp 等）：直接当参考图用，无需转换。

**其他格式**（docx、html 等）：自己写代码**先转成 PDF** 再进上面的管线（如
`soffice --headless --convert-to pdf`）；实在转不出来，告知用户请提供 PPT/PDF/图片版。

## Step 2：按页面角色选取参考图

模板可能几十页，且几乎必有多种版式。先固定使用五个 canonical role：
`cover`（封面）、`toc`（目录/议程）、`section`（章节过渡页）、`content`
（普通内容页，包含图表/表格/机制图/证据页）、`closing`（尾页/致谢/联系方式/免责声明）。
**不要逐页查看**，也**不要全篇只用一张参考图**（封面会长成内容页）。本步产出一张
「页面角色 → 模板页」映射，**同角色的所有新页共用一张参考图**。

1. **预分类（零渲染成本）**：PDF 先抽逐页文本（`pdftotext -layout`）按特征定角色——
   章节过渡页文本极少（仅章节名+固定页脚）、内容页含"图：/表："或大量数值、尾页是
   免责声明/联系方式。PPTX 同步参考 `parse_ooxml.py --json` 的文本、坐标、图片和母版信息。
2. **缩略图总览**：PPTX 已全量转出 PNG、图片集或页数较多时，用 `tile_pages.py` 生成带页码的 overview，让模型先全局看版式家族，再选代表页；模板 ≤5 页时可直接全部查看。

```bash
python3 scripts/tile_pages.py --input-dir "<rendered_pages_dir>" --output "<overview_output_path>" --cols 4 --thumb-width 360 --max-pages 40
```

`<overview_output_path>` 优先放 `workNN/template_overview.png`；如果此时还没有 `workNN`，先放在渲染页同级临时目录，后续把路径写入 `render_lock`。
若模板会归档到模板库，后续还要把 overview 复制为模板档案里的 `overview.png`；它只用于
总览、审计和重新选页，不直接作为生成时的 `reference_image`。

缩略图上方的**编号**跨批连续，= 输入目录自然排序第 N 个文件（全量渲染时即真实页码：第 8 格 → `page_008.png`）。**overview 仅供选页，禁止当 `--ref-image`/`reference_image` 用**——实测会丢模板细节（实底表头退化成泛品牌色样式），生成必须挂选中代表页的**原图**。缺 Pillow（脚本会报错提示）时退回按位置抽样：首页 + 中部 2-3 页 + 末页。

3. **每个 canonical role 最多看 1 页代表**，`read_media` 确认版式后记录映射（多页任务写入
   `workNN/render_lock.md` 的 master chrome 段）：

```
cover   → tmp/upload/模板_pages/page_001.png
toc     → tmp/upload/模板_pages/page_002.png
section → tmp/upload/模板_pages/page_003.png
content → tmp/upload/模板_pages/page_005.png
closing → tmp/upload/模板_pages/page_040.png
```

- 新 PPT 某角色在模板里没有对应版式时，就近选风格最通用的一页内容页
- 模板有多个内容变体（图表页、表格页、机制图页、要点页）时，优先选择最通用的一张作为 `content`；其他变体记录到 `style_layer.layout_features` / `render_lock`，不要扩张一级页面角色
- 仅当模板确实只有一种版式、或用户只给了一张参考图时，才退化为全局单参考图
- 模板是制式化报告（如新股分析、行业深度）时，新 PPT 的页面顺序可沿用其栏目框架（封面→目录→核心观点→…→风险提示），写进 deck_plan

## Step 2.5：提取品牌元素清单（参考稿含公司名/Logo 时必做）

抽样查看时同步记录一份品牌元素清单，后续写进每条 instruction：

| 元素      | 记录内容                                                                                                                                                                            |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Logo      | 图形特征、位置（如右上角）、大致尺寸占比、出现页型、是否来自母版/layout、是否必须保留；能从 OOXML 提取图片资产时记录对应 `asset_path` / hash                                            |
| 公司名    | 精确写法（全称/简称、中英文），不得改写或翻译                                                                                                                                       |
| 页眉/页脚 | 固定文字（公司名、保密声明、日期格式）、位置与样式                                                                                                                                  |
| 去除项    | 页码、页脚日期/期数、统计区间的位置——写进每条 instruction 的排除清单                                                                                                                |
| 品牌色    | 主色/强调色的色彩角色描述（如"深红主色、金色强调"）                                                                                                                                 |
| 字体签名  | 逐角色记录字体风格与层级：封面/章节大标题是宋体/楷宋/书法感/黑体/无衬线中的哪类、粗细、笔画对比、字间距、是否有淡金/白色/阴影；正文、图表标签、表格、来源注的字体类别与相对字号层级 |
| 版式特征  | 标题位置、色条/角标等母版装饰、来源标注位置                                                                                                                                         |

多页任务把这份清单写入 `workNN/render_lock.md` 的 master chrome 段，作为全部页面的统一约束。Logo 还要同步写入 `template.json` 的 `style_layer.brand_elements`，至少包含 `kind:"logo"`、`asset`、`source_page_role`、`bbox_px`、`padded_bbox_px`、`position`、`size_ratio`、`visible_text`、`identity`、`source`、`retain_policy`、`confidence` 和可选 `asset_path` / `sha256`。若模板大标题是高对比衬线、宋体、楷宋或书法感标题，必须在 `render_lock` 和每条封面/章节页 instruction 中正向写明该字体签名；不要只写"参考模板字体"，也不要让模型回落成粗黑体或现代无衬线标题。

**Logo 单独处理流程**：

1. 用视觉模型查看 `cover`、`toc`、`section`、`content`、`closing` 代表页，识别疑似 Logo / 机构名 / 固定页眉页脚，输出候选的 `bbox_px`、位置、可见文字、身份判断和置信度。OOXML 只负责补充候选与精确资产线索，不作为唯一判断来源。
2. 对候选做身份分类：`template_brand`（模板/出品机构品牌，默认继承）、`user_requested_brand`（用户指定品牌，继承或替换）、`subject_logo`（研究对象，不默认继承为模板品牌）、`source_logo`（数据/资料来源，不默认继承）、`audience_or_client`（受众/客户，不默认继承）、`old_author_or_stamp`（旧稿署名/日期/水印，不默认继承）、`unknown`。明显出现在封面、页眉、页脚或母版固定区且与模板风格绑定的金融机构 Logo，默认判为 `template_brand`，除非用户明确说不要或替换。
3. 对默认继承或用户指定继承的 Logo，用原始渲染页图片裁剪，不让生图模型重画正式 Logo：

```bash
python3 scripts/crop_brand_asset.py \
  --image "<代表页PNG>" \
  --bbox "x1,y1,x2,y2" \
  --padding 12 \
  --out "work01/brand_assets/logo_primary.png" \
  --label "logo_primary"
```

若视觉模型给的是相对坐标，使用 `--bbox-format relative`。裁剪后用视觉模型复查裁剪图是否完整、清晰、未混入无关内容；必要时调 padding 或 bbox 重新裁剪。

4. 如果 `parse_ooxml.py --json --extract-images` 找到与 bbox 对齐的图片 shape，记录其 `asset_path` / `sha256` / `source=slide|layout|master`；若对齐不上，仍以视觉裁剪资产作为审计和生成参考。
5. 把裁剪图作为 `--brand-asset logo_primary=...` 随模板归档，并在 `style_layer.brand_elements` 写入裁剪元信息。生成模型可以读取这个资产做兜底增强，但正式 Logo 来源仍是原模板裁剪资产，不是模型重绘结果。
6. 若用户要求替换 Logo，用用户提供或指定的 Logo 资产生成新的 `brand_assets/logo_primary.png`，在 `brand_elements` 中把原模板 Logo 标为 `retain_policy:"replace"` 或 `remove`，新 Logo 标为 `identity:"user_requested_brand"`、`retain_policy:"retain_by_default"`；若用户要求去掉模板 Logo，则每条生成 instruction 都要显式排除对应位置的 Logo/公司名。

**保留 vs 去除**：

- **默认保留**（模板品牌级）：出现在封面、页眉、页脚、母版固定区，且明显承担模板/出品机构品牌识别的 Logo、公司名、页眉页脚固定文字、品牌色、字体签名/字号层级、版式系统、图表风格。金融/券商/基金/机构路演模板中，这类 Logo 默认随模板继承，并作为全 deck 约束写入每条 instruction
- **用户覆盖**：用户明确说不要中金/某机构 Logo、去掉 Logo、换成自己公司 Logo、换成某个指定 Logo 时，用户指令优先于模板默认继承。保留模板版式、配色和内容表达，但替换或移除品牌元素
- **一律去除**（页面实例级）：**页码**（模板带页码 ≠ 新稿要页码——页码画进图片就是死的，页序一变即错；仅用户明确要求时例外）；参考页自身的日期/期数/统计区间；旧内容的来源文字（来源区样式保留，文字按新页真实来源重写）
- **不要带入**（内容级）：参考稿的旧标题、旧数据、旧正文、与新主题无关的图片
- **非模板身份不默认继承为品牌**：研究对象 Logo、客户/受众机构名、数据来源、资料来源、旧报告作者/署名/水印，不要误当模板品牌或出品方 Logo 继承；作者不明确则不新增作者身份
- **其他元素拿不准默认不带入**（水印、固定声明、页脚日期等，与身份规则同向），不停下来问用户；保留/去除清单随结果一并汇报，便于事后用编辑命令调整

> 与"不要发明 Logo"规则的关系：`image-renderer.md` / `visual-qa.md` 禁止的是**无中生有**的 logo 和来源；参考稿中默认继承或用户指定继承的真实模板品牌元素**必须保留**，不要把负向约束写成"不放 logo"。当前生成仍主要依赖 `reference_image`、裁剪出的 `brand_assets` 和显式 instruction 保留 Logo；OOXML 抽出的图片资产用于识别、审计和描述，不会自动贴回幻灯片，所以小 Logo/英文名必须写清位置和拼写。生成模型可用裁剪资产兜底增强，但不得把模型重绘 logo 当作权威品牌资产。

## Step 2.8：生成前归档模板库（上传 PPT/PPTX 且明显作为模板时）

只要用户上传的是 PPT/PPTX 文件，且用户意图明显是用它作为模板（如"按这个模板/风格做"
"用这个PPT模板""参考这份PPT版式"），完成 Step 1-2.5 的渲染、OOXML 解析、代表页选择
和品牌/版式提取后，必须先按 `template-library.md` 运行 `template_library.py insert`
保存模板档案，然后再进入 Step 3 生成 PPT。这样当前任务和未来任务都使用同一套稳定档案路径，
不依赖 `tmp/upload` 临时文件。

这类自动保存只更新 `latest.json`，不要自动设为默认；只有用户明确说"设为默认/以后默认用"
时才在 `insert` 时加 `--set-default`。若同一源文件已归档，`insert` 会复用已有档案并更新
`latest.json`，不要因此停止生成。归档完成后，用 `get latest --resolve-paths` 或 `insert`
输出中的 `profile_path` 定位模板档案，把后续生成所需的 `reference_image` 替换为
模板库内的绝对路径（优先用 `resolved_assets.selected_refs`；若手工读取 `template.json`，
则将 `assets.selected_refs` / `style_layer.page_role_map` 的相对路径拼到模板目录下）。有裁剪
Logo 时，同步使用 `resolved_assets.brand_assets` 中的稳定路径作为生成和 QA 的品牌参考。

## Step 3：生成新 PPT

所有**生成类命令**（`add`、`insert`、`batch-add`）均支持参考图参数：

| 命令                               | 参考图用法                     | 适用场景                                 |
| ---------------------------------- | ------------------------------ | ---------------------------------------- |
| `batch-add --items-json`           | 每项单独设 `reference_image`   | **默认**：按角色挂参考图，同角色共用一张 |
| `batch-add --ref-image <图片>`     | 全局参考图，所有未覆盖项共用   | 仅模板单一版式时                         |
| `add --ref-image <图片>`           | 单页生成，使用指定参考图风格   | 追加单张新页                             |
| `insert --at N --ref-image <图片>` | 在指定位置插入，使用参考图风格 | 中间插页                                 |

> `update` / `batch-update` 是编辑命令，不支持 `--ref-image`。
> **不要假设全局 `--ref-image` 与 `--items-json[].reference_image` 会叠加**——每项 `reference_image` 会覆盖全局参考图，默认逐项给图。
> 如果本轮上传的 PPT/PPTX 模板已按 Step 2.8 自动归档，当前生成也使用模板库中的
> `selected_refs` 绝对稳定路径作为 `reference_image`，不要再引用 `tmp/upload` 临时页图。

### 典型用法

**按角色挂参考图（默认）**：

```bash
paipai-slides init --id <简短中文名> --title "<标题>"
paipai-slides batch-add <bundle> \
  --items-json '[
    {"title":"封面","instruction":"封面页：...；只保留已确认的模板 Logo/品牌元素；不要保留参考图右下角的页码，不要复制参考稿旧标题和日期。","reference_image":".../page_001.png"},
    {"title":"章节一","instruction":"章节过渡页：01 行业格局 ...","reference_image":".../page_003.png"},
    {"title":"核心观点","instruction":"内容页：...","reference_image":".../page_005.png"},
    {"title":"财务分析","instruction":"内容页：...","reference_image":".../page_005.png"},
    {"title":"尾页","instruction":"尾页：...","reference_image":".../page_040.png"}
  ]'
```

**全局统一参考图（仅当模板单一版式、或只有一张参考图）**：

```bash
paipai-slides batch-add <bundle> \
  --ref-image "tmp/upload/reference.pages/slide_03.png" \
  --instruction "封面页：..." \
  --instruction "内容页：..."
```

**单页追加**：

```bash
paipai-slides add <bundle> --instruction "补充页：..." --ref-image "...page_005.png"
```

要点：

- 每条 instruction 开头写明页面角色（封面/章节过渡页/内容页），与所挂参考图角色一致；内容自包含，不要只写"参考模板"或"同上"
- 使用用户模板时，Style constraints 要同时写明：视觉外观参考模板，内容表达按全局内容表达基线执行；金融/投研页继续按 `institutional_research_default` 的研究页规则执行。普通页面用结论式标题 + 观点段/实质 bullet + 证据区，不把每个观点/KPI/bullet/图表放进圆角框或卡片，普通页 ICON 默认 0-1 个。只有用户明确要求沿用模板的信息图/卡片表达，或该模板模块对应真实流程、表格、机制节点、对比边界时，才保留这种表达。
- 如果没有参考图或参考图只提供内容框架，金融/投研/基金产品/机构路演页默认写明
  `institutional_research_default`：封面/章节页深蓝底白字，正文页通用极浅冷蓝到白色
  渐变纸面、深靛蓝结构线、深蓝/亮蓝强调、少量珊瑚红关键强调、思源黑体/Source Han Sans SC
  优先的紧凑无衬线字体（英文与数字使用 Helvetica/Arial/Inter-like 字体）、固定页眉页脚、观点+证据结构、朴素图表/表格，避免科技发布会/
  咨询信息图/SaaS dashboard/营销海报感。
- 如果没有用户模板，生成时仍要挂 skill 内置的 PPTX 截图参考图；这些路径相对当前
  `paipai-slides` skill 目录解析，调用 CLI 前必须转成绝对路径。封面用
  `assets/default-template/pptx-slide-01-cover.png`，目录页用
  `assets/default-template/pptx-slide-02-contents.png`，章节页用
  `assets/default-template/pptx-slide-03-section.png`，普通内容页用
  `assets/default-template/pptx-slide-04-title-page.png`，标题页可用
  `assets/default-template/pptx-slide-04-title-page.png`。这些参考图提供源 PPTX
  的视觉风格；其中旧标题、旧正文、年份、Source note、示意图表和示意数值都不得复制。
  Alpha/PaiWork 标识或页脚水印是内置模板品牌元素，默认在生成 instruction 中明确保留；
  用户要求去掉品牌、水印、页脚或替换 Logo 时应明确去除或替换。
- **品牌元素不能只靠 `--ref-image`**：生成模型对参考图中的小元素（Logo、页脚小字）可能丢失或变形，确认保留的元素必须在每条 instruction 显式写精确位置和拼写（如"右上角保留参考稿的公司 Logo 与公司名'XX科技'，页脚左下保留'内部资料，请勿外传'"）
- 金融行业模板若存在默认继承的券商/基金/机构 Logo，每条 instruction 都要写明 Logo 的位置、相对尺寸、颜色/图形特征、旁边公司名的精确中英文拼写，并引用模板档案里的 `brand_assets.logo_primary` 作为形态对照；用户要求替换/移除时，每条 instruction 都要显式写明替换资产或排除位置
- **去除项同样不能只靠默认**：参考图里的一切默认会被照搬，Step 2.5 的去除项要写进**每条** instruction 并给出位置（如"不要保留参考图右下角的页码块"）
- 有内容文件时，instruction 里的观点、数字全部来自提取结果（见文末），注明出处页码便于 QA 回查
- instruction 写法遵循 `slide-generation-guide.md`；用 `task <bundle> <taskId> --wait --timeout 560` 等待异步完成

## Step 4：QA

按常规 `task --wait` → `validate` → `visual-qa.md` 检查，额外关注：

- **版式角色核对**：封面像封面、章节过渡页像章节页——每页与其参考图的版式角色一致
- 新页面是否延续参考稿的视觉系统（配色、版式、品牌元素）
- 新页面内容组织是否仍保持机构研究页气质：观点直接排布、证据图表/表格支撑，未因参考模板变成大量圆角卡片、装饰 ICON、信息图海报或 SaaS dashboard
- **品牌保真**：Logo 是否变形，公司名/页脚小字是否与参考稿拼写完全一致（AI 生图易写错小字）。变形或错字用 `update --instruction` 定点描述修复，不可修复则带显式品牌约束重新生成该页
- 新内容是否被参考稿旧文字污染（不应出现旧标题、旧数字、旧日期、旧来源文字）
- **页码残留**：检查页脚四角（尤其右下角）有无带回参考图页码；残留用 `update --instruction` 定点描述去除（写清元素+位置，如"去掉右下角橙色页码块，其余不变"——框选坐标只能来自用户前端，agent 不自拟），或补排除项后重新生成该页
- 有内容文件时：页面观点、数字与提取结果一致，不得编造
- 当模板没有强约束或模板 AI 感较重时：普通内容页是否回到全局内容表达基线；金融/投研页是否回到机构投研材料风格，而不是
  科技发布会、咨询信息图、SaaS dashboard、数据大屏或营销海报

## Step 5：补充归档模板库（非自动归档场景）

当用户要求保存模板、设为默认、未来复用，或当前任务是"上传一个 PPT 模板给以后用"时，
按 `template-library.md` 把解析后的中间产物归档到
`/workspace/.paipai-slides/templates/`。必须复制文件，不要只保存 `tmp/upload` 或 `workNN`
里的临时路径。

注意：上传 PPT/PPTX 且明显作为模板使用的场景已在 Step 2.8 **生成前自动归档**，不要等
生成完成后才保存。Step 5 只用于图片/PDF 模板、用户生成后才要求保存、或其他未命中自动
归档规则的补充保存场景。

归档前准备：

- `selected_refs/`：按 canonical 页面角色选出的代表页 PNG，如 `cover`、`toc`、`section`、`content`、`closing`
- `brand_assets/`：由视觉模型定位、代码裁剪出的 Logo / 品牌元素，如 `logo_primary.png`
- `overview.png`：`tile_pages.py` 输出
- `ooxml.json`：PPTX/PPT 可用时，由 `parse_ooxml.py --json` 输出
- `rendered_pages/`：模板页图；中小模板默认保存全量，超大模板至少保存代表页 + overview + ooxml
- `style_layer`：页面角色映射、品牌元素清单、调色板/字体气质与字号层级、版式特征、图表/表格风格
- `content_layer`：deck 类型、可选栏目框架、写作风格、内容表达签名与页面槽位；只同类或显式要求时复用。内容表达签名应记录标题句式、段落/bullet 节奏、模块语义、图表旁注/结论写法、摘要/过渡页模式；页面槽位记录每类页面的可复用内容位置。只记录表达方式和槽位，不复制旧标题、旧正文、旧数字、旧日期或旧来源。

示例：

```bash
python3 scripts/template_library.py insert \
  --display-name "<模板展示名>" \
  --deck-type "<个股研究/行业深度/路演/其他>" \
  --source-file "<上传模板路径>" \
  --rendered-dir "<逐页PNG目录>" \
  --overview "<workNN/template_overview.png>" \
  --ooxml "<workNN/template_ooxml.json>" \
  --ref cover="<封面代表页PNG>" \
  --ref toc="<目录代表页PNG>" \
  --ref section="<章节页代表页PNG>" \
  --ref content="<普通内容页代表页PNG>" \
  --ref closing="<尾页代表页PNG>" \
  --brand-asset logo_primary="<裁剪Logo PNG>" \
  --style-layer-json "<workNN/template_style_layer.json>" \
  --content-layer-json "<workNN/template_content_layer.json>"
```

只有用户明确说"设为默认/以后默认用这个"时才加 `--set-default`。普通插入只更新
`latest.json`，不覆盖默认模板。

## 用户还提供了内容文件时

内容文件提供新 PPT 的**实质**（观点/数据/图表），与模板的"形式"互补。**只提取文本，
禁止整本转成图片来"读内容"**——转图慢几个数量级，且不如直接抽文本准。

- 解析：PDF 用 `pdftotext -layout`（表格再用 pdfplumber），Word 用 pandoc/python-docx，数据文件用 pandas，md/txt 直接读，其他格式自己写代码
- 大文档（几十页）先把全文落盘（如 PDF 同级 `<stem>.txt`），分章节读取提炼进 deck_plan，不要一次性全部塞进上下文
- 图表的标题、轴标签、数据标注通常就在文本层；仅个别纯位图图表、或扫描件（`pdftotext` 输出为空）时，才用 `render_png.py --first-page N --last-page N` 低 DPI 定点渲染那几页看图取数，由生成模型**按数据重绘**（图片式 PPT 不能贴原图，重绘也保证风格统一）
- **重组叙事**：报告章节 ≠ 幻灯片页，按 PPT 叙事重新规划页面；文档专属版面（文档目录页、免责声明、封底）默认不搬进 PPT；用户有明确取舍指示（如"去掉目录页""保留全部图表"）时照办
- **保留信息量**：用户提供大量参考资料（Word/PDF/Markdown 报告等）时，默认尽可能保留原始的信息量、事实和逻辑链——提炼是为了组织页面，不是删减内容。单份 PPT 最多 80 页；在上限内宁可增加页数或把次要内容放附录，也不要把资料压缩成几条口号式要点。超过 80 页时建议拆成多份 deck；仅当用户明确要求精简风格时才大幅压缩
