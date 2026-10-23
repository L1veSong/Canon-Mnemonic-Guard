---
type: ban
id: ban_no_disable_without_confirm
date: 2026-06-05
last_triggered: 2026-09-16
hit_count: 1
hits_block: 1
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: [err_20260605235500]
keywords: ['一刀切', 'hermes config set', 'task_recommendations', '擅自关闭', '没分析影响']
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
tags: [配置变更, 安全操作, 影响分析]
correction_template: |
  任何关闭/禁用现有功能前：
  1. 分析该功能的所有使用者
  2. 评估关闭后的影响范围
  3. clarify() 向用户确认
  4. 用户确认后才执行
---

# 禁止未经确认关闭已有功能

**2026-06-05 触发案例：** SSR 测试时，AI 认为"CMG task_recommendations 和 SSR 冲突"，直接 `hermes config set sentinel.task_recommendations false`。用户立即纠正：CMG 的推荐和 SSR 是不同维度的（质量护栏 vs 功能匹配），互补不冲突。

**根因：** 看到"两个东西在做类似的事"→ 未经分析就关闭其中一个。没有检查 CMG 推荐的技能（ralph-loop/VBC/diagnose）是否被 SSR 覆盖——它们没有被覆盖。

**正确做法：**
1. 任何关闭/禁用操作前 → 列出该功能的所有使用者
2. 评估关闭影响 → 哪些能力会丢失
3. clarify() 向用户确认 → 用户有最终决定权
4. 确认后才执行 → 不等用户主动纠正
