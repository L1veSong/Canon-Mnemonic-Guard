# HTML编辑防坑指南

## 核心铁律

1. **改前必须备份** — `cp file.html file.html.bak.$(date +%m%d%H%M)`
2. **用 `open()` 读文件，禁止用 `read_file()`** — `read_file()` 返回行号前缀 `373|373|`，写入文件会永久损坏
3. **改后立即 `grep` 验证** — 确认改动生效、计数正确、HTML标签闭合

## execute_code 陷阱

### 陷阱1：read_file 行号污染
```
❌ result = read_file(path) → 内容含 "374|374|<div id=..."
✅ with open(path) as f: html = f.read() → 纯净内容
```
`read_file()` 返回格式 `LINE_NUM|CONTENT`，直接写入会污染 HTML。

### 陷阱2：execute_code 多次调用互踩
每次 `execute_code` 从磁盘独立读取原始文件。如果两次调用修改同一文件，第二次会覆盖第一次。修改同一文件必须**一次 execute_code 完成所有操作**。

### 陷阱3：minified HTML 中的 patch 容易截断
单行超长 minified HTML，`patch` 的 old_string 如果不够独特，可能匹配到错误位置、截断内容。优先用 `execute_code` + Python 正则定位再 `str.replace`。

## 备份策略

- 每次修改前 `cp` 备份
- 保留最近 2-3 个备份即可，旧的及时清理
- 桌面不留超过 5 个 `.bak` 文件

## 动画修改陷阱

### 陷阱4：setAttribute('style', ...) + !important = 永久锁死

```html
<!-- ❌ 致命错误 -->
c.setAttribute('style', 'opacity:1!important;transform:translateY(0)!important');
```
`setAttribute` 替换整条行内样式，`!important` 让它无法被后续任何 CSS/JS 覆盖。交错结束后卡片永久锁定 `opacity:1`，后续的 hover、切标签、重新加载——全部过渡失效。

```html
<!-- ✅ 正确 -->
c.style.opacity = '1';
c.style.transform = 'translateY(0)';
```
用 `c.style.xxx` 逐属性设，不写 `!important`，不会锁死。

### 陷阱5：IntersectionObserver 与 DOMContentLoaded 竞速

Observer 在主脚本底部启动，DOMContentLoaded 晚一步触发。Observer 先加 `.visible` 类 → CSS 让卡片闪现 → DOMContentLoaded 的交错才设 `opacity:0`。折页下的卡片（D10/D11）尤其明显。

**✅ 正确做法：修改 Observer 回调本身加交错延迟**

```javascript
// 先给每个元素标序号
el.setAttribute('data-stagger', i);

// Observer 回调中按序号延迟
var idx = parseInt(e.target.getAttribute('data-stagger')) || 0;
setTimeout(function(){
  e.target.classList.add("visible");
}, idx * 80);
```

不要另起炉灶在 DOMContentLoaded 里加交错——跟 Observer 必然打架。

### 陷阱6：大屏幕上所有卡片同在视口 → Observer 瞬间全触发

3024×1964 等高分辨率屏幕，D1-D11 全在首屏。Observer 对所有卡片同时触发，不加延迟就是瞬间全弹出来。`data-stagger` + `idx*80` 是唯一可靠方案。

### 陷阱7：改旅行 HTML 只能动文字

用户明确区分"完美版"（特效/排版/布局不动）和"内容版"。修改时：
- ✅ 只替换文字：标题、日期、酒店名、行间内容、tips
- ❌ 不碰：CSS 类名、`@keyframes`、`<script>`、HTML 结构、`data-*` 属性
- 必须在改前 `cp` 备份，改后 `grep` 验证零残留

### 陷阱8：CSS 重复规则和冲突 transition 是无声炸弹

CSS 不会报错。两条同名规则、两个 `transition` 简写——浏览器静默取最后一条，第一条的过渡属性永久丢失。

**必须审计的项目：**
```bash
# 查重复规则
grep -o '\.glass-card[^{]*{' file.html | sort | uniq -c | grep -v ' 1 '

# 查同名伪元素
grep -o '\.glass-card::before' file.html | wc -l  # 必须 = 1
```

### 陷阱9：transition-delay 是最干净的卡片交错方案

```javascript
// ✅ 最简：Observer 不做交错，只加 CSS delay
dayCards.forEach(function(c,i){
  c.style.transitionDelay = (i*80) + 'ms';
});
```

- 不改 Observer 逻辑
- 不写 `!important`
- 不改现有 CSS 过渡
- `transition-delay` 是标准 CSS 属性，与 `transition` 共存

**放在 Observer 设置之后、第一次回调触发之前**，确保 delay 在 `.visible` 添加前已就位。

### 陷阱10：`#page-index .glass-card` 可能漏掉折页下卡片

HTML 中有 div 未闭合（329 open / 328 close），`#page-index` 容器可能在 D10 之前就关闭了。用全局 `.glass-card` 选择器 + `transition-delay` 一次解决，不再依赖父容器。

## 恢复流程

如文件已损坏（行号污染/截断/动画崩坏），按优先级：
1. 找最新 `.bak.*` 恢复
2. 找 `.pre-search.bak` / `.food.bak` 等命名备份
3. 找用户要新版备份
4. 动画崩坏且找不到备份 → 从最早备份恢复完整 `<script>` 块

## 元规则：修复级联反模式

**症状：** 一个动画问题 → 尝试方案A（失败）→ 叠方案B（更差）→ 方案C（引入新bug）→ 方案D（试图同时修A+B+C）→ 全崩。最终回退，浪费时间+信任。

**正确做法：**
1. 任何修复失败一次 → 先 `grep` 验证当前状态，不要盲猜
2. 第二次失败 → 回退到最近可用备份，重新分析
3. 用户说"越改越乱"/"别改了" → 立即停手，回退最新备份，承认不知道
4. **动画问题优先用 CSS 原生特性（`transition-delay`），不动 JS Observer**

## 成功模式：纯文字替换

本次最顺的部分：赛→伊→库→那 改成 赛→伊→那→唐→奎→乌，动了几十处文字和标题，零 bug。

**关键：**
- 只换 `<h3>` `<p>` `<li>` `<span>` 内的中文文本
- 不改任何 CSS 类名、HTML 结构、`<script>`、`<style>`
- 每批改完后逐天验证标题/日期/酒店一致
- 改前 `cp` 备份，改后全量 grep 残留

## 2026-06-19 新增

### 陷阱11：display:none 父容器吞掉子元素——DOM中有但看不到

**症状：** `<nav class="tabbar">` DOM中存在、5个子元素、`display:flex`、`position:fixed`，但页面完全看不到。`getBoundingClientRect()` 返回 `y=0, height=0`。

**根因：** nav 被嵌套在 `#page-budget` 内（`style="display:none"`）。之前替换 budget 内容时破坏了 div 嵌套平衡。

**诊断命令：**
```javascript
var el = document.querySelector('可疑元素');
while(el) {
  var cs = getComputedStyle(el);
  if(cs.display === 'none') {
    console.log('TRAPPED inside:', el.tagName + (el.id ? '#'+el.id : ''));
    break;
  }
  el = el.parentElement;
}
```

**修复：** nav 必须移到所有 `id="page-*"` div 的外面。补全缺失的 `</div>` 闭合标签。

### 陷阱13：拆分HTML时多余空`<script>`标签——浏览器吞掉外部JS

**症状：** 拆成 index.html + style.css + script.js 后，`switchPage` undefined，底部导航不工作。`<script src="script.js">` 标签存在但未加载。

**根因：** 从原文件提取 body 内容时，`</style>` 和 `<script>` 之间多了一个空 `<script>` 标签：
```html
<script>
<script src="script.js"></script>
```
浏览器解析：第一个 `<script>` 开启内联脚本块 → `<script src="script.js">` 被当作文本内容 → 外部 JS 永不加载。

**修复：** 构建 index.html 后，`grep -c '<script'` 必须 = 1。

### 陷阱14：预算页面替换破坏 div 嵌套平衡

**症状：** 替换 budget 页面的 HTML 文本后，底部导航栏消失。检查发现 nav 被嵌套在 `#page-budget`（`display:none`）内。

**根因：** 旧 budget 区域 18个 `<div` 开 / 9个 `</div>` 闭（净开9个），替换文本只有 3开4闭。page-budget 的闭合 `</div>` 被替换文本吞掉，导致 nav 落入 budget 容器。

**正确做法：**
1. 替换前数清 `grep -o '<div' old.txt | wc -l` 和 `grep -o '</div>' old.txt | wc -l`
2. 新文本保持相同 net opens/closes
3. 替换后用 browser_console 检查关键元素祖先链无 `display:none`

### 陷阱15：拆分时页面ID可能丢失

**症状：** 从完整版 HTML 提取 body → 构建新 index.html 后，`page-food`、`page-prepare` 等某个页面 div 消失。标签页点不动。

**正确做法：**
```javascript
// 部署后立即验证
['page-index','page-prepare','page-notes','page-food','page-budget']
  .map(id => id + ':' + !!document.getElementById(id))
```
任一返回 `false` → 从完整版 HTML 重新提取对应区域，`grep` 确认后再部署。

### 陷阱17：Token 管理——shell `echo` 会把 `...` 当字面量写入

**症状：** `echo "ghp_xxx...yyy" > /tmp/token` 写入的是字面的 `...`（三个点），不是完整 token。Python 读到 16 字节假 token，API 返回 401。

**正确做法：**
```python
# ✅ write_file 写入完整内容（不经过 shell 转义）
write_file("/tmp/gh_token", token_string)

# ✅ Python 读文件用完整 token
with open('/tmp/gh_token') as f:
    token = f.read().strip()
```

**token 存储：** `~/.hermes/tokens/api-keys.txt`，格式 `服务名: token`，不在对话中展示。

### 陷阱18：Fine-grained vs Classic GitHub Token——后者省心

| | Fine-grained | Classic |
|------|------------|--------|
| 权限 | 逐仓库选 + 逐权限勾 | 一把 `repo` 全通 |
| 适用 | 精细控制 | 个人项目 |
| 失效 | 漏选仓库 → 401 | 不易失效 |

**教训：** 用户数小时反复 401，根因是 Fine-grained token 没勾仓库的 Contents 写权限。换成 Classic (`ghp_`)，勾 `repo`，一次通过。

### 陷阱19：`transitionDelay` 对折页下卡片无效——要用 Observer 回调内延迟

**症状：** D1-D9 交错动画正常，D10-D11 瞬现无动画。

**根因：** `c.style.transitionDelay = (i*80) + 'ms'` 从页面加载开始计时。D10 延迟 720ms，D11 延迟 800ms。但它们是折页下的卡片——等用户滚动到视口时，延迟早已过期。

**正确做法：** 
```javascript
// 给卡片标序号，Observer 回调中延迟加 .visible——从滚动触发开始计时
var idx = parseInt(e.target.getAttribute('data-stagger')) || 0;
setTimeout(function(){ e.target.classList.add("visible"); }, idx * 80);
```

### 陷阱20：插入 nav 标签项——锚点必须选 `<div` 开头，不能选中途字符串

**症状：** 在 nav 中插入"景点"标签后，预算标签被拦腰截断。

**正确做法：**
```python
# ✅ 找完整的标签项开头
budget_marker = '<div class="tabbar-item" onclick="switchPage(\'budget\')">'
html.replace(budget_marker, spots_item_html + budget_marker)
```

### 陷阱21：Vercel 单 HTML 部署——GitHub API 422 "sha" 冲突

**正确做法：** 每次 PUT 前先 GET 获取最新 `sha`，不要复用旧值。

```python
# 1. GET sha
r = Request(f'https://api.github.com/repos/{repo}/contents/{path}')
sha = json.load(urlopen(r))['sha']
# 2. PUT with sha
body = {'message': msg, 'content': b64, 'sha': sha}
```

### 陷阱24：display:none 的页面——卡片需要 switchPage 手动交错，Observer 帮不上忙

**症状：** 美食页的城市卡在切标签时瞬现无动画。展开城市栏后美食店铺也没动画。

**根因：** 双层 Observer 失效：
1. **首层：** 主 Observer 给所有 `.glass-card` 加 `.reveal`，但 `#page-food` 有 `display:none` → 卡片尺寸为零 → Observer 不触发
2. **二层：** 美食 Observer 监听 `.guide-body`——这些也在 `display:none` 内

**正确做法：**
```javascript
if (n === 'food') {
  var foodCards = page.querySelectorAll('.glass-card');
  foodCards.forEach(function(c, i) {
    c.style.opacity = '0'; c.style.transform = 'translateY(20px)';
    setTimeout(function() {
      c.style.transition = 'opacity 0.5s ease,transform 0.5s cubic-bezier(0.16,1,0.3,1)';
      c.style.opacity = '1'; c.style.transform = 'translateY(0)';
    }, i * 80);
  });
}
```

**症状：** D1-D9 卡片有 blurFadeUp 交错动画，D10-D11 瞬现无动画。

**根因：** `:nth-child()` 按**父容器所有子元素**（不限 class）顺序编号。`:nth-child(12)`（D10）和 `:nth-child(13)`（D11）无规则 → `animation-delay:0s`（默认）→ 跟 D1 同时启动。

**正确做法：用 JS 计数匹配元素，设 `animation-delay`**
```javascript
var dayCards = document.querySelectorAll("#page-index .glass-card");
dayCards.forEach(function(c, i) {
  c.style.animationDelay = (i * 80) + 'ms';
});
```
JS `querySelectorAll` 返回严格匹配的元素列表，索引 0-10 精确对应 D1-D11。

**症状：** 一个 D10/D11 动画问题，尝试了 6+ 种方案全部失败。用户说"别改了"。

**规则：**
1. 同问题尝试 2 次修复失败 → 回退到最近可用备份
2. 用户说"别改"→ 立即停手，`cp .bak.最新` 回退
3. 承认不知道，记录问题等待更好时机
4. 清理所有残留（`data-stagger`、`inline position`、`nth-last-of-type` CSS）

---

## 2026-07-05 新增

### 陷阱25：畸形 HTML 标签 `<div <!-- COMMENT -->` — 一个字节毁掉整个 DOM

**症状：** 底部导航栏完全消失。div 总数平衡（opens==closes），`<nav class="tabbar">` 在 DOM 中可见，CSS `display:flex; position:fixed` 正常——但页面就是看不到。

**根因：** 原始文件第 616 行有畸形标签：
```html
<div <!-- ===== PAGE: SPOTS ===== -->
```
这不是合法的 HTML。浏览器将 `<!-- =====` 视为 `<div` 的属性，然后整个 spots 节、overlay 层、tabbar、script 全部被吞进一棵畸形 DOM 树。**div 配对扫描完全检测不到这个问题**——因为 `<div` 和 `</div>` 在字面上仍然配对，只是结构被破坏了。

**检测命令：**
```bash
grep -n '<div <!--' file.html    # 任何输出都是致命错误
grep -n '<div[^>]*<!--' file.html  # 更宽泛的检测
```

**修复：** 改畸形标签为正常注释 + 独立 `<div>`：
```html
<!-- ===== PAGE: SPOTS ===== -->
<div id="page-spots" style="display:none">
```

**教训：** div 数量平衡 ≠ DOM 结构正确。HTML 注释不能在 `<div>` 标签内部——浏览器解析器不会报错，只会静默地制造一个 DOM 黑洞。

### 陷阱26：补丁式编辑累积导致 div 嵌套漂移

**症状：** 连续 6 轮 `patch` 工具修改同一 HTML 文件，每次都验证 div 配对通过。但用户反复报告"导航栏还是没有"。最终发现 tabbar 被嵌套在 `#page-budget`（`display:none`）里。

**根因：** 8 次独立的 `patch` 调用 = 8 次独立的字符串替换。每次 patch 基于上一轮修改后的状态——一旦某次替换改变了关键 div 的边界，后续 patch 锚定旧位置就产生错位。单次验证 opens==closes 看不出嵌套顺序错误。

**正确做法（atomic write 原则）：**
1. 涉及 3+ 处编辑的同文件 → 恢复干净备份
2. 所有修改在**一次 `execute_code`** 中完成
3. 用 Python `str.replace()` 链式操作，全部完成后再一次 `write_file`
4. 改后立即 `grep -c '<div'` 和 `grep -c '</div>'` 验证总量，再用 diff 对比备份

```python
# ✅ atomic write
with open("file.html", "r") as f:
    html = f.read()
html = html.replace(old1, new1)
# ... all edits in one pass ...
with open("file.html", "w") as f:
    f.write(html)
```

**对比：** ❌ 6 个独立 `patch` → DOM 嵌套漂移 → 用户报 6 次"还是没有" → 信任消耗。✅ 1 个 `execute_code` 做 15 处编辑 → 一次验证 → 1 轮搞定。

### 陷阱27：Safari 强缓存 — CMD+R 不够

**症状：** 文件在磁盘上已修复且 `grep`/`diff` 多次验证正确，用户反复说"还是没有"。共报告 6 次。

**根因：** Safari 对本地 `file://` URL 的文件做**不区分时间戳的激进缓存**。CMD+R（普通刷新）不重新读取磁盘文件。

**正确做法：**
1. 确认文件正确后，必须告诉用户用 **CMD+Shift+R** 或隐身窗口打开
2. 如果用户第二次说"还是没有"→ **不要再改文件**（文件已经对了），直接告诉用户清缓存
3. 第三次 → 帮用户 `open -a Safari` 然后截图验证，不要进入修复循环

### 陷阱28：`spot-card-tap` 样式未定义 — 可点但无指针

**症状：** 景点卡片加了 `onclick="openSpot(...)"` 可以点开，但没有光标变化或 hover 效果，用户不知道可以点。

**修复（CSS）：**
```css
.spot-card-tap { cursor: pointer; }
.spot-card-tap:active { transform: scale(0.96); }
```

### 陷阱29：景点卡片 — 不去的景点不加，关闭的景点标注

**原则：**
- 行程里的景点 → 加卡片 + 叠层
- 参考攻略里提了但不在行程 → 不加卡片，不引入无关推荐
- 行程里有但关闭了 → 保留卡片，标注 `⚠️暂停开放`，叠层写替代方案
- 用户原话"留下我们去的，不去的删掉"——参考攻略是素材库，不是景点清单