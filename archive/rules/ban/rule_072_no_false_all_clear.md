---
type: ban
id: rule_072
date: 2026-05-28
last_triggered: 2026-09-21
hit_count: 5
hits_block: 5
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ["全部通过", "夸大", "测试不全", "如实报告"]
tags: ["测试", "说话", "诚实"]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  测试结果必须如实报告数字。N/M 通过 ≠ "全部通过"。有数据不足项 → 标注"待验证"。禁止使用"全部""完美""没问题"等概括词。
---

# 测试不全禁止说「全部通过」

**触发条件**: 声称"全部通过""完美""没问题"但实际有未测试项。

**拦截行为**: 必须逐项报告：✅ X/M 通过 + ⚠️ Y 项数据不足 + ❌ Z 项失败。
