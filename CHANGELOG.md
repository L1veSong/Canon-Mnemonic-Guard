# CMG 三省引擎更新日志

## v5.5.4 (2026-05-28) — cmg-guard 系统级拦截

### 变更: cmg-guard v1.1.0 → v1.2.0
- **步骤完整性检查** (`pre_llm_call`)：4 条强制规则 — 链接完整阅读、文件覆盖度校验、Orchestrator clarify、Skill workflow 执行
- **分阶段升级系统**：同一错误逐步升级（sentinel → warn → draft → blacklist），不再一刀切
- **新增 `post_llm_call` 钩子**：AI 回复后二次黑名单扫描
- 哨兵正则优化：新增 "又偷懒""记住" 等匹配模式
- 升级状态持久化到 `escalation.json`

### 四包版本
- canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3（未变）
- 插件：skill-autoload v1.0.1 / cmg-guard v1.2.0

### 说明
核心四线本次未变。这是 cmg-guard 配套插件的独立升级，ES 小升版记录。

---

## v5.5.2 (2026-05-26) — 稳定版

### 变更
- 默认固化阈值 `auto_solidify_threshold`：10 → 3
  - 新用户 init 即生效。老用户在 config.json 手动改或重跑 init
- 修复 `init.py` 版本号滞后
  - 激活标记、初始化标题、提示文本三处硬编码 v5.4.0，跨 v5.5.0/v5.5.1 未更新

### 四包版本
- canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3

---

## v5.5.1 (2026-05-25) — 三层闭环

### 新增: cmg-guard Plugin v1.0.0
- `transform_llm_output` 硬拦截 AI 输出
- 命中 ban 规则关键词 → 直接替换，用户看不到违规内容
- 37 条 ban 规则自动读取

### 新增: skill-autoload Plugin v1.0.0
- `pre_system_prompt` 自动加载 CMG
- 支持 config.yaml 按平台配置

### 四包稳定
- canon v2.7.1 / guard v4.8.1 / mnemonic v3.5.2（无变更）

---

## v5.5.0 (2026-05-25) — 微型调度器

### 新增
- 微型调度器：Guard 拦截自动匹配配套 skill
- P1-P4 全部完成，17 项待优化全部清零

### 四包
- canon v2.7.0 / guard v4.8.0 / mnemonic v3.5.0

---

## v5.4.0 (2026-05-24) — 大更

### 新增
- P1: 同会话重复快速升级（2 次触发 → block，24h 半衰期）
- P3: 用户纠正自动提升规则级别（monitor → soft → hard）
- P4: 误报自动降级 + 规则有效期（`--expires 7d`）
- Mnemonic v3.5.0: 命中上下文保留（解决 unknown 规则无法还原）

### 四包
- canon v2.7.0 / guard v4.8.0 / mnemonic v3.5.0

---

## v5.3.0 (2026-05-23) — 风险分级

### 新增
- Guard v4.7.1: 风险分级 — 不可逆操作（删除/覆盖）暂停确认

### 修复
- 四包独立 CMG 生态合集首次完整发布

---

## v5.2.0 (2026-05-22) — 四包制

### 新增
- C1: 定时扫盘（7 天自动触发）
- E2: !log 协调日志（三线统一视图）
- E3: !diagnose 一键诊断（五阶段深度体检）
- !scan-recommendations 推荐列表自动扫描

### 四包
- canon v2.5.0 / guard v4.5.0 / mnemonic v3.3.0

---

## v5.1.0 (2026-05-21) — 四包分装

### 变更
- Canon / Guard / Mnemonic 物理拆分为独立 Skill 包
- CMG 外观层保留为索引入口

---

## v5.0.0 (2026-05-20) — 三线合一

### 里程碑
- 典则（规则生产）+ 护栏（拦截执行）+ 忆存（模式识别）统一为三省引擎
- 外观模式：对外 `role: guard`，内部三线子角色

---

## v2.x 典则线早期版本

| 版本 | 变更 |
|------|------|
| v2.4.0 | 规则效果评分 + 角色声明制 + !import/!export |
| v2.3.0 | 依赖解耦（RuleReader 接口 + 7 适配器）+ 可配置扫描源 |
| v2.2.9 | 首次真实扫盘提取 + 固化执行 |
| v2.2.0 | 扫盘提取 |
| v2.0.0 | Obsidian 结构化 rules/ 目录 |

---

## 子包独立变更

### Canon 典则线

| 版本 | 变更 |
|------|------|
| v2.7.2 | 默认固化阈值 10→3 |
| v2.7.1 | P2 草稿快速通道 |
| v2.7.0 | 误报自动降级 + 规则有效期 |
| v2.6.0 | 规则分级 hard/soft/monitor + 修正模板 |
| v2.5.0 | 定时扫盘 |

### Guard 护栏线

| 版本 | 变更 |
|------|------|
| v4.8.2 | 默认固化阈值 10→3 |
| v4.8.1 | P2 session_id 追踪 + Mnemonic 联动钩子 |
| v4.8.0 | 上下文升级增强 + 用户纠正自动提升 |
| v4.7.0 | 闭环重试引擎 |
| v4.6.0 | 典忆卫・闭环校验器 |

### Mnemonic 忆存线

| 版本 | 变更 |
|------|------|
| v3.5.3 | 默认固化阈值 10→3 |
| v3.5.2 | M3: !patterns + !datasource |
| v3.5.1 | P2 session 追踪 |
| v3.5.0 | 命中上下文保留 |
| v3.4.0 | 模式识别加速（同会话 2 次推草稿） |
