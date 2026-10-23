---
type: ban
id: rule_ban_003_write_file_行号污染
date: 2026-05-23
hit_count: 1
severity: critical
keywords: [write_file 行号污染]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "execute_code 中 read_file 返回的内容含行号前缀，禁止直接传给 write_file。必须先 strip 行号前缀，或改用 terminal('cat') 获取原始内容。"
---

# write_file 行号污染

execute_code调用read_file获取带行号前缀的内容后,直接传给write_file写入文件,导致JSON损坏/YAML损坏/Markdown首行有N|前缀。重复3次以上。

触发 1 次 | 严重度: critical
