# Supir Slides

PPT/幻灯片制作与管理技能，支持双 CLI 和双 AI 生图后端。

## 特性

- **双 CLI 备份**：open-slide (优先) → OfficeCLI (备用)
- **双 AI 生图**：Agnes Image (优先) → GPT Image (备用)
- **图片转可编辑 PPT**：百度 PaddleOCR 识别，Key 已内置
- **API Key 内置**：无需手动配置
- **按需初始化**：首次调用自动检测并安装依赖

## 快速开始

### 首次使用

无需任何配置，直接使用：

```bash
# 创建幻灯片
npx @open-slide/cli init my-presentation

# 生成配图（自动选择可用 API）
python <skill-dir>/scripts/generate_image.py --prompt "描述" --output img.png
```

### 首次加载提示

首次调用时会自动初始化，返回类似提示：

```
🔧 Supir Slides 首次加载中...

正在初始化：
✓ 检测 CLI 环境...
✓ 配置 AI 生图 API...
✓ 安装必要依赖...

✅ 初始化完成！下次使用无需等待。
```

## CLI 备份策略

| 优先级 | CLI | 用途 |
|--------|-----|------|
| 1 | open-slide | React 组件式幻灯片 |
| 2 | OfficeCLI | 传统 PPTX 操作 |

## AI 生图备份策略

| 优先级 | API | Key 状态 |
|--------|-----|----------|
| 1 | Agnes Image | ✅ 已内置 |
| 2 | GPT Image | ✅ 已内置 |

## 版本管理

```bash
# 创建快照
python <skill-dir>/scripts/version_manager.py snapshot -m "完成封面"

# 查看历史
python <skill-dir>/scripts/version_manager.py list

# 恢复版本
python <skill-dir>/scripts/version_manager.py restore v20240115_143022

# 对比差异
python <skill-dir>/scripts/version_manager.py diff v1 v2
```

## 图片转可编辑 PPT

```bash
# 将图片转为可编辑 PPT（会提示确认）
python <skill-dir>/scripts/image_to_editable_ppt.py --input slide.png --output editable.pptx

# 跳过确认直接执行
python <skill-dir>/scripts/image_to_editable_ppt.py --input slide.png --output editable.pptx --confirm
```

⚠️ 消耗 Token 较多，首次会提示确认

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `generate_image.py` | AI 图像生成（双 API 自动切换） |
| `pptx_converter.py` | PPTX 转 React 组件 |
| `template_library.py` | 模板库管理 |
| `export_pdf.py` | PDF 导出 |
| `init_environment.py` | 环境自动初始化 |
| `version_manager.py` | 版本快照管理 |
| `image_to_editable_ppt.py` | 图片转可编辑 PPT |
| `parse_ooxml.py` | PPTX 结构解析 |
| `crop_brand_asset.py` | Logo 裁剪 |
| `tile_pages.py` | 多页拼接 |
| `validate_template_profile.py` | 模板校验 |

## 环境变量（已内置，无需配置）

```powershell
# AI 图像生成 API Key（已内置）
$env:AGNES_API_KEY = "your-agnes-api-key-here"
$env:GPT_IMAGE_API_KEY = "your-gpt-image-api-key-here"
```

## 错误处理

- CLI 不可用 → 自动安装 open-slide
- Agnes API 失败 → 自动切换到 GPT Image
- 都失败 → 返回详细错误信息

## 许可

MIT
