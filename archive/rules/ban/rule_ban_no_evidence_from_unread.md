---
type: ban
id: rule_ban_no_evidence_from_unread
level: monitor
downgrade_note: 2026-09-24 说明性用词误拦（用户要求降噪）；只记录+注入提醒，不再硬拦
date: 2026-05-30
last_triggered: 2026-09-22
hit_count: 9
hits_block: 9
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
source_ids: [err_cmg_fabrication_001]
keywords: ['未读取', '素材没读', '没读素材', '读不到', '无法访问', '我看了', '我确认', '我读完了', '三个AI', '交叉验证', '三方核对', '讨论了']
tags: [meta, enforcement, evidence, cognitive-honesty]
correction_template: |
  素材读取失败后禁止基于该素材生成任何结论。只能输出「链接/素材无法访问，无法获取内容，不能做任何结论」。
  禁止编造素材内的对话内容、验证结果、交叉核验说法。
---

# 禁止基于未读取素材做断言

## 规则

1. 任何网页链接、分享链接、截图素材，**未完整读取全部内容**则禁止基于该素材做以下任何操作：
   - 声称「已确认」「已读取」「三个 AI 都同意」「交叉验证完成」
   - 描述素材内的对话、讨论、结论
   - 引用素材内容作为证据支撑自己的判断

2. 素材读取失败（cookie 拦截、页面空白、图片加载失败等）时：
   - **必须**明确告知用户「该链接/素材无法访问，无法获取内容」
   - **禁止**编造任何关于该素材内容的说法
   - **禁止**猜测素材内容后伪装成已读取

3. 用户指出「无依据编造」时：
   - 立即承认错误，不辩解
   - 标记该行为，post_llm_call 额外扫描类似模式
