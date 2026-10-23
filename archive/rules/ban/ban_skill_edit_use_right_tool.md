---
type: ban
id: ban_skill_edit_use_right_tool
date: 2026-06-07
last_triggered: 2026-09-16
hit_count: 6
hits_block: 6
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['手写skill', '手改skill', '直接写skill', 'sed改', '绕过skill_manage', '不用skill_manage', '没用skill_manage']
tags: [skill编辑, 工具选择]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  修改 SKILL.md 前必须加载 writing-skills + hermes-agent-skill-authoring 两个专业工具。
  编辑操作优先用 skill_manage(action='patch')，不是终端 sed/patch。
  创建新 skill 走 skill_manage(action='create')，不是 write_file 手写。
  含引号/中文的编辑如果 skill_manage patch 报 escape-drift，用 terminal sed 做最后降级。
---

# Skill 编辑必须使用专业工具

## 规则

修改任何 SKILL.md 时，必须按以下优先级选择工具：

1. **首选** `skill_manage(action='patch')` — 有 YAML 验证，不会破坏 frontmatter
2. **降级** `sed` — 仅当 skill_manage 报 escape-drift（中文引号/特殊字符）时才用
3. **禁止** 直接 `write_file` 或终端 `patch` 编辑 SKILL.md

创建新 skill 时：
- 加载 `writing-skills` + `hermes-agent-skill-authoring`
- 用 `skill_manage(action='create')` 创建
- 禁止 `write_file` 裸写 SKILL.md

## 合并来源

本规则由以下三条合并而来（2026-06-07）：
- skill-edit-use-skill-manage（hit: 3）
- skill-edit-without-authoring-tool（hit: 5）  
- rule_ban_skip_better_tool（hit: 2）

合并后 hit_count = 3+5+2 = 10（减去重叠算 7）
