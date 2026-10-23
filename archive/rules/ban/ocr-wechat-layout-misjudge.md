---
type: ban
id: rule_ocr_wechat_layout_misjudge
date: 2026-05-23
last_triggered: 2026-09-22
hit_count: 24
hits_block: 0
hits_record: 24
telemetry_synced: 2026-09-22
false_positives: 0
level: monitor
source_ids: [err_layout_001]
# correction_template: (monitor 级别，不配置)
keywords: [OCR识别, x坐标, 微信聊天列表, 聊天区, 联系人]
tags: [desktop-control, macos, wechat, ocr]
---

# 禁止：用 OCR x 坐标判断微信左右区域

## 触发场景

用 OCR 识别到"文件传输助手"后，通过 x 坐标判断它是在左侧聊天列表还是右侧聊天区。

## 规则

**OCR 的 x 坐标不可靠——窗口大小变化导致比例漂移，字体渲染导致边界模糊。不能用 x 坐标判断"在聊天还是列表"。**

## 正确判断方式

不用 x 坐标，用内容上下文：

```
在聊天列表: 联系人名 + 消息预览 + Q搜索框可见 = 列表
在聊天中:   联系人名在顶部 + 底部有输入框 + 无Q搜索 = 聊天
```

或者根本**不做判断**——直接单击联系人，焦点自动到输入框，粘贴发送。如果在聊天中，单击也不会搞坏（会选中文字但焦点仍在输入框，粘贴回车照常发）。

## 错误案例

- OCR(952,492) 窗口内 x=594，占窗口 67%——以为是聊天区，实际是列表
- 窗口宽 880 → 594 偏右；窗口宽 1265 → 594 偏左。判断随窗口大小变
- 终端的 Python 代码被 OCR 识别到 x=180 左右，混入判断干扰

## 拦截行为

检测到用 `abs_x < 600` 或 `abs_x > 608` 等硬编码 x 阈值判断微信区域 → 拦截，要求改用内容上下文判断或不做判断。
