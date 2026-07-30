---
name: GordenImagePPTGen

description: "图片PPT生成 | 从图片生成 PowerPoint 演示文稿 | image PPT, generate, 图片生成PPT"
---

# GordenImagePPTGen — 生成图片格式的 PPT

把主题/内容变成「图片型 PPT」：设计 → 出图 → 合成。每页是一张由imagegen生成的图片。必须使用图片生成，不能通过SVG绘制，必须调用图片生成模型。

```
内容 ─▶ A2 设计大纲(outline.json) ─▶ A3 每页提示词 ─▶ A4 GPT imagegen 出图 ─▶ A5 合成图片型 .pptx
```

## 运行时与图片后端（先读）

图片生成的调用方式因运行时而异，**动手前先读 [`references/runtime-notes.md`](references/runtime-notes.md)**。核心约定：

1. **图片一律用 raster 图像生成后端**（Codex 必须调用内置 imagegen；其它运行时用其原生出图工具；**所有环境均可用本技能的 GPT Image API 作为统一后端**）。**禁止**用 SVG/HTML/Canvas/代码画图冒充。
2. **禁止在已生成的位图上用代码补字/盖字/改字**。文字错了没关系，后续改成可编辑pptx后支持手动修改。
3. Codex 内置工具出的图默认在 `$CODEX_HOME/generated_images/`，**用完务必复制到本任务输出目录**，并保留默认目录原图。
4. 阶段 A4 必须写 `imagegen-manifest.json`，逐页记录模型生成源图与复制后的 slide 路径；没有 manifest 或任一页缺 `generated_source`，本技能执行失败。

### GPT Image API 配置（一次配置，永久生效）

本技能内置了 GPT Image 2 API 调用能力，无需依赖 Codex 内置 imagegen：

**Setup（一次性）：**
1. 复制 `.env.example` 为 `.env`（如果 `.env` 尚未存在）
2. 填入 `GPT_IMAGE_API_KEY` 和 `GPT_IMAGE_API_URL`
3. 可选设置 `GPT_IMAGE_MODEL`（默认：`gpt-image-2`）

**Python 脚本调用：**
```bash
# 单张出图测试
python3 scripts/image_generator.py --prompt "你的提示词" --out output.png

# 批量出图（在 Python 代码中导入）
python3 -c "
from scripts.image_generator import ImageGenerator
gen = ImageGenerator()
gen.generate('prompt', 'slide_01.png', './slides')
"
```

依赖自动安装（`requests`, `python-dotenv`, `python-pptx`, `pillow`），无需手动 pip install。

## imagegen 硬门禁

本技能中的“生成图片”只指调用图像生成模型，不指用代码画 PNG。

禁止使用以下方式生成整页幻灯片图：
- Python/PIL、SVG、HTML、Canvas、matplotlib、PowerPoint shapes、截图渲染。
- 先生成可编辑 PPTX，再导出为图片。
- 用代码绘制页面骨架、图表、图标、文字并保存为 PNG。

允许代码做的事仅限：
- 写 `outline.json`、`prompts/NN-*.md`、`imagegen-manifest.json`、`deck.json`。
- 从 `$CODEX_HOME/generated_images/<thread-id>/...png` 复制已生成图片到 `slides/`。
- 裁切/缩放整张已生成图片以统一比例（不得补字或重画局部内容）。
- 合成图片型 PPTX、生成预览、做 QA 检查。

如果 imagegen 不可用，必须停止并说明阻塞原因，不能用代码绘图兜底。

## 全局铁律

1. 🔴 **绝不出占位符图**：本技能产出的是**含全部真实文字(verbatim)的成品幻灯片图**，不是空模板。出图提示词的【页面文字】必须写满真实文字；`outline.json` 的 `visual_generation_prompt`（只描述画面）**禁止单独出图**，必须与全部文字合并后再出（详见 image-prompt-guide 文首铁律）。出现 lorem/占位框/无字卡片即判失败、改提示词重出。
2. **数据零编造**：完全使用用户提供的数据/数值/专名。数据少就把内容做厚（真实的结构化拆解）+ 大字号/中心聚焦排版，**绝不**编造或填充虚假内容。
3. **语言跟随用户**：问答用用户语言；幻灯片内文字用内容语言（默认中文）。
4. **少用绿色**：尽量避免大面积纯绿（下游 GordenImage2PPTX 默认绿幕抠图会冲突）。
5. **页脚干净**：不加页码/logo/水印（除非用户要求）。

## 默认风格与复杂度

**默认 = 信息密度极高、排版复杂、模块化网格、每页一个不重复的高阶框架**（房子型/莫比乌斯环/Bento 便当盒/同心雷达/多层架构/鱼骨/漏斗/3D 阶梯等）。**简单 = 不合格**。完整提示词体系、复杂度强制清单、风格库、图表形式目录、verbatim 规则见 **[`references/image-prompt-guide.md`](references/image-prompt-guide.md)**。

- ⭐ **内容优先**（最易踩坑）：「排版太简单」几乎都是**每页内容太薄**。**先备厚内容、再出图**：每页 ≥4 个并列模块、每模块 标题+2~3 要点+1 个特大号指标，外加导语(关键词高亮)+底部横幅（≈20+ 信息点/页）。见 image-prompt-guide §0。
- **每页不重样 + 统一配色**：每页选一个**不同**的复杂框架；全篇**统一一套配色**（有参考图就提取其配色）。见 §1.7、§4。
- **豪华 ≠ 浮夸**：清晰永远第一，避免过度辉光/3D 戏剧化导致花哨难读；"清晰科技"是稳妥默认（浅底+细网格+扁平模块+克制强调+高密度）。见 §1.7、§5。
- **排版参考图库** `参考图/`：出图前挑结构相近的参考图，把**布局骨架**写进提示词（也可作 reference 传入后端），可学排版与风格气质，但不照搬其文字/品牌（§1.6）。
- **比例**：跟随用户。默认 16:9；用户要 3:2（或后端原生 3:2 且接受）就直接出 3:2，全套统一、不裁切。见 runtime-notes §5。

## 工作流（逐项打勾）

```
- [ ] A1 确认：风格 / 受众 / 页数 / 语言（除非用户说"直接生成/不用确认"）
- [ ] A2 大纲(outline.json)：解构内容 → 每页指派不重复的复杂框架、统一配色、写厚 detailed_content（见 image-prompt-guide §7 / §1.7）
- [ ] A3 每页提示词：把 outline 落地成 self-contained 提示词（含【全部真实文字 verbatim】），存 prompts/NN-*.md
- [ ] A4 出图：解析后端 → 逐页调用 imagegen 出图（每页含全部真实文字，绝不占位符）→ 复制到输出目录 → 写 imagegen-manifest.json
- [ ] A5 合成：compose_pptx.py 把每页图片做成全幅图片型 .pptx
```

要点：
- **页数**：用户指定就用；没指定按内容量自定（一般 11–20 页，封面+结尾必有）。
- **A3 提示词自包含**：颜色(hex)、版式、**全部文字**、图表形式、字体风格全写死，便于可复现、单页重出。
- **A4**：先确认所有 `prompts/NN-*.md` 就位再开跑；每页必须有一次真实 imagegen 调用；失败/错字只重试该页；复制源图时保留 `$CODEX_HOME/generated_images/...` 原图。
- **imagegen-manifest.json**：必须逐页记录 `slide`、`prompt_file`、`generated_source`、`copied_to`、`backend`。这是阶段 1 的验收证据。
- **A5**：生成 `deck.json`（每个 slide 只有 `background` 指向该页 PNG），跑：

```bash
python3 scripts/compose_pptx.py deck.json out/<topic>-image-deck.pptx
```

## 输出目录结构

```
<topic-slug>/
├── outline.json            # A2 设计大纲（逐页结构化）
├── imagegen-manifest.json  # A4 每页 imagegen 生成证据
├── prompts/NN-*.md         # A3 每页出图提示词（可复现）
├── slides/NN-*.png         # A4 生成的每页图片
├── deck.json               # A5 合成清单（每页 background）
└── out/<topic>-image-deck.pptx
```

## 脚本与依赖

| 脚本 | 干嘛 |
|---|---|
| `scripts/compose_pptx.py` | 把每页图片按 deck.json 合成全幅图片型 .pptx（`--preview-dir` 可出预览） |

- 依赖：`python3` + `python-pptx`、`Pillow`（缺就 `pip3 install python-pptx pillow`）。
- 下一步要可编辑 pptx → 用 **GordenImage2PPTX**；要一键全流程 → 用 **GordenSuperPPTSkill**。
