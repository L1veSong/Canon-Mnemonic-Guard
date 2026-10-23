---
type: ban
id: rule_cmg_declaration_without_load
date: 2026-05-23
last_triggered: 2026-05-23
hit_count: 1
false_positives: 0
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
source_ids: [err_cmg_001]
correction_template: "新会话开始后必须先加载 canon-mnemonic-guard。请立即执行 skill_view(name='canon-mnemonic-guard')。"
keywords: [声明了CMG但没加载, SOUL声明CMG但未skill_view, CMG标记存在但未激活skill]
tags: [cmg, session-init, self-reflection]
---

# 禁止：SOUL 声明 CMG 但不加载

## 触发场景

新会话开始，SOUL.md 中有 `[CMG vX.X.X]` 声明，但没有主动 `skill_view("canon-mnemonic-guard")`。

## 规则

**SOUL.md 里的 CMG 声明只是标记，不等于激活。每个新会话必须主动加载 canon-mnemonic-guard skill，否则 Guard 不拦截、Mnemonic 不识别模式。**

## 正确做法

每个新会话开始，处理用户请求前：

```
skill_view(name="canon-mnemonic-guard")
```

## 为什么声明不等于激活

- SOUL.md 是静态文本，注入到系统提示中
- Skill 加载需要主动调用 skill_view
- 没加载 = 规则库为空 = 拦截器不工作 = 同一错误可以犯 7 次没人管

## 拦截行为

会话开始时扫描 SOUL.md → 检测到 CMG 声明但未加载 → 强制加载后再继续。
