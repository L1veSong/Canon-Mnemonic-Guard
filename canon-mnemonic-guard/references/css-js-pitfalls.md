# CSS/JS 常见坑点

> 来源：新疆伊犁行程 HTML 编辑实战（2026-06-19）

## 坑点 1：CSS 重复规则互盖

**症状：** `.glass-card` 有两个 `transition` 声明，第二个完全覆盖第一个，导致 `border-color` 过渡丢失。

**根因：** CSS 中同名选择器的 `transition` 是 shorthand——后出现的覆盖前一个，不是合并。

**检测命令：**
```bash
grep -n '\.glass-card{transition:' style.css
# 如果输出多行 → 有覆盖问题
```

**修复：** 合并为一条：
```css
/* ❌ 两条会互盖 */
.glass-card{transition:transform 0.35s...,border-color 0.3s}
.glass-card{transition:transform 0.35s...,box-shadow 0.3s}

/* ✅ 合并为一条 */
.glass-card{transition:transform 0.35s...,border-color 0.3s,box-shadow 0.3s}
```

## 坑点 2：CSS 伪元素重复定义

**症状：** `.glass-card::before` 出现两次完全相同的规则。浏览器只认最后一个。

**检测：**
```bash
grep -c '\.glass-card::before' style.css
# >1 → 有重复
```

**修复：** 删掉第一个，只保留一个。

## 坑点 3：空 CSS 规则

**症状：** 无用规则如 `.glass-card{}` 不报错但浪费字节、混淆审计。

**检测：**
```bash
grep -n '\{\s*\}' style.css
```

**修复：** 直接删除。

## 坑点 4：IntersectionObserver 与 DOMContentLoaded 的竞态

**症状：** Observer 在脚本末尾同步设置、异步触发 → 早于 DOMContentLoaded 回调执行 → 卡片提前显示 → D10/D11 不参与交错序列。

**根因：** 执行顺序：
1. 脚本末尾：加 `.reveal` 类 → 启动 Observer
2. Observer 异步回调触发 → 加 `.visible` → CSS 过渡开始
3. DOMContentLoaded 才设 `transitionDelay` → **太晚了**

**修复：** 交错逻辑（`transitionDelay` 等）必须放在 Observer 启动**之后、回流之前**的同步代码中，不能放在 DOMContentLoaded。

## 坑点 5：`!important` 行内样式锁死后续过渡

**症状：** 在 `setAttribute('style', 'opacity:0!important...')` 之后，卡片的 `opacity` 被永久锁死 → 后续 `switchPage` 的 `c.style.opacity='0'`（无 `!important`）无法覆盖 → 切标签页动画失效。

**修复：** 绝对不用 `setAttribute('style', ...)` 加 `!important`。用 `c.style.setProperty('opacity', '0', 'important')` 单独设，后续用 `c.style.opacity = '1'` 普通覆盖。

## 坑点 6：`transition-delay` 行内样式兼容性

**正确用法：** `c.style.transitionDelay = (i*80)+'ms'` — 与 CSS 的 `transition` shorthand 并存，不会互相覆盖。

**错误用法：** 用 `setAttribute('style', 'transition-delay:80ms')` 会替换掉所有行内样式。

## 坑点 7：文件拆分后路径问题

**症状：** 单 HTML 拆成 `index.html` + `style.css` + `script.js` 后，本地打开空白。

**检查清单：**
- [ ] `<link href="style.css">` 路径正确（相对，不带 `/`）
- [ ] `<script src="script.js">` 路径正确
- [ ] CSS/JS 文件大小 >0（不是空文件）
- [ ] `open index.html` 直接打开能看到内容
