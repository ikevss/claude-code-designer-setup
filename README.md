# 🎨 Claude Code Designer Pack v2.0

> **130+ 个设计/动效/视觉/系统 skill，一键安装，全部中文触发。**
>
> 装完就能说中文让 AI 做设计——"审查这个页面""帮我建暗色模式""滚到这里把元素钉住""生成一张橙线风插图"。
> 
> 🌐 **[官方网站](https://ikevss.github.io/claude-code-designer-setup/)**

---

## 30 秒安装

```bash
git clone https://github.com/ikevss/claude-code-designer-setup.git ~/claude-designer
cd ~/claude-designer && bash designer-setup.sh
```

重启 Claude Code，说中文做设计。

---

## 设计师能力栈（8 层架构）

### 🎯 设计决策层（2）
- **idesign**（设计总监）— 23 子命令：审查/打磨/配色/排版/动效/布局/简化/加固/UX文案/响应式/新手引导/浏览器实时迭代
- **motion-design**（动效方法论）— 迪士尼动画原则、缓动/时长/编排指导——只出决策不写代码

### 📐 设计系统层（23）
- **Token 体系**：design-tokens（新建生成）、design-token（已有命名）、token-build-pipeline（自动化 CI/CD）
- **视觉基础**：color-system、spacing-system、layout-grid、typography-scale
- **主题**：dark-mode-design、theming-system（品牌/暗色/高对比度）
- **组件**：component-spec（规格）、pattern-library（模式库）
- **治理**：design-system-governance、design-system-crosswalk（跨平台映射）、design-system-interop（互操作）
- **图标**：icon-system
- **动效规范**：motion-system（时长Token/缓动词汇/reduced-motion策略）
- **排版**：web-typography（项目方案）、better-typography（CSS精修）

### 🎬 动效实现层（19）
- **GSAP 引擎**（9）：core / timeline / plugins / react / frameworks / scrolltrigger / performance / utils / gsap-web
- **专项动效**（6）：micro-interaction / svg-animation / lottie-animation / page-transition-animation / ascii-animation / glassmorphism
- **性能/无障碍**（3）：60fps-animation / accessible-animation / web-performance-vitals
- **美学**（2）：aesthetic-systems / motion-choreography

### 🖼️ 视觉创建层（17）
- **AI 生图**（6）：baoyu-image-gen / baoyu-article-illustrator / orange-line-illustration / baoyu-danger-gemini-web / gpt-image-2-style-library / baoyu-xhs-images
- **封面/信息图**（3）：baoyu-cover-image / baoyu-infographic / canvas-design
- **数据可视化**（4）：chart-visualization / scientific-visualization / markdown-mermaid-writing / graphify
- **图像处理**（2）：baoyu-compress-image / imagemagick-conversion
- **邮件**：react-email

### 📊 幻灯片层（15）
- **AI 全流程**：GordenSuperPPTSkill（生图→可编辑 PPTX 端到端）、GordenPPTSkill（21 套模板）
- **投研风格**：supir-slides
- **传统编辑**：pptx / pptx-generator / ppt-design-master
- **Slidev**：create-slide / current-slide / slide-authoring / baoyu-slide-deck / orange-ppt-skill / guizang-ppt-skill / supir-slides
- **备用 CLI**：open-slide（全局已装）

### ♿ 无障碍层（10）
- **审计**：accessibility-audit（WCAG AA）、wcag-aaa-upgrade（AAA 升级）
- **实现**：aria-patterns（WAI-ARIA 模式）、vision-accessibility（低视力/色盲）、cognitive-accessibility（认知障碍）
- **国际化**：i18n-rtl-design（RTL/阿拉伯语/希伯来语）
- **其他**：accessible-animation、ux-writing-skill

### 🔄 工作流层（8）
- **交接**：design-to-code-handoff / figma-integration-workflow
- **验证**：design-qa-checklist / heuristic-evaluation
- **审计**：redesign-audit
- **研究**：prototyping-user-research / prototype-strategy / wireframe-prototyping / wireframe-spec

### 🛠️ 框架指南层（3）
- react-tailwind-guide / nextjs-design-guide / swiftui-design-guide

### 综合设计（4）
- baoyu-design / superdesign-1.0.0 / marketing-psychology / voice-tone-ux-writing

---

## 常用触发词速查

| 你说 | 自动执行 |
|------|---------|
| 审查这个页面 / 把把关 | /idesign audit 或 critique |
| 配色调整 / 品牌色 | /idesign colorize |
| 字体层级 / 排版 | /idesign typeset |
| 布局重构 / 间距对齐 | /idesign layout |
| 打磨 / 精修 / 润色 | /idesign polish |
| 帮我生成设计 Token | design-tokens |
| 帮我建暗色模式 | dark-mode-design |
| 滚到那钉住 / 视差 | gsap-web |
| 按钮 hover 触感 | micro-interaction |
| 线条一笔笔画出 | svg-animation |
| 橙线风插图 | orange-line-illustration |
| 数据做信息图 | baoyu-infographic |
| 画流程图 / 架构图 | markdown-mermaid-writing |
| 做个 AI 生图 PPT | GordenSuperPPTSkill |
| 检查无障碍 / a11y | accessibility-audit |
| 定品牌语调 | voice-tone-ux-writing |

---

## 依赖

- Claude Code 已安装
- Node.js ≥ 22（idesign 检测器建议）
- 无需 API Key（生图类需要自行配置 .env）

## License

Apache 2.0 — 可自由商用和修改。
