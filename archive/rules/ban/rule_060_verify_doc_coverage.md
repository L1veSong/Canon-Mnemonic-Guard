---
type: ban
id: rule_060
date: 2026-05-28
last_triggered: 2026-09-22
hit_count: 2
hits_block: 2
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: [err_session_20260528_001]
keywords: [创建文件后, 覆盖度, 逐条核对, 文档遗漏]
tags: [偷懒, 文档完整性, planning]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "创建任何持久化文件（planning/project/文档）后，必须回顾本次会话全部讨论点，逐条核对是否已记录。核对完输出 'N/N 条已覆盖，无遗漏'。未完成此校验步骤不得声称'记完了'。"
---

# 规则：持久化文件必须逐条核对覆盖度

## 触发条件
创建或修改任何跨会话持久化文件（planning/project文件、文档、笔记）后，声称"记完了"或类似表述之前。

## 拦截行为
强制回顾本次会话全部讨论点 → 逐条核对 → 补充遗漏 → 输出 N/N 覆盖确认。

## 违规记录
2026-05-28：创建 Marvis 项目 plan/findings/progress 三个文件后，未经逐条核对就声称"记完了"，遗漏4个讨论点（环境兼容性、API不通、Skill不通用、统一平台愿景），被用户当场指出。
