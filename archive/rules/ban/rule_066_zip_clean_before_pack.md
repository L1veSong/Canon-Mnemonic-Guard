---
type: ban
id: rule_066
date: 2026-05-28
last_triggered: 2026-05-28
hit_count: 1
false_positives: 0
keywords: ['DS_Store', '打包前清理']
tags: [发布流程, 打包]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "ZIP打包前必须清理.DS_Store等系统垃圾文件。打包后解压验证ZIP内无残留。"
---

# 规则：ZIP打包前清理系统垃圾文件

## 触发条件
zip命令前。

## 拦截行为
1. find删除所有.DS_Store
2. 打包后unzip -l检查无残留
3. 确认干净
