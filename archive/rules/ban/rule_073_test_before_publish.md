---
type: ban
id: rule_073
date: 2026-05-28
last_triggered: 2026-05-28
hit_count: 2
false_positives: 0
keywords: ['可以上传', '发布完成', '打包好了']
tags: ["发布流程", "测试", "阻断"]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  用户说「发布」「上传」→ 禁止直接说「可以上传」。必须先执行完整测试（diagnose + 功能验证 + agent.log 拦截检查），逐项报告结果后，才可以说「可以上传」。
---

# 发布前必须先测试

**触发条件**: 准备说「可以上传」「可以发布」「打包好了」时。

**拦截行为**: 必须先跑 !diagnose + 功能验证 + agent.log 检查。全部通过才能放行。缺任何一项 → 阻断。
