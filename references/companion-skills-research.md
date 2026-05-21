# 增强包调研报告

对 canon-mnemonic-guard 推荐配套 Skill 的完整评估记录。

---

## 评估标准（v2.2.9 修订）

**核心标准：CMG 能否自动感知并调用。** 第三方 skill 的安装难度与 CMG 无关——用户自己负责装上。CMG 只关心：装完后能不能自动识别、零适配调用。

| 维度 | 标准 | 权重 |
|------|------|------|
| 自动感知 | 标准安装后，CMG 无需额外配置即可发现该 skill | 40% |
| 零适配调用 | CMG 的 checklist/扫盘/拦截逻辑可直接触发该 skill | 40% |
| 互补非重叠 | 该 skill 提供 CMG 不具备的能力，非功能重复 | 20% |

> **与旧标准的区别：** 旧标准要求第三方 skill 必须 `npx skills add` 一键安装。新标准不关心第三方安装方式——那是用户的事。只要 CMG 装上后能自动感知调用，就合格。

---

## 通过（8 个）— 对 CMG 有明确增强

| 推荐 | 类型 | 增强点 | CMG 写入第三方？ | 第三方行为被修改？ |
|------|------|--------|:---:|:---:|
| `idea-foundry` | Skill | CMG 规则集注入 IF 代码生成阶段 | ❌ | ❌ |
| `ralph-loop` | Skill | 执行闭环 | ❌ | ❌ |
| `verification-before-completion` | Skill | 证据先于断言 | ❌ | ❌ |
| `diagnose` | Skill | 根因调试 | ❌ | ❌ |
| `rtk-hermes` | Hermes 插件 | 压缩 token 60-90% | ❌ | ❌ |
| `plur` | MCP 服务器 | 扩展规则来源（v2.3.0） | ❌ | ❌ |
| `obsidian` | Skill | rules/ 可视化 | ❌ | ❌ |
| `karpathy-coding-guidelines` | Skill | 行为准则 | ❌ | ❌ |
| `memory` (Hermes 内置) | 内置 | 跨会话记忆 | ❌ | ❌ |

**集成模式：全部添加式（CMG 只读，第三方完全不受影响）**

### 新增：调度联动

Idea Foundry 作为 CMG 的调度联动伙伴，在 IF 的 Phase -3 开启「启用 CMG 规则集」后，CMG 的 rules/ 目录作为只读约束源注入到 IF 的代码生成阶段。CMG 不修改 IF 的行为，IF 也不修改 CMG 的数据——纯粹的消费关系。

---

## pending（v2.3.0 后可配置源接入）

| Skill | 类型 | v2.3.0 后 |
|-------|------|----------|
| **plur** (plur-ai/plur) | TypeScript MCP 服务器 | 用户配置 `custom: [{path: "~/.plur/", pattern: "*.yaml"}]` → CMG 扫盘可读 plur 记忆 → 固化为规则。与 Hermes 内置 memory 无冲突（独立 MCP 进程，独立存储路径）。CMG 已覆盖其核心功能（错误记忆+去重固化）。ACT-R 衰减模型有参考价值 |

---

## 否决（9 个）

### CMG 无法自动感知 / 无调用接口

| Skill | 类型 | 否决理由 |
|-------|------|---------|
| **MemPalace** | Python CLI + ChromaDB | 独立向量数据库，CMG 无调用接口 |
| **agentmemory** | TypeScript 服务器 + Docker | 独立服务，CMG 无调用接口 |
| **MemSkill** | PyTorch 训练框架 | 学术论文，非用户工具 |
| **CLI-Anything** | Python 方法论工具包 | 开发工具包，CMG 无调用接口。可独立使用但与 CMG 无联动 |
| **mano-p** | GUI 视觉模型 | 需独立部署模型服务，CMG 无法调用 |
| **shotgun_code** | Go+Vue 桌面应用 | 需编译的桌面应用，CMG 无法调用 |

### 其他

| Skill | 否决理由 |
|-------|---------|
| **echomind_memory.skill** | MemoryProvider 插件，非标准 skill |
| **hermes-memory-installer** | 多步手动配置，非标准 skill |
| **basic-memory-skills** | MCP 服务器依赖 |
| **Diamond Memory** | 不存在 |
| **skill.guard** | Hermes 内置安全扫描器 |

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-05-21 | v2.3.2: 新增 idea-foundry 调度联动推荐。IF Phase -3 可读取 CMG rules/ 作为约束源 |
| 2026-05-21 | 初版：评估 14 个候选，8 通过、6 否决。三线分列推荐表 |
| 2026-05-21 | 初版：评估 14 个候选，6 通过、8 否决 |
