---
name: hermes-self-reflection
description: 自省引擎 — Hermes 错题本+免疫系统。用户指出一次错误，永久生效。每次行动前自动检索规则库，拦截违规行为。
version: 1.0.0
role: guard
stage: pre_action
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
---

# Hermes 自省引擎 v1.0.0

> **角色**: guard (护栏管道) | **阶段**: pre_action (每次行动前) | **位置**: 在所有执行之前
>
> 本 Skill 是管道而非竞争者——不与任何 Skill 竞争优先级。每次行动前强制检查。

---

## 文件结构

```
~/.hermes/self-reflection/
├── errors.jsonl              # 原始错误记录 (永久追加)
├── patterns.json             # 匹配模式库 (去重压缩)
├── rules.permanent.md        # 固化永久规则 (自动生成)
├── config.json               # 用户配置
└── checklists/               # 防偷懒清单
    ├── default.yaml
    ├── essay.yaml
    ├── coding.yaml
    └── skill-call.yaml
```

---

## 启动时（Skill 加载）

### 1. 加载配置
读取 `~/.hermes/self-reflection/config.json`。如不存在，使用默认配置：
- `match_mode`: layered
- `load_mode`: full_preload
- `semantic_match`: auto
- `auto_solidify_threshold`: 10

### 2. 加载永久规则 & 注入系统提示
读取 `~/.hermes/self-reflection/rules.permanent.md`。
- 如文件不存在 → 跳过
- 如存在 → 将全文追加到系统提示，紧跟在 SOUL.md 之后

```
═══════════════════════════════════════
自省引擎 · 永久规则 (自动注入，请勿忽略)
═══════════════════════════════════════
[rules.permanent.md 全文]
═══════════════════════════════════════
```

### 3. 加载防偷懒清单
读取 `~/.hermes/self-reflection/checklists/` 下所有 YAML 文件。

### 4. 检查固化阈值
读取 `~/.hermes/self-reflection/errors.jsonl`，统计行数。如果 ≥ `auto_solidify_threshold` (默认 10)，自动触发固化。

### 5. 输出激活状态
**必须输出**: "自省引擎已激活。X 条禁止 / Y 条缺失 / Z 条偷懒。"

---

## 用户指出错误时（「记住」触发）

### 触发词
- "记住" / "记下" / "记录这个错误"
- "这是错的" / "以后禁止" / "不要这样做"
- "你又犯这个错了" / "上次不就说过了吗"
- "把这条加到规则里" / "这条也拦一下"
- 任何表达"记录错误行为 + 希望未来避免"的语句

### 执行流程

**Step 1: 确定错误类型**
分析用户语句推断 type：
- 包含"禁止/不要/拦截" → `ban`
- 包含"不够/还差/不足" → `gap`
- 包含"跳过/偷懒/没做" → `lazy`
- 不确定 → 反问确认

**Step 2: 提取规则**
- `rule`: 完整规则描述
- `context`: 触发场景
- `trigger`: "用户指出:{摘要}"

**Step 3: 生成匹配条件**
- `match.exact`: 3-5 个精确匹配关键词
- `match.semantic`: 1 句语义描述

**Step 4: 写入 errors.jsonl**
```json
{"ts":"ISO8601","type":"ban|gap|lazy","trigger":"用户指出:...","rule":"规则描述","context":"触发场景","match":{"exact":["kw1","kw2"],"semantic":"语义描述"}}
```

**Step 5: 更新 patterns.json**
增量更新，同类规则合并 keywords，新规则新增条目。

**Step 6: 反馈确认**
"已记录。规则: [{rule}]，类型: {type}。下次匹配到将{拦截/补齐/追加}。"

---

## 每次行动前（拦截检查）

### 1. 精确匹配（必须执行）
当前行为文本 → patterns.json keywords → 命中则触发。

### 2. 语义匹配（条件执行）
精确匹配未命中 + semantic_match ≠ off → AI 语义对比。
超时 5 秒 → 降级为精确匹配。

### 3. 命中后的行为

**ban（禁止项）→ 立即拦截**
```
⛔ 拦截。命中禁止规则: [{rule}]。来源: 用户于 {ts} 指出。已阻止。
```

**gap（缺失项）→ 自动补齐**
```
⚠️ 检测到不满足: [{rule}]。自动补齐中...
```

**lazy（偷懒项）→ 追加执行**
```
⚠️ 检测到可能跳步骤: [{rule}]。追加执行中...
```

### 4. 防偷懒清单自检
逐项对照 checklists/，未通过 → 执行 action_on_fail。

---

## 固化引擎

### 触发条件
1. errors.jsonl 新增行数 ≥ `auto_solidify_threshold` (默认 10)
2. 用户说 "固化规则" / "整理规则" / "去重规则"

### 执行流程

1. 读取 errors.jsonl 全部行
2. 去重合并同类规则
3. 生成 rules.permanent.md:
```markdown
# 自省永久规则 · 固化于 YYYY-MM-DD HH:MM
# ⚠️ 此文件由固化引擎自动生成，请勿手动修改

## 禁止项 (ban) — 命中即拦截
1. 规则描述 (来源: err_001, hit: 2)

## 缺失项 (gap) — 命中即补齐
...

## 偷懒项 (lazy) — 命中即追加
...
```
4. 生成 patterns.json
5. 反馈: "固化完成。N 条原始记录 → M 条永久规则。"

---

## 安装

1. 创建 `~/.hermes/self-reflection/` 目录
2. 复制模板: errors.jsonl, patterns.json, config.json
3. 复制 checklists/
4. 注入 SOUL.md 硬规则 (无 SOUL.md → 生成 prompt.md 兜底)
5. 输出: "自省引擎已安装。你只需说「记住」，我会从此记住。"

## 卸载

1. 保留 `~/.hermes/self-reflection/` 目录
2. 移除 SOUL.md 注入块
3. 输出: "自省引擎已卸载。规则文件保留。"

---

## 异常处理 & 降级

| 场景 | 处理 |
|------|------|
| errors.jsonl 损坏 | 告警 + 跳过，通知用户 |
| patterns.json 损坏 | 回退 errors.jsonl 全量扫描 |
| 存储目录不可写 | 降级内存模式，警告 |
| 语义匹配超时 (>5s) | 关闭语义匹配，仅精确匹配 |
| 规则冲突 (同类型) | 暂停，clarify 让用户裁定 |
| 自省引擎加载失败 | "护栏不可用"，全部放行 |

### 环境降级

| 环境 | 精确匹配 | 语义匹配 | 可用性 |
|------|---------|---------|-------|
| 大模型 | ✅ | ✅ AI | 🟢 完整 |
| 中等模型 | ✅ | ⚠️ 启发式 | 🟡 够用 |
| 小模型 | ✅ | ❌ 关闭 | 🟢 核心可用 |

---

## 自保机制（元规则）

1. 启动时必须输出激活状态
2. 每次拦截必须说明原因
3. 规则库为空时默认放行
4. 引擎不能修改自己的 SKILL.md 或 config.json

## 误报处理

1. 用户说 "这不是违规，放行" → 放行 + 记录误报
2. 同一规则累积 3 次误报 → 提示调整
3. 后续同类场景 → 先问再拦

---

## 版本路线

- **v1.0.0** (当前): Skill 形态，单文件 rules.permanent.md
- **v2**: Obsidian 结构化 — 每条规则独立 .md
- **v3**: gbrain 式系统集成
