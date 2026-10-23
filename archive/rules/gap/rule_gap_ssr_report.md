---
type: gap
id: rule_gap_ssr_report
date: 2026-07-25
last_triggered: null
hit_count: 0
false_positives: 0
source_ids: [manual]
keywords: ['SSR', 'report', '汇报', '推荐', '使用情况']
level: soft
correction_template: |
  当 ssr.report: true 时，每轮回复末尾必须汇报 SSR 使用情况。
  格式：`[SSR 使用] 推荐: X, Y | 已用: X | 跳过: Y(原因)`
  无推荐时：`[SSR 使用] 本轮无推荐`
tags: [ssr, reporting, transparency]
---

# SSR 使用汇报规则

## 触发条件

`config.yaml` 中 `ssr.report: true` 时生效。

## 行为

每次回复必须包含 SSR 使用汇报：

**有推荐时：**
```
[SSR 使用] 推荐: plan, skill-creator | 已用: plan | 跳过: skill-creator(小改动不需要)
```

**无推荐时：**
```
[SSR 使用] 本轮无推荐
```

## 格式要求

- 一行，放在回复末尾
- "已用"列出实际加载/使用的 skill
- "跳过"必须附带简短原因（如"不需要""已手动""图快"）
- 如果推荐了多个但都没用，全部列在跳过里
