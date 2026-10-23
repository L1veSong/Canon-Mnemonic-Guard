---type: ban
id: rule_ban_006_发布前不做全量审计
date: 2026-05-23
hit_count: 1
severity: critical
keywords:
- 发布前不做全量审计
level: hard
correction_template: 声称发布前必须跑全量审计脚本：版本号一致性、JSON 合法性、Markdown 首行干净、ZIP 吻合桌面包、所有文件存在。任一项未通过即中止发布。
superseded: rule_073_test_before_publish
superseded_date: '2026-09-07'
---

# 发布前不做全量审计

三次声称'可以发布'每次都有遗漏: ZIP版本不对、Markdown有行号污染、JSON损坏、版本号不一致。第4次才通过。

触发 1 次 | 严重度: critical
