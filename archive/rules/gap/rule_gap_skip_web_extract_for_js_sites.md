---
type: gap
id: rule_gap_skip_web_extract_for_js_sites
date: 2026-06-25
last_triggered: 2026-06-25
hit_count: 0
detector: inject
triggers: ["https://", "http://", "web_extract"]
false_positives: 0
source_ids: [user_correction_20260625]
keywords: [web_extract, JS渲染, SPA, 空壳, 浪费一步, 域名预判]
tags: [效率, 工具选择]
level: soft
correction_template: |
  外部链接先判断域名类型：
  - raw.githubusercontent.com / .md / .json / .txt / API 文档 → web_extract
  - 官网 / 文档站 / 博客（大概率 JS 渲染 SPA）→ 直接 browser
  禁止无条件先调 web_extract 再切 browser，浪费一步。
---

# 跳过 web_extract 的 JS 渲染站点预判

> **父规则：** 本规则是 [[rule_063_link_complete_reading]] 的例外条款——静态站点仍走 web_extract，JS 站点直接 browser。

## 触发条件

处理任何外部链接时，判断目标是否为 JS 渲染站点（SPA）。

## 规则

| 站点类型 | 工具 |
|---------|------|
| `raw.githubusercontent.com`、`.md`、`.json`、`.txt`、API 裸接口 | web_extract |
| 官网、文档站、博客、论坛 | 直接 browser |

## 原因

CMG 原规则「外部来源必须先 web_extract 验证」对 JS 渲染网站无效——web_extract 只能拿到空壳，80% 的情况下需要再开 browser。两步浪费。

## 拦截行为

soft 级——不做硬拦截，只在思考阶段提醒。AI 自觉判断。
