---
name: canon-mnemonic-guard
description: 三省引擎 (CMG) — 取自「吾日三省吾身」。v5.5.5 cmg-guard v1.3.0(17hooks+pre_tool_call+自披露闭环)。对外 role:guard stage:pre_action，内部三模块各自独立。
version: 5.5.5
role: guard
dependencies: [canon, guard, mnemonic]
_comment: "v5.5.5 cmg-guard v1.3.0(17hooks+pre_tool_call)。Canon v2.7.2 + Guard v4.8.2 + Mnemonic v3.5.3。skill-autoload v1.0.1 + cmg-guard v1.3.0。"
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
metadata:
  hermes:
    tags: [cmg, facade, orchestration, self-reflection]
    related_skills: [canon, guard, mnemonic]
---

# 三省引擎 (CMG) v5.5.5 — 四包制外观引擎

> **对外身份**: guard (护栏) | **阶段**: pre_action | **中文名**: 三省引擎，取自「吾日三省吾身」
> v5.5.0: +微型调度器 | v5.4.2: M3清零 | v5.4.0: 四大增强 | v5.2.0: 六大功能
>
> v2.2.0: + 扫盘提取 | v5.0.0: 三线合一外观模式 | v5.1.0: 四包制分装 | v5.2.0: 六大功能大更新 | v5.3.0: 典忆卫・闭环校验器 | v5.4.0: 四大增强 | v5.5.0: P2补全 | v5.5.0: M3清零

---

## 版本变更

| 版本 | 变更 |
|------|------|
| v5.5.5 | +cmg-guard v1.3.0(17hooks+pre_tool_call堵SKILL.md未经authoring即改+自披露闭环=断言须附证据) +四名冲突检测 | 当前 |
| v5.5.3 | +双层哨兵(A层正则+B层LLM语义) +init.py自动配置config.yaml +一键卸载 --uninstall +意图识别meta规则 +坑点17:发布打包审计 | |
| v5.5.2 | +默认固化阈值10→3 +修复init.py版本号滞后(跨两个大版本) |
| v5.5.1 | +README更新: 推荐skill-autoload插件自动加载CMG |
| v5.4.2 | +M3清零: !patterns+!datasource。待优化表全部清零。Canon v2.7.1 / Guard v4.8.1 / Mnemonic v3.5.2 |
| v5.4.1 | +P2补全: Guard session_id+Mnemonic联动钩子。Canon v2.7.1 / Guard v4.8.1 / Mnemonic v3.5.1 |
| v5.4.0 | +大更: P1同会话升级+P3用户纠正提升+P4误报降级+上下文保留。Canon v2.7.0 / Guard v4.8.0 / Mnemonic v3.5.0 |
| v5.2.1 | +SOUL 激活机制: init时询问是否写一行 `[CMG v5.3.1]` 到 SOUL.md。扫盘时自动检测标记存在+版本匹配。用户删标记即停用。Canon v2.6.0 |
| v5.2.0 | +C1 定时扫盘(Canon v2.5.1) +G2/G3/G4 动态清单+上下文感知+效能分析(Guard v4.5.0) +M1 数据源降级链(Mnemonic v3.3.0) +E2 协调日志(!log) +E3 一键诊断(!diagnose) +推荐列表自动扫描(!scan-recommendations)。7项功能，四包同步升版。 |
| v5.1.0 | 四包制分装: Canon v2.4.1 + Guard v4.4.0 + Mnemonic v3.2.0 独立Skill包 + CMG外观索引 |
| v2.3.1 | + 规则冲突检测: 写入前扫描同类型规则 / + 冲突裁决: clarify四选一(A保留新/B保留旧/C都留标记/D编辑) / + 自动裁决: 明确指定>最近使用>更严格 |
| v2.3.0 | + 依赖解耦: RuleReader接口+7个适配器(JSON/SOUL/Obsidian/Memory/Skill/Plur/Custom) / + 可配置扫描源(config.json) / + 模式切换(expert/simple) / + PlurRuleSource / + 扫描源白名单制 |
| v2.2.9 | + 首次真实扫盘提取+固化执行(15条/4源/8ban+3gap+4lazy) / + rules/目录+errors.jsonl+patterns.json+state.json全部实装 / 典则线v2.x功能闭环 |
| v2.2.3 | + 角色声明制: 废除数字优先级(priority:110→role+stage) / + 声明式层级替换数字排序 / + 冲突声明表改为stage驱动 / + 流水线图改为stage自然排列 |
| v2.2.2 | + 设计哲学: 彻底解耦·物理拆分·单向依赖 / + 三线职责边界严格定义 / + v5.0.0 架构预览 / + 设计参考（gstack/Ports&Adapters/Microkernel） |
| v2.2.1 | + 版本路线补全: 护栏线 Guard (4.x.x) 路线图，三线并行→v5.0.0 统一引擎 |
| v2.2.0 | + 扫盘提取: 安装时自动扫描 SOUL.md/Obsidian/memory 中的准则类内容 / + 推荐配套 Skill 声明 |
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
三省引擎 v5.5.5 · 永久规则 (自动注入)
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

**必须输出**: "三省引擎 v5.5.5 已激活。X 条禁止 / Y 条缺失 / Z 条偷懒。典则·护栏·忆存。"

**🔴 X/Y/Z 必须从 rules/ 目录实际文件数统计，禁止凭记忆或 state.json 的 total_rules 字段报数。** 统计命令：
```bash
ls ~/.hermes/self-reflection/rules/ban/*.md | wc -l  # X
ls ~/.hermes/self-reflection/rules/gap/*.md | wc -l  # Y
ls ~/.hermes/self-reflection/rules/lazy/*.md | wc -l # Z
```
2026-05-25 实战：将 33/8/9 错报为 10/2/2，用户立刻纠正。state.json 的 `total_rules: 4` 严重滞后——不可信。

**⚠️ 数字必须验证（坑点 13）**：X/Y/Z 不是凭记忆报的数。输出激活消息前，**必须** count rules/ban/ rules/gap/ rules/lazy/ 三个目录的实际文件数。禁止凭记忆张嘴就来——数字错一次就触发用户纠正（2026-05-25：33/8/9 错报为 10/2/2）。

---

## 用户指出错误时（「记住」触发）

**触发条件（意图识别，非关键词匹配）：** 用户任何表达「记录错误行为 + 希望未来避免」的语句都触发——不限于「记住」「记录」。包含但不限于：

- 「这是错的，下次别这样」「你又犯这个了」「别再犯」
- 「readme没更新」「版本号怎么又不对」「不是说了要同步吗」
- 任何隐含「AGAIN? I told you last time」的纠正句式

**切勿将纠正当成单次修复请求。** 必须识别为需永久避免的错误模式，立刻执行三步走：生成规则 → 写入 rules/ → 更新 patterns.json。未执行三步走不得继续。

执行流程：

### Step 4.5: 更新 state.json (v2.1.0)

追加 errors.jsonl 后:
```
state.errors_since_solidify += 1
```

### Step 5: 冲突检测 (v2.3.1)

新规则写入前，扫描 rules/ 目录中同类型规则（同为 ban 或同为 gap 或同为 lazy）。

**检测规则对是否冲突：**

```
1. 关键词重叠但行为相反 → 冲突
   例: 规则A「禁止跳过验证」 vs 规则B「用户说跳过就跳过」
2. 同一场景触发两条不同的 ban 规则 → 需确认优先级
3. 规则语义矛盾（一条强制、一条禁止同一行为） → 冲突
```

**冲突裁决（自动暂停 → clarify）：**

发现冲突时输出：

```
⚠️ 规则冲突检测
  新规则: [{new_rule}] (类型: {type})
  冲突规则: [{existing_rule}] (创建于 {date}, 命中 {hit_count} 次)

  建议: {明确指定优先 > 最近使用优先 > 更严格规则优先}

  A) 保留新规则（覆盖旧规则）
  B) 保留旧规则（丢弃新规则）
  C) 两条都保留，标注冲突（人工裁决标记）
  D) 编辑新规则后再写入
```

**自动裁决（仅当满足条件时）：**
- 新规则明确标注「覆盖旧规则 XXX」→ 自动采用新规则
- 旧规则 180 天未命中 + 新规则来源更可靠（用户明确记住 vs 扫盘提取）→ 自动采用新规则
- 新规则比旧规则更严格（ban 比 lazy 严格）→ 自动提示但仍需确认

### Step 6: 钩子缺口检测 (v5.5.5)

新规则写入后，自动分析此规则是否依赖 cmg-guard 特定钩子才能强制拦截。如果所需钩子未开启，提示用户。

**检测映射表：**

| 规则特征 | 所需钩子 | config.yaml 路径 |
|---------|---------|-----------------|
| 涉及 `patch`/`skill_manage` + `SKILL.md` | pre_tool_call | cmg_guard.hooks.pre_tool_call |
| 涉及 `rm -rf`/`DROP TABLE`/`force-push` | pre_tool_call | cmg_guard.hooks.pre_tool_call |
| 涉及「不能说」「禁止输出」「关键词」 | transform_llm_output | cmg_guard.hooks.transform_llm_output |
| 涉及「安装成功但实际失败」「工具假报」 | transform_tool_result | cmg_guard.hooks.transform_tool_result |

**检测流程：**

```
1. 分析新规则的 keywords + description
2. 按映射表匹配所需钩子
3. 读取 ~/.hermes/config.yaml → cmg_guard.hooks.<hook> 是否开启
4. 如果未开启 → clarify 弹窗：

   ⚠️ 规则已记录，但当前配置无法强制拦截。
   此规则需要开启 cmg_guard.hooks.<hook_name> 钩子。

   A) 现在开启（自动写入 config.yaml）
   B) 先不开，仅靠 AI 自觉
   C) 开启 + 以后此类规则自动开启

5. 用户选 A/C → 自动修改 config.yaml 对应字段为 true
```

---

## 规则效果评分 (v2.4.0)

固化引擎每次运行后，自动为每条规则计算效果评分并写入 `rules/` 目录的 frontmatter。

**评分指标：**

| 指标 | 计算方式 | 用途 |
|------|---------|------|
| 命中率 | 触发次数 ÷ 会话数 | 衡量规则的实际使用频率 |
| 误报率 | 用户标记误报次数 ÷ 触发次数 | 衡量规则的精准度 |
| 最后命中 | 距上次触发的天数 | 判断规则是否已过时 |
| 创建日期 | 规则首次写入日期 | 跟踪规则生命周期 |

**自动维护规则：**
- 误报率 > 30%（`scoring.false_positive_threshold`）→ 自动标记「待调整」，下次触发时先 clarify 确认
- 180 天未命中（`scoring.expiry_days`）→ 提示「此规则 180 天未触发，是否移除？」
- 固化报告增加规则效果排行（Top 5 高频规则 + Bottom 5 低频规则）

### 动态固化阈值 (C2)

`config.json` 的 `solidify_threshold_mode` 设为 `adaptive` 时，阈值根据用户纠正频率动态调整：

```
高频纠正(日均≥3次) → 阈值降低至5(更快固化)
正常频率 → 阈值保持10
低频纠正(周均<1次) → 阈值升高至20(避免空固化)
```

用户可切换为 `fixed` 模式使用固定阈值。

**与 Guard 联动（v4.2.0）：** Canon 输出规则评分 → Guard 读取后调整拦截策略。

### 跨类型冲突检测 (C4)

冲突检测不限于同类型——ban↔gap↔lazy 之间也进行语义去重：

```
例: lazy规则「论文必须检查字数」 vs gap规则「论文字数不够自动补齐」
→ 本质同一件事的不同表述 → 检测到语义重叠 → clarify 合并
```

`config.json` 的 `conflict_detection.cross_type: true` 控制开关。

### 规则导入/导出 (C3)

```
!export → 打包 rules/ 目录 + state.json + patterns.json → rules-export-YYYYMMDD.zip
!import <path-to-zip> → 解压 ZIP → 逐条冲突检测(含跨类型) → 逐条确认导入
```

导入保持来源标记（`source: imported`），与本地规则区分。

---

## 角色声明制 (v2.4.0)

废除数字优先级，Canon 以角色声明自己在管道中的位置：

```yaml
role: producer           # 规则生产锚点
stage: system_anchor     # 系统锚点层：最先加载，最后决策
```

**三线角色声明协作：**

```
Canon:   role: producer, stage: system_anchor  → 只生产规则，不执行拦截
Mnemonic: role: memory,   stage: background     → 只记状态，不生产不执行
Guard:   role: guard,     stage: pre_action     → 只执行拦截，不生产不存记忆
```

新 skill 加入只需声明 `role + stage`，自动归入对应阶段。终结 `priority: 110` 式军备竞赛。

---

## 命令参考 (v2.4.0)

### 简化触发词

| 触发词 | 等价自然语言 | 说明 |
|--------|------------|------|
| `!remember 禁止xxx` | 「记住，禁止xxx」 | 快速记录规则 |
| `!solidify` | 「固化规则」 | 手动触发固化 |
| `!scan` | 「扫盘」 | 手动触发扫盘提取 |
| `!export` | 「导出规则」 | 导出 rules/ 为 ZIP |
| `!import <path>` | 「导入规则」 | 从 ZIP 导入外部规则集 |
| `!log` | 「协调日志」 | 汇总三线日志统一视图（v5.2.0 E2） |
| `!diagnose` | 「诊断」/「自我检查」 | 一键诊断五文件+跨模块一致性（v5.2.0 E3） |
| `!patterns` | 「查看模式」/「识别模式」 | 查看 Mnemonic 识别的重复违规模式（v5.5.0 M3） |
| `!datasource` | 「数据源」/「数据源状态」 | 查看当前数据源状态和切换历史（v5.5.0 M3） |
| `!scan-recommendations` | 「扫描推荐」/「检查推荐列表」 | 扫描推荐列表，检测已安装但未配置的工具（v5.2.0） |

### 初始化命令

```bash
python3 scripts/init.py               # 完整安装（自动配置 config.yaml）
python3 scripts/init.py --uninstall   # 一键卸载，恢复安装前状态
```

**安装流程：**
1. 检查/安装子包（canon/guard/mnemonic）
2. 创建 rules/ 目录 + config.json + state.json + patterns.json
3. **自动配置 config.yaml** — `plugins.enabled` + `skill_autoload.skills`
4. 可选写入 SOUL.md 激活标记

**卸载（`--uninstall`）:** 移除 config.yaml 条目 + 删除插件/skill 文件 + 清除 SOUL 标记。**保留用户数据。** `--purge` 彻底清除。

### 规则导入/导出

```
!export → 打包 rules/ 目录为 rules-export-YYYYMMDD.zip
!import <path-to-zip> → 解压 ZIP → 冲突检测 → 逐条确认导入
```

导入时自动运行冲突检测。与现有规则冲突的条目触发交互裁决。

## 每次行动前（拦截检查）

> **v2.4.1：护栏逻辑已剥离至 `references/guard-spec.md`。** Canon 不再直接执行拦截——Canon 只生产规则，Guard（v4.0.0）执行拦截。当前过渡期，拦截逻辑仍可运行但视为「Guard 寄生」。

规则匹配逻辑不变（精确匹配 → 语义匹配 → 清单自检）。

### 评分计数器 (v2.4.1)

每次拦截检查后，更新 rules/ 目录中对应规则的 frontmatter：

```
命中: hit_count += 1, last_triggered = now()
误报: false_positives += 1 (用户说「这不是错误」后写入)
```

固化引擎运行时读取 hit_count / false_positives 计算评分。详见「规则效果评分」章节。

---

## 与现有 SOUL.md 铁则共存策略 (遗漏点 5)

### 共存模式

```
自省引擎的 rules/ 目录  ≠  SOUL.md 铁则
     ↓                        ↓
  结构化、可检索           纯文本、手动编辑
  自省引擎维护             用户手动维护
```

### 声明式层级（废除数字优先级）

```
注入顺序（由 stage 声明决定，非数字排序）:
  stage: system_anchor  → SOUL.md     (用户元规则，最高锚点)
  stage: pre_action     → rules/ 目录  (自省引擎规则，护栏层)
  stage: dispatch       → Skill 指令   (执行层)
```

**冲突处理：**
- 如果 SOUL.md 和自省引擎对同一行为有不同规则 → 自省引擎规则覆盖（因为是更新的、用户明确记录的）
- 如果自省引擎检测到 SOUL.md 中已有类似规则 → 提示用户 "SOUL.md 中已有类似规则，是否迁移到自省引擎？"
- 两种规则都生效，重叠时自省引擎拦截
- **不存在数字优先级竞争：** 处理顺序由 `stage` 声明决定（system_anchor → pre_action → dispatch），非 `priority: 110` 式军备竞赛

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

## 健康检查 (E1)

每次启动时自动检测核心文件完整性。`config.json` 的 `health_check.enabled: true` 控制开关：

```
检查项:
  rules/ 目录 → 存在且有内容
  state.json → 可解析且字段完整
  patterns.json → 可解析且 ban/gap/lazy 分类存在
  intercept_log.jsonl → 存在(Guard 写入)
  mnemonic_state.json → 存在(Mnemonic 写入)

任一失败 → 输出警告 + 降级运行
全部通过 → "健康检查通过。"
```

---

## 协调日志 (E2 · v5.2.0)

> **触发词**: `!log` 或「协调日志」「看日志」「汇总日志」

聚合三线独立日志为统一视图。一次调用看全貌。

### 执行步骤

```
1. Canon 数据:
   - 读取 state.json → 规则总数、last_solidify_at、last_scan_at
   - 读取 rules/_index.md → 规则分类（ban/gap/lazy 各 N 条）
   - 读取 errors.jsonl → 总错误数、最近 5 条错误

2. Guard 数据:
   - 读取 intercept_log.jsonl → 总拦截数、最近 5 条拦截
   - 按 interceptor 分类统计: Ban {N} / Fabrication {N} / StepCompleteness {N} / SkillLoad {N} / Clarify {N}
   - 当前模式: full / lightweight

3. Mnemonic 数据:
   - 读取 mnemonic_state.json → 识别模式数、草稿队列数、数据源状态
   - 最近推送至 Canon 的草稿（如有）

4. 输出统一视图
```

### 输出格式

```
╭─────────────────────────────────╮
│       三省引擎 · 协调日志       │
╰─────────────────────────────────╯

  📋 典则线 Canon (v2.5.0)
     规则: 10条 (ban:6 / gap:2 / lazy:2)
     上次固化: 2026-05-20 15:30
     上次扫盘: 2026-05-22 08:00 (0天前)
     错误记录: 23条总计

  🛡️ 护栏线 Guard (v4.5.0)
     模式: full (规则≤20)
     拦截总计: 15次
     └─ Ban: 8 / Fabrication: 2 / StepCompleteness: 3 / SkillLoad: 1 / Clarify: 1

  🧠 忆存线 Mnemonic (v3.3.0)
     数据源: guard_intercept (正常)
     识别模式: 3个 / 草稿队列: 1条待确认

  ── 三省引擎 v5.5.5
```

**降级：** 任一线数据缺失 → 标注 `⚠️ 缺失`，不阻塞其他线路输出。

---

## 一键诊断 (E3 · v5.2.0)

> **触发词**: `!diagnose` 或「诊断」「自我检查」「检查引擎」

启动时健康检查（E1）只检查文件存在性。E3 更进一步——深度检查文件内容有效性和跨模块一致性。

### 诊断步骤

#### Phase 1: 文件完整性（同 E1 健康检查）

```
1. rules/ 目录 → 存在且非空
2. state.json → 可解析且关键字段完整
3. patterns.json → 可解析且 ban/gap/lazy 分类存在
4. intercept_log.jsonl → 存在（Guard 写入）
5. mnemonic_state.json → 存在（Mnemonic 写入）
```

#### Phase 2: 规则有效性

```
1. 遍历 rules/ban/*.md rules/gap/*.md rules/lazy/*.md
2. 逐条验证:
   - frontmatter 是否可解析（YAML 语法）
   - type 字段是否匹配所在目录（ban/ → type: ban）
   - keywords 字段是否非空
   - [v2.6.0+] level 字段是否存在且值为 hard/soft/monitor
   - [v2.6.0+] correction_template 字段是否存在（hard 规则必须非空）
3. 统计覆盖率: 有完整 frontmatter 的 / 缺少字段的 → 输出摘要
4. 可选: 运行 `python3 ~/.hermes/skills/software-development/canon/scripts/check-frontmatter.py` 获取详细清单
5. 检查 _index.md 表格行数是否匹配实际文件数
6. 发现不一致 → 输出警告 + 差异详情
```

#### Phase 3: 跨模块引用一致性

```
1. 扫描 intercept_log.jsonl → 提取所有 rule_id
2. 对比 rules/ 目录 → 确认每条 rule_id 都有对应规则文件
3. 孤立的 rule_id（日志中有但 rules/ 中无）→ 输出警告
4. 孤立的规则文件（rules/ 中有但日志从未引用）→ 标记「未触发」
5. 扫描 mnemonic_state.json draft_queue → 确认 rule_id 不与 rules/ 重复
```

#### Phase 4: 数据源健康

```
1. 检查 intercept_log.jsonl 最后写入时间
   - 距现在 > 7 天 → ⚠️ Guard 可能未激活
2. 检查 errors.jsonl 最后写入时间
   - 距 state.json last_solidify_at 后无新增 → 正常（无新错误）
3. 检查 mnemonic_state.json data_source_history
   - none_sessions 占比 > 50% → ⚠️ 数据源长期缺失
```

#### Phase 5: 子包版本一致性

```
1. 读取 canon SKILL.md → 版本号
2. 读取 guard SKILL.md → 版本号
3. 读取 mnemonic SKILL.md → 版本号
4. 对比 CMG 自身 _comment 中声明的版本号
5. 不匹配 → ⚠️ 子包版本与外观层声明的版本不一致
```

#### Phase 6: 四名冲突检测 (v5.5.5)

```
1. 运行 scripts/check-name-conflicts.py
2. 扫描 ~/.hermes/skills/ + ~/.agents/skills/ 所有 SKILL.md
3. 检测 canon/guard/mnemonic/canon-mnemonic-guard 是否与第三方重名
4. 发现冲突 → ⚠️ 列出冲突详情 + 建议运行 python3 scripts/check-name-conflicts.py --fix
```

### 输出格式

```
╭─────────────────────────────────╮
│       三省引擎 · 诊断报告       │
╰─────────────────────────────────╯

  📁 文件完整性  ··········  ✅ 5/5
     rules/ ✓  state.json ✓  patterns.json ✓
     intercept_log.jsonl ✓  mnemonic_state.json ✓

  📋 规则有效性  ··········  ✅ 10/10
     ban: 6条  gap: 2条  lazy: 2条
     _index.md 表格: 匹配

  🔗 跨模块引用  ··········  ✅ 无孤立引用
     日志引用 5 条 rule_id → rules/ 全部匹配
     未触发规则: rule_007 (lazy/论文格式检查，创建于 05-15)

  📡 数据源健康  ··········  ✅ 正常
     Guard 拦截日志: 活跃 (最后写入 2026-05-22 09:12)
     Canon 错误记录: 23条 (最后写入 2026-05-21)

  📦 子包版本    ··········  ✅ 一致
     canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3

  🔤 四名冲突    ··········  ✅ canon/guard/mnemonic/CMG 无冲突

  🟢 总体状态：健康
     建议: 规则 rule_007 60天未触发，可在下次固化工单中复核。
  ── 三省引擎 v5.5.5
```

### 诊断级别

| 级别 | 图标 | 含义 | 行为 |
|------|------|------|------|
| 🟢 健康 | 全部检查通过 | 继续 |
| 🟡 注意 | ⚠️ 非关键问题（如1条规则未触发） | 输出建议，不阻塞 |
| 🟠 警告 | 部分文件缺失/数据源长期离线 | 输出修复建议 |
| 🔴 严重 | rules/ 目录为空 / state.json 损坏 | 提示运行 `npx canon-mnemonic-guard init` 重置 |

---

- [init.py 名冲突检测设计](references/init-name-conflict-detection.md) — CMG 四名保护 + 双触发点检测 + 三选一解决
- [联动待测清单](references/integration-test-checklist.md) — ralph-loop/VBC/diagnose 验证条件和状态
- [配套Skill协同测试指南](references/companion-skill-testing-guide.md) — 四步检测法
- [v5.5.2 发布教训](references/v5.5.2-release-lessons.md) — 生态包子包文件缺失 + README 版本号滞后 + 合集 README 第二次敷衍
- [Hermes 升级适配指南](references/hermes-upgrade-adaptation.md) — v0.13→v0.14.0 hook 迁移 + skill 恢复流程
- [双层防御模型](references/layered-defense-model.md) — A 层正则哨兵 + B 层 LLM 语义判断架构
- [v5.5.4 发布教训](references/v5.5.4-release-lessons.md) — 发布流程六条铁律
- [自披露闭环参考案例](references/self-disclosure-loop.md) — 断言须附证据的三步闭环，cmg-guard v1.3.0 内置
- [自披露闭环](references/self-disclosure-loop.md) — AI 断言必须附带证据，缺了拦截→重做（cmg-guard v1.3.0+ 内置）

## 常见坑点 (维护本 Skill 时必读)

> 以下坑点来自实际维护过程中的反复修正，写入此处避免重犯。

### 坑点 1: 禁止交叉引用外部 Skill 的版本号

本 Skill 的三线架构（Canon 2.x / Mnemonic 3.x / Guard 4.x）有独立的版本体系。**绝不**在文档中引用 Idea Foundry 的 v8/v9 或其他外部 Skill 的内部版本号——这会造成读者的严重混淆。

- ❌ `v8 时代用 priority: 110 → v9 改为 role+stage`（这是 Idea Foundry 的版本号，不是本 Skill 的）
- ✅ `旧范式用 priority: 110 → 本 Skill 的答案：role+stage`

### 坑点 2: 未来规划不能混入当前设计哲学

角色声明制是未来 v2.4.0 / v3.0.0 / v4.0.0 的规划，当前 v2.2.6 仍用层级模型。写文档时：
- 角色声明制 → 放在版本路线的各线未来版本中
- 设计哲学章节 → 只写已确定的解耦原则，不写未实现的功能
- 冲突声明表 / 流水线图 → 用当前生效的层级模型，不用未来的 stage 语言

### 坑点 3: CHANGELOG 必须覆盖完整历史

初版 v1.0.0 原始名称为 `hermes-self-reflection`（SKILL.md 在桌面 zip 中存档），v2.0.0 重命名为 `hermes-canon-mnemonic-guard`，v2.2.9 进一步精简为 `canon-mnemonic-guard`。编写 CHANGELOG 时：
- 必须从 v1.0.0 开始，包含原始名称和完整功能清单
- v2.0.0 条目必须标注重命名
- 不要从 v2.2.0 开始——那是中间快照，不是起点

### 坑点 4: 三条线各自独立 Skill 包，不可混写

未来 v3 和 v4 发布时：
- v3 忆存线 → 独立 `mnemonic` Skill 包，不写入当前 SKILL.md
- v4 护栏线 → 独立 `guard` Skill 包，不写入当前 SKILL.md
- 三条线只在 v5.0.0 合并为一个统一引擎包
- 详见 `references/future-release-plan.md`

### 坑点 5: 推荐标准是 CMG 自动感知调用，非第三方安装难度

推荐列表不是愿望清单。准入标准是 **CMG 能否自动感知并调用**，不是第三方好不好装：

1. 自动感知 — 标准安装后，CMG 无需额外配置即可发现该 skill
2. 零适配调用 — CMG 的 checklist/扫盘/拦截逻辑可直接触发该 skill
3. 互补非重叠 — 该 skill 提供 CMG 不具备的能力

第三方 skill 的安装难度（npm/pip/cargo/docker）与 CMG 无关——那是用户自己负责装上的事。CMG 只关心：装上后能不能联动。

详见 `references/companion-skills-research.md`。

### 坑点 6: 不可凭类型推断冲突，必须验证实际交互路径

分析某个第三方工具是否与 CMG 冲突时，**不能凭"它是什么类型"推断风险**。

- ❌ 错误：plur 是 MemoryProvider 插件 → 它会拦截 Hermes memory → CMG 扫盘会读到脏数据
- ✅ 正确：plur 实际是 TypeScript MCP 服务器，独立进程，数据存 `~/.plur/`，与 Hermes memory 完全隔离。CMG 扫盘默认不扫 `~/.plur/`，不存在冲突
- 教训：必须阅读实际代码/架构再下冲突结论，不可凭名称或分类推断

### 坑点 6: 推荐 Skill 归属不能单线强制

某些 Skill 天然服务多条线——强行归入任一条线都会在后续发现它其实也服务另一条，造成反复横跳。

**本 Skill 实战案例：** obsidian 先被归入典则线（可视化 rules/*.md），后发现它也能检索忆存线的 errors.jsonl/state.json。两次重分类后最终发现它本就该在「跨线共享」。

**正确做法：**
- 当一个 Skill 经过 2 次以上归属调整仍无法稳定 → 它很可能就是跨线共享
- 新增「跨线共享」分类，明确标注服务哪些线
- 不要为了整齐而强行归入单线——不准确的分类比多一个分类更差

### 坑点 8: 三线开发顺序不可颠倒（v4 必须早于 v3）

原路线是 v2→v3→v4，但实际依赖链决定了必须 v4 先于 v3：

```
v3 自动模式识别 → 需要分析拦截数据 → 数据谁产生？ Guard 的计数器
Guard 独立了吗？ → 如果没有，计数器不工作 → v3 开发时面对空库
```

**正确顺序：** v2 典则（规则生产）→ v4 Guard（拦截执行，计数器激活）→ v3 Mnemonic（读取拦截日志，模式识别）→ v5 统一。

### 坑点 9: errors.jsonl 写入后必须及时固化（2026-05-19 实战）

**症状：** 28 条错误记录已写入 `errors.jsonl`，但 CMG Guard 在用户违规时没有拦截。

**根因：** errors.jsonl 只是原始记录。Guard 只读取 `rules/ban/` `rules/gap/` `rules/lazy/` 目录下的活跃规则。28 条错误没有经过 `!solidify` 固化成活跃规则 → Guard 的拦截层是空的。

**正确做法：** 每次用户「记住」或写入 errors.jsonl 后，检查 `state.errors_since_solidify`。达到阈值（默认 10 条）→ 提示用户执行 `!solidify`。`!solidify` 执行：读取 errors.jsonl → 去重合并 → 生成 rules/ban|gap|lazy/*.md → 更新 _index.md → 更新 state.json → Guard 拦截层激活。

### 坑点 10: 统一引擎命名不能倒退到旧名

v5.0.0 合并时误将统一外观命名为 `self-reflection-engine`——这是初版 v1.0.0 的旧名（`hermes-self-reflection`）。用户立刻指出不一致。

**正确做法：** 统一引擎沿用项目主名称。本项目主名为 `canon-mnemonic-guard`，v5.0.0 统一外观直接升版主 Skill，不另创新名。创建了错误的独立 engine Skill 后立即删除，内容并入主 Skill。

推荐列表的准入标准经历了一次关键修正：

- ❌ 旧标准：第三方必须零配置安装
- ✅ 新标准：CMG 安装后，用户装推荐 → CMG 自动感知 → 无需适配即可调用。第三方好不好装是它自己的事

**后果：** 之前以"需要 pip install"为由否决了多个候选，但这个理由不成立。重新审视时发现 plur 可以作为可配置扫描源接入，rtk-hermes 作为被动受益方。

### 坑点 7: 版本号变更后必须全文件同步验证

版本号只改了 frontmatter 和标题，但注入消息、激活消息、README 标题、典则线当前标记、CHANGELOG 标题等散布在多处的硬编码版本号全部滞后。

**本 Skill 实战案例：** v2.2.9 发布时 README 标题仍写 v2.2.6；注入消息和激活消息仍写 v2.2.3。

**正确做法：** 每次版本号变更后，逐项执行 `references/release-checklist.md` 的 13 项发布自检，勾完才算发布完成。不可凭记忆。

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
| 准则类 (铁则库, karpathy-coding-guidelines) | 互补 | 并行生效，重叠时 Guard 拦截为准。karpathy 已双向声明 CMG 为配套 skill |
| 安全类 (gstack/guard, gstack/careful) | 互补 | 不同层：CMG 守行为层（AI做什么），gstack 守命令层（OS执行什么）。无冲突 |
| 调度类 (Idea Foundry) | 护栏→调度 | 自省引擎在调度之前执行（stage 声明决定，非数字优先级） |
| 执行类 (其他所有) | 监督—被监督 | 每次行动前检查，不修改被监督 skill 行为 |

## 配套 Skill 生态

自省引擎独立可用。搭配以下第三方工具形成增强生态。**核心原则：添加式集成，CMG 只消费第三方产出，绝不修改第三方行为。**

> 完整调研见 `references/companion-skills-research.md`（14 候选 → 8 通过）。

### 三线归属

#### 护栏线（拦截执行 · 验证闭环）

| 推荐 | 增强点 | 集成方式 |
|------|--------|---------|
| `ralph-loop` | 执行闭环 | Guard 拦截跳步骤 → 自动触发闭环验证 |
| `verification-before-completion` | 证据先于断言 | Guard 拦截「声称完成」→ VBC 证据协议 |
| `diagnose` | 根因调试 | 同规则连续命中 → !diagnose 诊断根因 |
| `karpathy-coding-guidelines` | 进攻型行为准则 | 防守+进攻互补，已双向认可 |

#### 典则线（规则扩展 · 可视化）

| 推荐 | 增强点 | 集成方式 |
|------|--------|---------|
| `plur` | 扩展规则来源 | RuleReader 读取 `~/.plur/engrams.yaml` |
| `obsidian` | rules/ 可视化 | .md 原生格式，Dataview 查询 + 图谱链接 |

#### 跨线共享

| 推荐 | 增强点 | 集成方式 |
|------|--------|---------|
| `skill-autoload` | v1.0.1: 自动加载 CMG，零手动 | Plugin，`pre_llm_call` 钩子。配套插件，非核心四线 |
| `cmg-guard` | v1.3.0: 17hook硬拦截 + pre_tool_call阻断 + 自披露闭环 | Plugin，`pre_llm_call` + `transform_llm_output` + `post_llm_call` 三钩子。配套插件，非核心四线。详见 `references/cmg-guard-v1.3.0-escalation.md` |
| `rtk-rewrite` | 压缩终端输出 60-90% token | Gateway 插件，安装即自动运行 |
| `hermes-agent-skill-authoring` | 发布流程风控 | 13 项自检清单 + 版本号 grep 验证 |

> **核心四线 vs 配套插件：** Canon/Guard/Mnemonic/外观层 是 CMG 核心四线——规则体系的基石。skill-autoload 和 cmg-guard 是配套插件——辅助核心工作，离开 Hermes 不可用，换了平台需要重新适配。
| `agent-s-deployment` | Agent S 部署与配置（本地 UI-TARS/HF/Gemini/Together/OpenRouter grounding 方案对比） |

#### 参考模式（Hermes 下 hook 不生效）

| 参考 | 模式价值 |
|------|---------|
| `gstack/careful` | 破坏性命令检测模式（rm -rf/DROP/force-push） |
| `gstack/guard` | careful+freeze 三层过滤（命令→路径→行为） |

### 微型调度器（v5.5.0）

Guard 拦截时自动匹配配套 skill，提示加载。

**拦截触发型：**

| 拦截场景 | 推荐 |
|---------|------|
| 过设计/复杂化 | `karpathy-coding-guidelines` |
| 跳步骤/未闭环 | `ralph-loop` |
| 声称完成未验证 | `verification-before-completion` |
| 同规则连续命中≥3次 | `diagnose` |

**被动/基础设施型（标注状态即可）：**

| 推荐 | 状态 |
|------|------|
| `rtk-rewrite` | 已安装即自动运行 |
| `plur` | CMG 扫盘时自动读取 |
| `obsidian` | 直接浏览 rules/*.md |
| `hermes-agent-skill-authoring` | 发布时手动加载 |
| `gstack/careful` | ⚠️ Hermes hook 限制 |
| `gstack/guard` | ⚠️ 同上 + ⚠️ 与CMG/guard同名冲突（Skill层name: guard），需手动改名gstack-guard |

---

## 设计哲学：彻底解耦·物理拆分·单向依赖

### 核心拆分原则

```
典则 Canon (2.x)  = 规则生产库
    ↓ 只管「规则从哪来、怎么固化、好不好用」
    ↓ 绝对不包含拦截执行代码、不碰记忆、不做校验
    
忆存 Mnemonic (3.x) = 状态记忆层
    ↓ 只管「记录错误、提取模式、上下文感知」
    ↓ 不生产规则、不执行拦截

护栏 Guard (4.x)  = 规则执行器
    ↓ 只管「拿到规则、执行拦截、校验放行」
    ↓ 不生产规则、不存记忆
```

**运行时联动：** Canon → Mnemonic → Guard 单向调用。护栏只消费典则+忆存的标准化输出，不反向污染。

**物理拆分目标（v5.0.0 前）：** 三个模块各自独立可拆出为单独 Skill，按需启用。护栏模块完全不依赖典则内部实现，只调用典则输出的标准化规则接口。

### 设计参考（未来版本消化，不在当前迭代）

本 Skill 的完整设计方法论（9 条核心原则）详见 `references/design-methodology.md`。

| 来源 | 模式 | 借鉴方向 |
|------|------|---------|
| **gstack** 管线式 stage 分离 | plan→design→eng→review→ship 每个阶段独立 skill，顺序串联 | 验证 Canon→Mnemonic→Guard 管线模式的可行性；`/careful` 作为可叠加护栏的参考 |
| **Matt Pocock Interface Design** | Ports & Adapters + "Design It Twice" | v2.3.0 RuleReader/Validator 接口设计时参考：定义清洁接口→适配器实现→多方案对比择优 |
| **Microkernel (Agent-Kernel)** | 内核+插件架构，插件注册表，内核不感知插件实现 | v5.0.0 统一引擎的终极形态：Canon 为内核，Guard/Mnemonic 为插件，通过标准化接口注册和消费 |

---

## v5.5.0 改进方向（外部评审）

四条优化建议经 DeepSeek 评审，详见 `references/v5.5.0-improvement-directions.md`：
- 规则分级 hard/soft/monitor（★★★★★）
- 同会话重复快速升级（★★★★☆）
- Mnemonic 2次推草稿（★★★★★）
- 用户纠正提升一级非直接 hard（★★★☆☆）
- 额外：误报降级、场景感知、规则有效期

## 版本路线

### 三大模块化引擎（完全独立，无寄生）

| 线路 | 版本号 | 定位 | 职责边界 |
|------|--------|------|---------|
| **Canon 典则线** | 2.x | 硬规则引擎 | 规则来源、固化、扫描、效果评分。纯静态规则层。 |
| **Mnemonic 忆存线** | 3.x | 记忆引擎 | 会话记忆、错误模式、自动规则草稿。纯记忆状态层。 |
| **Guard 护栏线** | 4.x | 拦截引擎 | 前置校验、动态清单、拦截效能、上下文感知。纯执行校验层。 |

**铁律：** 三条线严格独立迭代，互不寄生。只在运行时通过标准化接口联动。

---

### 典则线 · Canon (2.x.x) — 硬规则引擎

> **定位：** 规则生产库。典则线仅输出标准化规则，不含任何拦截、校验、执行逻辑。

**v5.4.0:** 四包制(Canon v2.7.0/Guard v4.8.0/Mnemonic v3.5.0独立+CMG外观)

**v5.4.0:** 四包制(Canon v2.7.0/Guard v4.8.0/Mnemonic v3.5.0独立+CMG外观)

---

**v2.3.0: 依赖解耦 + 可配置扫描源（前置基建）**

把「读规则」逻辑拆成接口 + 适配器。解耦后 CMG 能读取任意第三方数据源（plur、OpenClaw、外部文件），这是后续所有跨 skill 联动的基础。

```
RuleReader 接口      ← 只管读规则，不管从哪读
  ├── JSONRuleSource        内置默认 → 零外部依赖
  ├── SOULRuleSource        builtin
  ├── ObsidianRuleSource    obsidian 配置驱动
  ├── MemoryRuleSource      builtin
  ├── SkillRuleSource       builtin
  ├── PlurRuleSource        v2.3.0 新增：读取 ~/.plur/engrams.yaml
  └── CustomRuleSource      遍历 config.json custom[] 列表
```

**可配置扫描源（白名单制，绝不全盘扫描）：**

```json
{
  "scan_sources": {
    "builtin": {"soul": true, "memory": true, "skills": true},
    "obsidian": {"enabled": true, "vault_path": "~/obsidian", "rule_dirs": ["🔒 HERMES-全局铁则库"]},
    "custom": [
      {"name": "openclaw_memory", "path": "~/.openclaw/memory/", "file_pattern": "*.md", "enabled": true},
      {"name": "plur_engrams", "path": "~/.plur/", "file_pattern": "engrams.yaml", "enabled": false}
    ]
  }
}
```

---

**Phase 1（v2.3.x）: 规则冲突机制 + 模式切换 + Idea Foundry 规则集联动**

| 任务 | 说明 |
|------|------|
| **规则冲突解决** | 明确指定 > 最近使用 > 更严格规则。两条 ban 规则矛盾时自动暂停 → clarify 让用户裁定 |
| **傻瓜模式 / 专家模式** | 傻瓜模式：自动记录纠正（带「准则类」过滤器，不记录无关键词的临时纠正）→ 阈值触发固化提示。专家模式：每次记录前 clarify 确认，可编辑规则内容后写入 |
| **Idea Foundry 规则集开关** | Idea Foundry Phase -3 增加「启用 CMG 规则集」选项。开启后 CMG 的 rules/ 作为约束注入到流水线的代码生成阶段 |

---

**Phase 2（v2.4.0）: 规则评分 + 角色声明制 + 工具链完善**

| 任务 | 说明 |
|------|------|
| **规则效果评分** | 每条规则跟踪命中率/误报率/最后命中时间。误报率>30%→标记待调整，180天未命中→提示过期 |
| **角色声明制引入** | Canon 以 `role: producer, stage: system_anchor` 声明规则生产锚点。与 Guard v4.2.0 联动：Canon 输出评分→Guard 调整拦截策略 |
| **初始化命令** | `npx canon-mnemonic-guard init` 自动创建 rules/ 目录结构 + 示例规则 + config.json |
| **简化触发词** | `!remember 禁止xxx` / `!solidify` / `!scan` 短触发词，与自然语言触发并行 |
| **规则导入/导出** | `!export` 导出 rules/ 目录为 ZIP，`!import <path>` 导入外部规则集。用于分享和备份 |

---

### 忆存线 · Mnemonic (3.x.x) — 记忆引擎

> **定位：** 状态记忆层。只记录、只提取、只推送。不生产规则、不执行拦截。

**v3.0.0: CLI + 独立触发 + 角色声明制引入**

- `hermes reflect status` — 查看当前规则库状态
- `hermes reflect add "规则"` — 命令行添加规则
- `hermes reflect scan` — 手动触发扫盘
- 独立进程模式：不作为 Skill 加载，作为 Hermes 守护进程常驻
- 首次实现：基于现有 state.json + errors.jsonl，不引入新存储
- **角色声明制引入：** Mnemonic 以 `role: memory, stage: background` 声明自己是后台记忆层，只记录状态不生产规则不执行拦截。与 Canon/Guard 通过标准化接口联动

**v3.1.0: 自动模式识别**

- 分析 errors.jsonl 历史 → 识别高频错误模式
- 同一关键词 7 天内出现 ≥ 3 次 → 自动生成规则草稿
- **推送至典则线：** 草稿不直接写入 rules/，而是通过标准化接口推送至 Canon 固化引擎，由 Canon 负责去重、分类、写入
- 使用 clarify 提醒用户确认，不自动写入
- 误报率高时自动降低该模式的匹配置信度

---

### 护栏线 · Guard (4.x.x) — 拦截引擎

> **定位：** 规则执行器。运行时读取 Canon 规则库 + Mnemonic 记忆库，独立执行 pre_action 前置拦截。**v4.0.0 已发布为独立 Skill（`software-development/guard`）。**

**v4.0.0: 独立化拆分 + 角色声明制**

从典则线彻底剥离，实现独立拦截器模块：

```
Interceptor 接口       ← 每个拦截器独立开关、独立日志
  ├── BanInterceptor              精确匹配拦截
  ├── FabricationInterceptor      防幻觉拦截
  ├── StepCompletenessInterceptor 防跳步骤拦截
  ├── SkillLoadInterceptor        防偷懒拦截
  └── ClarifyInterceptor          防瞎猜拦截
```

- 运行时读取 Canon 规则库（rules/ 目录）→ 加载拦截规则
- 运行时读取 Mnemonic 记忆库（state.json）→ 感知上下文
- 拦截日志独立记录到 `intercept_log.jsonl`
- **护栏模块完全不依赖典则内部实现，只调用典则输出的标准化规则接口**

**同步引入角色声明制：** 废除数字优先级，Guard 以 `role: guard, stage: pre_action` 声明自己在管道中的位置。三条线统一更换为 role+stage 声明式协作：

```
Canon:  role: producer, stage: system_anchor  → 只生产规则，不执行拦截
Mnemonic: role: memory,   stage: background     → 只记状态，不生产不执行
Guard:   role: guard,     stage: pre_action     → 只执行拦截，不生产不存记忆
```

新 skill 加入只需声明 `role + stage`，自动归入对应阶段，无需重排任何数字。彻底终结 `priority: 110` 式军备竞赛。

**v4.1.0: 动态清单生成**

脱离静态 YAML checklist 文件。根据任务类型 + 历史错误实时生成：

```
任务类型检测
    │
    ├── 论文 → 从 errors.jsonl 提取该类型高频遗漏 → 自动生成检查项
    ├── 代码 → 同上
    └── 通用 → default 项 + 最近 7 天新增的高频错误项
```

连续三次同类遗漏 → 自动追加到清单。

**v4.2.0: 拦截效能分析**

| 指标 | 用途 |
|------|------|
| 命中率 | 该规则被触发的频率 |
| 误报率 | 用户说「这不是错误」的次数 ÷ 触发次数 |
| 拦截延迟 | 从检测到拦截的耗时 |
| 最后命中 | 距上次命中天数 |

- 误报率 > 30% → 自动降级：不再拦截，改为"提醒"
- 180 天未命中 → 提示"是否已过时"
- **与 Canon v2.4.0 双向联动：** Canon 输出规则评分（好不好）→ Guard 消费并反馈拦截效果（拦得准不准）→ Canon 更新评分

**v4.3.0: 上下文感知拦截**

不只看当前动作，还感知运行上下文：

| 上下文 | 行为 |
|--------|------|
| 同一错误 5 分钟内重复 3 次 | 升级拦截级别（提醒→警告→阻断） |
| 用户明确说「跳过检查」 | 临时放行（会话级豁免，Mnemonic state.json 记录） |
| Agent 连续跳步骤 | 检测到「赶工模式」→ 提升敏感度 |
| 上下文窗口快满 | 切换轻量模式（只跑 ban_check，跳过其余四层） |

---

## 三线并行 → 统一引擎

```
典则线 Canon (2.x)      忆存线 Mnemonic (3.x)       护栏线 Guard (4.x)
─────────────────       ──────────────────        ────────────────
v2.2 ✓ 扫盘提取          [未启动]                   [寄生在 Canon 里]
v2.3   依赖解耦
v2.4   规则效果评分        v3.0   ✅ 已发布        v4.0   ✅ 已发布
  +角色制 producer         +角色制 memory    v4.1   ✅ 动态清单
  system_anchor            background        v4.2   ✅ 效能分析
                          v3.1   ✅ 模式增强  v4.3   ✅ 上下文感知
        ↓                       ↓                        ↓
        └───────────────────────┴────────────────────────┘
                                ↓
            v5.0.0 三线合一 + 角色制统一引擎
```

**v5.0.0 架构预览：外观模式 · 主角色 + 内部子角色**

```
                    外部视角 (唯一契约)
         ┌──────────────────────────────────┐
         │     v5.0.0 统一自省引擎             │
         │     role: guard                   │  ← 对外唯一身份，前向兼容
         │     stage: pre_action              │
         └──────────────┬───────────────────┘
                        │ 内部封装
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  Canon   │   │ Mnemonic │   │  Guard   │
  │ producer │ → │  memory  │ → │  guard   │  ← 内部子角色保留
  │  anchor  │   │ bkgrnd   │   │pre_action│    协同逻辑不变
  └──────────┘   └──────────┘   └──────────┘
     规则生产        状态记忆        规则执行
```

**设计决策：** 采用外观模式。v5.0.0 对外声明单一角色 `role: guard, stage: pre_action`，与 v2.2.x 当前版本完全一致，所有依赖方无需任何改动。内部三条线保留各自子角色（`producer` / `memory` / `guard`），通过标准化接口（rules/*.md / errors.jsonl / state.json）协同运行，子角色不对外暴露。

**为什么不能多角色声明：** 多 `roles: [producer, memory, guard]` 会把内部架构泄露成外部契约，迫使调度器理解三线协同逻辑——这不是大一统，是把复杂度转嫁给了生态。封装即协同。

**前向兼容：** 外部 skill 只看到一个护栏 `stage: pre_action`——从 v2.2.6 到今天到 v5.0.0，契约不变。未来加第四条线（如 Analyst），对外 `role: guard` 依旧不变，外部完全无感。

> **v5.0.0 = 外观模式（对外 `role: guard`）+ 内部三线子角色（producer/memory/guard）+ 标准化接口联动 = 封装式统一免疫系统。**

---

## 未来更新方向（各模块独立迭代）

### Canon v2.x 待优化

| # | 方向 | 说明 |
|---|------|------|
| C1 | ✅ 定时扫盘（v2.5.0） | 加载时检查距上次扫盘天数，超阈值自动触发 |
| C2 | ✅ 动态固化阈值（v5.0.2） | adaptive/fixed双模式 |
| C3 | ✅ 导入导出（v5.0.2） | !export打包+!import逐条确认 |
| C4 | ✅ 跨类型冲突检测（v5.0.2） | ban↔gap↔lazy语义去重 |

### Guard v4.x 待优化

| # | 方向 | 说明 |
|---|------|------|
| G1 | ✅ 五层拦截器运行时实现（v4.3.1） | |
| G2 | ✅ 动态清单真实数据（v4.5.0） | errors.jsonl实时生成检查项 |
| G3 | ✅ 上下文感知实现（v4.5.0） | 重复错误升级/赶工检测/轻量模式/用户豁免 |
| G4 | ✅ 效能分析真实数据（v4.5.0） | 命中率/误报率自动调优+降级+过期标记 |
| G5 | ✅ 重名解决（v4.4.0） | 全路径加载 software-development/guard |

### Mnemonic v3.x 待优化

| # | 方向 | 说明 |
|---|------|------|
| M1 | ✅ 数据源降级链（v3.3.0） | intercept_log.jsonl → errors.jsonl → 等待状态 |
| M2 | ✅ 独立持久化（v3.2.0） | mnemonic_state.json |
| M3 | ✅ !patterns + !datasource 触发词实现（v5.5.0） | 零外部依赖，完全自主可控 |
| M4 | ✅ 误报率双向调节（v3.2.0） | 置信度±0.1/0.2 浮动 |

### Engine v5.x 待优化

| # | 方向 | 说明 |
|---|------|------|
| E1 | ✅ 健康检查（v5.0.2） | 启动时五文件完整性检测 |
| E2 | ✅ 协调日志（v5.2.0） | !log 统一日志视图 |
| E3 | ✅ 一键诊断（v5.2.0） | !diagnose 五阶段深度诊断+跨模块一致性 |
| E4 | ✅ 四包制分装（v5.1.0 已发布） | canon/guard/mnemonic 独立 Skill 包 + CMG 外观索引 |

> **17 项全部完成。** CMG 功能闭环，无遗留待办。

---

## P 系列增强追踪（v5.5.0 引入的编号方案）

> v5.5.0 大更使用 P1-P4 编号标记跨模块增强。此编号体系与 C/G/M/E 序列独立——P 系列是跨线功能，C/G/M/E 是单线优化。

| # | 内容 | 涉及模块 | 状态 |
|---|------|---------|:--:|
| P1 | 同会话重复快速升级（2次触发→block，24h半衰期） | Guard | ✅ v5.5.0 |
| P2 | Mnemonic同会话2次推草稿+session追踪+Guard联动钩子（原7天3次加速） | Mnemonic + Guard | ✅ v5.5.0 |
| P3 | 用户纠正自动提升（monitor→soft→hard） | Guard + Canon | ✅ v5.5.0 |
| P4 | 误报自动降级 + 规则有效期（`--expires 7d`） | Canon | ✅ v5.5.0 |
| P5 | 傻瓜/专家模式切换（`!mode simple|expert`） | Canon + Guard | ⏳ 规划中 |

> **注意：** P 系列计划不在此 SKILL.md 中展开（内容由用户逐版本指定）。每次发布后更新此表状态。下个版本从 P5（!mode）开始。

### 坑点 12: 过度迭代——小变更不值得升版（2026-05-25 两次被制止）

补两个 !trigger 命令、更新推荐列表、修几行文档——这些**不是小版本升级的理由**。

- ❌ v5.4.1 刚发布就准备 v5.5.0（P2 只是文档补全+联动钩子）
- ❌ v5.5.0 补两个命令就准备升版（被用户喊停）
- ✅ 正确：文档微调、推荐列表更新 → 积累 2-3 个变更再一起发。或作为下次打包时附带。

**判断标准：** 改一行推荐列表 ≠ 发一个版本。改 SKILL.md 核心逻辑/加新章节/加新功能 → 才值得升版。

**版本号节约：** Canon(2.x)、Guard(4.x) 小版本空间有限（~2.99/4.99）。每个功能补丁用 .1 递增（2.7.0→2.7.1），不是每个文档更新。

P1-P4 增强体系在 v5.4.0 发布时引入，但未出现在「未来更新方向」的 C/G/M/E 表格中。导致后续会话无法搜索到 v5.5.0 计划。**每次引入新编号体系必须在此章节记录。**

### 坑点 12: 补丁变更不可升四包子包小版本号（2026-05-25）

v5.4.0 刚发布，P2 增量只是文档补全+联动钩子，却准备升 Guard v4.9.0 / Canon v2.8.0 / Mnemonic v3.6.0。用户制止：「这属于过度迭代。没有重大新功能不需要过大版本号更新。」

**正确做法：** 文档补全、细节完善、小联动钩子 → 补丁版本（z+1）。新功能、架构变更 → minor 版本（y+1.0）。四包多子包发布时所有子包同步补丁——Guard 4.8.0→4.8.1，不是 4.9.0。

### 坑点 14: Hermes 大版本升级后 CMG 必溃（2026-05-26）

Hermes v0.13→v0.14.0 实际影响：
- `pre_system_prompt` hook 被移除 → skill-autoload v1.0.0 完全失效
- CMG 四包 SKILL.md 在升级时被清空 → canon/guard/mnemonic/canon-mnemonic-guard 全部消失
- config.yaml 和 SOUL.md 的配置通常保留，但 skill 文件没了等于空跑

**每次 Hermes 大版本升级后的验证清单：**
1. `grep 'unknown hook' ~/.hermes/logs/agent.log` → 有则适配插件
2. `ls ~/.hermes/skills/canon/SKILL.md` → 不存在则从 GitHub zip 恢复
3. 对照最新 VALID_HOOKS 列表验证 skill-autoload 和 cmg-guard 的 hook 声明
4. skill-autoload 需升级到 v1.0.1（`pre_llm_call`，详见 `references/hermes-upgrade-adaptation.md`）
5. 重启 Hermes，确认日志无 `unknown hook` 警告

### 坑点 15: 用户纠正不能只调 memory（2026-05-26）

用户纠正后只写 memory 不走 CMG 三步走 → CMG ban 规则永远不更新 → 再犯时 Guard 拦不住。

**正确做法：** 用户任何表达「纠正+希望避免」的语句 → 三步走全流程：
1. `errors.jsonl` 追加记录
2. `rules/ban/*.md` 创建规则（含 frontmatter）
3. `_index.md` + `state.json` + `patterns.json` 同步更新

**禁止：** 只调 memory、说「下次注意」不固化、等用户说「记在CMG」才记。

### 坑点 16: 不要误判 clarify 行为来源（2026-05-28）

用户问"刚才弹选择让我选是谁触发的"，我回答"Hermes 基础设施"。用户纠正：brainstorming、IF、CMG 都会触发 clarify——不是 Hermes 基层。**Clarify 工具是 Hermes 提供的，但什么时候用它、什么条件下触发，是 skill 定义的规则。** CMG 的 ClarifyInterceptor（≥2选项且需决策→必须 clarify）就是其中一种。

- ❌ 「这个选择是 Hermes 基层行为」
- ✅ 「clarify 是 Hermes 工具，触发条件由各 skill 定义：CMG 的 ClarifyInterceptor、IF 的编排逻辑、brainstorming 的交互设计」

### 坑点 17: 发布打包必须逐项审计（2026-05-26）

**症状：** 26/26 功能测试全绿，但打包环节反复出错——ZIP 嵌套路径、桌面旧版本残留、CHANGELOG 日期错、版本号不一致。

**发布前审计：**
1. `grep -r "版本号"` 所有涉及文件，确认全部一致
2. 逐个解压 ZIP，确认顶层目录是包名而非嵌套路径
3. 桌面只保留当前版本文件
4. CHANGELOG 日期用实际发布日期
5. 测试全绿 ≠ 发布就绪。打包是门面。

详见 `references/release-checklist.md`。

CMG SKILL.md 设计的触发条件是「意图识别，非关键词匹配」，但 cmg-guard 插件只做了子串匹配。导致口语化纠正漏过——"你不能这么说话""确认好了再说""你咋老这样"全部漏过。

**过渡方案：** rule_019 已扩充至 18 个关键词。**治本方向：** 双层防御模型——A 插件层（轻量正则否定词扫描）+ B Skill 层（LLM 语义意图判断）。A 负责不漏，B 负责不错。详见 `references/layered-defense-model.md`。

### 坑点 18: 发布后遗留同名副本导致加载歧义（2026-05-28）

**症状：** 发布 v5.5.3 时，先将包安装到 `~/.hermes/skills/canon-mnemonic-guard/`（12:46），后又归类到 `software-development/` 子目录（12:50），但未删除根目录旧副本。导致 Hermes 技能加载时遇到两个同名 `canon-mnemonic-guard` → "Ambiguous skill name… 2 skills match… Refusing to guess"。

**正确做法：** 发布后清理旧位置。`mv`（移动）而非 `cp`（复制），或复制后立即删除源文件。归类操作完成后执行 `ls ~/.hermes/skills/canon-mnemonic-guard ~/.hermes/skills/*/canon-mnemonic-guard 2>/dev/null` 确认唯一性。

### 坑点 19: Guard 不拦截内容覆盖度缺失（2026-05-28）

**症状：** 创建 persistent 文件后声称「记完了」，但遗漏了本会话多个讨论点。

**根因：** CMG 拦截器管行为违规，不管语义层面的内容完整性。

详见当前文档坑点 19 原文。

### 坑点 24: 验证先于结论——动作快过验证（2026-05-29，单次会话 4 次）

**症状：** 本次会话所有错误的上游根因。→ CMG 规则 `ban_act_before_verify`（meta-level）
- 说 Obsidian 能用但从未验证是否安装
- 扫描用固定路径不递归，假警报
- 说 gstack/guard「不能用」但没读代码
- 删文件后才找备份

**修复：** 做断言前三步——1) 证据在哪？2) 亲手验证过吗？3) 不确定就查，查到再开口。

详见 `references/v5.5.5-session-lessons.md`。

- `clarify` **工具**由 Hermes 提供（就像 terminal、web_search 一样）
- `clarify` 的**触发条件**由具体 skill 定义——CMG Guard 的 `ClarifyInterceptor`（"≥2选项且需用户决策 → 必须 clarify"）、brainstorming 的交互设计、IF 的编排逻辑
- **不是** Hermes 自带"遇到选择自动弹窗"的能力

向用户解释时必须区分"谁提供的工具"和"谁触发的调用"。说"Hermes 基层行为"是错的——正确说法是"CMG Guard 防瞎猜规则要求的"，或指出具体是哪个 skill 的规则在驱动。

**教训：** 需要分析因果关系时不能只看表面。用户观察到的"安装 brainstorming 后才出现选择弹窗"是线索——顺着这个线索找到 Guard 的 ClarifyInterceptor 规格才算挖到根。详见 `references/guard-spec.md` 第五层拦截器。

### 坑点 24: 推荐/讨论配套 skill 前必须加载该 skill（2026-05-29）

**症状：** 向用户推荐 obsidian 作为 CMG 配套可视化工具，讨论数周（图谱视图、vault 结构、CMG 规则浏览），但从未加载 obsidian skill。该 skill 明确要求「推荐前先 `ls /Applications/Obsidian.app` 验证」，却因未加载而漏过。用户问「在哪打开图谱视图」时才发现应用根本不存在。

**根因：** CMG 推荐列表里的 obsidian 被当作"已就绪"——vault 文件存在误判为应用已安装。如果每次讨论 obsidian 前加载该 skill，预检步骤会立即暴露缺失。

**正确做法：**
1. 推荐或讨论任何配套 skill 前，必须 `skill_view` 加载该 skill
2. 按 skill 中的预检步骤验证前置条件
3. 不通过预检 → 先帮用户安装/配置，再继续讨论功能
4. vault 文件 ≠ 应用安装——`ls` 验证是唯一可靠方式

### 坑点 26: 结论先于验证——所有局部错误的共同根因（2026-05-29 元规则）

**症状：** 单次会话内出现 4 次同一模式的错误：默认 Obsidian 装了（没验证）、扫描不递归报假缺失（没验证）、说 gstack/guard 不能用（没验证就断言）、删完才找备份（动作排在验证前）。每一次都是同一条链：冲动下结论 → 事后被纠正 → 补记规则。

**根因：** 这不是孤立的 4 个错误——是「验证先于动作」这条元规则没有被内化。CMG 有 56 条 ban 规则但缺少最高层级的约束：**做任何断言前先查证，做任何删除前先确认有备份。**

**正确做法：**
1. 推荐工具前 → `ls` / `pip3 show` / `skill_view` 验证安装状态
2. 说「不能用」前 → 读源码或查文档确认 Hook/指令是否真的不兼容
3. 删文件前 → 确认有备份（源码仓库、本地副本、可恢复路径）
4. 下结论前 → 找到至少一个可追溯的证据来源

**相关规则：** 本坑点被同时记录为 CMG ban 规则 `ban_act_before_verify`（ban 类型，56 条中的第 56 条）。这是「为什么其他规则被反复违反」的上游原因。

### 坑点 25: 全局扫描必须用递归路径，浅扫给出假阴性（2026-05-29）

**症状：** 用户要求「全盘大检查」验证 CMG 推荐列表所有 companion skill 是否安装。第一次扫描用了非递归路径（`ls ~/.hermes/skills/ralph-loop/SKILL.md`），三个 skill 报告为缺失。第二次用 `find ~/.hermes/skills -name SKILL.md | xargs grep -l` 递归扫描——全部在 `software-development/` 子目录下，早已装好。

**教训：** Hermes skills 按类别分布在多层子目录下（`~/.hermes/skills/category/skill-name/`）。任何"检查是否安装"的扫描必须用 `find -name SKILL.md` 递归，不能用 `ls` 顶层目录。浅扫的假阴性比不扫更差——它制造虚假的紧迫感，导致在没问题上浪费时间。

**正确做法：**
1. 检查 skill 是否安装 → `find ~/.hermes/skills -name "SKILL.md" | xargs grep -l "^name: <skill-name>"`
2. 检查 app 是否安装 → `ls /Applications/XXX.app`
3. 检查 pip 包 → `pip3 show <package>`
4. 每条验证命令必须覆盖完整搜索域，不能只搜顶层

### 坑点 22: correction_template 含反斜杠必须用 YAML literal block scalar（2026-05-28）

**症状：** 规则 rule_018（版本号变更必须全文件同步）的 `correction_template` 值为 `grep -rn 'v[0-9]\.[0-9]\.[0-9]' ...`，写在双引号内。YAML 解析时 `\.` 被当作转义序列 → `ScannerError: found unknown escape character '.'`。diagnose Phase 2 报 frontmatter 异常。

**根因：** `correction_template` 经常包含 shell 命令（grep/sed/awk），命令中常有反斜杠。YAML 双引号处理转义序列（`\n`、`\t` 等），`\.` 不是合法转义 → 解析失败。

**正确做法（按优先级）：**
1. **首选 literal block scalar（`|`）：**
   ```yaml
   correction_template: |
     版本号变更后必须全文件 grep 验证：grep -rn 'v[0-9]\.[0-9]\.[0-9]' SKILL.md
   ```
   所有字符原样保留，无需转义。
2. 双引号 + 双重转义：`\\.[0-9]`（容易漏，不推荐）
3. 单引号：不支持内容中有单引号，不推荐

**检查方法：** 写规则后立刻运行 `python3 -c "import yaml; yaml.safe_load(open('规则文件.md').read().split('---')[1])"` 验证。

### 坑点 27: gstack/guard 与 CMG guard 同名冲突（2026-05-29）

**症状：** 用户同时安装 CMG 和 gstack 后，Hermes 技能加载遇到两个 `name: guard` → 歧义报错。

**根因：** CMG 护栏线 skill 的 `name: guard` 与 gstack 的 `/guard` skill 同名。两者功能不同（CMG 守行为层，gstack 守命令层），但 Hermes 按 `name:` 识别 skill，同名即冲突。

**正确做法：**
- **本地解决：** 将 gstack/guard 复制一份，改 `name: gstack-guard`。CMG 的 guard 保持原名（三线命名不可变）
- **未来版本：** init.py 安装时检测同名冲突，自动重命名外部 skill
- **CMG 文档：** 配套 Skill 参考模式标注「⚠️ 与 gstack/guard 同名，需手动改名 gstack-guard」

### 坑点 28: 推荐工具前必须验证安装状态（2026-05-29）

**症状：** CMG 推荐列表里 obsidian 挂了数个版本，文档讨论图谱可视化，但实际 `/Applications/Obsidian.app` 从未存在过。vault 文件存在 ≠ 应用安装。

**根因：** 看到数据文件（~/obsidian/）就假设应用已装。推荐流程没有 `ls` 验证这一步。

**正确做法：** 讨论/推荐任何工具前先 `ls` 验证实际安装。数据目录 ≠ 可执行程序。

### 坑点 23: _index.md 索引与 rules/ 实际文件数漂移（2026-05-28）

**症状：** diagnose Phase 2 报 `_index.md 表格行数: 0 (实际规则: 67)`。实际 _index.md 声称 58 条规则，但 rules/ 目录有 67 条（后来发现是表格行数为 0，标题却写 58——双重不一致）。

**根因：** 每次新增/删除规则文件后，_index.md 不会自动更新。多次操作后漂移累积。

**缓解：**
- diagnose Phase 2 已检测此项（表格行数 vs 实际文件数）
- 发现不一致时建议立即重建（脚本：`python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/rebuild-index.py`）
- 未来方向：固化引擎（!solidify）执行时自动重建 _index.md

### 坑点 21: 推荐付费服务前必须检查用户成本偏好（2026-05-28 两次违反）

**症状：** 向用户推荐付费/有限额服务时，忽略了 memory 中明确记录的「对 token 成本敏感，能省的绝不浪费」。先说 OpenRouter「3毛一次不算贵」，后说 Together AI「充 $5 就行」。用户当场纠正。

**正确做法：**
1. 推荐任何付费/有限额服务前，先查 memory 中的成本偏好
2. 优先推荐免费方案（本地部署、已有 API、免费额度）
3. 付费方案必须标注「备选」+ 具体费用
4. 禁止「不贵」「才几块钱」「充一下就行」等轻描淡写措辞

**根因：** 用户是个人用户不是企业。$5 在开发预算里不算钱，在个人场景是门槛。AI 容易以自己的「开发成本视角」判断费用合理与否。

### 坑点 20: `clarify` 工具与触发源混淆（2026-05-28）

**症状：** 会话中出现 `clarify` 弹窗让用户选择（如"删哪个skill副本？"），用户问"这是哪个skill触发的？"。错误回答"Hermes 基层行为"——被打脸。用户指出：安装 brainstorming 前从未出现过这种弹窗，安装后才出现。

**正确理解：** 
- `clarify` **工具**由 Hermes 提供（就像 terminal、web_search 一样）
- `clarify` 的**触发条件**由具体 skill 定义——CMG Guard 的 `ClarifyInterceptor`（"≥2选项且需用户决策 → 必须 clarify"）、brainstorming 的交互设计、IF 的编排逻辑
- **不是** Hermes 自带"遇到选择自动弹窗"的能力

**教训：** 向用户解释时必须区分"谁提供的工具"和"谁触发的调用"。说"Hermes 基层行为"是错的——正确说法是"CMG Guard 防瞎猜规则要求的"，或指出具体是哪个 skill 的规则在驱动。详见 `references/guard-spec.md` 第五层拦截器。
