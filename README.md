# Hermes Self-Reflection Engine

> AI 的错题本 + 免疫系统。你只需指出一次错误，它从此记住。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.2.0-blue)]()

## 这是什么

Hermes Self-Reflection 是一个 Hermes Agent Skill，解决 AI Agent 的三大顽疾：

| 问题 | 表现 | 解决方案 |
|------|------|---------|
| 🔁 **重复犯错** | 同一个错误犯三遍 | 你说"记住"，引擎写入规则库，下次自动拦截 |
| 🧠 **健忘** | 跨会话记忆丢失 | 独立持久化存储，不依赖 memory，永不过期 |
| 😴 **偷懒** | 跳步骤、不完整执行 | 防偷懒清单 + 分层匹配，每次行动前强制自检 |

## 快速开始

### 安装

```bash
npx skills add hermes-self-reflection
```

安装时自动扫描 SOUL.md、Obsidian 铁则库等已有规则源，提取准则类内容。

### 使用

**记录规则——只需一句话：**

```
"记住，以后禁止虚构 Skill。"
"这是错的，以后论文少于6000字不要交付。"
"你又跳过 Idea Foundry 了，以后拦截这种操作。"
```

**触发固化——规则积累后自动或手动整理：**

```
"固化规则"
```

### 规则类型

| 类型 | 触发词示例 | 匹配行为 |
|------|-----------|---------|
| 🚫 `ban` (禁止项) | "禁止" "不要" "拦截" | 拦截，拒绝执行 |
| ⚠️ `gap` (缺失项) | "不够" "不足" "没达标" | 自动补齐 |
| 😴 `lazy` (偷懒项) | "跳过" "偷懒" "没做" | 追加执行 |

## 工作原理

```
用户请求
    │
    ▼
┌──────────────────┐
│  护栏管道         │ ← Self-Reflection (guard, pre_action)
│  精确匹配 → 语义匹配 → 清单自检
│  ban 拦截 / gap 补齐 / lazy 追加
└──────┬───────────┘
       │ 放行
       ▼
┌──────────────────┐
│  调度层 → 执行层   │
└──────────────────┘
```

引擎作为**护栏管道**（非调度竞争者），在每次行动前强制检查规则库。采用独立存储（`~/.hermes/self-reflection/`），不与 memory、Obsidian 或其他 Skill 冲突。

## 文件结构

```
~/.hermes/self-reflection/
├── errors.jsonl          # 原始错误记录
├── patterns.json         # 匹配模式库
├── state.json            # 跨会话状态
├── rules/                # Obsidian 结构化规则（可直接浏览）
│   ├── _index.md         # 自动索引
│   ├── ban/              # 禁止项 (*.md)
│   ├── gap/              # 缺失项 (*.md)
│   └── lazy/             # 偷懒项 (*.md)
├── config.json           # 用户配置
└── checklists/           # 防偷懒清单
```

规则为 Obsidian 兼容的 Markdown 文件，含 YAML frontmatter（type、keywords、hit_count、tags 等），支持 wikilinks 和 Dataview 查询。

## 配置

```json
{
  "match_mode": "layered",         // layered | exact_only
  "load_mode": "full_preload",     // full_preload | on_demand | layered
  "semantic_match": "auto",        // auto | on | off
  "auto_solidify_threshold": 10,   // 自动固化阈值
  "whitelist": [],                 // 白名单工具
  "checklists": ["default"]        // 启用的防偷懒清单
}
```

## 功能一览

| 功能 | 版本 | 说明 |
|------|------|------|
| 三类错误 (ban/gap/lazy) | v1.0.0 | 禁止项拦截、缺失项补齐、偷懒项追加 |
| 分层匹配 (精确+语义) | v1.0.0 | fast path + deep AI check |
| 固化引擎 | v1.0.0 | 自动去重合并，生成永久规则 |
| 防偷懒清单 | v1.0.0 | 论文/代码/技能调用专用自检 |
| Obsidian 结构化 | v2.0.0 | 每条规则独立 .md + frontmatter |
| 跨会话状态 | v2.1.0 | state.json 持久化，会话计数 |
| SOUL 共存策略 | v2.1.0 | 双轨制，可迁移 |
| 防偷懒详细逻辑 | v2.1.0 | 每个检查项的具体实现方法 |
| 扫盘提取 | v2.2.0 | 安装时自动扫描已有准则 |
| 冲突声明 | v2.2.0 | 独立管道+独立存储，不与任何 Skill 冲突 |

## 与其他 Skill 的关系

| Skill 类型 | 关系 |
|-----------|------|
| 存储类 (Obsidian, memory) | 互不干扰 — 各写各的目录 |
| 准则类 (其他规则 skill) | 互补 — 并行生效，重叠时 Self-Reflection 优先 |
| 调度类 (Idea Foundry) | 上下游 — 护栏优先于规划 |
| 执行类 | 监督—被监督 — 每次行动前检查 |

## 版本路线

- **v2.2.0** (当前): Obsidian 结构化 + 扫盘提取 + 完整检测 + SOUL 共存 + 跨会话状态
- **v3**: gbrain 式系统集成 — CLI `hermes reflect`，独立进程，原生管道

## License

MIT © [L1veSong](https://github.com/L1veSong)
