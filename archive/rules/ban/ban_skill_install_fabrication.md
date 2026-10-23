---
type: ban
id: ban_skill_install_fabrication
date: 2026-05-23
last_triggered: 2026-09-19
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: [安装skill, 我瞎编, 官方仓库, 复制原文, 没查源码, 没看官方仓库]
tags: [skill安装]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "安装 Skill 必须从官方源（GitHub/ClawHub/npm）获取。禁止编造不存在的 skill。安装失败如实报告错误，不自己写假的替代。"
---

# 安装 Skill 必须从官方源，禁止瞎编

**规则：** 安装任何 Skill/插件/工具时，必须搜索官方 GitHub 仓库或 ClawHub 等权威源确认，不得凭记忆或猜测包名。

**禁止：**
- 不搜索直接 pip install <猜测的包名>
- 存在多个同名 Skill 时随便选一个装
- 搜索失败后自己编一个 SKILL.md

**正确流程：**
1. web_search 搜索官方仓库
2. 确认正确的安装命令/包名
3. 存在重名 → 告知用户选择
4. 找不到 → 如实告知用户
5. 找到源码 → clone仓库 → 复制SKILL.md → 只加Hermes metadata（version/author/license/metadata.hermes）→ 不改原skill内容

**禁止（2026-06-07新增）：**
- 即使找到了GitHub源码，也不自己手写SKILL.md——必须从源码仓库直接复制原文
- 手写=凭空编造格式/丢原作者署名/无法溯源
- 正确做法：`git clone → cp SKILL.md ~/.hermes/skills/ → skill_manage patch 加 metadata`
