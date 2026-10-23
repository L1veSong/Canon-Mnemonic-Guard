---
type: gap
id: rule_gap_007_不用专业skill写skill
date: 2026-05-23
hit_count: 1
severity: high
detector: toolseq
triggers: ["写skill", "写SKILL.md", "创建skill", "开发skill"]
required_tools: ["skill_manage"]
keywords: [不用专业skill写skill]
level: hard
correction_template: "创建或迭代 Skill 前必须先加载 writing-skills 和 hermes-agent-skill-authoring。禁止不加载专业工具就直接手写 skill。"
---

# 不用专业skill写skill

整个v1→v9开发过程中从未加载writing-skills(TDD流程/CSO规范)或hermes-agent-skill-authoring(发布checklist/版本号grep验证)。全程手写patch+edit。

触发 1 次 | 严重度: high
