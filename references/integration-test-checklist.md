# 联动待测清单

> Guard 拦截成功后会写 intercept_log.jsonl。
> 以下三项依赖 Guard 真实拦截数据——等积累够了逐个验证。

---

## 1. ralph-loop — 多步骤闭环验证

**触发条件：** Guard 拦截「跳步骤」且剩余步骤 ≥ 3 个

**如何验证：**
1. 用户给出 5+ 步骤的复杂指令
2. Agent 只做了 2 步就说「完成了」
3. Guard StepCompletenessInterceptor 拦截
4. Agent 判断剩余 ≥ 3 步 → 调 ralph-loop
5. ralph-loop 逐步骤执行 → 全部闭环

**状态：** ❌ 待测（需真实多步骤遗漏场景）

---

## 2. VBC — 证据先于断言

**触发条件：** Agent 声称「已完成但是」未附验证证据

**如何验证：**
1. Agent 完成一项任务后说「已完成」
2. 没有附任何验证证据（文件存在？测试通过？）
3. Guard FabricationInterceptor 拦截「声称完成未验证」
4. Agent 调 VBC
5. VBC 要求：列出每项 → 附证据 → 通过才放行

**状态：** ❌ 待测（需真实声称未验证场景）

---

## 3. diagnose — 高频命中根因分析

**触发条件：** 同一规则短期内被命中 ≥ 3 次（已测 escalation 模式通过）

**如何验证：**
1. 同一规则被 Guard 频繁拦截（已测：「跳过检查直接交付」×3）
2. Agent 调 diagnose
3. diagnose 分析根因 → 输出改进建议

**状态：** ⚠️ escalation 已验证，diagnose 自动触发未测

---

## 4. plur → CMG 规则提取

**触发条件：** plur 中有「准则类」内容 + CMG 扫盘

**如何验证：**
1. plur learn 写入一条含「禁止/必须」的规则
2. CMG !scan 扫盘读取 ~/.plur/engrams.yaml
3. 提取准则 → 提示导入 → 固化为 rules/ 规则

**状态：** ✅ plur 数据已验证，扫盘读取路径已通

---
最后更新: 2026-05-22
