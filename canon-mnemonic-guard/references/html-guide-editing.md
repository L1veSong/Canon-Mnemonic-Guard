# HTML 旅行攻略编辑安全规则

> 2026-06-15 · 新疆伊犁攻略编辑实战教训
> 关联 CMG 坑点系列：execute_code 沙箱隔离、div 平衡、备份铁律

## 铁律

1. **改前必 cp 备份** — `cp file file.bak.$(date +%m%d%H%M)` 每次改前执行
2. **改后验 div 平衡** — `grep -c '<div'` vs `grep -c '</div>'` 必须相等
3. **验证再报完成** — grep 确认新内容存在后才说"好了"

## execute_code 编辑陷阱

### 陷阱 A：read_file 输出写入会带行号

`read_file()` 返回 `LINE_NUM|CONTENT` 格式。如果直接写回文件，行号前缀被当作文本内容。

✅ `open()` 读原始文件
❌ `read_file()` 作为编辑源

### 陷阱 B：多次 execute_code 互踩

每次 execute_code 独立读原始文件。先后修改同一文件时，第二次读到修改前版本，覆盖第一次。

✅ 一次 execute_code 完成所有修改

### 陷阱 C：删除 HTML 区段导致 div 不平衡

每个 food-city 卡片结尾需 5 个 `</div>`：
```
food-shop → guide-body → guide-content → day-body → glass-card
```
再加 2 个（container + page-container）才到下一页区段。

删除后必须：
1. `grep -c '<div'` vs `grep -c '</div>'` 验证
2. 检查边界 `</div>` 数量是否正确

## 高德 POI

- 精确格式：`https://www.amap.com/ssr/place/{POI_ID}`
- `web_extract` 对高德 SSR 页面 100% 失败 — 不要反复尝试
- 用户从手机提供 POI ID，AI 只替换链接+同步店名

## CSS nth-child 陷阱 (2026-06-19)

**❌ `.glass-card:nth-child(N)`** — nth-child 计所有 DOM 子元素，不按 class 过滤。D10/D11 在父容器是第12/13子元素，CSS 只写到11，漏了。

**✅ 用 JS 精确计数：**
```javascript
var cards = document.querySelectorAll("#page-index .glass-card");
cards.forEach(function(c, i) {
    c.style.animationDelay = (i * 80) + 'ms'; // 只数 .glass-card
});
```

## CSS/JS 拆分陷阱 (2026-06-19)

拆分单文件 HTML 为 index.html + style.css + script.js 时：
- body 提取后**必须检查有无多余空 `<script>` 标签**——浏览器将空 script 吞掉后面的 `<script src="...">`
- `grep -c '<script' index.html` 必须 = 1
- `grep -c '</head>'` 和 `grep -c '<body>'` 必须各 = 1
- 拆分后逐页面检查 tabbar 是否在 display:none 父容器内

## HTML 结构插入必须在完整标签前 (2026-06-19)

```python
# ❌ 切在 <div 和 id= 之间
html[:html.find('id="page-budget"')] + new + html[...]
# → 产生 id="page-budget"... 的裸露文本

# ✅ 找到完整 <div id="page-budget"
div_start = html.rfind('<div', 0, html.find('id="page-budget"'))
html[:div_start] + new + html[div_start:]
```

## display:none 页面的 Observer 盲区 (2026-06-19)

`#page-food` 等非首页默认 `display:none`，IntersectionObserver 在 setup 时无法检测内部元素。切标签时 `switchPage` 必须手动触发卡片交错渐入，不能仅依赖 Observer。
