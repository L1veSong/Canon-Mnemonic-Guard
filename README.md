# Canon Mnemonic Guard — 典则线 v2.3.0

> AI 的错题本 + 免疫系统。你只需指出一次错误，它从此记住。
>
> **当前状态：** 仅典则线 (Canon v2.x) 已发布为独立 Skill。忆存线 (Mnemonic v3.x) 和护栏线 (Guard v4.x) 仍在规划中。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.3.1-blue)]()

---

## 这是什么

**典则线 (Canon)** 是自省引擎的规则生产模块。它负责规则的来源、固化、存储和效果评分。

三大核心能力：

| 能力 | 说明 |
|------|------|
| 🔁 **错题记忆** | 你说"记住"，引擎写入 errors.jsonl，自动去重合并为永久规则 |
| 🧠 **跨会话持久化** | 独立存储 (`~/.hermes/self-reflection/`)，不依赖 Hermes memory，永不过期 |
| 📊 **规则评分** | 跟踪每条规则的命中率/误报率，自动标记需调整的规则 |

---

## 三线架构总览

```
┌─────────────────────────────────────────────────┐
│              自省引擎 · 三线架构                    │
│                                                   │
│  v2.x 典则 Canon    v3.x 忆存 Mnemonic  v4.x 护栏 Guard
│  ✅ 已发布           📋 规划中            📋 规划中
│  规则生产库          状态记忆层           规则执行器
│  role: producer      role: memory         role: guard
│  stage: anchor       stage: background    stage: pre_action
│                                                   │
│        ↓ 未来合并为 v5.0.0 统一引擎                │
└─────────────────────────────────────────────────┘
```

**未来发布计划（严格独立，互不寄生）：**

| 版本系列 | Skill 包名 | 时机 |
|---------|-----------|------|
| v2.x | `canon` — 典则线独立 Skill | ✅ 当前 |
| v3.x | `mnemonic` — 忆存线独立 Skill | Mnemonic 规划完成时 |
| v4.x | `guard` — 护栏线独立 Skill | Guard 规划完成时 |
| v5.0.0 | `self-reflection-engine` — 三合一统一 Skill | 三条线各自成熟后 |
| | **外观模式：** 对外 `role: guard`，内部子角色保留 | |

> **铁律：** v3 和 v4 发布时必须作为独立 Skill 包，不与典则线混在同一 SKILL.md 中。三条线通过标准化接口联动，非文件寄生。

---

## 快速开始

### 安装

```bash
npx skills add canon-mnemonic-guard
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

| 类型 | 触发词示例 | 行为 |
|------|-----------|------|
| 🚫 `ban` (禁止项) | "禁止" "不要" "拦截" | 拦截，拒绝执行 |
| ⚠️ `gap` (缺失项) | "不够" "不足" "没达标" | 自动补齐 |
| 😴 `lazy` (偷懒项) | "跳过" "偷懒" "没做" | 追加执行 |

---

## 工作原理

```
用户请求
    │
    ▼
┌──────────────────┐
│  护栏管道         │ ← stage: pre_action
│  精确匹配 → 语义匹配 → 清单自检
│  ban 拦截 / gap 补齐 / lazy 追加
└──────┬───────────┘
       │ 放行
       ▼
┌──────────────────┐
│  调度层 → 执行层   │
└──────────────────┘
```

引擎作为**护栏管道**（非调度竞争者），在每次行动前强制检查规则库。采用独立存储，不与 memory、Obsidian 或其他 Skill 冲突。

---

## 文件结构

```
~/.hermes/self-reflection/
├── errors.jsonl          # 原始错误记录
├── patterns.json         # 匹配模式库
├── state.json            # 跨会话状态
├── rules/                # Obsidian 结构化规则
│   ├── _index.md         # 自动索引 + wikilinks
│   ├── ban/              # 禁止项 (*.md)
│   ├── gap/              # 缺失项 (*.md)
│   └── lazy/             # 偷懒项 (*.md)
├── config.json           # 用户配置
└── checklists/           # 防偷懒清单
```

规则为 Obsidian 兼容 Markdown，含 YAML frontmatter，支持 wikilinks 和 Dataview。

---

## 配置

```json
{
  "match_mode": "layered",
  "load_mode": "full_preload",
  "semantic_match": "auto",
  "auto_solidify_threshold": 10,
  "whitelist": [],
  "checklists": ["default"]
}
```

---

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
| 扫盘提取 | v2.2.0 | 安装时自动扫描已有准则 |
| 三线架构规划 | v2.2.x | 典则/忆存/护栏解耦设计 |
| 角色声明制规划 | v2.2.5+ | role+stage 未来替换数字优先级 |

---

## 配套 Skill（推荐，非必需）

| Skill | 分工 | 协同 |
|-------|------|------|
| `karpathy-coding-guidelines` | 进攻型行为准则 | Guard 防守 + Karpathy 进攻 = 攻守兼备 |
| `ralph-loop` | 执行闭环 | Guard 拦截 → Ralph 闭环验证 |
| `obsidian` | 结构化存储 | rules/ 目录 Obsidian 原生兼容 |

---

## 版本路线

详见 [SKILL.md](./SKILL.md) 的「版本路线」章节和 [CHANGELOG.md](./CHANGELOG.md)。

- **典则线 Canon (v2.x):** 规则来源、固化、扫描、效果评分 ← 当前
- **忆存线 Mnemonic (v3.x):** 会话记忆、错误模式、自动草稿 ← 规划中
- **护栏线 Guard (v4.x):** 前置校验、动态清单、拦截效能 ← 规划中
- **统一引擎 (v5.0.0):** 三线合一 + 角色制统一 ← 未来

---

## ☕ 支持作者

如果这个项目对你有帮助，欢迎请我喝杯咖啡。完全自愿。

**🇨🇳 国内**

| 微信 | 支付宝 |
|------|--------|
| <img src="assets/wechat-pay.png" width="180"> | <img src="assets/alipay-pay.png" width="180"> |

**🌍 International**

| Recipient | J Li |
| Bank | ERSTE BANK |
| IBAN | AT41 2011 1845 3888 8800 |
| BIC / SWIFT | GIBAATWWXXX |

---

## 💡 建议与反馈

- 有 Bug？[提交 Issue](https://github.com/L1veSong/Canon-Mnemonic-Guard/issues/new?template=bug_report.md)
- 有想法？[提交 Feature Request](https://github.com/L1veSong/Canon-Mnemonic-Guard/issues/new?template=feature_request.md)

我会认真阅读每一条反馈，择优纳入后续版本迭代。

## License

MIT © [L1veSong](https://github.com/L1veSong)
