---
type: gap
id: rule_gap_008_不走TDD
date: 2026-05-23
hit_count: 1
severity: high
detector: toolseq
triggers: ["TDD", "测试驱动", "写测试"]
required_tools: ["skill_view::test-driven-development", "skill_view::tdd"]
keywords: [不走TDD]
level: soft
correction_template: "开发新功能时遵循 TDD 流程：先写测试（RED）→ 写代码通过（GREEN）→ 重构。不可跳过测试直接写实现。"
---

# 不走TDD

多次skill迭代未跑基线测试未验证修改效果。writing-skills铁律'NO SKILL WITHOUT A FAILING TEST FIRST'被跳过。

触发 1 次 | 严重度: high
