---
type: gap
id: rule_gap_ssr_no_limit
date: 2026-06-09
last_triggered: 2026-06-09
hit_count: 1
false_positives: 0
source_ids: []
keywords: [上限, 限制, 推荐数量, 无限, 不设限, 全推]
tags: [ssr, design]
level: hard
correction_template: |
  SSR 的职责是匹配，不是筛选：匹配多少推多少，让 AI 自行判断加载；
  不做数量截断。
---

# SSR 不应设置推荐数量上限

用户明确偏好"能用的都推，AI 自己判断"。SSR 的角色是匹配，不是筛选。匹配多少推多少，让 AI 根据上下文自主决定加载哪些 skill。

已连续纠正三次：1→3→8→10→无限。每次都在"放宽上限"而非"去除上限"。
