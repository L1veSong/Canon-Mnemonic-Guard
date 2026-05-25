# CMG 生态系统更新日志

## v5.5.2 (2026-05-26) — 稳定版

### canon-mnemonic-guard v5.5.2
- 默认固化阈值 10→3
- 修复 init.py 版本号滞后（v5.4.0 → v5.5.2）

### 子包
- canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3（同步补丁）

### 插件
- skill-autoload v1.0.0 / cmg-guard v1.0.0（无变更）

---

## v5.5.1 (2026-05-25) — 三层闭环首次发布

### 新增插件
- skill-autoload v1.0.0: pre_system_prompt 自动加载 CMG
- cmg-guard v1.0.0: transform_llm_output 硬拦截

### canon-mnemonic-guard v5.5.1
- README 更新为三层闭环说明
- 配套生态加入两个新插件

---

## v5.5.0 (2026-05-25) — 微型调度器
- 微型调度器：Guard 拦截自动匹配配套 skill
- P1-P4 全部完成

---

## v5.4.0 (2026-05-24) — 大更
- P1: 同会话升级 + P3: 用户纠正提升 + P4: 误报降级
- Mnemonic v3.5.0: 上下文保留

---

## v5.3.0 (2026-05-23) — 风险分级
- Guard 风险分级（不可逆操作暂停确认）

---

## v5.2.0 (2026-05-22) — 四包制
- 定时扫盘 + 协调日志 + 一键诊断
- !scan-recommendations

---

## v5.1.0 (2026-05-21) — 四包分装
- Canon / Guard / Mnemonic 物理拆分

---

## v5.0.0 (2026-05-20) — 三线合一
- 典则 + 护栏 + 忆存 → 三省引擎
