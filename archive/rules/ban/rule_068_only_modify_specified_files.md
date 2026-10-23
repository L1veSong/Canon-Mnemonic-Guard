---
type: ban
id: rule_068
date: 2026-05-28
last_triggered: 2026-09-19
hit_count: 1
hits_block: 1
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['改多了', '越权修改', '越权改动', '越权操作', '不该改']
tags: [发布流程, 越权]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "用户说'只改X'→只能改X相关的文件。禁止顺手'优化'其他文件。发布包里的变更必须和用户确认过的完全一致。"
---

# 规则：只改用户指定的文件

## 触发条件
用户明确说"只改某文件/某组件"时。

## 拦截行为
变更清单必须和用户指令一致。多改一个文件就是越权。


**豁免：** 用户明确要求省略该步骤、或声明成本/时间优先时，允许跳过，但须在回复中说明原因。
