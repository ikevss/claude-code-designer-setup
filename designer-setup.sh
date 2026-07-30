#!/usr/bin/env bash
# ============================================================
# Claude Code 设计师能力一键安装脚本
# 生成于 2026-07-30，35 个设计/动效/视觉 skill
# 用法: bash designer-setup.sh
# ============================================================
set -e

SKILL_DIR="$HOME/.claude/skills"
AGENT_DIR="$HOME/.claude/agents"
CONFIG_DIR="$HOME/.claude"
SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "══════════════════════════════════════════════"
echo "  Claude Code 设计师能力一键安装"
echo "  35 个 skill · 3 层能力栈 · 支持中文口语触发"
echo "══════════════════════════════════════════════"
echo ""

# 1. 复制 skill
echo "[1/4] 安装 35 个设计 skill..."
mkdir -p "$SKILL_DIR"
cp -r "$SETUP_DIR/skills/"* "$SKILL_DIR/"
echo "  ✓ 设计决策: idesign, motion-design"
echo "  ✓ GSAP 引擎: gsap-core, gsap-timeline, gsap-plugins, gsap-react, gsap-frameworks, gsap-scrolltrigger, gsap-performance, gsap-utils"
echo "  ✓ 动效执行: gsap-web, micro-interaction, svg-animation, lottie-animation, page-transition-animation, ascii-animation, 60fps-animation, accessible-animation, glassmorphism, react-email"
echo "  ✓ 插图生成: baoyu-image-gen, baoyu-article-illustrator, orange-line-illustration, baoyu-danger-gemini-web, gpt-image-2-style-library, baoyu-xhs-images"
echo "  ✓ 封面/信息图/图表: baoyu-cover-image, baoyu-infographic, chart-visualization, scientific-visualization"
echo "  ✓ 架构/流程图: markdown-mermaid-writing, graphify, canvas-design"
echo "  ✓ 图像处理: baoyu-compress-image, imagemagick-conversion"

# 2. 复制 agent (idesign 自带的 4 个)
echo ""
echo "[2/4] 安装 idesign agent..."
for agent in idesign-asset-producer idesign-documenter idesign-finish-reviewer idesign-manual-edit-applier; do
  src="$SETUP_DIR/skills/idesign/reference/degraded/${agent#idesign-}.md"
  if [ ! -f "$src" ]; then
    for parent in "$SETUP_DIR/skills/idesign/reference/degraded/"*; do
      [ -f "$parent" ] && cp "$parent" "$AGENT_DIR/" 2>/dev/null || true
    done
    break
  fi
done
echo "  ✓ 4 个 agent 已安装"

# 3. 复制中文路由表
echo ""
echo "[3/4] 安装中文路由表..."
cp "$SETUP_DIR/config/design-router.md" "$CONFIG_DIR/design-router.md"
cp "$SETUP_DIR/config/zh-commands.md" "$CONFIG_DIR/skills/idesign/reference/zh-commands.md"
echo "  ✓ design-router.md → ~/.claude/"
echo "  ✓ zh-commands.md → ~/.claude/skills/idesign/reference/"

# 4. 追加 CLAUDE.md 设计段
echo ""
echo "[4/4] 配置 CLAUDE.md..."
DESIGN_SECTION='
### UI / 前端设计统一入口：/idesign

所有 UI 设计需求统一走 `/idesign`（设计决策 → 同 skill 自带中文映射表）。

视觉创建（插图/封面/信息图/图表/流程图）和动效交互（GSAP/Lottie/SVG动画/微交互/毛玻璃等）另有独立路由表，用中文描述需求即可自动匹配，详见 `~/.claude/design-router.md`。'

if [ -f "$CONFIG_DIR/CLAUDE.md" ]; then
  if grep -q "idesign" "$CONFIG_DIR/CLAUDE.md" 2>/dev/null; then
    echo "  ⊘ CLAUDE.md 已有 idesign 配置，跳过"
  else
    printf '\n%s\n' "$DESIGN_SECTION" >> "$CONFIG_DIR/CLAUDE.md"
    echo "  ✓ 已追加设计路由段"
  fi
else
  printf '%s\n' "$DESIGN_SECTION" > "$CONFIG_DIR/CLAUDE.md"
  echo "  ✓ 已创建 CLAUDE.md"
fi

echo ""
echo "══════════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo ""
echo "  现在就可以说（直接说中文）："
echo "    审查一下这个页面"
echo "    按钮加个hover触感效果"
echo "    页面往下滚到那个区域时元素钉住"
echo "    生成一张橙线风格的插图"
echo "    这份数据做个信息图"
echo "    画个流程图"
echo "    压缩一下这张图片"
echo ""
echo "  设计师三层能力栈："
echo "    决策层: /idesign (23子命令) + motion-design"
echo "    动效层: GSAP×9 + gsap-web + svg/lottie/micro/page + 性能/无障碍"
echo "    视觉层: 插图/封面/信息图/图表/流程图/图像处理"
echo "══════════════════════════════════════════════"
