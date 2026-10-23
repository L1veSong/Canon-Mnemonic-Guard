---
type: ban
id: rule_ban_no_periodic_tasks
date: 2026-09-21
last_triggered: 2026-09-21
hit_count: 1
hits_block: 0
hits_record: 1
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: []
keywords: ['部署定时任务', '加个定时', '周期性任务', '周期任务', '每日自动任务', 'launchd StartInterval', '自动巡检部署', '设置 cron', '定时巡检']
tags: [infra, preference, scheduling]
level: soft
correction_template: |
  用户不要周期性定时任务（笔记本常离线，断网时报错）。
  凡"自动巡检/定期维护"需求 → 默认做成手动脚本或点名触发（用户说跑才跑）。
  不得擅自部署 cron / launchd 周期任务；已装的发现即报用户并清。
---
# 禁止部署周期性定时任务

2026-09-21：部署 hindsight-watch（120s launchd 巡检）后用户明确表示不喜欢定时任务——
笔记本经常没网/合盖，周期任务断网报错，噪音大于收益。

- 巡检、看门、维护类工具 → 手动脚本（放 ~/.hermes/scripts/）+ 点名触发
- 不新增 launchd StartInterval / cron / 每日任务
- 若某场景确实需要自动化，先问用户，默认答案为否
