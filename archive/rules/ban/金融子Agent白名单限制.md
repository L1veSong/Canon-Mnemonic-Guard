---
type: ban
id: rule_005
date: 2026-05-21
last_triggered: 2026-09-14
hit_count: 3
hits_block: 3
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: [disk_scan]
source: Memory
keywords: ['金融白名单', '任务白名单', '帮我炒股', '替我炒股', 'cron job', '金融子agent']
tags: ["金融", "安全"]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "金融子 Agent 只能调用白名单内的技能（finance-news-analyzer、technical-analysis、stock-screen-monitor、tushare-finance）。禁止调用白名单外的任何技能进行金融分析。"
---

# 金融子Agent白名单限制

**规则描述**: 金融子Agent仅允许6个白名单Skill。禁止调用白名单外任何Skill。

**匹配关键词**: 金融, 白名单, 炒股, cron job

**触发场景**: 检测到 金融, 白名单, 炒股 等相关行为时触发

**拦截行为**: 立即拦截并说明原因

**来源记录**: 扫盘提取于 2026-05-21，源: Memory
