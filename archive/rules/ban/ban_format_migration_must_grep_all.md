---
type: ban
id: ban_format_migration_must_grep_all
date: 2026-06-22
last_triggered: 2026-09-22
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: [err_v3_migration_incomplete]
keywords: ['格式迁移', '格式变更', '字段名', '命名规范', '只改主流程', '全量grep', '维护函数']
tags: [code-quality, migration, audit]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  任何涉及格式/字段/命名变更的改动，完成后必须:
  1. grep -rn '旧字段名\|旧格式' 扫描全部相关文件
  2. 列出所有命中位置
  3. 逐项确认已更新或标注为「故意保留（后向兼容）」
  4. 禁止只改主流程，必须有审计报告
  反例: v2(skills)→v3(keywords)只改了_match_a_layer_keyword和_pre_llm_call，
  漏了_promote_to_a、_hot_remove_skill、_cleanup_a_rules、_auto_gen_a_rules四处。
---

# 格式迁移必须全量 grep 审计

**触发条件:** 任何涉及字段名、数据格式、命名规范的变更。

**禁止行为:**
- 只改主流程函数，漏掉维护函数
- 改完说「改好了」未提供 grep 审计结果
- 凭记忆判断「应该都改了」

**正确流程:**
1. 确定旧格式/旧字段名
2. `grep -rn '旧格式'` 全量扫描
3. 逐项确认：已更新 / 故意保留 / 不相关
4. 输出审计报告再收工

**实战案例 (2026-06-22):**
v2 `skills` → v3 `keywords` 迁移时，主流程 `_match_a_layer_keyword`、`_pre_llm_call` 正确更新，
但维护函数 `_promote_to_a`、`_hot_remove_skill`、`_cleanup_a_rules`、`_auto_gen_a_rules` 
四处仍用 v2 格式，导致 B→A 自学习报废、热删除漏清理、死规则检测失效。
用户在反复追问「有没有 bug」后才发现——如果迁移时做了全量 grep，一轮就能发现。
