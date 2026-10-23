---
type: gap
id: rule_gap_read_before_write
date: 2026-06-08
hit_count: 0
keywords: [write_file, 追加, 末尾, 覆盖, 截断, 写入, 写文件, 更新文件]
level: hard
correction_template: |
  检测到准备调用 write_file 写入已有文件。
  write_file = 全量覆盖，不是追加（append）。
  必须先 read_file 读取该文件的当前完整内容，确认内容完整后再拼接写入。
  如果只是追加内容到文末 → 使用 patch（追加模式），不用 write_file。
  本规则是 rule_ban_003（行号污染）的上位规则：rule_ban_003 覆盖 execute_code 内 write_file，
  本规则覆盖所有场景下的 write_file 操作。
source: 2026-06-08 58,000字计划被4,500字附录覆盖截断
---

# write_file 前必须先 read_file 确认全文

任何对已有文件的 `write_file` 操作前，必须先 `read_file` 读取全文确认内容完整。

## 为什么

`write_file` = 全量替换文件内容，不是追加。如果只读取了文件的部分（如带 offset/limit），或根本没读，`write_file` 会覆盖未读取的部分。`patch` 工具才是安全的追加方式。

## 正确做法

| 场景 | 正确工具 |
|------|---------|
| 创建新文件 | `write_file` ✅ |
| 修改已有文件（替换特定内容） | `patch(old_string=..., new_string=...)` |
| 追加内容到文件末尾 | `patch`（old_string=文末几行, new_string=文末几行+新内容） |
| 必须全量覆盖已有文件 | 先 `read_file` 读全文 → 确认完整 → 再 `write_file` |

## 实战案例

2026-06-08：往 `/Users/holiday_home/.hermes/plans/ai-short-drama-dual-plan.md`（58,000 字，含 12 章节 + 4 附录）末尾追加附录 E 时，直接调用 `write_file` 写入约 4,500 字内容。`write_file` 全量覆盖了整个文件，原始章节 1-12 全部丢失。只能从对话历史逐段重建。

如果当时用 `patch`（old_string=文末几行, new_string=文末几行+附录E），不会发生截断。
