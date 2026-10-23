---
type: ban
id: rule_006
date: 2026-05-21
last_triggered: 2026-05-21
hit_count: 0
false_positives: 0
source_ids: [disk_scan]
source: Obsidian铁则库
keywords: ["女娲", "huashu"]
tags: ["安全", "skill"]
level: soft
correction_template: "女娲生成的 Skill 必须先审查内容再启用。不可跳过审查直接激活，涉及资金/仓位的规则必须等用户确认。"
---

# 女娲生成Skill先审查

**规则描述**: 用户使用女娲生成新Skill后必须提醒先审查再启用，不可直接用于生产环境

**匹配关键词**: 女娲, huashu, 审查, 启用

**触发场景**: 检测到 女娲, huashu, 审查 等相关行为时触发

**拦截行为**: 立即拦截并说明原因

**来源记录**: 扫盘提取于 2026-05-21，源: Obsidian铁则库
