# Changelog

All notable changes to Hermes Canon Mnemonic Guard (原 hermes-self-reflection).

---

## [2.2.7] — 2026-05-20

### Added
- v5.0.0 外观模式设计决策：主角色 `guard` + 内部子角色 `producer/memory/guard`
- 多角色声明方案否决分析：内部架构不应泄露为外部契约
- 前向兼容分析：v2.2.x 到 v5.0.0 契约不变
- `references/future-release-plan.md` 独立 Skill 包发布计划
- SKILL.md 新增「常见坑点」章节（4 条维护铁律）

### Changed
- v5.0.0 架构图从三并列改为外观模式分层图

---

## [2.2.6] — 2026-05-20

### Changed
- v5.0.0 三线合一 + 角色制统一：预览图标注每条线 role+stage
- README.md 全面更新：三线架构总览、未来发布计划、独立 Skill 包规划
- SKILL.md frontmatter description 改为典则线定位
- 注入消息和激活消息版本号同步

### Fixed
- 硬编码版本号多处不一致

---

## [2.2.5] — 2026-05-20

### Added
- 三线角色声明制统一规划（Canon producer/anchor, Mnemonic memory/background, Guard guard/pre_action）

---

## [2.2.4] — 2026-05-20

### Changed
- 角色声明制从设计哲学迁至 Guard v4.0.0 未来规划

### Fixed
- 硬编码版本号修正

---

## [2.2.3] — 2026-05-20

### Added
- 角色声明制设计（后续回滚至未来规划）

---

## [2.2.2] — 2026-05-20

### Added
- 设计哲学：彻底解耦·物理拆分·单向依赖
- 三线职责边界严格定义
- v5.0.0 架构预览
- 设计参考（gstack / Ports & Adapters / Microkernel）
- 护栏线 Guard (4.x.x) 完整路线图

---

## [2.2.1] — 2026-05-20

### Added
- 版本路线补全：护栏线 Guard (4.x.x) 路线图
- 三线并行 → v5.0.0 统一引擎规划

---

## [2.2.0] — 2026-05-19

### Added
- 扫盘提取：安装时自动扫描 SOUL.md / Obsidian / memory / 其他 Skill 中的准则类内容
- 推荐配套 Skill 声明（karpathy-coding-guidelines / ralph-loop / obsidian）
- 冲突声明章节

---

## [2.1.0] — 2026-05-19

### Added
- 防偷懒清单检测详细机制（load_skills / ban_check / no_fabrication / complete_steps / use_clarify）
- SOUL 共存策略 —— 双轨制 + 迁移辅助
- 跨会话状态管理 —— state.json + 会话计数 + 引擎健康指标
- 固化阈值自动触发

---

## [2.0.0] — 2026-05-19

### Added
- Obsidian 结构化：rules/ 目录 (ban/ gap/ lazy/)，每条规则独立 .md
- YAML frontmatter 规范（type, id, keywords, hit_count, tags 等）
- _index.md 自动索引 + wikilinks 表格
- 三层加载模式（full_preload / on_demand / layered）

### Changed
- Skill 重命名：`hermes-self-reflection` → `hermes-canon-mnemonic-guard`
- 规则存储从单文件 rules.permanent.md → rules/ 目录

### Deprecated
- rules.permanent.md（保留为降级兼容）

---

## [1.0.0] — 2026-05-18

### 发布名称
`hermes-self-reflection` — Hermes 自省引擎

### 核心功能
- **三类错误系统：** ban（禁止项，拦截）/ gap（缺失项，补齐）/ lazy（偷懒项，追加）
- **分层匹配：** 精确匹配 → 语义匹配 → 清单自检，语义匹配超时 5 秒降级
- **固化引擎：** errors.jsonl → 去重合并 → rules.permanent.md 单文件 + patterns.json
- **防偷懒清单：** default / essay / coding / skill-call 四种 YAML 清单
- **自保机制：** 4 条元规则（启动输出状态、拦截说明原因、空库放行、不改自身文件）
- **误报处理：** 同一规则累积 3 次误报 → 提示调整
- **环境降级：** 大模型完整 → 中等模型启发式 → 小模型仅精确匹配

### 文件结构
```
~/.hermes/self-reflection/
├── errors.jsonl           # 原始错误记录
├── patterns.json          # 匹配模式库
├── rules.permanent.md     # 固化永久规则（单文件）
├── config.json            # 用户配置
└── checklists/            # 防偷懒清单
```

### 版本路线（v1.0.0 原始规划）
- v1.0.0: Skill 形态，单文件 rules.permanent.md
- v2: Obsidian 结构化 — 每条规则独立 .md
- v3: gbrain 式系统集成
