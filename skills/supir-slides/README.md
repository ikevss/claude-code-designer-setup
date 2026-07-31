# Supir Slides Manager

风格驱动的 PPT 制作技能，**默认以 image2 (gpt-image-2) 生图**输出图片型 PPTX。

## 特性

* **双 CLI 备份**：open-slide (优先) → OfficeCLI (备用)
* **AI 生图**：GPT Image 2 via aigateway 网关
* **图像优化**：自动对比度、曝光补偿
* **数据驱动**：支持多来源数据导入

## 安装

```bash
# 创建幻灯片
npx @open-slide/cli init my-presentation

# 生成配图（自动选择可用 API）
python scripts/generate_image.py --prompt "your prompt" --output slide.png
```

## 核心工作流程

### 阶段 1：需求理解与类型检测

**触发**：用户说"做个 PPT"、"生成幻灯片"、"制作演示文稿"

### 阶段 2：内容生成

根据检测到的类型，使用对应的 GPT Image 2 API 生成配图。

### 阶段 3：图片转 PPT

生成的图片通过双 CLI 备份策略转换为可编辑的 PPTX：

| 优先级 | CLI        | 用途           |
| --- | ---------- | ------------ |
| 1   | open-slide | React 组件式幻灯片 |
| 2   | OfficeCLI  | 传统 PPTX 操作   |

## API 配置

使用 aigateway.edgecloudapp.com 网关，模型 `gpt-image-2`，文生图 `/images/generations` + 参考图生图 `/images/edits`（JSON body）。

详见 WPS 笔记 "GPT 生图 API — 速查手册"。

## 错误处理

* 生图失败 → 自动重试 (max 3 次)
* CLI 不可用 → 自动安装 open-slide
* Agnes API 失败 → 自动切换到 GPT Image 2
