# BBox Editing Protocol

## Input Contract

Each edit must identify:

- internal page id, if available; this is not a visible page number
- target `slide_id`
- bbox/region context from the editor when available
- prompt
- scope: `local`, `local_plus_style`, or `global`

```json
{
  "page": "P04",
  "slide_id": "s_abc12345",
  "regions": [{"x1": 0.115, "y1": 0.167, "x2": 0.510, "y2": 0.648}],
  "prompt": "Make the left chart visually cleaner and emphasize the 2025 rebound.",
  "scope": "local"
}
```

## Coordinate Rules

- Origin is top-left.
- 坐标归一化 0~1（`x1,y1` = 左上角，`x2,y2` = 右下角），由 `ImageRegion` 校验。
- 多区域写为 `regions: [...]`。
- In editor context, the runtime injects regions via
  `$PAIPAI_SLIDES_REGIONS_JSON_B64`; `update` / `batch-update` read them by
  slideId automatically. The Agent should not invent or manually type coordinates.
- The region is passed to the edit model as a soft mask: content inside the
  mask is fully re-synthesized, and pixels outside are not guaranteed unchanged.

## Edit Discipline

For `local` edits:

- Preserve all pixels outside bbox; verify after the edit — the soft mask
  does not guarantee it.
- Do not change master chrome, logo, or footer. Do not change a user-required
  page number; a page number inherited from a template/reference image is not
  required unless the user explicitly asked to keep page numbers.
- Do not alter numbers or labels unless prompt explicitly names replacements.
- If the region contains a chart/table, consult the corresponding chart/table spec first.

For `local_plus_style`:

- Region may be restyled to match the deck, but neighboring alignment and
  colors must remain consistent.
- Unless the user explicitly asks for another expression, restyling should keep
  the deck's global content-expression baseline: conclusion-first wording,
  substantive viewpoint text where applicable, reviewable evidence artifacts,
  few/no decorative icons, and no card-grid/dashboard/marketing-poster drift.

For `global`:

- Allowed only when user explicitly asks for a whole-page restyle or rerender.
- Whole-page restyles default back to the global content-expression baseline
  unless the user explicitly requested another style.

## Spatial Understanding via annotate-region

框选编辑前，先标注区域理解空间上下文，再写精准 instruction：

```bash
paipai-slides annotate-region <file> --slide-id <SID> 2>&1        # 输出 JSON 含 annotatedImagePath
# → 用 read_media 查看标注图，定位框内要改的元素，记下其内容与位置特征
paipai-slides update <file> --slide-id <SID> --instruction "<基于所见写空间描述型指令>" 2>&1
paipai-slides task <file> <taskId> --wait                          # 输出 JSON 含 filePath（新图，如 s_x-2.png）
# → 用 read_media 看【task 返回的 filePath】这张新图复查——不是标注图、也不是改前的旧图
```

**红框只存在于标注图上**：标注图是给 Agent 定位用的一次性辅助图；`update` 提交后，编辑模型拿到的是**无框原图**和你的 instruction（框选坐标由系统作为软 mask 随原图传入，不进提示词）。模型看不到红框——instruction 里出现"红框/标注/框选/选中区域"只会让它困惑，甚至把红色方框当成要绘制的内容画进图里。

固定动作：看完标注图，先把"红框内的 X"**翻译**成 X 的内容+位置描述（如"标题下方、饼图右侧的两行说明文字"），再写修改要求。

正反例：

- ✓ `将柱状图中第三根柱子的数据标签从'89亿'更新为'92亿'，其他柱体和坐标轴不变`
- ✓ `将页面顶部深蓝色背景条中的白色加粗中文标题改为英文"Private Deployment Dominates"，保持字体样式、背景条和左侧锁形图标不变`
- ✗ `把红框里的内容改一下`（提了红框，位置和目标也不明确）
- ✗ `将红框区域内的中文标题改为英文"Private Deployment Dominates"，其他不变`（**指令再具体，出现"红框"就不行**——模型看不到框；应按内容+位置点名："页面顶部深蓝色背景条中的白色中文标题"）
- ✗ `这个区域换个数据`（位置和目标值都不明确）

## Tool Invocation

Apply bbox/region edits only through `paipai-slides update --instruction`, then
wait for the async task.

The system/caller attaches any region arguments. Do not manually add
coordinates. Without editor context, first inspect the deck and write a
semantic local edit instruction:

```bash
paipai-slides show <file>
paipai-slides update <file> --slide-id <SID> --instruction "Modify only the described element: current ... target ..."
paipai-slides task <file> <taskId> --wait                 # 取返回的 filePath
# → read_media 这个返回的 filePath 复查；看不到变化先确认读的是新图（见下「QA After BBox Edit」），别急着返工
```

## Output Contract

For simple one-off edits, do not create a work directory. For complex bbox
edits, repeated local edits, or edits tied to full-deck QA, append an edit
record under the current `workNN/edits/`:

```json
{
  "edit_id": "P04-E02",
  "page": "P04",
  "slide_id": "s_abc12345",
  "task_id": "t_12345678",
  "regions": [{"x1": 0.115, "y1": 0.167, "x2": 0.510, "y2": 0.648}],
  "prompt": "...",
  "status": "applied",
  "qa": ["outside region unchanged", "footer preserved", "no data drift"]
}
```

## QA After BBox Edit

**先读对图**：复查必须 `read_media` 上一步 `task --wait` 返回的 `filePath`（新版本，如 `s_x-2.png`）——**不是** annotate-region 的 `.annotated_*.png` 标注图，**也不是**改前的旧图。每次编辑都生成新文件，复用旧路径只会看到改前的图、误判"没改上"而反复返工。看不到预期变化时，先核对读的是不是最新 `filePath`（拿不准用 `show`/`paths` 取当前 `file_path`），再决定是否真要返工。

Check (against the returned new image):

- no visible seam at bbox boundary
- no unintended change outside bbox
- text is readable
- data labels match source
- page still follows `workNN/render_lock.md`
- layout alignment still feels intentional
