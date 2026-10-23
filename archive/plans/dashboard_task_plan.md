# CMG Dashboard — 独立项目规划

> 2026-06-14 | 状态: ✅ Phase 1-4 已完成 | 最新: v5.6.0 自适应版

## 交付物

`~/.hermes/dashboard/server.py`（Python HTTP 服务器，local-only，端口 8765）

## 当前功能（全部已实现）

### Phase 1: 规则可视化 ✅
- 规则总数 / 分类（ban/gap/lazy/meta）
- 命中率排行
- 误报率监控（>30% 标红）
- 最后命中时间（>180 天标灰）
- 搜索/筛选/排序/导出/批量删除

### Phase 2: 拦截统计 ✅
- 总拦截次数 / 近 30 天趋势图（Canvas 柱状图）
- 系统拦截数（intercept_log.jsonl）
- 错误记录数（errors.jsonl）

### Phase 3: 配置管理 ✅
- Hook 开关（17 hooks toggle）
- 拦截通知模式切换
- 任务推荐开关
- 配套 Skill 状态查看

### Phase 4: 健康面板 ✅
- 规则总数/命中/拦截/错误/高误报/长期未触发 六卡片
- 引擎版本信息（从 SKILL.md 自适应读取）
- 时区修复（naive→UTC）

## 2026-06-14 修复 (v5.6.0)

| # | Bug | 根因 | 修复 |
|---|-----|------|------|
| 1 | 配置读写用旧 key cmg_guard | 改名后未同步 | read/write_config → SENTINEL_KEY 自适应 |
| 2 | 版本号硬编码 v5.5.5 | HTML 模板字面量 | 从 SKILL.md 动态读取 CMG_VERSION |
| 3 | "近30天无拦截记录"始终显示 | intercept_log 时区不匹配 | naive→UTC + 数据驱动渲染 |
| 4 | 趋势图空白 | TypeError 被 except 吞掉 | 修复时区 + fallback ts 字段 |
| 5 | 趋势图模糊 | 未适配 Retina DPR | canvas × dpr + ctx.scale |
| 6 | 英文残留中文（导出/批量/主题） | 手动 i18n 三步走遗漏 | 全量 data-i18n + JS t() 替换 |
| 7 | 统计卡文字换行 | 未设 white-space | nowrap + text-overflow |

## 自适应改进

- 版本号：从 CMG SKILL.md frontmatter 读取，不再硬编码
- 配置 key：从 sentinel/plugin.yaml 自动检测
- i18n 审计：切英文后自动扫描，发现汉字→红框标记 `⚠ Untranslated`

## 技术选型（已确定）

纯 Python HTTP 服务器 + 内嵌 HTML/CSS/JS
- 数据源：本地文件系统（rules/、intercept_log.jsonl、errors.jsonl、state.json、config.yaml）
- 无外部依赖（仅标准库）
- 端口 8765，仅 localhost
