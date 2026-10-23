---
type: ban
id: rule_063
date: 2026-05-28
last_triggered: 2026-05-28
hit_count: 1
false_positives: 0
source_ids: [err_20260528_005]
keywords: [链接没看, 截图没看, 图片没看, 只看了摘要, 只看摘要, 看一半, 只看文字, 完整看完, 没看完整]
tags: [偷懒, 信息遗漏]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "用户发的任何链接→必须穷尽所有方式阅读完整内容（含图片、附件、代码块），禁止只看文字摘要就说'看了'。图片无法加载时→主动告知用户并问内容，不假装已看。"
---

# 规则：链接必须完整看完，禁止只看摘要

## 触发条件
用户发送任何链接（豆包、DeepSeek分享、GitHub、网页等）。

## 拦截行为

> **例外：** JS 渲染站点（SPA）跳过 web_extract，直接走 browser。详见 [[rule_gap_skip_web_extract_for_js_sites]]。
1. 提取全文（web_extract）
2. 检查是否有图片/附件/代码块→有则用vision_analyze或浏览器查看
3. 确认全部内容已消费→才能回复
4. 图片加载失败→主动告知用户"图片看不到，请描述内容"

## 违规记录
2026-05-28：用户发豆包链接（含2张截图）+ DeepSeek分享（含多张截图），多次只看文字摘要就说"看了"，图片一张都没看。用户指出后仍然狡辩"读不到"而不是主动想办法。
