# 🌊 Glassmorphism 毛玻璃效果

**一个零依赖的 CSS + SVG 玻璃效果实现方案，支持移动端和无障碍访问。**

---

## 快速演示

![](https://i.imgur.com/placeholder-preview.jpg)  
*鼠标悬停卡片查看玻璃折射和高光扫掠效果*

[在线演示](demo.html) | [查看配方](references/glass-recipes.md)

## 核心技术原理

### 四要素定律（Four Ingredients）

真实的玻璃必须同时具备这四个元素，缺一不可：

| 要素 | CSS 实现 | 目的 |
|------|----------|------|
| **霜（Frost）** | `backdrop-filter: blur(16px) saturate(160%)` | 让背景模糊成柔和色彩 |
| **半透明（Translucency）** | `background: rgba(255,255,255,0.12)` | 让内容可透视但不刺眼 |
| **边缘高光（Edge Highlight）** | `::before` + 线性渐变模拟光线扫掠 | 制造曲率和光线反射感 |
| **深度（Depth）** | 多层 `box-shadow` + inset 高光 | 让面板从背景中浮起 |

## 核心特性

- ✅ **苹果式 UI**：轻松打造 macOS/iOS 风格的透明界面
- ✅ **液态玻璃**：SVG 滤镜模拟真实液体折射
- ✅ **无障碍优先**：自动适配系统减少动效/透明度偏好
- ✅ **性能优化**：避免动画 blur-radius，使用 transform/backdrop-filter 分离
- ✅ **零构建依赖**：纯 CSS/SVG，直接使用

## 安装使用

直接复制 CSS 到你的样式表：

```css
/* 基础玻璃 */
.glass {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.35),
    inset 0 -1px 0 rgba(0, 0, 0, 0.12);
}

/* 悬停动画 */
.glass {
  transition: 
    backdrop-filter 0.4s ease,
    background 0.4s ease,
    box-shadow 0.4s ease,
    transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass:hover {
  backdrop-filter: blur(24px) saturate(180%);
  transform: translateY(-4px);
  box-shadow:
    0 16px 48px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.18);
}
```

## 进阶配方参考

- [边角高光](#edge-highlight) — 创建真实的光线反射环
- [抗噪点处理](#banding-removal) — 消除强模糊下的色彩断层
- [液态玻璃](#liquid-glass) — SVG feDisplacementMap 折射效果
- [无障碍降级](#accessibility) — 系统偏好兼容
- [性能调优](#performance) — 浏览器渲染最佳实践

## 兼容性支持

- Chrome/Edge/Firefox: 完整支持 `backdrop-filter`
- Safari: 需 `-webkit-backdrop-filter` 前缀（已包含）
- IE11: 不支持，提供 fallback 不透明样式
- 移动端: iOS Safari 支持良好，Android 部分版本有限

## 许可证

MIT License — 可以自由商用和修改。

[查看源代码](SKILL.md) | [贡献指南](CONTRIBUTING.md)

