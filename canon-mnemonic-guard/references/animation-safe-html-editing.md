# 动画安全HTML编辑指南

> 来源：2026-06-17 新疆旅行攻略HTML动画调试，3小时12次迭代

## 核心原则

**改HTML内容时，绝不碰CSS/JS动画代码。** 一旦触碰，连锁崩溃很难恢复。

## 铁律

### 1. 改前备份（CMG已有，重申）
```bash
cp file.html file.html.bak.$(date +%m%d%H%M)
```

### 2. 永远不要用 setAttribute('style', ...) 来隐藏/显示元素
- `setAttribute` 整条替换行内样式，`!important` 永久锁死后无法覆盖
- 后果：切标签后卡片无法再隐藏、hover过渡失效、所有CSS动画僵死
- ✅ 用 `c.style.opacity = '0'`（普通行内样式，可被后续代码覆盖）

### 3. 永远不要修改 IntersectionObserver 的回调逻辑
- Observer 只负责加/去 CSS 类，不改时序
- 要加交错延迟 → 用 CSS `transition-delay`，不改 Observer
- ✅ 错：在 Observer 回调里加 setTimeout
- ✅ 对：`c.style.transitionDelay = (i*80)+'ms'`

### 4. transition-delay 必须在 Observer 触发前写入
- Observer 回调是异步的（下次微任务/动画帧）
- 在 `obs.observe(el)` 之后、Observer 回调之前同步写入 `transitionDelay`
- 如果放在 `DOMContentLoaded` 里 → 太晚，Observer 已触发

### 5. 避免容器选择器 `#page-id .class`
- DOM 嵌套层级复杂时，`#container .glass-card` 可能找不全
- 容器关闭位置漂移导致部分元素被排除
- ✅ 用 `.glass-card` 全局选择器（确保页面内无同名类冲突）

## 调试技巧

### 验证交错是否生效
```javascript
// 在控制台检查
document.querySelectorAll(".glass-card").forEach((c,i) => {
  console.log(i, c.style.transitionDelay, c.querySelector('h3').textContent);
});
```

### 快速诊断：动画"生硬"
- 检查是否有 `!important` 行内样式残留 → `grep '!important' file.html`
- 检查 `transition` 是否被覆盖 → CSS 中多个同名规则，后者覆盖前者
- 检查时长 → 原版 0.6s cubic-bezier，改错成 0.5s ease

### 快速诊断：D10/D11 不接序列
- 确认选择器找全了 → `querySelectorAll(".glass-card").length === 11`
- 确认 `transitionDelay` 在 Observer 触发前写入 → 检查代码顺序
- 检查 `#page-index` 是否提前闭合 → 数 div 开闭次数

## 本次实战教训

| 失败尝试 | 为什么失败 |
|---------|-----------|
| `setAttribute('style','opacity:0!important')` | 永久锁死行内样式，后续操作无效 |
| 修改 Observer 回调加 setTimeout | 与 CSS 类过渡冲突，D10/D11 闪烁 |
| DOMContentLoaded 里写 transitionDelay | Observer 已在主脚本触发，时间差导致丢卡 |
| `#page-index .glass-card` 选择器 | 容器 div 不平衡，D10/D11 不在选择范围内 |

**最终可行方案**：主脚本中 `obs.observe()` 之后立即用 `.glass-card` 全局选择器写入 `transitionDelay`，不改 Observer，不设 !important。
