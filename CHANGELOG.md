# Changelog

All notable changes to Canon Mnemonic Guard (原 hermes-self-reflection).

---

## [5.0.0] — 2026-05-21

### 三线合一外观模式

**架构**
- 外观模式统一引擎：对外 `role: guard, stage: pre_action`
- 内部三模块：Canon(规则生产) + Guard(拦截执行) + Mnemonic(模式识别)
- 四模块严格独立互不混合
- 闭环验证：10 拦截→2 草稿→2 固化

**16 条未来方向入库**

---

## [2.4.1] — 2026-05-21

### v2 功能闭环：护栏剥离 + 评分实装 + 角色生效

**护栏剥离**
- 五层拦截逻辑完整迁移至 `references/guard-spec.md`
- Canon 不再直接执行拦截——只生产规则，Guard（v4.0.0）执行拦截
- 过渡期拦截仍可运行但视为「Guard 寄生」

**评分计数器实装**
- 每次拦截命中自动 `hit_count += 1, last_triggered = now()`
- 用户标记误报自动 `false_positives += 1`
- 固化引擎运行时读取计数器计算评分

**角色声明制生效**
- `role: producer, stage: system_anchor` 正式启用
- 头部描述同步更新

---

## [2.4.0] — 2026-05-21

### Phase 2: 规则评分 + 角色声明制 + 工具链完善

**规则效果评分**
- 每条规则跟踪命中率/误报率/最后命中时间/创建日期
- 误报率>30%自动标记「待调整」，180天未命中提示过期
- 固化报告增加规则效果排行（Top 5高频 + Bottom 5低频）
- 与 Guard v4.2.0 双向联动：Canon 输出评分→Guard 调整拦截策略

**角色声明制**
- Canon 以 `role: producer, stage: system_anchor` 声明规则生产锚点
- 废除数字优先级（`priority: 110`），三线统一使用 `role+stage` 声明式协作
- 新 skill 加入只需声明 role+stage，自动归入对应阶段

**工具链完善**
- 简化触发词：`!remember` / `!solidify` / `!scan` / `!export` / `!import`
- 初始化命令：`npx canon-mnemonic-guard init`
- 规则导入/导出：`!export` ZIP打包 / `!import <path>` 外部规则集导入（自动冲突检测）
- config.json 新增 `scoring`、`role`、`commands` 配置段

### Changed
- 典则线版本从 v2.3.2 → v2.4.0
- 激活消息改为：角色: producer / 评分: on/off / 模式: expert/simple

---

## [2.3.2] — 2026-05-21

### Idea Foundry 规则集联动
- CMG rules/ 目录对外暴露为 IF 可消费约束源（`config.json` 的 `if_integration` 字段）
- IF Phase -3 开启「启用 CMG 规则集」后，rules/ 中的 ban 规则作为约束注入到代码生成阶段
- 推荐列表新增「调度联动」分类：`idea-foundry`
- 激活消息新增 `IF联动: {on/off}` 输出

---

## [2.3.1] — 2026-05-21

### 规则冲突检测与裁决
- 新规则写入前自动扫描 rules/ 目录同类型规则（同为 ban/gap/lazy）
- 冲突检测：关键词重叠但行为相反 / 同一场景触发两条不同规则 / 语义矛盾
- 冲突裁决：clarify 四选一（覆盖旧规则 / 保留旧规则 / 都保留标记 / 编辑后写入）
- 自动裁决：明确指定 > 最近使用 > 更严格规则
- 激活消息新增 `冲突裁决: {auto/manual}` 输出

---

## [2.3.0] — 2026-05-21

### 依赖解耦 + 可配置扫描源（前置基建）
- RuleReader 接口 + 7 个适配器：JSONRuleSource / SOULRuleSource / ObsidianRuleSource / MemoryRuleSource / SkillRuleSource / PlurRuleSource / CustomRuleSource
- 适配器按需加载，检测到对应源存在才激活，未装静默跳过
- PlurRuleSource：v2.3.0 新增，读取 `~/.plur/engrams.yaml` 中的纠正经验作为额外规则来源
- 可配置扫描源白名单制：`~/.hermes/self-reflection/config.json` 的 `scan_sources` 字段
- 支持自定义源（OpenClaw、plur 等），用户不配就不扫，绝不全盘扫描

### 模式切换
- expert 模式：每次记录前 clarify 确认，可编辑规则内容后写入（默认）
- simple 模式：自动记录纠正（带「准则类」过滤器）→ 阈值触发固化提示
- 通过 `config.json` 的 `mode` 字段切换
- 激活消息新增 `模式: {expert/simple}` 输出

### Changed
- 可配置扫描源取代硬编码 4 源体系
- 典则线版本从 v2.2.9 → v2.3.0

---

## [2.2.9] — 2026-05-21

### 扫盘提取 + 固化（真实运行数据）
- 首次完整执行扫盘提取：4 个源（SOUL.md / Obsidian 铁则库 / Memory / 其他 Skill）
- 发现 15 条准则 → 自动分类：8 禁止 (ban) / 3 缺失 (gap) / 4 偷懒 (lazy)
- 固化引擎写入 rules/ 目录（每条独立 .md + frontmatter）
- errors.jsonl: 15 条原始记录
- patterns.json: 3 类模式（ban/gap/lazy），39 个关键词
- state.json: 初始化完成（total_errors: 15, total_rules: 15）
- _index.md: wikilinks 索引自动生成

### 典则线 v2.x 功能闭环
- 扫盘提取 → 用户确认 → 固化写入 → 注入系统提示 完整链路验证通过
- 典则线正式达到「设计+实施」双竣工状态
- 下一步：v2.3.0 依赖解耦

---

## [2.2.8] — 2026-05-21

### Added
- 推荐列表三线分列：典则线（obsidian）、护栏线（ralph-loop / verification-before-completion / diagnose）、行为准则（karpathy-coding-guidelines）
- `references/companion-skills-research.md`：14 候选 → 6 通过 → 8 否决的完整调研报告
- 零配置安装标准：所有推荐必须满足 `npx skills add --yes --global` 一键安装

### Fixed
- obsidian 从忆存线归位至典则线（rules/ 目录原生浏览器，由 Canon 生产）

### Changed
- 流水线图改为三线分层架构（典则 → 护栏 → 全栈覆盖）

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
- Skill 重命名：`hermes-self-reflection` → `hermes-canon-mnemonic-guard`（v2.2.9 再精简为 `canon-mnemonic-guard`）
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
