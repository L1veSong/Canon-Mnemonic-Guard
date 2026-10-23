---type: ban
id: rule_changelog_history_no_gaps
date: 2026-05-24
last_triggered: 2026-05-24
hit_count: 1
false_positives: 0
source_ids:
- err_changelog_gap_001
keywords:
- CHANGELOG
- 跳号
- 缺失
- 历史
- 版本
- 完整
- 全部
- 发布
tags:
- release
- changelog
- versioning
level: hard
correction_template: 发布前必须检查 CHANGELOG 版本历史是否完整——从第一个发布版本到当前版本，中间不许跳号。如有缺失，从 SKILL.md
  版本变更表中提取遗漏版本功能描述，逐条补全后再发布。
superseded: rule_064_release_version_grep
superseded_date: '2026-09-07'
---

# 禁止：CHANGELOG 版本历史跳号

## 触发场景

Skill 发布前的 "全部" 检查。

## 规则

**发布前检查"全部" = SKILL.md(版本号+激活消息) + README.md(标题) + CHANGELOG.md(完整历史无跳号)。**

CHANGELOG 历史必须从第一个发布版本到当前版本连续无间隙。如有缺失，从 SKILL.md 版本变更表中提取遗漏版本的功能描述，逐条补全。

## 检查方法

```bash
# 1. 查 SKILL.md 变更表中有哪些版本
grep "| v" SKILL.md

# 2. 查 CHANGELOG 中有哪些版本
grep "^##" CHANGELOG.md

# 3. 对比——SKILL.md 有而 CHANGELOG 无的 = 缺失
```

## 违规记录

| 日期 | 缺失 |
|------|------|
| 2026-05-24 | Canon v2.5.0/2.5.1/2.5.2、Mnemonic v3.1.0/3.2.0/3.3.0 |

## 拦截行为

检测到发布声明但 CHANGELOG 版本历史不连续 → 拦截，要求补全。
