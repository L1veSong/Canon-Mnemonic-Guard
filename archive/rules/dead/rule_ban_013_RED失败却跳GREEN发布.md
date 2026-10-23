---type: ban
id: rule_ban_013_RED失败却跳GREEN发布
date: 2026-05-23
hit_count: 1
severity: critical
keywords:
- RED失败却跳GREEN发布
level: hard
correction_template: TDD 基线测试 RED 阶段失败时绝不可跳到 GREEN 发布。必须修复所有失败项，重新跑测试全部通过后才能发布。如实报告
  N/总数 通过。
superseded: rule_073_test_before_publish
superseded_date: '2026-09-07'
---

# RED失败却跳GREEN发布

v9.0.0发布前基线测试3项失败(功能缺失+CHANGELOG污染+README缺deprecated)，未修复即重写README+打包ZIP，三次声称'可以发布'后才补测。CMG ban规则'发布前不做全量审计'已存在但未触发拦截检查。

触发 1 次 | 严重度: critical
