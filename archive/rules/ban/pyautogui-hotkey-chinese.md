---
type: ban
id: rule_pyautogui_hotkey_chinese
date: 2026-05-23
last_triggered: 2026-09-19
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_hotkey_001]
correction_template: "禁止 pyautogui.hotkey('cmd','v')。请替换为 osascript keystroke 'v' using command down。"
keywords: ['pyautogui', 'hotkey 粘贴', 'cmd+v', '粘贴中文', '修饰键', 'Cmd丢失']
tags: [desktop-control, macos, wechat, input]
---

# 禁止：pyautogui hotkey 粘贴中文

## 触发场景

在 macOS 上用 pyautogui 的 hotkey 模拟 Cmd+V 粘贴中文。

## 规则

**pyautogui hotkey("cmd", "v") 在 macOS 上 Cmd 修饰键经常丢失，只输出字母 v。粘贴中文必须用 AppleScript。**

## 错误示例

```bash
# ❌ pyautogui hotkey——只打出一个字母 v
python3 -c "import pyautogui; pyautogui.hotkey('cmd', 'v')"

# ✅ AppleScript——正确粘贴
osascript -e 'tell application "System Events" to tell process "WeChat" to keystroke "v" using command down'
```

## 完整粘贴流程（配合剪贴板）

```bash
osascript -e 'set the clipboard to "要粘贴的中文"'
osascript -e 'tell application "System Events" to tell process "目标App" to keystroke "v" using command down'
```

## 拦截行为

检测到 pyautogui.hotkey 或 cli.py hotkey 用于粘贴中文 → 拦截，要求改用 AppleScript。
