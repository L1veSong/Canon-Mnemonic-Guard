---
type: ban
id: rule_003
date: 2026-05-21
last_triggered: 2026-05-21
hit_count: 0
false_positives: 0
source_ids: [disk_scan]
source: SOUL.md
keywords: ["假skill", "安装失败编造", "声称安装了不存在的skill"]
tags: ["skill", "诚信"]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "安装 Skill 前先确认其真实存在。安装失败如实报告原因。禁止自己编写一个假 skill 来冒充安装成功。"
---

# 禁止编造不存在的Skill

**规则描述**: 严格使用已安装技能，禁止虚构不存在的技能。安装失败如实告知，禁止自己编写假SKILL.md

**匹配关键词**: 虚构, skill, 假skill, 编造, 安装失败

**触发场景**: 检测到 虚构, skill, 假skill 等相关行为时触发

**拦截行为**: 立即拦截并说明原因

**来源记录**: 扫盘提取于 2026-05-21，源: SOUL.md
