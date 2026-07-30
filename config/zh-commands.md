# 中文命令映射表

用户说中文即自动路由到对应 idesign 子命令，无需记英文名。表里的触发词匹配时，加载对应的英文 reference 执行。

| 你说（中文口语） | 自动执行 | 加载 |
|---------|---------|------|
| 设计/建/做/画/写 个XX页面/组件/界面 | `shape` | [shape.md](shape.md) |
| 审查/检查/看看/把把关 XX | `audit`（技术质量）或 `critique`（UX体验） | [audit.md](audit.md) / [critique.md](critique.md) |
| 打磨/精修/润色/调整一下/再改改 XX | `polish` | [polish.md](polish.md) |
| 配色/颜色/调色/品牌色 XX | `colorize` | [colorize.md](colorize.md) |
| 字体/排版/字号/文字层级 XX | `typeset` | [typeset.md](typeset.md) |
| 动效/动画/过渡/交互效果 XX | `animate` | [animate.md](animate.md) |
| 设计规范/设计系统/token/组件库整理 XX | `extract` | [extract.md](extract.md) |
| 初始化项目/建立设计上下文 | `init` | [init.md](init.md) |
| 文案/按钮文字/标签/提示/报错信息 XX | `clarify` | [clarify.md](clarify.md) |
| 布局/间距/对齐/栅格 XX | `layout` | [layout.md](layout.md) |
| 简化/去掉多余/做减法/太花哨了 XX | `distill` | [distill.md](distill.md) |
| 加固/边界情况/空状态/加载态/出错处理 XX | `harden` | [harden.md](harden.md) |
| 浏览器里调/边改边看 XX | `live` | [live.md](live.md) |
| 大胆一点/更有冲击力 XX | `bolder` | [bolder.md](bolder.md) |
| 低调一点/收敛一点 XX | `quieter` | [quieter.md](quieter.md) |
| 加点惊喜/趣味/记忆点 XX | `delight` | [delight.md](delight.md) |
| 适应不同屏幕/手机适配/响应式 XX | `adapt` | [adapt.md](adapt.md) |
| 性能/加载慢/优化速度 XX | `optimize` | [optimize.md](optimize.md) |
| 新人引导/首次使用/空页面引导 XX | `onboard` | [onboard.md](onboard.md) |

> **注意**：`audit` 和 `critique` 的区别——`audit` 是技术质量（a11y/性能/响应式/语义化），`critique` 是 UX 体验（信息架构/认知负荷/视觉层次/可用性）。不确定时优先 `critique`。
