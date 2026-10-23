---
type: gap
id: rule_gap_009_不跑checklist
date: 2026-05-23
hit_count: 1
severity: high
detector: toolseq
triggers: ["发布", "release", "打包上传"]
required_tools: ["skill_view::hermes-agent-skill-authoring"]
keywords: [不跑checklist]
level: soft
correction_template: "发布前必须跑完整的 Release Checklist，逐项通过。不可跳过任何检查项。任一项未通过即中止发布。"
---

# 不跑checklist

hermes-agent-skill-authoring的PRE-RELEASE GATE(grep版本号同步)被跳过。v9.0.0发布时SKILL.md/README中仍有v8.3.1旧版本号残留。

触发 1 次 | 严重度: high
