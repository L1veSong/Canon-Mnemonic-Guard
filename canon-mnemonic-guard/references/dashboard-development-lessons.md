# Dashboard 开发教训

> 2026-05-30 | 来源：CMG Dashboard 从零到可用的完整开发过程

## 架构

- `~/.hermes/dashboard/server.py` — HTTP服务器（localhost:8765），Python 标准库零依赖
- `~/.hermes/dashboard/generate.py` — 静态 HTML 生成器（备用，生成独立 HTML 文件）
- CLI 入口：`cmg dashboard`（`~/bin/cmg` wrapper）
- Hermes 入口：`!dashboard`

## Server 模式 vs 静态模式

| 模式 | 方式 | 数据 | 配置修改 |
|------|------|------|:--:|
| Server | `python3 server.py` | API实时读取 | ✅ POST /api/config |
| 静态 | `python3 generate.py` | 生成时嵌入JSON | ❌ |

Server 模式支持三个 API 端点：`GET /api/rules` `GET /api/stats` `GET /api/config`，以及 `POST /api/config` `POST /api/rules` `DELETE /api/rules`。

## 开发教训

### 1. 不要对嵌入HTML的Python文件做增量patch

**症状：** 整个开发过程用 `execute_code` 做增量 `content.replace()`，每次只改几行。结果：
- 替换漏了目标行（匹配到其他地方的同名文本）
- 引号转义被 Python/JS 双重解析吃掉（`\'` 在 Python 三重引号里只剩 `'`）
- CSS 规则被重复覆盖产生冲突（`position:fixed` 覆盖了 `position:absolute`）
- 列对齐丢失（header 加了 `<th>` 但 body 行没对应 `<td>`）

**正确做法：** 嵌入 HTML 的 Python 文件，改 HTML 部分时用 `write_file` 整段重写 HTML 模板字符串。不要 patch 单行。

### 2. table 单元格 tooltip 需要 z-index + overflow:visible

关键词展开气泡被 `overflow:hidden` 裁剪了三轮才修好。需要：
- `.table-wrap { overflow:visible }`
- `.keyword-cell { overflow:visible }`
- `.kw-tip { position:absolute; z-index:9999 }`
- 绝对定位的 tooltip 需要父元素 `position:relative`

### 3. 排序指示器不要用 JS 修改 textContent

用 `th span { padding-right:1.2em }` 预留固定空间，JS 只改箭头字符。避免字词位移。

### 4. innerHTML 重建会丢失展开状态

`renderRules()` 用 `innerHTML = html` 重建 tbody，会丢失用户展开的 detail 行。排序前要保存展开的 ID 列表，渲染后恢复。

### 5. 引用转义规则

在 Python 三重引号字符串中写 JS 的 onclick：
- `onclick="fn(\''+var+'\')"` → Python 解析时 `\'` → `'`，JS 得到 `fn(''+var+'')` → 语法错误
- 正确：用 `data-*` 属性 + `this.dataset.xxx` 完全避开引号问题

### 6. JS 全局代码在 DOM 就绪前执行

`var el = document.getElementById(...)` 写在全局作用域，脚本解析时 DOM 尚未渲染。必须放在 DOMContentLoaded 回调或 `loadAll()` 内部。

## 已安装的第三方 skill 使用情况

- `popular-web-designs` — 加载了 Linear 暗色设计系统作为视觉参考
- `claude-design` — 引用了 Motion 原则（subtle, clarifies state, respects reduced-motion）
- `ui-ux-pro-max` — uipro-cli 存在但搜索命令格式不对，实际未使用样式库
