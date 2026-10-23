---
type: ban
id: rule_ban_api_key_leak
date: 2026-06-08
hit_count: 23
hits_block: 23
hits_record: 0
telemetry_synced: 2026-09-22
severity: critical
keywords: ['sk-', '密钥是', '密钥为', '密钥：', '密钥:', '泄露密钥', '输出密钥', '明文存储', '明文保存', '明文传输', '明文密码', 'token:', 'Authorization:', 'nvapi-', '5f0e256e']
level: monitor
downgrade_note: 2026-09-24 说明性用词误拦（用户要求降噪）；只记录+注入提醒，不再硬拦
correction_template: |
  检测到对话中疑似出现 API key 明文。
  禁止在对话中粘贴任何 API key/密钥/Bearer token。
  用户应使用 hermes config set 写入配置文件，或发截图替代明文。
  如果用户确实需要传递 key → clarify 提醒风险，等用户确认后再继续。
source: 2026-06-08 李吉扬粘贴火山引擎key到对话
---

# API key 禁止明文暴露

禁止在对话中以明文形式粘贴任何 API key、密钥、Bearer token、Access Key。

## 触发场景

- 用户或 AI 在消息中直接粘贴包含 `sk-`、`api_key`、`Bearer`、`Authorization:` 等模式的字符串
- 来自外部来源（网页、文件）的 key 被直接回显到对话

## 拦截行为

发现疑似 API key → 立即提醒用户风险 → 建议用配置工具写入或发截图替代

## 实战案例

2026-06-08：李吉扬直接将火山引擎 API key `5f0e256e-a774-4529-b2d3-8138c0642182` 粘贴到对话中。虽日志本地存储无外部泄露风险，但坏习惯一旦养成，后续充值的 key 可能通过截图/日志分享泄露。
