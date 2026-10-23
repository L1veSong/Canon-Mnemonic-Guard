---
type: ban
id: rule_pyautogui_screenshot_blocks_window
date: 2026-05-23
last_triggered: 2026-09-21
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_screenshot_001]
correction_template: "禁止 pyautogui/cli.py screenshot。请替换为 macOS 原生 screencapture -x（-x 静默无窗口）。"
keywords: [pyautogui, screenshot, 窗口遮挡, screencapture, 截图遮挡窗口]
tags: [desktop-control, macos, wechat]
---

# 禁止：pyautogui screenshot 用于桌面控制

## 触发场景

需要截取屏幕用于 OCR 定位/验证时。

## 规则

**pyautogui/cli.py screenshot 启动 Python 进程会让终端弹到前台，刚好挡住目标窗口。必须用 macOS 原生 `screencapture -x`（-x 无声音、零窗口）。**

## 错误模式

```bash
# ❌ 截图=弹终端=挡住微信=OCR只读到Python代码
python3 ~/.hermes/skills/desktop-control/cli.py screenshot /tmp/wx.png

# ✅ 静默截图，不弹任何窗口
screencapture -x /tmp/wx.png
```

## 为什么 pyautogui 截图会弹窗

- `python3 cli.py` 启动 → 终端窗口获得焦点 → 提到最前
- 截图时机：终端已在最前 → 微信被挡 → OCR 读到全是终端内容
- screencapture 是系统级命令，不在终端运行，不抢焦点

## 拦截行为

检测到 `cli.py screenshot` 或 `pyautogui.screenshot()` 用于桌面控制目的 → 拦截，替换为 `screencapture -x`。
