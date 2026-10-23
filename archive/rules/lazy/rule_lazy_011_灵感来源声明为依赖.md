---
type: lazy
id: rule_lazy_011_灵感来源声明为依赖
date: 2026-05-23
hit_count: 1
severity: medium
detector: inject
triggers: ["灵感", "借鉴", "参考了"]
keywords: [灵感来源声明为依赖]
level: soft
correction_template: "借鉴设计思想 ≠ 声明为技术依赖。能独立运行就不是依赖。灵感在 spec 注明即可，实现必须内置、零外部依赖。"
---

# 灵感来源声明为依赖

设计时将参考过的Skill写入架构依赖链,用户指出'这不就锁死绑定了吗?又不是我独有的,使用率大大降低,还有侵权风险'。借鉴≠依赖。

触发 1 次 | 严重度: medium
