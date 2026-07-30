# Claude Code 设计师开箱包

> **一键装好 35 个设计/动效/视觉 skill，支持中文口语触发。**
> 
> 装完就能说中文让 AI 做设计——"审查这个页面""按钮加个 hover 效果""滚到这里把元素钉住""生成一张橙线风插图"。

## 设计师能力概览

### 决策层（2）
- **idesign**（设计总监）— 23 子命令：建页面/审查/打磨/配色/排版/动效/布局/简化/加固/UX文案/响应式/性能/新手引导/浏览器实时迭代
- **motion-design**（动效方法论）— 迪士尼动画原则、缓动/时长/编排指导

### 动效实现层（19）
- **GSAP 引擎**（9）：gsap-core / timeline / plugins / react / frameworks / scrolltrigger / performance / utils / gsap-web（滚动动画一条龙）
- **微交互**：按钮 hover、开关 toggle、点赞心跳、Toast 弹窗、共享元素过渡
- **SVG 动画**：描边绘制、路径形变、图标动效
- **Lottie**：After Effects 动画播放、滚动联动、颜色控制
- **页面过渡**：路由切换、View Transitions API、Framer Motion
- **ASCII 动画**：黑客帝国风、终端字符画、网页复古特效
- **毛玻璃**：苹果风半透明模糊、磨砂弹窗、液态玻璃
- **60fps 优化**：卡顿排查、layout thrashing 诊断
- **无障碍动效**：prefers-reduced-motion、WCAG 合规
- **React 邮件模板**

### 视觉创建层（14）
- **插图/图像**（6）：通用 AI 出图 / 文章配图 / 橙线纽约客风 / Gemini 逆向出图 / GPT 风格库 / 小红书配图
- **封面**：5维×11色调×7渲染风格封面生成
- **信息图**：21×22 风格矩阵专业信息图
- **图表**：数据图表 + 科学可视化
- **架构/流程图**：Mermaid 图表 + 知识图谱 + 画布设计
- **图像处理**：压缩（WebP/PNG）+ ImageMagick 格式转换

## 安装方式

### 方式 1：一键脚本

```bash
# 解压并安装
tar -xzf designer-setup-*.tar.gz
cd designer-setup-*
bash designer-setup.sh
```

### 方式 2：手动安装

```bash
# 复制全部 35 个 skill
cp -r skills/* ~/.claude/skills/

# 复制中文路由表和 idesign 中文映射
cp config/design-router.md ~/.claude/
cp config/zh-commands.md ~/.claude/skills/idesign/reference/

# 如果 CLAUDE.md 还没有设计段，追加
echo '
### UI / 前端设计统一入口：/idesign

所有 UI 设计需求统一走 /idesign。视觉创建和动效交互另有独立路由表，详见 ~/.claude/design-router.md。
' >> ~/.claude/CLAUDE.md
```

## 装完直接说这些（中文=英文命令）

| 说什么 | 自动执行 |
|--------|---------|
| 审查 / 检查 / 把把关 这个页面 | /idesign audit 或 critique |
| 配色 / 调色 / 品牌色调整 | /idesign colorize |
| 字体 / 排版 / 字号层级 | /idesign typeset |
| 布局 / 间距 / 对齐 / 栅格 | /idesign layout |
| 打磨 / 精修 / 润色 / 再改改 | /idesign polish |
| 简化 / 做减法 / 太花哨了 | /idesign distill |
| 加点惊喜 / 趣味 / 记忆点 | /idesign delight |
| 大胆一点 / 收敛一点 | /idesign bolder / quieter |
| 浏览器里调 / 边改边看 | /idesign live |
| 动效设计 / 动画节奏 / 缓动 | motion-design |
| 滚动到那钉住 / 视差 / 气口 | gsap-web |
| 按钮 hover 触感 / 点赞心跳 | micro-interaction |
| 线条画出来 / SVG 形变 | svg-animation |
| 动画卡顿 / 掉帧 / 不流畅 | 60fps-animation |
| 毛玻璃 / 苹果风半透明 | glassmorphism |
| 生成 AI 插图 / 出图 | baoyu-image-gen |
| 文章配图 | baoyu-article-illustrator |
| 橙线风 / 纽约客插画 | orange-line-illustration |
| 封面图 / 头图 | baoyu-cover-image |
| 信息图 / 长图 / 一图读懂 | baoyu-infographic |
| 流程图 / 架构图 | markdown-mermaid-writing |
| 压缩图片 | baoyu-compress-image |

## 依赖

- Node.js ≥ 22（idesign 检测器需要）
- 无需 API Key（skill 自带）
- Claude Code 已安装

## 文件清单

```
designer-setup/
├── designer-setup.sh          # 一键安装脚本
├── README.md                  # 本文件
├── config/
│   ├── design-router.md       # 70条中文触发词→英文skill路由表
│   └── zh-commands.md         # idesign 子命令中文映射表
└── skills/                    # 35 个 skill 目录
    ├── idesign/
    ├── motion-design/
    ├── gsap-{core,timeline,plugins,react,frameworks,scrolltrigger,performance,utils,web}/
    ├── micro-interaction/
    ├── svg-animation/
    ├── lottie-animation/
    ├── page-transition-animation/
    ├── ascii-animation/
    ├── 60fps-animation/
    ├── accessible-animation/
    ├── glassmorphism/
    ├── react-email/
    ├── baoyu-{image-gen,article-illustrator,danger-gemini-web,xhs-images,cover-image,infographic,compress-image}/
    ├── orange-line-illustration/
    ├── gpt-image-2-style-library/
    ├── chart-visualization/
    ├── scientific-visualization/
    ├── markdown-mermaid-writing/
    ├── graphify/
    ├── canvas-design/
    └── imagemagick-conversion/
```

## 贡献

- idesign（原名 impeccable）by [Paul Bakaus](https://github.com/pbakaus/impeccable)
- GSAP skills by [GreenSock](https://github.com/greensock/gsap-skills)
- 其余 skill 来自 Claude Code Skills Marketplace
- 中文路由表 + 打包脚本由云龙维护
