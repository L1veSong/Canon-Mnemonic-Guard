# 增强包调研报告

对 hermes-canon-mnemonic-guard 推荐配套 Skill 的完整评估记录。

---

## 通过（6 个）— 零配置，npx skills add 一键安装

| Skill | 归属线路 | 安装命令 | 协同方式 |
|-------|---------|---------|---------|
| `obsidian` | 典则线 | `npx skills add obsidian --yes --global` | rules/*.md 原生可视化 |
| `ralph-loop` | 护栏线 | `npx skills add ralph-loop --yes --global` | 拦截后闭环验证 |
| `verification-before-completion` | 护栏线 | 已内置 | Guard coding.yaml 引用 |
| `diagnose` | 护栏线 | 已内置 | 高频拦截→根因分析 |
| `karpathy-coding-guidelines` | 行为准则 | `npx skills add karpathy-coding-guidelines --yes --global` | 攻守兼备 |
| `memory` (Hermes 内置) | 内置 | 无需安装 | 扫盘提取已接入 |

---

## 否决（8 个）— 原因记录

### 非 SKILL.md skill（无法 npx skills add）

| Skill | 类型 | 否决理由 |
|-------|------|---------|
| **MemPalace** | Python CLI + ChromaDB | pip install + mempalace init + 300MB 嵌入模型 + 独立进程。52k stars 但完全不是 skill 形态 |
| **agentmemory (rohitg00)** | TypeScript 服务器 | 需 Node.js >= 20 + npx 启动独立服务 + Docker。14k stars 但非零配置 |
| **MemSkill (ViktorAxelsen)** | PyTorch 训练框架 | arXiv 学术论文，需 GPU + 数据集 + PPO 训练。482 stars，完全不属于 Hermes skill 生态 |

### MemoryProvider 插件（需改 Hermes 核心配置）

| Skill | 否决理由 |
|-------|---------|
| **echomind_memory.skill** | cp -r 到插件目录 + hermes config set memory.provider + Python 服务常驻。非标准 skill，配置侵入 |
| **hermes-memory-installer** | git clone + python setup.py install + systemctl + .env。名字叫"一键安装器"但自己需要四步手动配置 |

### MCP 服务器依赖

| Skill | 否决理由 |
|-------|---------|
| **basic-memory-skills** | 依赖 Basic Memory MCP 服务器，需要先部署 MCP 后端 |

### 不存在

| Skill | 否决理由 |
|-------|---------|
| **Diamond Memory** | 不存在于任何 AI agent skill 仓库。仅有一家硬件内存条公司叫这个名字 |
| **skill.guard** | Hermes 内置安全扫描器（tools/skills_guard.py），非用户可安装 skill |

---

## 评估标准

所有推荐必须同时满足：

1. **SKILL.md 标准格式** — 可通过 `npx skills add` 安装
2. **零配置** — 安装后无需手动编辑配置文件、启动服务、设置环境变量
3. **Hermes 原生兼容** — 在 Hermes Agent 中直接可用，不依赖 Claude Code 特有功能
4. **稳定可靠** — 有维护记录，非一次性实验项目
5. **协同明确** — 与 Canon/Guard 有清晰的互补关系，非功能完全重叠

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-05-21 | 初版：评估 14 个候选，6 通过、8 否决。三线分列推荐表 |
