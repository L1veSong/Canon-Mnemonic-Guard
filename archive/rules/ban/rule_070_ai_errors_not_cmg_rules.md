---
type: ban
id: rule_070
date: 2026-05-28
last_triggered: 2026-09-21
hit_count: 7
hits_block: 7
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['AI执行错误', '固化成规则', '固化到规则库', '固化进规则库', '写进规则', '写入规则', '记进规则库', '写进规则库', '加进规则库', '写进cmg规则', '记进cmg规则']
tags: [越权, CMG]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "AI自身的执行错误≠CMG ban规则。AI的错记errors.jsonl，用户纠正的行为才进rules/ban/。禁止把'我今天偷懒了'写成CMG规则。"
---

# 规则：AI执行错误不进CMG规则库

## 触发条件
想把AI自身执行失败写成CMG ban规则时。

## 拦截行为
区分两类：
- 用户纠正的行为 → rules/ban/
- AI自己执行偷懒 → errors.jsonl，不污染规则库
