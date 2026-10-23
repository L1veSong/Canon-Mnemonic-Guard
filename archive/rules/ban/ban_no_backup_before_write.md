---
type: ban
id: ban_no_backup_before_write
date: 2026-06-24
last_triggered: 2026-09-08
hit_count: 9
hits_block: 9
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: ['未备份', '没有备份', '不备份就改', '不备份就写', '不备份就直接']
tags: [文件安全, HTML, dashboard]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  用 write_file 或 patch 覆盖任何文件前，必须执行:
  cp <file> <file>.bak.$(date +%m%d%H%M)
  先验证备份存在，再执行修改。
  尤其 HTML/dashboard/server.py 等无版本控制的文件。
---

# 禁止：write_file/patch 前不备份

## 触发场景
任何 write_file、patch 操作涉及覆写整个文件内容时，必须先备份。

## 拦截行为
1. 修改前必须 cp 备份
2. 备份文件命名: `<原文件名>.bak.<MMDDHHMM>`
3. 验证备份存在后再执行修改
4. CMG 应在 pre_tool_call 检测 write_file + HTML/py/md 触发提醒

## 实战案例
2026-06-24: dashboard.html 重构，write_file 全量替换 CSS，丢失 HTML/JS。
因审计时清理了所有 .bak 文件，无备份可恢复。只能手写重建。

2026-06-15: HTML 美食栏目用 execute_code 修改，多次互踩致文件损坏。
所有备份都是 5 天前的旧版本。
