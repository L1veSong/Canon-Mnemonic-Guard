---type: ban
id: rule_no_version_skip_in_series
date: 2026-05-24
last_triggered: 2026-05-24
hit_count: 1
false_positives: 0
source_ids:
- err_version_skip_001
keywords:
- 跳号
- 版本号
- 小系列
- Canon 2.x
- Mnemonic 3.x
- Guard 4.x
- 不够用
- 浪费
tags:
- release
- versioning
level: hard
correction_template: 小系列版本号不可跳号（Canon 2.x、Mnemonic 3.x、Guard 4.x）。每个功能变更必须按顺序发布，不可跳过中间版本。如果上一个发布版本是
  2.5.2，下一个必须是 2.5.3 或 2.6.0，不能直接跳到 2.7.0。
superseded: rule_064_release_version_grep
superseded_date: '2026-09-07'
---

# 禁止：小系列版本号跳号

## 触发场景

Skill 升级版本号时。

## 规则

**Canon(2.x)、Mnemonic(3.x)、Guard(4.x) 各自锁死在独立小系列内。版本号必须连续，不可跳号。因为小版本空间有限（2.6→2.99 约40个），跳号会加速耗尽。**

## 正确做法

```
Canon 上一个发布版本 = 2.5.2
下一个可以是: 2.5.3（补丁）或 2.6.0（小版本）
下一个不能是: 2.7.0（跳了 2.6.x 系列）

Mnemonic 上一个 = 3.3.0
下一个: 3.3.1 或 3.4.0
下一个不能是: 3.5.0
```

## 违规记录

| 日期 | 事件 |
|------|------|
| 2026-05-24 | Canon 从 2.4.1 到 2.6.0，中间 v2.5.0-2.5.2 虽然实际存在过但 CHANGELOG 缺失，造成跳号的假象 |

## 拦截行为

检测到新版本号与 CHANGELOG 最后版本号之间间隔 > 1 个小版本 → 拦截，要求要么补全历史版本 CHANGELOG，要么降回连续版本号。
