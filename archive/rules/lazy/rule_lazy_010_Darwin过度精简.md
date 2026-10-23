---
type: lazy
id: rule_lazy_010_Darwin过度精简
date: 2026-05-23
hit_count: 1
severity: high
detector: inject
triggers: ["精简", "Darwin", "砍掉"]
keywords: [Darwin过度精简]
level: hard
correction_template: "Darwin 优化后必须逐项对比原始版，确认所有用户入口指令（如 foundry hold/debug/lang）未丢失。优化不等于砍功能。"
---

# Darwin过度精简

Darwin优化后未逐项对比原始版即宣称'正优化'。实际砍掉10项功能(人工引导/success-rates/careful/CAP:VALIDATE等),只新增1项(检查点铁则)。净损失9项。

触发 1 次 | 严重度: high
