---type: ban
id: ban_skill_edit_must_load_writing_skills
date: 2026-05-25
last_triggered: 2026-05-25
hit_count: 3
false_positives: 0
source_ids:
- err_cmg_v520_pitfall18
- err_cmg_v520_pitfall18_repeat
- err_cmg_v540_hand_patch
keywords:
- patch SKILL.md
- write_file SKILL.md
- 修改skill
- 改skill
- 更新skill
- 迭代skill
- 手改
- 手工patch
- 不用skill_manage
- 跳过writing-skills
tags:
- skill编辑
- 流程规范
- 硬锁
level: hard
correction_template: 修改任何 SKILL.md 前必须先加载 writing-skills（skill_view name='software-development/writing-skills'）和
  hermes-agent-skill-authoring。使用 skill_manage(action='patch') 操作 SKILL.md 文件，禁止使用
  terminal patch/sed/execute_code 手工修改。加载完成后立即输出 'writing-skills 已加载，进入 TDD 流程' 以证明已加载。
level_history:
- from: soft
  to: hard
  reason: 第三次违规——v5.2.0两次+v5.4.0一次，累计3次自动升级为hard
  date: '2026-05-25'
superseded: ban_skill_edit_use_right_tool
superseded_date: '2026-09-07'
---

# 修改 SKILL.md 前必须加载专业工具

## 触发场景

Agent 准备修改任何 `SKILL.md` 文件时（包括 patch、write_file、skill_manage、execute_code 写入）。

## 规则

**修改 SKILL.md 前必须先加载 `writing-skills` + `hermes-agent-skill-authoring`。** 使用 `skill_manage` 操作 SKILL.md。禁止手工 patch/sed/execute_code 直接修改。

## 违规记录

| 日期 | 事件 |
|------|------|
| 2026-05-22 | CMG v5.2.0 四包同步升版，全手写 patch+skill_manage edit，未加载 authoring skill（pitfall 18 第一次） |
| 2026-05-22 | CMG v5.2.0→v5.2.1，同一模式重演（pitfall 18 第二次） |
| 2026-05-25 | CMG v5.4.0 大更，四包全手工 patch，跳过 writing-skills TDD 流程。基线 20/20 通过但流程违规 |

## 拦截行为

检测到 Agent 准备执行 patch/write_file/skill_manage 操作 → 检查 writing-skills + hermes-agent-skill-authoring 是否已在本会话加载 → 未加载 → 硬阻断，要求先加载工具再操作。

## 纠正级别

累计 3 次违规 → 自动从 soft 升级为 hard。不可跳过、不可豁免。
