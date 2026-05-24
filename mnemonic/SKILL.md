---
name: mnemonic
description: 三省引擎(CMG)忆存线 (Mnemonic) — 状态记忆层。v3.4.0 模式识别加速(同会话2次推草稿，原7天3次)。纯记忆状态层，不生产规则不执行拦截。
version: 3.4.0
role: memory
stage: background
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
metadata:
  hermes:
    tags: [cmg, mnemonic, memory, pattern-recognition]
    related_skills: [canon, guard, canon-mnemonic-guard]
---

# Mnemonic 忆存线 v3.3.0

> **角色**: memory (状态记忆层) | **阶段**: background (后台常驻) | **位置**: Guard 之后，Canon 之前
>
> 读取 Guard 的 intercept_log.jsonl 和 state.json，自动识别高频错误模式，推送规则草稿至 Canon 固化引擎。不生产规则、不执行拦截。

---

## 文件结构

```
~/.hermes/self-reflection/
├── intercept_log.jsonl      # 拦截日志 (Guard 写入，Mnemonic 主数据源)
├── errors.jsonl             # 原始错误记录 (Canon 写入，Mnemonic 降级数据源)
├── state.json               # 跨会话状态 (Mnemonic 维护)
├── mnemonic_state.json      # 独立持久化状态 (Mnemonic 维护)
├── rules/                   # 规则库 (Canon 生产)
└── config.json              # 用户配置
```

---

## 版本变更

| 版本 | 变更 |
|------|------|
| v3.3.0 | +M1 数据源降级链: intercept_log.jsonl → errors.jsonl → 等待状态，零报错 |
| v3.2.0 | +M2 独立持久化 mnemonic_state.json +M4 误报率双向调节(置信度±0.1/0.2) |
| v3.1.0 | +自动模式识别(7天≥3次→草稿→推Canon) |
| v3.0.0 | CLI规格 + 独立触发 + 角色声明制 |

---

## 启动时（Skill 加载）

### 1. 选择数据源（M1 · v3.3.0）

**数据源降级链：** 优先读取 Guard 拦截日志，无则回退 Canon 错误记录，全无则等待。

**执行步骤：**

```
1. 检查 ~/.hermes/self-reflection/intercept_log.jsonl
   - 存在且非空 → data_source = "guard_intercept"
     → 加载最近 7 天拦截记录
     → 分组统计关键词频次
     → 输出: "Mnemonic v3.4.0: 数据源=Guard拦截日志（{N}条/7天）"

2. 不存在或为空 → 降级检查 errors.jsonl
   - 存在且非空 → data_source = "canon_errors"
     → 加载全部错误记录（无时间窗口限制，因 errors.jsonl 永久追加）
     → 分组统计关键词频次
     → 输出: "Mnemonic v3.4.0: 数据源=Canon错误记录（降级，{N}条总计）。等待 Guard 拦截日志积累后自动切换。"

3. 两个都不存在或都为空 → data_source = "none"
   - 跳过模式识别
   - 仍正常加载 mnemonic_state.json 和 state.json
   → 输出: "Mnemonic v3.4.0: 数据源=等待中（无拦截日志，无错误记录）。模式识别暂停。"
```

**关键：** 不报错、不崩溃、不空转。无论数据源状态如何，Mnemonic 正常激活，只是模式识别能力随数据可用性动态调整。

### 2. 读取拦截日志（主数据源）

当 `data_source = "guard_intercept"` 时，加载 `~/.hermes/self-reflection/intercept_log.jsonl`，统计最近 7 天拦截事件。按关键词分组，计算出现频次。

### 3. 读取状态

加载 `~/.hermes/self-reflection/state.json` 和 `~/.hermes/self-reflection/mnemonic_state.json`。

### 4. 输出激活状态

**必须输出**: "Mnemonic v3.4.0 已激活。数据源: {guard_intercept/canon_errors/none}。近 7 天拦截 {N} 次。模式识别: {on/degraded/off}。"

---

## 自动模式识别

### 触发条件

**v3.4.0 加速：**

| 场景 | 阈值 | 行为 |
|------|:---:|------|
| **同会话** | 同类违规 ≥ 2 次 | 立即推草稿 + 用户确认 |
| **跨会话** | 7 天内累计 ≥ 2 次 | 推草稿 + 用户确认 |
| **主数据源** | 同一 rule_id 被 RetryLoop 超限 ≥ 2 次 | 自动推草稿（标记为待复核） |

**降级数据源（errors.jsonl）：** 阈值仍为 ≥ 5 次（无时间窗口，因 errors.jsonl 永久追加）。

**防噪音：** 每次推送带置信度评分。同会话2次→置信度0.7，跨会话7天2次→置信度0.5。置信度<0.5的草稿仅记录不推送。

### 识别流程

```
1. 遍历数据源记录 → 按 rule_id + interceptor（或 error_type）分组
2. 统计每组频次 → 筛选 ≥ 阈值的模式
3. 与 rules/ 已固化规则去重 → 排除已覆盖的
4. 与 mnemonic_state.json 已推送草稿去重 → 排除重复推送
5. 生成规则草稿 → clarify 提醒用户确认
6. 用户确认 → 推送至 Canon 固化引擎
```

### 规则草稿格式

```json
{
  "ts": "ISO8601",
  "type": "ban",
  "rule": "自动识别: 高频违规XXX",
  "context": "近7天触发{N}次，数据源: {guard_intercept/canon_errors}",
  "match": {
    "exact": ["关键词1", "关键词2"],
    "semantic": "语义描述"
  },
  "source": "mnemonic_pattern",
  "data_source": "guard_intercept"
}
```

### 推送至典则线

草稿不直接写入 rules/，而是通过标准化接口推送至 Canon 固化引擎。Canon 负责去重、分类、冲突检测、写入。

### 误报率自适应 (M4)

同一模式误报率高时自动降低匹配置信度。误报减少后自动回升：

```
连续5次命中无误报 → 置信度 +0.1 (最高1.0)
连续3次误报 → 置信度 -0.2 (最低0.1)
置信度<0.3 → 不再自动推送，仅记录日志到 mnemonic_state.json
置信度恢复>0.5 → 恢复自动推送
```

### 独立持久化 (M2)

独立维护 `~/.hermes/self-reflection/mnemonic_state.json`：

```json
{
  "pattern_history": [{"keyword":"虚构","count":4,"last_seen":"ISO8601","confidence":0.8}],
  "draft_queue": [{"rule_id":"draft_001","status":"pending_confirm"}],
  "recognition_stats": {"total_patterns":12,"pushed_to_canon":3,"false_positives":2},
  "data_source_history": {"guard_intercept_sessions": 45, "canon_errors_sessions": 12, "none_sessions": 3}
}
```

`data_source_history` 追踪各数据源的使用会话数（v3.3.0 新增），用于判断何时从降级切回主数据源。

### 数据源切换监控（M1 · v3.3.0）

每次加载时自动检测：

```
1. 当前 data_source = "canon_errors"（降级模式）
2. 检查 intercept_log.jsonl 是否已出现且非空
3. 是 → 自动切换 data_source = "guard_intercept"
   → 输出: "🔄 Mnemonic 数据源已升级: canon_errors → guard_intercept（检测到 Guard 拦截日志）。"
4. mnemonic_state.json 记录切换事件
```

---

## CLI 命令

| 命令 | 说明 |
|------|------|
| `hermes reflect status` | 查看规则库状态（总数/分类/最近固化时间） |
| `hermes reflect add "规则"` | 手动添加规则 |
| `hermes reflect scan` | 手动触发扫盘 |
| `hermes reflect patterns` | 查看当前识别到的高频模式 |
| `hermes reflect datasource` | 查看当前数据源状态和切换历史（v3.3.0 新增） |

---

## 与 Canon / Guard 联动

```
Guard (pre_action)
    │  写入 intercept_log.jsonl
    ▼
Mnemonic (background)
    │  读取拦截日志 → 模式识别 → 生成草稿
    │  如无拦截日志 → 降级读 errors.jsonl → 模式识别
    │  推送至 Canon 固化引擎
    ▼
Canon (system_anchor)
    │  去重 → 冲突检测 → 写入 rules/
    ▼
Guard 下一轮拦截使用更新后的规则
```

---

## 安装

```bash
npx skills add mnemonic --yes --global
```
