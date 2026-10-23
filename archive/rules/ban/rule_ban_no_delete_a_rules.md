---
type: ban
id: rule_ban_no_del_a_rules
date: 2026-06-09
last_triggered: 2026-09-15
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: []
keywords: ['a_rules.json', '清空 a_rules', '删除 a_rules', '覆盖 a_rules', 'rm -rf a_rules', 'cp a_rules', 'write_file a_rules', 'restore a_rules', '恢复 a_rules', '恢复a_rules', 'restore golden', 'golden 丢失', '规则丢失']
tags: [ssr, data-loss]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  黄金基线文件（SSR 的 B 层规则积累）任何删除/清空/覆盖操作前：
  1. 先备份（同目录 .bak 副本）
  2. 确认真的需要删除（格式问题优先修复，不重建）
  3. 禁止无备份直接删改。
---

# 禁止删除/清空 A 层规则不备份

SSR 的 a_rules.json 包含 B 层升级积累的高质量规则。删除前必须：
1. `cp a_rules.json a_rules.json.bak.$(date +%Y%m%d)`
2. 确认需要删除（不是格式兼容问题可修复）
3. 优先修复格式而非清空重建

auto-gen 生成的粗糙关键词无法替代 B 层学习积累。
