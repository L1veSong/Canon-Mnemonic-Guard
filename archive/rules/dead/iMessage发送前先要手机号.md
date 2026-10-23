---
type: gap
id: rule_011
date: 2026-05-21
last_triggered: 2026-05-21
hit_count: 0
false_positives: 0
source_ids: [disk_scan]
source: Obsidian铁则库
keywords: ["iMessage", "手机号", "联系人", "发送"]
tags: ["消息", "iMessage"]
level: soft
correction_template: "发送 iMessage 前必须先获取收件人手机号。不可假设或猜测号码。没有号码就先询问用户。"
---

# iMessage发送前先要手机号

**规则描述**: 用户只说联系人姓名时必须先提醒提供手机号，绝不要直接用姓名尝试发送

**匹配关键词**: iMessage, 手机号, 联系人, 发送

**触发场景**: 检测到 iMessage, 手机号, 联系人 等相关行为时触发

**拦截行为**: 自动补齐缺失项

**来源记录**: 扫盘提取于 2026-05-21，源: Obsidian铁则库
