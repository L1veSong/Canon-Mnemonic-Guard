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

**集成模式：全部添加式（CMG 只读，第三方完全不受影响）。准入标准经历关键修正：从「第三方必须零配置安装」→「CMG 能否自动感知并调用」。第三方好不好装与 CMG 无关。**

**三线分列（三省引擎口径）：** 典则线(暂无专属) / 护栏线(ralph-loop, VBC, diagnose) / 成本优化(rtk-hermes) / 规则扩展(plur, v2.3.0) / 跨线共享(obsidian) / 行为准则(karpathy) / 内置(memory)

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
- 教训：必须阅读实际代码/架构再下冲突结论，不可凭名称或分类推断

### 评估标准修正记录

| 问题 | 修正 |
|------|------|
| plur 误判为 MemoryProvider 插件 | 实际是 TypeScript MCP 服务器，独立进程，数据存 `~/.plur/` |
| rtk-hermes 集成方式 | 被动受益——压缩所有输出，CMG 自然省 token |

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-05-22 | rtk-hermes+plur 最终结论；plur 误判修正 |
| 2026-05-21 | 初版：14候选，8通过/6否决 |
| 形态 | Hermes 插件 | 独立 CLI 代理 |
| 安装 | `pip3 install rtk-hermes` | `cargo install rtk` |
| 集成 | 直接嵌入 Hermes 管道 | 命令行包裹 `rtk cargo build ...` |
| 省 token | 60-90% | 60-90% |
| 关系 | 同一团队产品（作者邮箱含 rtk-ai） | 核心引擎 |
- 教训：必须阅读实际代码/架构再下冲突结论，不可凭名称或分类推断

### 评估标准修正记录

| 问题 | 修正 |
|------|------|
| plur 误判为 MemoryProvider 插件 | 实际是 TypeScript MCP 服务器，独立进程，数据存 `~/.plur/` |
| rtk-hermes 集成方式 | 被动受益——压缩所有输出，CMG 自然省 token |

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-05-22 | rtk-hermes+plur 最终结论；plur 误判修正 |
| 2026-05-21 | 初版：14候选，8通过/6否决 |
| 2026-05-21 | 初版：评估 14 个候选，6 通过、8 否决。三线分列推荐表 |
| 2026-05-21 | v2.3.2: 新增 idea-foundry 调度联动推荐。IF Phase -3 可读取 CMG rules/ 作为约束源 |
| 2026-05-21 | 初版：评估 14 个候选，8 通过、6 否决 |

---

## 维护坑点

### 不可凭类型推断冲突

分析第三方工具是否与 CMG 冲突时，**必须阅读实际代码/架构**，不可凭名称或分类推断。

- ❌ 误判：plur 是 MemoryProvider 插件 → 会拦截 Hermes memory → CMG 扫盘读脏数据
- ✅ 实际：plur 是 TypeScript MCP 服务器，独立进程，`~/.plur/` 隔离存储，CMG 扫盘默认不扫该路径
- 教训：名称和类型推断不可靠，必须看实际架构
