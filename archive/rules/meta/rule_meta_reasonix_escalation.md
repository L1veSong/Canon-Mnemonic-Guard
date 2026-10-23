---
type: meta
id: rule_meta_reasonix_escalation
date: 2026-06-14
last_triggered: 2026-06-14
hit_count: 1
false_positives: 0
detector: inject
triggers: ["委派", "Reasonix"]
source_ids: [err_reasonix_waste_on_mechanical]
keywords: [Reasonix, ACP, delegate_task, 委派, 委Reasonix, 编程委]
tags: [meta, tool-selection, delegation]
level: hard
correction_template: |
  编程改动分级：
  - 逻辑变更/新函数/新功能/多文件协调/复杂调试 → 委 Reasonix(acp)
  - 机械替换（字符串替换/版本号同步/单行改/find-and-replace）→ 直接 patch
  判断标准：改动是否涉及推理决策？是→Reasonix，否→直接上。
  Reasonix ACP 慢 3-5x（166s vs 20-40s），机械活不换精度只换延迟。
---

# Reasonix 委派分级规则

## 规则

编程改动必须按复杂度分级选择工具，不可一刀切。

## 分级标准

| 场景 | 工具 | 理由 |
|------|------|------|
| 逻辑变更（新函数、条件分支、算法） | Reasonix(acp) | 需推理深度 |
| 新功能/新模块 | Reasonix(acp) | 需设计决策 |
| 多文件协调改动 | Reasonix(acp) | 需全局一致性 |
| 复杂调试（根因未知） | Reasonix(acp) | 需系统性排查 |
| 字符串替换（find-and-replace） | 直接 patch | 零推理 |
| 版本号同步 | 直接 patch | 零推理 |
| 单行修（改一个字/一个字符） | 直接 patch | 零推理 |
| YAML/JSON 字段值修改 | 直接 patch | 零推理 |

## 判断标准

**改动的核心是"替换"还是"设计"？**

- 替换已知字符串 → 直接上
- 需要判断"怎么写才对" → Reasonix

## 证据

2026-06-14 实测：SSR echo bug 修复（3 个 `\\n`→`\n` + 版本号字符串替换），委 Reasonix 耗时 166s，产出与直接 patch 完全相同。Reasonix 不换工具链，优势在推理深度——机械替换没有推理需求，多等 3 分钟零收益。
