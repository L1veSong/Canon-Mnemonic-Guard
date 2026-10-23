---
type: ban
id: rule_067
date: 2026-05-28
last_triggered: 2026-09-17
hit_count: 1
hits_block: 1
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: [orchestrator, clarify, 直接输出, 闷头干, 跳过确认, 跳过检查]
tags: [偷懒, 交互缺失]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "orchestrator流程中每阶段必须用clarify()让用户确认，禁止跳过交互直接替用户产出最终结果。"
---

# 规则：Orchestrator流程不可跳过clarify

## 触发条件
执行任何orchestrator/工作流类skill时。

## 拦截行为
每个Phase完成后→必须clarify()→用户确认→才能进入下一Phase。
禁止直接输出最终产物说"写好了"。
