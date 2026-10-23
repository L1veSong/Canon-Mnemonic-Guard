---type: ban
id: ban_no_cmg_abbreviation
date: 2026-05-30
last_triggered: 2026-05-30
hit_count: 1
false_positives: 1
source_ids: []
keywords:
- CMG Dashboard
- CMG v5.
- CMG 三省引擎
- CMG 配套
- CMG 合集
- CMG 生态系统
tags:
- 命名规范
- 对外发布
level: monitor
correction_template: '在所有对外文档、README、CHANGELOG、Dashboard、公告中使用完整名称。

  "CMG"仅限内部会话快速指代，不得出现在任何对外分发的文本中。

  替代：Canon-Mnemonic-Guard（英文）/ 三省引擎（中文）。

  '
superseded: rule_071_no_cmg_abbreviation
superseded_date: '2026-09-07'
---

# 禁止在对外文本中使用"CMG"缩写

## 规则
任何对外分发的文档、界面、公告中，禁止使用"CMG"作为项目简称。
必须使用完整名称 "Canon-Mnemonic-Guard"（英文语境）或 "三省引擎"（中文语境）。

## 触发场景
- 撰写 README.md / CHANGELOG.md
- 生成 Dashboard 等可视化界面
- 编写 GitHub 发布公告
- 任何用户以外的受众会看到的文本

## 例外
内部会话中快速指代可以使用"CMG"，因为是内部沟通。
