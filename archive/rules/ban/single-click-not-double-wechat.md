---
type: ban
id: rule_single_click_not_double_wechat
date: 2026-05-23
last_triggered: 2026-05-23
hit_count: 3
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_click_001]
correction_template: "微信聊天列表禁止双击。请使用单击（--clicks 1 或不指定），单击即可进入聊天。"
keywords: ['双击聊天', '双击列表', '双击联系人', 'single-click', 'double-click', '聊天列表', '进入聊天']
tags: [desktop-control, macos, wechat]
---

# 禁止：微信聊天列表双击

## 触发场景

用桌面控制在微信聊天列表中点击联系人进入聊天。

## 规则

**微信单击联系人 = 进入聊天。双击 = 进入后立刻退出（白点）。在聊天中双击 = 关闭当前聊天。无论什么场景，微信桌面控制只用单击。**

## 错误模式

```bash
# ❌ 双击——进去又出来，或把聊天关了
python3 cli.py click 475 246 --clicks 2

# ✅ 单击
python3 cli.py click 475 246
```

## 实际案例

- 第二次单击进入聊天 → 所有 OCR 验证都说"还在列表" → 我改用双击 → 进聊天立刻退出 → OCR 当然还显示在列表 → 死循环
- 已经在聊天中 → 双击 → 关掉了 → 下一次粘贴发到空白处

## 拦截行为

检测到 `--clicks 2` 或 `clicks=2` 配合微信操作 → 拦截，强制改为单击。
