# Changelog

All notable changes to Canon Mnemonic Guard (原 hermes-self-reflection).

---

## [5.5.0] — 2026-05-25

### 微型调度器

- **场景→配套自动映射**：Guard 拦截时自动匹配推荐 skill，提示加载
- 映射表：过设计→karpathy / 跳步骤→ralph-loop / 声称完成→VBC / 连续命中→diagnose
- 轻量版中控调度，完整的中央调度器在 roadmap 中作为独立项目

### 子包版本

- Canon / Guard / Mnemonic 不变

---

## [5.4.2] — 2026-05-25

### 补丁：M3 清零

- **!patterns**：查看 Mnemonic 识别的重复违规模式（本会话命中/7天命中/推荐操作）
- **!datasource**：查看当前数据源状态和切换历史
- 待优化表 17 项全部清零，CMG 功能闭环

### 子包版本

- Mnemonic v3.5.1 → v3.5.2
- Canon / Guard 不变

---

## [5.4.1] — 2026-05-25

### 补丁：P2 补全

- **P2 Mnemonic 加速模式识别**：Guard 拦截日志新增 session_id + Mnemonic联动钩子
- Guard→Mnemonic：同会话第2次命中自动通知推草稿
- Mnemonic session_tracking：mnemonic_state.json 新增同会话推送去重
- Canon 草稿快速通道：加速接收 Mnemonic 推送

### 子包版本

- Canon v2.7.0 → v2.7.1
- Guard v4.8.0 → v4.8.1
- Mnemonic v3.5.0 → v3.5.1

---

## [5.4.0] — 2026-05-25

### 大更：四大增强

- **P1 同会话重复快速升级**：Guard 上下文升级阈值从3次降为2次，新增半衰期衰减(24h计数减半)
- **P3 用户纠正自动提升**：用户纠正规则后自动提升拦截级别(monitor→soft→hard)
- **P4 误报自动降级 + 规则有效期**：连续否决≥3次自动降级，`!remember --expires 7d` 临时规则
- **Mnemonic 上下文保留**：每次命中记录触发场景，解决unknown规则无法还原的问题

### 子包版本

- Canon v2.6.0 → v2.7.0
- Guard v4.7.1 → v4.8.0
- Mnemonic v3.4.0 → v3.5.0

---

- 同步 Guard v4.7.1 风险分级：hard 规则按操作类型自动分流
- 不可逆操作（删除/覆盖/清空/改铁则库）→ clarify 暂停确认
- 可自动修复（坐标/格式/行号/版本号）→ RetryLoop 自动重试

---

## [5.3.0] — 2026-05-22

### 典忆卫・闭环校验器

Guard v4.6.0 新增原生监工机制——StepCompleteness 拦截后不再只 block，剩余步骤 ≥ 2 时自动进入逐步骤催办模式，直到全部闭环。

- **零外部依赖** — 不依赖 ralph-loop、不写文件、不委派子 Agent
- **典忆卫原生设计** — 用自己的规则体系、对话上下文、拦截器框架实现
- **逐步骤验证** — 每步执行后必须附验证证据才放行

### 版本

| 包 | 版本 | 变更 |
|----|------|------|
| canon-mnemonic-guard | v5.3.0 | 闭环校验器外观索引 |
| guard | v4.6.0 | +典忆卫・闭环校验器 |
| canon | v2.5.2 | 无变更 |
| mnemonic | v3.3.0 | 无变更 |

---

## [5.2.1] — 2026-05-22

SOUL 激活机制 + init.py + 推荐列表扫描 + 5 项联动全部验证通过。

---

## [5.2.0] — 2026-05-22

六大功能大更新: C1定时扫盘 + G2/G3/G4 + M1数据源降级 + E2/E3运维。

---

## [5.1.0] — 2026-05-22

四包制分装: canon/guard/mnemonic 独立 Skill 包 + CMG 外观索引。

---

## [5.0.x] — 2026-05-21~22

三线合一外观模式 + 7 项低风险优化 + 四包制。

---

## [2.x] — 2026-05-19~21

扫盘提取 → 依赖解耦 → 规则冲突裁决 → 角色声明制 → 规则评分。

---

## [1.0.0] — 2026-05-18

hermes-self-reflection 初始发布: 三类错误系统、分层匹配、固化引擎。

## v5.3.1 — 补丁更新 (2026-05-23)

### 子包版本
| canon | guard | mnemonic |
|:---:|:---:|:---:|
| v2.6.0 | v4.6.0 | v3.4.0 |

### 变更
- Canon v2.6.0: 规则分级 hard/soft/monitor + 修正模板 correction_template（纯规则层，立即可用）
- Mnemonic v3.4.0: 模式识别加速（同会话2次推草稿，原7天3次）
- Guard v4.6.0: 不变

### 已知限制
- Guard v4.7.0 (RetryLoop 闭环重试引擎) 未包含——需要 Hermes 核心 agent loop 改造
- 详见 references/v5.4.0-roadmap.md
