---
name: guard
description: 自省引擎护栏线 (Guard) — 规则执行器。运行时读取 Canon 规则库 + Mnemonic 记忆库，独立执行 pre_action 前置拦截。纯执行校验层。
version: 4.0.0
role: guard
stage: pre_action
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
---

# Guard 护栏线 v4.0.0

> **角色**: guard (规则执行器) | **阶段**: pre_action (每次行动前) | **位置**: Canon 之后，所有执行之前
>
> 从 Canon Mnemonic Guard v2.4.1 剥离。读取 Canon 的 rules/ 目录作为规则源，读取 Mnemonic 的 state.json 感知上下文。

---

## 文件结构

```
~/.hermes/self-reflection/
├── intercept_log.jsonl      # 拦截日志 (Guard 写入)
├── rules/                   # 规则库 (Canon 生产，Guard 读取)
├── state.json               # 跨会话状态 (Mnemonic 生产，Guard 读取)
├── errors.jsonl             # 原始错误记录 (Canon 写入)
├── patterns.json            # 匹配模式库 (Canon 维护)
└── config.json              # 用户配置
```

---

## 启动时（Skill 加载）

### 1. 加载 Canon 规则库

读取 `~/.hermes/self-reflection/rules/` 目录，遍历 ban/gap/lazy 三类规则，解析 frontmatter 中的 type、keywords、tags，构建拦截匹配表。

### 2. 加载 Mnemonic 状态

读取 `~/.hermes/self-reflection/state.json`，获取跨会话状态（会话计数、引擎健康指标、上下文豁免标记）。

### 3. 初始化拦截日志

如 `~/.hermes/self-reflection/intercept_log.jsonl` 不存在则创建。

### 4. 输出激活状态

**必须输出**: "Guard v4.0.0 已激活。读取 Canon {N} 条规则。Mnemonic 状态: 会话 #{sessions}。"

---

## 五层拦截器

```
Interceptor 接口       ← 每个拦截器独立开关、独立日志
  ├── BanInterceptor              精确匹配拦截
  ├── FabricationInterceptor      防幻觉拦截
  ├── StepCompletenessInterceptor 防跳步骤拦截
  ├── SkillLoadInterceptor        防偷懒拦截
  └── ClarifyInterceptor          防瞎猜拦截
```

### 1. BanInterceptor — 精确匹配

当前思考文本 → 逐条比对 patterns.json 中所有 ban keywords → 命中则拦截。

### 2. FabricationInterceptor — 防幻觉

识别"声称型语句"（我能/我有/我会/已创建/存在...）→ 逐条核实（查 skills_list/API/源）→ 无法核实则拦截。

### 3. StepCompletenessInterceptor — 防跳步骤

用户原始指令 → 拆解为步骤列表 → 已完成 vs 未完成 → 有遗漏则拦截追加执行。

### 4. SkillLoadInterceptor — 防偷懒

任务文本 → 提取领域关键词 → 扫描 skills_list → 0 个匹配 Skill 已加载则拦截。

### 5. ClarifyInterceptor — 防瞎猜

当前步骤 ≥ 2 个可选项且需用户决策 → 检查是否已调用 clarify → 未调用则拦截。

---

## 评分计数器

每次拦截检查后，更新 Canon rules/ 目录中对应规则的 frontmatter：

```
命中时: hit_count += 1, last_triggered = now()
误报时: false_positives += 1 (用户说「这不是错误」后回调写入)
```

Canon 固化引擎运行时读取 hit_count / false_positives 计算评分。高分规则严格拦截，低分规则降级为提醒。

---

## 拦截日志

每次拦截写入 `intercept_log.jsonl`：

```json
{"ts":"ISO8601","interceptor":"Ban","rule_id":"rule_001","action":"block","reason":"关键词匹配: 虚构","context":"用户要求输出一个不存在的API"}
```

---

## 与 Canon / Mnemonic 联动

```
Canon (producer, system_anchor)
    │  生产 rules/*.md + patterns.json + errors.jsonl
    ▼
Guard (guard, pre_action)
    │  读取 Canon 规则 → 五层拦截 → 命中/误报计数
    │  写入 intercept_log.jsonl
    ▼
Mnemonic (memory, background)
    │  读取 intercept_log.jsonl → 自动模式识别 → 推送规则草稿至 Canon
    ▼
Canon 固化引擎 → 去重 → 写入 rules/
```

---

## 安装

```bash
npx skills add guard --yes --global
```

或从 Canon Mnemonic Guard 仓库独立获取。
