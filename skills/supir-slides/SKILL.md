---
name: supir-slides
description: "SuPIR 幻灯片制作 | 制作与编辑 PPT 演示文稿，含双 CLI/双 AI 生图，风格驱动工作流 | slide, PPT, presentation, image generation, 幻灯片, 配图"
---

# Supir Slides Manager

风格驱动的 PPT 制作技能，支持双 CLI 和双 AI 生图后端。

## 核心工作流程

### 阶段 1：需求理解与类型检测

**触发**：用户说"做个 PPT"、"生成幻灯片"、"制作演示文稿"

**执行步骤**：

1. **自动检测输入类型**
   - 用户提供文档/文章 → 从文档生成 PPT
   - 用户提供参考图 → 提炼风格并生成
   - 用户上传图片型 PPT → 自动触发转换流程
   - 用户无输入 → 从零开始

2. **仅在必要时询问参数**
   - 页数：用户指定 或 建议
   - 比例：默认 16:9
   - 语言：默认中文
   - 文字密度：默认低密度

### 阶段 2：风格决策

**执行步骤**：

1. **判断用户意图**
   - 用户说"按这个风格做" / "保持原有风格" → 提炼并应用，**跳过确认**
   - 用户指定风格名 → 直接使用
   - 用户提供参考图 → 提炼风格
   - 无指定 → 使用默认风格

2. **风格内容**
   - 颜色系统（背景/主色/强调色）
   - 字体气质（标题/正文）
   - 构图语言（封面/内容页/结论页）
   - 图形元素（边框/卡片/装饰）
   - 信息密度规则

### 阶段 3：内容结构化

**执行步骤**（如有输入文档）：

1. 提取主题与核心观点
2. 识别可视觉化对象
3. 规划每页标题与信息
4. 内部生成 outline，**不展示给用户**

### 阶段 4：提示词生成

**执行步骤**：

1. 内部生成 prompts，**不展示给用户**
2. 仅在用户要求时才展示

### 阶段 5：生成可编辑 PPT

**默认输出类型**：可编辑文字 PPTX（非图片型）

**执行步骤**：

1. **使用 OfficeCLI 生成可编辑内容**
   - 每页创建文本框、形状、图表
   - 保留文字可编辑性
   - 应用风格配置（颜色、字体）

2. **显示进度**
   - 显示"正在生成第 X/Y 页..."
   - 实时更新进度

3. **错误恢复**
   - 失败自动重试（最多 2 次）
   - 重试仍失败则报告错误

### 阶段 6：交付

**执行步骤**：

1. **交付可编辑 PPTX 文件**
   - 默认交付 .pptx 文件
   - 文字可直接编辑
   - 图表可修改数据

2. **清理临时文件**
   - 删除所有中间产物
   - 用户只看到最终 .pptx 文件

---

## 输出类型说明

| 输出类型 | 说明 | 使用场景 |
|---------|------|---------|
| **可编辑 PPTX**（默认） | 文字可编辑的 .pptx | 日常 PPT 制作 |
| 图片型 PPTX | 每页一张图片的 .pptx | 需要视觉效果时 |
| 单张图片 | 单独的 .png 图片 | 需要配图时 |

---

## 确认点规则

| 场景 | 是否需要确认 |
|------|-------------|
| 用户说"按这个风格做" | ❌ 跳过 |
| 用户说"保持原有风格" | ❌ 跳过 |
| 用户说"做个 PPT" | ✅ 需要确认 |
| 单页生成 | ❌ 直接交付 |
| 多页生成 | ✅ 确认大纲 |

---

## CLI 双备份策略

### 优先：open-slide

```bash
npx @open-slide/cli init <project-name>
```

- React 组件式幻灯片
- 1920x1080 画布
- 支持 TypeScript/React

### 备用：OfficeCLI（实验性）

```bash
npx officecli <command>
```

- 传统 PPTX 操作
- 添加/修改/删除幻灯片

---

## AI 生图双备份策略

### 优先：Agnes Image API

```python
# 从 .env 读取
AGNES_API_KEY = os.environ.get("AGNES_API_KEY")
```

- 模型：`agnes-image-2.1-flash`
- 价格：$0.003/张

### 备用：GPT Image API

```python
# 从 .env 读取
GPT_IMAGE_API_KEY = os.environ.get("GPT_IMAGE_API_KEY")
```

- 模型：`gpt-image-2-plus`

---

## 图片转可编辑 PPT

将图片型 PPT 转换为可编辑的 PPTX 格式。

### 使用方法

```bash
python <skill-dir>/scripts/image_to_editable_ppt.py --input slide.png --output editable.pptx
```

### 注意事项

⚠️ **消耗 Token 较多**：此功能需要调用图像识别服务，消耗 Token 和时间较多。

首次使用会提示确认：
```
============================================================
⚠️  图片转可编辑 PPT 需要消耗较多 Token 和时间
============================================================
输入文件: slide.png
文件大小: 2.50 MB
预计耗时: 60-180 秒（取决于图片复杂度）
============================================================
是否继续？(y/n)
```

---

## 风格管理

### 保存风格

从参考图提炼风格后，自动询问是否保存：

```
是否将此风格保存为可复用风格？(y/n)
```

保存后可在下次使用时直接调用。

### 列出可用风格

```bash
python <skill-dir>/scripts/style_manager.py list
```

### 使用已有风格

```bash
python <skill-dir>/scripts/style_manager.py get <style-name>
```

---

## 环境配置

### API Key 配置

在 `.env` 文件中配置：

```env
# AI 图像生成
AGNES_API_KEY=your_agnes_key
GPT_IMAGE_API_KEY=your_gpt_key

# 图片转 PPT
PADDLE_OCR_TOKEN=your_paddle_token
```

---

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `generate_image.py` | AI 图像生成（双 API 自动切换，含进度和重试） |
| `pptx_converter.py` | PPTX 转 React 组件 |
| `template_library.py` | 模板库管理 |
| `style_manager.py` | 风格管理（保存/列出/加载） |
| `export_pdf.py` | PDF 导出 |
| `init_environment.py` | 环境自动初始化 |
| `version_manager.py` | 版本快照管理 |
| `image_to_editable_ppt.py` | 图片转可编辑 PPT |
| `parse_ooxml.py` | PPTX 结构解析 |
| `crop_brand_asset.py` | Logo 裁剪 |
| `tile_pages.py` | 多页拼接 |
| `validate_template_profile.py` | 模板校验 |

---

## 错误处理

### CLI 不可用

```
⚠️ open-slide 和 OfficeCLI 都不可用
正在自动安装 open-slide...
✅ 安装完成，继续执行
```

### API 调用失败

```
⚠️ Agnes API 调用失败，切换到 GPT Image...
✅ 使用 GPT Image 生成成功
```

### 生成失败重试

```
⚠️ 第 1 次生成失败，正在重试...
✅ 重试成功
```

### 都失败

```
❌ 无法生成图像
原因：Agnes API 超时，GPT Image API 认证失败
建议：检查网络连接或 API Key 是否有效
```
