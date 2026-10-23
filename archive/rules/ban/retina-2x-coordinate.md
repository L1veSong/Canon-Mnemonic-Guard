---
type: ban
id: rule_retina_2x_coordinate
date: 2026-05-23
last_triggered: 2026-05-23
hit_count: 7
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_retina_001]
correction_template: "所有 OCR 坐标必须除以 2。请将你输出的所有坐标数值全部除以 2 后再输出。"
keywords: ['retina 坐标', 'pyautogui', 'screencapture', '截图分辨率', 'Retina坐标']
tags: [desktop-control, macos, wechat]
---

# 禁止：OCR 坐标直接传给 pyautogui

## 触发场景

在 macOS 上用 screencapture 截图后用 OCR 获取坐标，再用 pyautogui 点击。

## 规则

**screencapture 截图是 Retina 2x 分辨率（如 3024x1964），pyautogui 使用逻辑分辨率（如 1512x982）。OCR 坐标必须除以 2 才能传给 pyautogui。**

## 错误示例

```python
# ❌ 直接传 OCR 坐标——点到屏幕外面去了
ocr_x, ocr_y = 950, 490  # 从 3024x1964 截图 OCR 得到
pyautogui.click(ocr_x, ocr_y)  # 偏到右下角

# ✅ 除以 2
pyautogui.click(ocr_x // 2, ocr_y // 2)  # (475, 245) 正确
```

## 拦截行为

检测到 pyautogui click/move 坐标超过屏幕逻辑分辨率一半 → 拦截，提示除2。
