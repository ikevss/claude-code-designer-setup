# 动效与视觉创建 — 中文路由表

你不需要记住任何英文 skill 名。用中文描述你要做什么，AI 自动匹配下表，路由到正确的 skill。

---

## 动效与交互（Motion & Interaction）

> **决策优先**：动效问题先看 `motion-design`（该不该动、怎么动舒服），再找实现 skill（怎么写代码）。

### 决策层

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 动画节奏不对、不知道用哪个缓动曲线 | `motion-design` | 动效方法论指导（时长/缓动/编排） |
| 加载动画没灵魂、页面过渡太生硬 | `motion-design` | 迪士尼动画原则应用 |
| 多个元素动画怎么编排先后顺序 | `motion-design` | 动效编排指导 |
| 这个动画该不该加、怎么加才舒服 | `motion-design` | 动效设计决策 |

### 执行层

| 你说 | 路由 | 做什么 |
|------|------|--------|
| **滚动动画** |
| 页面往下滚才触发动画 | `gsap-web` | GSAP ScrollTrigger 滚动触发动画 |
| 滚到某个区域把元素钉住/吸顶/固定 | `gsap-web` | pin 固定元素 |
| 横向滚动页面、横滚效果 | `gsap-web` | 横向滚动 |
| 滚动时动画跟着手指走、scrub | `gsap-web` | scrub 滚动绑定 |
| 首页大标题逐词飞入、入场动画时间线 | `gsap-web` | 复杂滚动动画编排 |
| 滚动时图片/卡片不同速度、视差滚动 | `gsap-web` | parallax |
| **微交互** |
| 按钮hover/press的反馈效果 | `micro-interaction` | 按钮微交互 |
| 开关toggle过渡、点赞心跳动效 | `micro-interaction` | toggle/点赞动效 |
| Toast通知滑入滑出、提示弹窗动画 | `micro-interaction` | 通知/弹窗动画 |
| 列表项增删排序动效 | `micro-interaction` | 列表过渡动画 |
| 点击一张图展开到详情页（共享元素过渡） | `micro-interaction` | 共享元素过渡 |
| 抽屉/弹窗进出动画 | `micro-interaction` | overlay 动画 |
| **SVG 动画** |
| 线条一笔笔画出、描边动画、签名效果 | `svg-animation` | SVG 描边动画 |
| 一个形状变成另一个形状（路径形变/morph） | `svg-animation` | SVG path morphing |
| 图标/Logo 动起来、元素沿路径移动 | `svg-animation` | SVG 图标/路径动画 |
| SVG渐变或滤镜的动画 | `svg-animation` | SVG 滤镜动画 |
| **Lottie 动画** |
| 在网页/App里播放AE动画 | `lottie-animation` | Lottie 播放 |
| 动画跟着滚动播放、运行时改Lottie颜色 | `lottie-animation` | Lottie 交互控制 |
| 用Lottie做loading动效或空状态 | `lottie-animation` | Lottie 状态动画 |
| AE动画导出Lottie注意事项 | `lottie-animation` | Lottie 导出指导 |
| **页面过渡** |
| 路由跳转过渡、页面间淡入淡出/滑动 | `page-transition-animation` | 页面切换动画 |
| View Transitions API、Next.js 页面过渡 | `page-transition-animation` | View Transitions / Next.js |
| Framer Motion AnimatePresence 离开动画 | `page-transition-animation` | AnimatePresence 调试 |
| **GSAP 底层引擎**（gsap-web 不够用、需要精细控制时） |
| 做动画、让元素动起来、入场出场 | `gsap-core` | GSAP 核心 tween API |
| 多个动画排队、时间轴编排 | `gsap-timeline` | GSAP Timeline |
| 需要 GSAP 某个插件、文字逐字动画 | `gsap-plugins` | 插件查询（SplitText/DrawSVG/Flip等） |
| React 里怎么写 GSAP | `gsap-react` | useGSAP Hook |
| Vue/Svelte/Nuxt 里怎么写 GSAP | `gsap-frameworks` | 非 React 框架集成 |
| GSAP 动画卡顿、掉帧、性能优化 | `gsap-performance` | 性能调优 |
| GSAP 工具函数、mapRange/clamp/random | `gsap-utils` | 工具函数 |
| **性能与无障碍** |
| 动画不流畅、掉帧、页面滚动卡 | `60fps-animation` | 60fps 性能诊断 |
| hover效果一顿一顿、CSS动画性能差 | `60fps-animation` | layout thrashing 排查 |
| 用户嫌动画晃眼、有人会晕动症 | `accessible-animation` | prefers-reduced-motion |
| 需要尊重系统"减少动态效果"设置 | `accessible-animation` | 无障碍动效合规 |
| **特殊效果** |
| 毛玻璃/磨砂/半透明模糊卡片或导航栏 | `glassmorphism` | Glassmorphism |
| 苹果风格半透明效果、frosted glass | `glassmorphism` | frosted glass UI |
| 黑客帝国风格字符动画、终端loading | `ascii-animation` | ASCII 动画 |

---

## 视觉创建（Visual Creation）

### 插图/图片生成

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 生成一张插图/配图、AI出图 | `baoyu-image-gen` | 通用 AI 图像生成（GPT/Azure/Google/OpenRouter 多厂商，默认主力） |
| 给文章生成配图、文章插图 | `baoyu-article-illustrator` | 文章配图（自动分析文章结构+匹配风格） |
| 纽约客风格插画、细黑墨线橙点缀 | `orange-line-illustration` | 橙线风格极简插画 |
| Gemini 出图、需要多轮对话调图 | `baoyu-danger-gemini-web` | Gemini Web 独有能力（逆向 API + 视觉输入） |
| GPT Image 风格参考、看有哪些风格可选 | `gpt-image-2-style-library` | GPT Image 2 风格库（参考工具，非生成器） |
| 小红书配图/图文 | `baoyu-xhs-images` | 小红书图片 |

### 封面/头图

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 生成封面图/文章封面/头图 | `baoyu-cover-image` | 5维×11色调×7渲染封面生成 |
| 电影宽屏封面、banner横幅 | `baoyu-cover-image` | 封面图 |

### 信息图

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 做信息图、长图、一图读懂、图解 | `baoyu-infographic` | 21种布局×22种风格信息图（唯一主力） |
| 把文字内容做成信息图 | `baoyu-infographic` | 信息图生成 |
| 把数据做成可视化图表 | `chart-visualization` | 数据图表 |
| 科学研究数据可视化、学术图表 | `scientific-visualization` | 科学可视化 |

### 架构图/流程图

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 画流程图、时序图、架构图、类图 | `markdown-mermaid-writing` | Mermaid 图表 |
| 知识图谱、关系图谱 | `graphify` | 知识图谱 |

### 图像处理

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 压缩图片、转 WebP/PNG | `baoyu-compress-image` | 图片压缩 |
| 图片格式转换、裁剪、缩放、加水印 | `imagemagick-conversion` | ImageMagick 图像处理 |

### 邮件模板

| 你说 | 路由 | 做什么 |
|------|------|--------|
| 做欢迎邮件/密码重置/通知/订单确认邮件 | `react-email` | React 邮件模板 |
| 用 React 组件写 HTML 邮件 | `react-email` | react-email 组件 |

---

## 路由规则

1. **动效问题优先问 motion-design**：不知道该怎么做动画时，先让动效方法论给建议，再找实现 skill
2. **信息图用 baoyu-infographic**（唯一主力，infographic-creator 和 infographics 已禁用）
3. **插图生成默认用 baoyu-image-gen**（多厂商覆盖面最广），特定风格时按表路由（橙线→orange-line-illustration，Gemini 多轮→gemini-web）
4. **GSAP 优先用 gsap-web**：高层封装满足大多数场景；需要精细控制时才下沉到 gsap-core/timeline
5. **idesign 管 UI 设计，本表管动效+视觉创建**：不重叠，但可串联（idesign 说"这里需要动效"→ motion-design 给方案 → gsap-web 实现）
