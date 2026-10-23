---
type: ban
id: rule_071
date: 2026-05-28
last_triggered: 2026-09-18
hit_count: 5
hits_block: 5
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['CMG Dashboard', 'CMG v5.', 'CMG简写', 'CMG缩写', 'CMG简称', 'CMG配套']
tags: ["输出", "命名", "格式"]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  任何对外输出（诊断报告、协调日志、激活消息、README、CHANGELOG、错误提示等）禁止使用 CMG 简写，必须用全名「三省引擎」。CMG 是内部代号，对外人毫无意义。
---

# 规则：对外输出禁止 CMG 简写

**触发条件**: 任何 AI 回复中包含 "CMG" 字样（不包括 SKILL.md 内部文档、代码注释、变量名）。

**拦截行为**: 替换为「三省引擎」。

**例外**: 技术文档中的代码/路径/frontmatter（如 `sentinel`、`canon-mnemonic-guard`）不受此限制——这些是文件名/插件名。
