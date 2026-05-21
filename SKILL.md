---
name: mnemonic
description: 三省引擎(CMG)忆存线 (Mnemonic) — 状态记忆层。读取 Guard 拦截日志，自动识别高频错误模式，生成规则草稿推送至 Canon 固化引擎。纯记忆状态层，不生产规则不执行拦截。
version: 3.1.0
role: memory
stage: background
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
---

# Mnemonic 忆存线 v3.1.0

> **角色**: memory (状态记忆层) | **阶段**: background (后台常驻) | **位置**: Guard 之后，Canon 之前
>
> 读取 Guard 的 intercept_log.jsonl 和 state.json，自动识别高频错误模式，推送规则草稿至 Canon 固化引擎。不生产规则、不执行拦截。

---

## 文件结构

```
~/.hermes/self-reflection/
├── intercept_log.jsonl      # 拦截日志 (Guard 写入，Mnemonic 读取)
├── state.json               # 跨会话状态 (Mnemonic 维护)
├── errors.jsonl             # 原始错误记录 (Canon 写入，Mnemonic 读取)
├── rules/                   # 规则库 (Canon 生产)
└── config.json              # 用户配置
```

---

## 启动时（Skill 加载）

### 1. 读取 Guard 拦截日志

加载 `~/.hermes/self-reflection/intercept_log.jsonl`，统计最近 7 天拦截事件。按关键词分组，计算出现频次。

### 2. 读取状态

加载 `~/.hermes/self-reflection/state.json`，获取会话计数和引擎健康指标。

### 3. 输出激活状态

**必须输出**: "Mnemonic v3.0.0 已激活。近 7 天拦截 {N} 次。模式识别: {on/off}。"

---

## 自动模式识别

### 触发条件

同一关键词在 `intercept_log.jsonl` 中 7 天内出现 ≥ 3 次。

### 识别流程

```
1. 遍历 intercept_log.jsonl → 按 rule_id + interceptor 分组
2. 统计每组频次 → 筛选 ≥3 次的模式
3. 与 rules/ 已固化规则去重 → 排除已覆盖的
4. 生成规则草稿 → clarify 提醒用户确认
5. 用户确认 → 推送至 Canon 固化引擎
```

### 规则草稿格式

```json
{
  "ts": "ISO8601",
  "type": "ban",
  "rule": "自动识别: 高频违规XXX",
  "context": "近7天触发3次，拦截器: BanInterceptor",
  "match": {
    "exact": ["关键词1", "关键词2"],
    "semantic": "语义描述"
  },
  "source": "mnemonic_pattern"
}
```

### 推送至典则线

草稿不直接写入 rules/，而是通过标准化接口推送至 Canon 固化引擎。Canon 负责去重、分类、冲突检测、写入。

### 误报率自适应

同一模式误报率高时自动降低匹配置信度，减少不必要的 clarify 弹窗。

---

## CLI 命令

| 命令 | 说明 |
|------|------|
| `hermes reflect status` | 查看规则库状态（总数/分类/最近固化时间） |
| `hermes reflect add "规则"` | 手动添加规则 |
| `hermes reflect scan` | 手动触发扫盘 |
| `hermes reflect patterns` | 查看当前识别到的高频模式 |

---

## 与 Canon / Guard 联动

```
Guard (pre_action)
    │  写入 intercept_log.jsonl
    ▼
Mnemonic (background)
    │  读取拦截日志 → 模式识别 → 生成草稿
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
