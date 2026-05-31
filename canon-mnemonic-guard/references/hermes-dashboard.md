# CMG Dashboard — 配套可视化工具

> 独立项目，不入 CMG 四包。Python 脚本读取 self-reflection/ 数据 → 生成单个 HTML 文件 → 浏览器打开。

## 文件位置

- 生成器: `~/.hermes/dashboard/generate.py`（含 CMG SKILL.md scripts/ 副本）
- 输出: `~/Desktop/canon-mnemonic-guard-dashboard.html`（可自定义 `--output` 参数）
- 规划: `~/.hermes/plans/cmg-dashboard_task_plan.md`

## 设计风格

GitHub 暗色系 + Linear 风格：
- 暗色背景 `#0d1117` · 亮色背景 `#ffffff` · 强调色 `#5c5cff` · Inter 字体
- 一键亮暗切换，自动记忆 + 跟随系统 `prefers-color-scheme`
- 来源: `popular-web-designs/templates/linear.app.md`

## Phase 1 功能（已实现）

- 6 张统计卡片（规则总数 / 累计命中 / 系统拦截 / 错误记录 / 高误报 / 长期未触发）
- Top 5 / Bottom 5 规则排行面板
- 全部规则可排序可筛选表格（类型筛选 + 关键词搜索 + 6 列排序）
- 数据内嵌为 JSON，零外部依赖
- JS 异常捕获 + 行数显示

## Phase 2-4 规划

见 `~/.hermes/plans/cmg-dashboard_task_plan.md`

## 技术要点

- 纯 Python 3 脚本，零第三方依赖（标准库 yaml + json + glob + re + datetime）
- HTML 数据内嵌，不发起网络请求，无 CORS 问题
- 浏览器安全沙箱兼容：数据在生成时预嵌入，不在运行时读本地文件

## 坑点（本 Session 学到）

### 1. 对外文本禁止使用 "CMG" 缩写
Dashboard 作为对外分发的项目，界面中必须使用完整名称 "Canon-Mnemonic-Guard" 或 "三省引擎"。已入 ban 规则 `ban_no_cmg_abbreviation`。

### 2. 暗色主题对比度必须足够
Linear 原版 `#08090a` + `#d0d6e0` 在部分屏幕上可读性差。降级到 GitHub 暗色系 `#0d1117` + `#c9d1d9`/`#e6edf3`。同时提供亮色模式兜底。

### 3. days_since 日期解析必须处理多种 ISO 格式
`datetime.fromisoformat()` 对 date-only、naive datetime、timezone-aware datetime 行为不同。用多格式 fallback 循环 + 显式 tzinfo 补齐。

### 4. JSON 嵌入 HTML 必须转义 `</script>`
规则关键词中如果出现 `</script>` 会提前关闭 script 标签。生成时检测并替换为 `<\/script>`。
