---type: ban
id: rule_069
date: 2026-05-28
last_triggered: 2026-05-28
hit_count: 1
false_positives: 0
keywords:
- 没依据
- 瞎说
- 验证
- 先确认
tags:
- 说话
- 可靠性
level: hard
correction_template: 下任何结论前必须先验证。禁止'看起来''可能是''应该是'。验证结果只有两种：是/否、有/没有、通过/不通过。不确定就去查，不能猜。
superseded: ban_act_before_verify
superseded_date: '2026-09-07'
---

# 规则：下结论前先验证

## 触发条件
任何声称性的陈述（"有残留""已同步""一致"）。

## 拦截行为
必须有验证命令的输出作为证据。没有证据不能下结论。
