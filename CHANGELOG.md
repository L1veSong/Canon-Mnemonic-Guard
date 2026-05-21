# Changelog

All notable changes to Canon Mnemonic Guard (原 hermes-self-reflection).

---

## [5.2.1] — 2026-05-22

### SOUL 激活机制 + 推荐自动扫描

**新增**
- SOUL 激活标记: init 时选 Y → SOUL.md 末尾写入一行 `[CMG v5.2.1]`。Hermes 读到后自动加载护栏。删掉即停用，扫盘检测标记丢失时提醒恢复
- init.py: 一键初始化脚本 — 创建目录/配置/状态文件 → 自动扫描 9 项推荐列表 → 询问 SOUL 激活
- 推荐列表自动扫描: 扫盘时自动包含推荐检测。`!scan-recommendations` 手动触发。config.json 新增 `recommendations` 字段（9 项）
- plugins 扫描源: config.json 新增 `scan_sources.plugins`，支持扫描插件目录和 pip entry points
- 数据修复: mnemonic_state.json 创建，last_scan_at 设置，intercept_log timestamps 修复

**规格更新**
- Canon v2.5.1 → v2.5.2: +推荐扫描 + SOUL 激活检测
- Guard v4.5.0 → v4.5.1: +激活标记检测 + 文档化三种激活方式
- CMG v5.2.0 → v5.2.1: SOUL 激活 + init 脚本 + 推荐扫描

**配套**
- plur 安装：CMG 扫盘可读取 `~/.plur/` 记忆作为额外规则来源
- rtk-rewrite 完成配置：config.yaml 格式修正 + gateway 重启生效

---

## [5.2.0] — 2026-05-22

### 六大功能大更新

| 编号 | 内容 | 所属 |
|------|------|------|
| C1 | 定时扫盘 | Canon v2.5.0 |
| G2 | 动态清单真实数据 | Guard v4.5.0 |
| G3 | 上下文感知实现 | Guard v4.5.0 |
| G4 | 效能分析真实数据 | Guard v4.5.0 |
| M1 | 数据源降级链 | Mnemonic v3.3.0 |
| E2+E3 | !log 协调日志 + !diagnose 一键诊断 | Engine |

---

## [5.1.0] — 2026-05-22

### E4: 四包制分装

| 包 | 版本 | 说明 |
|----|------|------|
| `canon-mnemonic-guard` | v5.1.0 | 外观索引层 |
| `canon` | v2.4.1 | 典则线独立 Skill |
| `guard` | v4.4.0 | 护栏线独立 Skill |
| `mnemonic` | v3.2.0 | 忆存线独立 Skill |

---

## [5.0.2] — 2026-05-22

7项低风险优化全面落地: C2动态固化阈值 / C3导入导出 / C4跨类型冲突检测 / G5重名解决 / M2独立持久化 / M4误报率双向调节 / E1健康检查

---

## [5.0.0] — 2026-05-21

三线合一外观模式: 对外 role:guard，内部 Canon+Guard+Mnemonic 三模块独立。16条优化项入库。

---

## [2.x 系列] — 2026-05-19 ~ 2026-05-21

扫盘提取 → 依赖解耦 → 规则冲突裁决 → 角色声明制 → 规则评分 → Idea Foundry 联动。完整 Changelog 见 SKILL.md 版本变更章节。

---

## [1.0.0] — 2026-05-18

`hermes-self-reflection` 初始发布: 三类错误系统(ban/gap/lazy)、分层匹配、固化引擎、防偷懒清单、自保机制。
