<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ikevss/design-skillhub/main/assets/01-hero-sm.jpg">
    <img src="https://raw.githubusercontent.com/ikevss/design-skillhub/main/assets/01-hero-sm.jpg" width="800" alt="Design SkillHub - 几何宝石插图">
  </picture>
</p>

# Design SkillHub

**说中文，让 AI 做设计。** 审查页面、调配色、加动效、画图表、生成 PPT——用口语触发，零学习成本。

[![Website](https://img.shields.io/badge/官网-ikevss.github.io/design--skillhub-16a085?style=flat-square)](https://ikevss.github.io/design-skillhub/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-130+-brightgreen?style=flat-square)]()

---

## 这东西能做什么

<p align="center">
  <img src="https://raw.githubusercontent.com/ikevss/design-skillhub/main/assets/02-before-after-sm.jpg" width="800" alt="改之前 vs 改之后">
</p>

你只要用**自己的话**描述想要什么，剩下的所有设计工作自动完成：

| 你说的话 | 它做的事 |
|---------|---------|
| "帮我看看这个页面有什么问题" | 10 项启发式评估 + 认知负荷分析 + 多角色走查 |
| "几个页面长得不像一家人" | 自动扫描提取颜色/字体/间距，生成统一 Design Token |
| "页面像 PPT 一样死板" | 给你写弹性按钮、滚动入场、加载过渡的动画代码 |
| "帮我做暗色模式" | 完整暗色主题方案，全局应用 |
| "这份数据画个图表" | 自动选图表类型 + 生成可视化 |
| "帮我画个流程图" | 文字描述 → 清晰结构化流程图 |
| "明天汇报 PPT 还是白板" | 内容大纲 → 整份可编辑 PPT（21 套模板） |
| "这篇文章配张封面图" | AI 生成匹配内容的封面图 |
| "检查无障碍有没有问题" | WCAG AA/AAA 审计 + 修复建议 |
| "这个组件没有设计感" | 统一品牌色、建立层级、等宽数字、克制排版 |

<p align="center">
  <img src="https://raw.githubusercontent.com/ikevss/design-skillhub/main/assets/03-animation-sm.jpg" width="800" alt="动效设计">
</p>

---

## 安装

```bash
git clone https://github.com/ikevss/design-skillhub.git ~/design-skillhub
cd ~/design-skillhub && bash designer-setup.sh
```

装完重启你的 AI 工具。**无需 API Key，纯本地，不修改系统配置。**

> 其他 AI 工具用户直接复制 `skills/` 目录到对应 skill 路径即可——标准 Markdown 格式，零平台依赖。

---

## 适配工具

| 工具 | Skill 目录 |
|------|-----------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| TRAE Work | `~/.trae/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Cursor | `~/.cursor/skills/` |
| Gemini CLI | `~/.gemini/antigravity/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |
| QwenWork / Qoder | `~/.qoder/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| Kiro CLI | `~/.kiro/skills/` |

---

## 能力栈（8 层 · 130+ skills）

<p align="center">
  <img src="https://raw.githubusercontent.com/ikevss/design-skillhub/main/assets/04-system-sm.jpg" width="800" alt="设计系统">
</p>

| 层级 | 做什么 | 包含 |
|------|--------|------|
| **设计决策** | 像设计总监一样把关 | idesign（23 子命令审查/配色/排版/动效/UX文案/响应式）、motion-design（动效方法论） |
| **设计系统** | 统一项目视觉规范 | Token 体系、色彩/间距/网格、暗色模式、组件规格、图标系统、排版精修 |
| **动效实现** | 让页面活起来 | GSAP 引擎 ×9、微交互、SVG/Lottie/ASCII 动画、页面过渡、毛玻璃、60fps 性能 |
| **视觉创建** | 从文字到图像 | AI 生图 ×6、封面/信息图/数据图表/流程图、知识图谱、图片处理 |
| **幻灯片** | 一键生成 PPT | AI 全流程生图→可编辑 PPTX、21 套模板、投研风格、Slidev 系列 |
| **无障碍** | 让所有人能用 | WCAG AA/AAA 审计、ARIA 模式、认知无障碍、国际化 RTL |
| **工作流** | 设计→代码投产 | Figma 集成、设计审查、原型研究、Token 构建管线、Web 性能 |
| **框架指南** | 平台落地 | React/Tailwind、Next.js、SwiftUI 设计集成指南 |

---

## 依赖

- 任意支持 Markdown / SKILL.md 规范的 AI 编码工具
- Node.js ≥ 22（idesign 检测器建议）
- 无需 API Key（生图类需自行配置 `.env`）

## License

Apache 2.0 — 可自由商用和修改。
