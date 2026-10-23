---
type: ban
id: rule_extra_click_wechat_input
date: 2026-05-23
last_triggered: 2026-09-16
hit_count: 1
hits_block: 1
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_extra_click_001]
correction_template: "进入微信聊天后焦点自动在输入框，禁止额外点击输入框。请跳过点击输入框的步骤，直接粘贴文字。"
keywords: ['点击输入框', '窗口焦点', '额外点击', 'wechat 输入框', '自动聚焦', '微信输入框']
tags: [desktop-control, macos, wechat]
---

# 禁止：进入微信聊天后额外点击输入框

## 触发场景

用桌面控制点击微信联系人进入聊天后，额外点击输入框区域。

## 规则

**微信桌面客户端：点击联系人进入聊天后，焦点自动在消息输入框。不需要额外点击。额外点击会导致焦点跳到别处——可能误入其他聊天或关闭当前聊天。**

## 正确流程

```bash
# ✅ 三步完成
1. 点击联系人 → 进入聊天
2. 粘贴消息（AppleScript Cmd+V）
3. 回车发送

# ❌ 四步——多此一举，可能坏事
1. 点击联系人 → 进入聊天
2. 点击输入框 → 焦点跑偏
3. 粘贴消息 → 发到别处
4. 回车发送
```

## 拦截行为

检测到「点击联系人」后跟「点击聊天区域底部」→ 拦截第二个点击，提示焦点已在输入框。
