---
type: ban
id: rule_065
date: 2026-05-28
last_triggered: 2026-09-14
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['隐私没扫', '隐私扫描漏', '没扫就发外网', '直接发外网']
tags: [发布流程, 隐私]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "上传GitHub前必须扫一遍所有文件，确认无个人隐私（姓名/路径/API key/对话细节）。SKILL.md和references/下的坑点章节尤其需要检查——容易混入具体会话内容。"
---

# 规则：上传前隐私扫描

## 触发条件
打包完成、准备上传GitHub时。

## 拦截行为
1. 搜索所有文件中的个人信息（姓名/路径/API key/会话细节）
2. 重点检查 SKILL.md 的"坑点"章节和 references/ 目录
3. 确认干净后才能上传
4. 本地版本可保留个人配置（~/.hermes/ 下），桌面发布包必须干净


**豁免：** 用户明确要求省略该步骤、或声明成本/时间优先时，允许跳过，但须在回复中说明原因。
