---
type: ban
id: rule_doc_patch_no_append
date: 2026-05-25
last_triggered: 2026-05-25
hit_count: 1
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "修改 SKILL.md 的某个段落时，必须整段替换（old_string 包含完整旧段落），不可在旧内容旁追加新段落。修改后用 grep 检查无重复段落。"
keywords: [增量patch, 文档重复, 追加不删]
tags: [doc-maintenance, skill-authoring]
---

# 禁止：文档增量 patch 不删旧内容

## 触发场景

修改 SKILL.md 中已有段落（如推荐列表、命令表、版本表）时。

## 规则

**修改已有段落 → 整段替换，不追加。** old_string 必须包含完整的旧段落（从标题到末尾），new_string 替换为新版本。不允许在旧段落旁边插入新段落导致两份共存。

## 违规记录

| 日期 | 事件 |
|------|------|
| 2026-05-25 | CMG 推荐列表被增量 patch 四次，三套重复表共存（三线归属/配套列表/建议配套） |

## 拦截行为

检测到同一 SKILL.md 中存在两个高度相似的推荐列表/命令表/版本表 → 拦截，要求去重后重新提交。
