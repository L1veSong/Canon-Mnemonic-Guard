---
name: hermes-self-reflection
description: 自省引擎 — Hermes 错题本+免疫系统。用户指出一次错误，永久生效。每次行动前自动检索规则库，拦截违规行为。
version: 2.2.0
role: guard
stage: pre_action
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
---

# Hermes 自省引擎 v2.2.0

> **角色**: guard (护栏管道) | **阶段**: pre_action (每次行动前) | **位置**: 在所有执行之前
>
> v2.2.0: + 扫盘提取 (安装时自动扫描已有准则) | 不与存储/记忆类 Skill 冲突 (独立管道+独立存储)

---

## 版本变更

| 版本 | 变更 |
|------|------|
| v2.2.0 | + 扫盘提取: 安装时自动扫描 SOUL.md/Obsidian/memory 中的准则类内容 |
| v2.1.0 | + 遗漏4: 防偷懒检测详细逻辑 / + 遗漏5: SOUL 共存策略 / + 遗漏6: 跨会话状态管理 |
| v2.0.0 | Obsidian 结构化: rules/ 独立 .md + frontmatter + `_index.md`。rules.permanent.md deprecated |
| v1.0.0 | 初始版本: 单文件 rules.permanent.md，核心拦截/固化逻辑 |

---

## 文件结构 (v2.0.0+)

```
~/.hermes/self-reflection/
├── errors.jsonl              # 原始错误记录 (永久追加)
├── patterns.json             # 匹配模式库 (去重压缩)
├── state.json                # 跨会话状态 (v2.1.0 新增)
├── rules.permanent.md        # [deprecated] v1 兼容，不再主动生成
├── rules/                    # [v2.0.0] Obsidian 结构化规则目录
│   ├── _index.md             # 自动索引 + wikilinks 表格
│   ├── ban/                  # 禁止项
│   │   └── 规则文件名.md      # 每条规则独立 .md，含 frontmatter
│   ├── gap/                  # 缺失项
│   └── lazy/                 # 偷懒项
├── config.json               # 用户配置
└── checklists/               # 防偷懒清单
    ├── default.yaml
    ├── essay.yaml
    ├── coding.yaml
    └── skill-call.yaml
```

### 规则 .md frontmatter 规范

每条规则文件包含 YAML frontmatter:

```yaml
---
type: ban | gap | lazy
id: rule_xxx
date: 2026-05-19
last_triggered: 2026-05-20
hit_count: 3
false_positives: 0
source_ids: [err_001, err_007]
keywords: [关键词1, 关键词2]
tags: [分类标签]
---
```

直接可在 Obsidian 中浏览——wikilinks ([[规则名]]) 支持、Dataview 查询支持、图谱链接支持。

---

## 启动时（Skill 加载）

### 1. 加载配置

读取 `~/.hermes/self-reflection/config.json`。如不存在，使用默认值。

### 2. 加载规则库 (v2.0.0: 优先 rules/ 目录)

**加载优先级:**
1. 如果 `rules/` 目录存在且有内容 → 加载 rules/ 目录
2. 否则 → 降级加载 `rules.permanent.md`（v1 兼容）

**rules/ 目录加载流程:**
- 读取 `rules/_index.md` → 获取规则总览
- 遍历 `rules/ban/` `rules/gap/` `rules/lazy/` 下的所有 .md 文件
- 解析每个文件的 YAML frontmatter → 提取 type, keywords, tags
- 将 frontmatter 摘要注入系统提示

**注入格式:**
```
═══════════════════════════════════════
自省引擎 v2.1.0 · 永久规则 (自动注入)
═══════════════════════════════════════
[从 rules/_index.md 的表格 + 各规则的 frontmatter 摘要]
═══════════════════════════════════════
```

加载模式行为：

| 模式 | 注入内容 |
|------|---------|
| `full_preload` | 所有规则 frontmatter 全文 |
| `on_demand` | 仅 `_index.md` 表格 |
| `layered` | ban 规则全文 + gap/lazy 摘要 |

### 3. 加载跨会话状态 (v2.1.0 新增)

读取 `~/.hermes/self-reflection/state.json`:
```json
{
  "last_solidify_at": "ISO8601",
  "errors_since_solidify": 5,
  "sessions_since_start": 12,
  "last_activation": "ISO8601"
}
```

- `errors_since_solidify`: 上次固化后 errors.jsonl 新增行数。跨会话持久化，不依赖 Skill 加载时实时统计。
- `sessions_since_start`: 安装后的会话计数。
- 每次 Skill 加载时 `sessions_since_start += 1`。

### 4. 检查固化阈值

比较 `state.json` 中的 `errors_since_solidify` 与 `auto_solidify_threshold`。

### 5. 加载防偷懒清单

读取 `checklists/` 下 `config.json` 中启用的 YAML 文件。

### 6. 输出激活状态

**必须输出**: "自省引擎 v2.1.0 已激活。X 条禁止 / Y 条缺失 / Z 条偷懒。上次固化: {日期}。跨会话 # {N}。"

---

## 用户指出错误时（「记住」触发）

触发词不变（同 v1.0.0），执行流程新增：

### Step 4.5: 更新 state.json (v2.1.0)

追加 errors.jsonl 后:
```
state.errors_since_solidify += 1
```

---

## 每次行动前（拦截检查）

规则匹配逻辑不变（精确匹配 → 语义匹配 → 清单自检），但 v2.1.0 新增:

### 防偷懒清单检测详细机制 (遗漏点 4)

之前只在清单里写了"check: xxx"，v2.1.0 补上具体检测逻辑:

**`load_skills` 检查:**
```
当前任务文本 → 提取领域关键词 (如 "论文"→学术, "代码"→开发, "金融"→数据)
→ 扫描 skills_list 输出 → 匹配领域 Skill
→ 检查是否已通过 skill_view 加载
→ 如果 0 个匹配 Skill 已加载 → 触发 action_on_fail
```

**`ban_check` 检查:**
```
当前思考文本 → 逐条比对 patterns.json 中所有 ban keywords
→ 命中 → 触发拦截
→ 未命中 → 通过
```

**`no_fabrication` 检查:**
```
当前输出文本 → 识别"声称型语句" (我能/我有/我会/已经创建了/存在...)
→ 每一条声称 → 核实:
  - 声称 Skill → 查 skills_list
  - 声称 API → 查 web_search 或 memory
  - 声称数据 → 查 source
→ 有 1 条无法核实 → 触发 action_on_fail
```

**`complete_steps` 检查:**
```
用户原始指令 → 拆解为步骤列表
→ 已完成步骤 → 从上下文提取
→ 未完成步骤 → 触发 action_on_fail (追加执行)
```

**`use_clarify` 检查:**
```
当前步骤 ≥ 2 个可选项 且 需要用户决策
→ 检查是否已调用 clarify
→ 未调用 → 触发 action_on_fail
```

---

## 与现有 SOUL.md 铁则共存策略 (遗漏点 5)

### 共存模式

```
自省引擎的 rules/ 目录  ≠  SOUL.md 铁则
     ↓                        ↓
  结构化、可检索           纯文本、手动编辑
  自省引擎维护             用户手动维护
```

### 优先级

```
合并注入到系统提示:
  1. SOUL.md (用户元规则)
  2. rules/ 目录 (自省引擎规则)  ← 追加在 SOUL.md 之后
  3. Skill 指令
```

**冲突处理:**
- 如果 SOUL.md 和自省引擎对同一行为有不同规则 → 自省引擎规则优先（因为是更新的、用户明确记录的）
- 如果自省引擎检测到 SOUL.md 中已有类似规则 → 提示用户 "SOUL.md 中已有类似规则，是否迁移到自省引擎？"
- 两种规则都生效，重叠时自省引擎拦截

### 迁移辅助 (v2.1.0)

用户说 "迁移铁则" → 自省引擎:
1. 读取 SOUL.md → 解析规则块 → 逐条判断是 ban/gap/lazy
2. 对每条规则 → 确认是否迁移 → 写入 rules/ 目录
3. 标记 SOUL.md 中已迁移的规则（不删除，加注释 `# [已迁移到自省引擎]`）

---

## 扫盘提取 (v2.2.0)

### 定位

自省引擎**不是存储类 Skill**。它只写禁止和准则，不写普通记忆/对话/日志。扫盘提取是这个定位的体现——从已有系统中提取「准则类」内容，滤掉存储类噪音。

### 触发时机

1. **初次安装时** — 自动执行，作为安装流程的第 4.5 步
2. **用户说「扫盘」/「扫描规则」/「提取准则」/「从铁则导入」** — 手动触发

### 扫描源

| 源 | 路径 | 提取条件 |
|----|------|---------|
| SOUL.md | Hermes 系统提示 | 提取所有规则块（非闲聊、非偏好） |
| Obsidian 铁则库 | `~/obsidian/🔒 HERMES-全局铁则库/` | 所有 .md 文件全文 |
| Memory 约束条目 | Hermes memory store | 搜索 "禁止/不要/必须/规则/铁则/约束" |
| 其他 Skill 约束 | skills_list → 扫描含 <HARD-GATE> / "禁止" / "必须" 的段落 | 提取 HARD-GATE 和禁令块 |

### 过滤规则 — 只留「准则类」

```
准则类 (提取)                    非准则类 (跳过)
─────────────────────────────────────────────
包含「禁止」/「不许」/「不能」       纯偏好 (我喜欢/我不喜欢)
包含「必须」/「强制」/「硬性」       闲聊/对话记录
包含「规则」/「约束」/「铁则」       临时 TODO/进度记录
包含 <HARD-GATE> 或类似标记          日志/流水
结构化列表 (1. 2. 3.)               纯事实陈述 (OS 版本、路径等)
明确的行为指令                       

判定方法:
  1. 关键词匹配 (快筛)
  2. 结构检测 (列表/编号/粗体标题 → 更像准则)
  3. AI 二次确认 (不确定时)
```

### 执行流程

#### Step 1: 扫描各源

```
SOUL.md → 读取全文 → 按段落拆分 → 过滤准则类
Obsidian → 遍历 🔒 HERMES-全局铁则库/*.md → 过滤准则类
Memory → 搜索关键词 → 过滤准则类
Skill → 遍历 skill_view → 提取 HARD-GATE 和禁令块
```

#### Step 2: 逐条展示 + 用户确认

对每条提取到的准则:

```
发现准则 [{序号}/{总数}]:
  来源: {SOUL.md / Obsidian / ...}
  内容: "{准则原文}"
  推断类型: [{ban}禁止项 / {gap}缺失项 / {lazy}偷懒项]
  
  导入? [Y] 确认 [N] 跳过 [E] 编辑后导入 [A] 全部确认 [Q] 停止扫盘
```

#### Step 3: 写入 rules/ 目录

确认导入的准则:
- 生成独立 .md 文件 (含 frontmatter)
- type 由内容推断 + 用户确认
- 更新 `rules/_index.md`
- source 标记为 `disk_scan` (区别于用户手动「记住」)

#### Step 4: 反馈

输出: "扫盘完成。扫描 {N} 个源 → 发现 {M} 条准则 → 确认导入 {K} 条。已写入 rules/ 目录。"

### 跳过重复

如果扫盘发现的准则与 rules/ 中已有规则内容相同 → 自动跳过，提示 "(已存在)"。

### 扫盘后的清理

不删除源文件。规则同时存在于源（SOUL.md/Obsidian）和 rules/ 目录。用户可自行决定是否清理源文件。用「迁移铁则」命令可自动标记源中已导入的准则。

---

## 固化引擎 (v2.0.0 更新)

### 生成 rules/ 目录而非单文件

触发条件不变。执行流程更新:

#### Step 1: 读取原始记录
同 v1.0.0。

#### Step 2: 去重合并
同 v1.0.0。

#### Step 3: 生成 rules/ 目录结构

为每条规则生成独立 .md 文件:
```
rules/
├── ban/
│   ├── 禁止虚构skill.md
│   └── 禁止跳步骤交付.md
├── gap/
│   └── 论文字数检查.md
└── lazy/
    └── 必须触发Idea-Foundry.md
```

每个 .md 文件包含完整 frontmatter + 规则描述 + 触发场景 + 拦截行为。

#### Step 4: 生成 _index.md

- 遍历 rules/ 目录生成 wikilinks 表格
- 统计各类型数量

#### Step 5: 更新 state.json

```
state.last_solidify_at = now()
state.errors_since_solidify = 0
```

#### Step 6: 更新 patterns.json (同 v1.0.0)

#### Step 7: 反馈统计

输出: "固化完成。N 条原始记录 → M 条永久规则。已写入 rules/ 目录，可直接在 Obsidian 中浏览。"

---

## 跨会话状态管理 (遗漏点 6)

### 问题

v1.0.0 缺乏跨会话状态：
- errors.jsonl 新增统计在 Skill 加载时计算 → 如果 errors.jsonl 很大，每次都要全量扫描
- `auto_solidify_threshold` 依赖实时统计 → 不知道"上次固化后加了多少条"

### 解决方案: state.json

```json
{
  "version": "2.1.0",
  "created_at": "2026-05-19T00:00:00Z",
  "last_modified": "2026-05-19T18:30:00Z",
  "last_solidify_at": "2026-05-19T12:00:00Z",
  "errors_since_solidify": 5,
  "total_errors": 23,
  "total_rules": 8,
  "sessions_since_start": 12,
  "last_activation": "2026-05-19T18:30:00Z",
  "engine_health": {
    "load_failures": 0,
    "intercept_count": 3,
    "false_positive_count": 1
  }
}
```

### 更新时机

| 事件 | 更新字段 |
|------|---------|
| Skill 加载 | `sessions_since_start += 1`, `last_activation = now()` |
| 用户「记住」 | `errors_since_solidify += 1`, `total_errors += 1` |
| 固化完成 | `last_solidify_at = now()`, `errors_since_solidify = 0`, `total_rules = count(rules/)` |
| 拦截发生 | `engine_health.intercept_count += 1` |
| 误报 | `engine_health.false_positive_count += 1` |
| 加载失败 | `engine_health.load_failures += 1` |

### 数据一致性

- Skill 加载时立即写入 `last_activation` → 即使会话中崩溃也有记录
- `errors_since_solidify` 在每次追加 errors.jsonl 后立即更新 → 不依赖最终统计
- 如果 state.json 损坏 → 回退到扫描 errors.jsonl 计算

---

## 异常处理 & 降级 (同 v1.0.0 + 新增)

| 场景 | 处理 |
|------|------|
| state.json 损坏 | 回退扫描 errors.jsonl，重建 state |
| rules/ 目录和 rules.permanent.md 都不存在 | 规则库为空，默认放行 |
| rules/ 目录存在但为空 | 同"规则库为空" |
| Obsidian 不可用 | 不影响——规则 .md 文件任何编辑器都能读 |

---

## 安装 (v2.0.0 更新)

安装时额外:
- 创建 `rules/ban/` `rules/gap/` `rules/lazy/` 空目录
- 生成初始 `rules/_index.md`（"暂无规则"）
- 初始化 `state.json`

---

## 自保机制（元规则，不可修改）

同 v1.0.0。v2.1.0 新增:
5. state.json 写入失败不阻塞引擎加载

---

## 与其他 Skill 的冲突声明 (v2.2.0)

### 不会冲突

自省引擎采用**独立管道 + 独立存储**：

- **管道模式**: stage=pre_action，在管道中执行，不参与 skill 调度竞争
- **独立存储**: 只写 `~/.hermes/self-reflection/` 下的 rules/ 目录和 state.json
- **不做通用存储**: 不写 Obsidian、不写 memory、不写其他 skill 目录

### 与各类 Skill 的关系

| Skill 类型 | 关系 | 说明 |
|-----------|------|------|
| 存储类 (Obsidian, memory) | 互不干扰 | 各写各的目录，读取只做扫盘提取 |
| 记忆/准则类 (铁则库, 其他规则 skill) | 互补 | 并行生效，重叠时自省引擎优先 |
| 调度类 (Idea Foundry) | 上—下游 | 自省引擎在调度之前执行（护栏优先于规划） |
| 执行类 (其他所有) | 监督—被监督 | 每次行动前检查，不修改被监督 skill 的行为 |

---

## 版本路线

- **v2.2.0** (当前): Obsidian 结构化 + 扫盘提取 + 完整检测逻辑 + SOUL 共存 + 跨会话状态
- **v3**: gbrain 式系统集成 — CLI `hermes reflect`，独立进程，原生管道
