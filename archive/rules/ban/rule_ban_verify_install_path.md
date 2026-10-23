---
type: ban
id: rule_ban_verify_install_path
date: 2026-06-25
last_triggered: 2026-06-25
hit_count: 1
false_positives: 0
source_ids: [err_install_path_miss]
keywords: ['没验证就说没装', '没查就说不存在', '没查就说没找到', '凭印象说没装', '凭印象说不存在', 'install path']
tags: [验证, 路径, 搜索]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  说"X没装"前必须先：
  1. 检查对应 skill 文档中的安装路径声明
  2. 搜索 /tmp/、~/、~/.hermes/ 等所有可能路径
  3. 确认后再下结论
---

# 禁止：搜索不全就说"没装"

## 触发场景
说某个工具/软件"没装/不存在"时，只搜了部分路径（如只搜 ~/Desktop），遗漏了 skill 文档声明的安装路径（如 /tmp）。

## 拦截行为
说"没装"前必须：
1. 检查相关 skill 文档中的安装路径声明
2. 搜索所有可能路径（~、/tmp、~/.hermes 等）
3. 确认后再下结论

## 实战案例
2026-06-25：用户问 MediaCrawler 是否导致小红书封号。AI 只搜 ~/Desktop，没搜 /tmp（social-media-crawler skill 声明安装路径），说"没装"。用户纠正后才在 /tmp 找到。
