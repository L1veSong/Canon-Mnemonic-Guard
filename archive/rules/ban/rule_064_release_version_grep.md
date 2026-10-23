---
type: ban
id: rule_064
date: 2026-05-28
last_triggered: 2026-09-14
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['changelog没更新', 'changelog未更新', '没做全量检查', '没全量检查', '跳过全量检查', '跳号', '小系列', 'canon 2.x', 'mnemonic 3.x', 'guard 4.x', '版本号残留', '版本号漏改', '版本没同步']
tags: [发布流程, 版本号]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "发布前必须全量grep版本号（所有.md/.py/.yaml文件），禁止只看SKILL.md就声称'改完了'。确认零残留后才能打包。"
---

# 规则：发布前全量版本号检查

## 触发条件
声称"发布完成""打包完成"或类似表述前。

## 拦截行为
1. grep -rn 搜索所有文件中当前版本号的旧号
2. 确认零残留
3. 确认 init.py 等 scripts/ 下的硬编码版本号已同步
4. 输出 N/N 已同步确认
