---
type: ban
id: rule_ban_target_agent_automation
date: 2026-09-21
last_triggered: 2026-09-21
hit_count: 1
false_positives: 0
source_ids: []
keywords: ['过一遍Hermes', '经过Hermes', '人工中转', '靠人喊', '点名跑', 'Hermes 在链路里', '让Hermes代做', '人工对账']
tags: [design, automation, agent]
level: soft
correction_template: |
  新 agent 目标态设计铁律：**全自动、零人工/Hermes 中转**。
  任何"需要人喊一句/需要 Hermes 在场"的环节，只允许存在于施工期；
  写设计时必须同时给出其自动化替代；记忆＝自动写＋自动读＋对号，
  对号不确定 → 转人工（宁停不错）。
---
# 目标态不得依赖 Hermes 或人工中转

2026-09-21 用户纠正：客服agent 的记忆/回复/交易"都是新业务 agent 的活，全自动"；
把"用户点名 → Hermes 跑"设计进目标态 = 方向错误。

- 记忆卡/总表等文件 = 夹具与格式（施工期产物），不是产品本体
- 运行态链路：收信 → 对号 → 读记忆 → 回复 → 写记忆 → 交易，全程 agent 自动
- Hermes 角色 = 搭台、喂料、校准、盲测；不进入运行链路
