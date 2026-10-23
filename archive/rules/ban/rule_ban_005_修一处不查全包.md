---
type: ban
id: rule_ban_005_修一处不查全包
date: 2026-05-23
hit_count: 1
severity: critical
keywords: [修一处不查全包]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "修改任何单个文件后，必须逐文件验证整个包：所有 MD 首行干净、所有 JSON 可解析、所有文件版本号一致。不可只检查修改的那一个文件。"
---

# 修一处不查全包

修复README的markdown格式后JSON配置文件被清空(0字节)或版本不一致。修复SKILL.md后桌面package.json/global-priority.json损坏。

触发 1 次 | 严重度: critical
