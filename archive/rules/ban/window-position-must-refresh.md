---
type: ban
id: rule_window_position_must_refresh
date: 2026-05-23
last_triggered: 2026-09-13
hit_count: 2
hits_block: 2
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_window_pos_001]
correction_template: "禁止硬编码窗口坐标。每次截图前用 osascript 重新获取 process WeChat window 1 的 {position, size}。"
keywords: ['硬编码坐标', '坐标硬编码', '窗口位置刷新', '窗口位置硬编码', 'osascript 坐标']
tags: [desktop-control, macos, wechat, ocr]
---

# 禁止：硬编码窗口坐标

## 触发场景

用 OCR 分析截图前，对图片做 crop 裁剪到微信窗口区域。

## 规则

**微信窗口位置不固定——可能被拖拽、缩放、最小化。每次截图前必须用 osascript 重新获取窗口 position + size，禁止用上次的坐标。**

## 错误模式

```python
# ❌ 硬编码——窗口可能已经跑了
left, top, w, h = 358, 179, 880, 640
region = img.crop((left, top, left+w, top+h))

# ✅ 每次重新获取
import subprocess, re
r = subprocess.run(['osascript', '-e',
    'tell application "System Events" to tell process "WeChat" to tell window 1 to get {position, size}'],
    capture_output=True, text=True)
nums = [int(x) for x in re.findall(r'\d+', r.stdout)]
left, top, w, h = nums[0], nums[1], nums[2], nums[3]
region = img.crop((left, top, left+w, top+h))
```

## 实际案例

- 会话中窗口从 (358,179,880,640) 跑了三次：(131,38,1265,859)、(639,680,84,77)、(358,179,880,640)
- 84x77 那次是窗口被缩到极小，截图 crop 区域完全失效

## 拦截行为

检测到 OCR crop 代码中窗口坐标为硬编码数字（非变量）→ 拦截，要求先用 osascript 获取。
