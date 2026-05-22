---
name: guard
description: 三省引擎(CMG)护栏线 (Guard) — 规则执行器。读取 Canon 规则库 + Mnemonic 状态，独立执行五层 pre_action 前置拦截。纯执行校验层，不生产规则不存记忆。
version: 4.6.0
role: guard
stage: pre_action
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
metadata:
  hermes:
    tags: [cmg, guard, interception, pre-action]
    related_skills: [canon, mnemonic, canon-mnemonic-guard]
---

# Guard 护栏线 v4.6.0

> **角色**: guard (规则执行器) | **阶段**: pre_action (每次行动前) | **位置**: Canon 之后，所有执行之前
>
> 三省引擎(CMG)护栏线，从 CMG v2.4.1 剥离独立。读取 Canon 的 rules/ 目录作为规则源，读取 Mnemonic 的 state.json 感知上下文。

---

## 文件结构

```
~/.hermes/self-reflection/
├── intercept_log.jsonl      # 拦截日志 (Guard 写入)
├── rules/                   # 规则库 (Canon 生产，Guard 读取)
├── state.json               # 跨会话状态 (Mnemonic 生产，Guard 读取)
├── errors.jsonl             # 原始错误记录 (Canon 写入)
├── patterns.json            # 匹配模式库 (Canon 维护)
└── config.json              # 用户配置
```

---

## 版本变更

| 版本 | 变更 |
|------|------|
| v4.6.0 | +典忆卫・闭环校验器: StepCompleteness拦截后自动逐步骤催办，直到全部闭环。零外部依赖。 |
| v4.5.1 | +SOUL 激活标记检测: 加载时检查 SOUL.md 是否存在 [CMG v] 标记，缺失时提示写入。文档化三种激活方式。 |
| v4.4.0 | 全路径加载 software-development/guard，解决重名冲突 |
| v4.3.1 | 五层拦截器运行时实现 |
| v4.3.0 | +上下文感知拦截规格 |
| v4.2.0 | +拦截效能分析规格 |
| v4.1.0 | +动态清单生成规格 |
| v4.0.0 | 独立化拆分 + 角色声明制 + Interceptor 接口 |

---

## 启动时（Skill 加载）

> **⚠️ 重要：Hermes 技能系统靠任务匹配加载，不自动加载 Guard。** 想让 Guard 在每次对话中自动生效，请通过 CMG 的 init 流程在 SOUL.md 写入激活标记。否则用 `/skill guard` 手动加载。

### 激活方式

| 方式 | 自动 | 操作 |
|------|:---:|------|
| **SOUL 激活标记**（推荐） | ✅ | CMG init 时选 Y → 在 SOUL.md 末尾写入 `[CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则`。Hermes 读到这行后自动加载 CMG → Guard 生效。 |
| `/skill guard` | ❌ | 每次新会话手动输入 |
| `hermes -s guard` | ❌ | 启动时命令行指定 |

SOUL 激活流程详见 canon-mnemonic-guard SKILL.md 的「安装与激活」章节。

### 激活标记检测（v4.5.1 新增）

Guard 加载后检查 SOUL.md 是否存在 `[CMG v` 标记：
- ✅ 存在 → 正常激活
- ❌ 不存在 → 提示：「Guard 已手动加载，但 SOUL.md 中无激活标记，下次新会话不会自动生效。是否写入？[Y/N]」

### 1. 加载 Canon 规则库

读取 `~/.hermes/self-reflection/rules/` 目录，遍历 ban/gap/lazy 三类规则，解析 frontmatter 中的 type、keywords、tags，构建拦截匹配表。

### 2. 加载 Mnemonic 状态

读取 `~/.hermes/self-reflection/state.json`，获取跨会话状态（会话计数、引擎健康指标、上下文豁免标记）。

### 3. 效能分析（G4 · v4.5.0）

**每次加载时自动执行。** 分析 `intercept_log.jsonl` 中的拦截记录，计算每条规则的效能指标，自动调整拦截策略。

**执行步骤：**

```
1. 读取 intercept_log.jsonl → 按 rule_id 分组统计
2. 对每条规则计算:
   - hit_rate = 命中次数 ÷ 会话数（自规则创建起）
   - false_positive_rate = 误报次数 ÷ 命中次数
   - days_since_last_hit = now - last_triggered
3. 自动调整:
   - false_positive_rate > 30% → 该规则降级: 拦截→提醒
     → 输出: "⚠️ 规则 [{rule_id}] 误报率 {N}% > 30%，已降级为提醒。"
   - days_since_last_hit > 180 → 标记过期
     → 输出: "📅 规则 [{rule_id}] {N} 天未命中，可能已过时。建议 !diagnose 复查。"
   - hit_rate 最高前 3 条 → 严格拦截（不可跳过）
   - hit_rate 最低后 3 条 → 仅提醒（可跳过）
4. 回写 rules/ 中对应规则的 frontmatter（hit_count / false_positives / last_triggered）
```

**降级：** intercept_log.jsonl 不存在或为空 → 跳过效能分析，默认拦截策略。

### 4. 上下文感知检测（G3 · v4.5.0）

**每次加载时自动执行。** 扫描拦截日志中的时间模式，调整 Guard 运行参数。

**执行步骤：**

```
1. 重复错误检测:
   - 扫描 intercept_log.jsonl 最近 5 分钟窗口
   - 同一 rule_id 出现 ≥ 3 次 → 升级该规则拦截级别: 提醒→警告→阻断
     → 输出: "🔥 规则 [{rule_id}] 5分钟内触发 {N} 次，拦截已升级为阻断。"

2. 赶工模式检测:
   - 扫描最近 10 次拦截记录
   - StepCompletenessInterceptor 命中 ≥ 4 次 → 检测到赶工模式
     → 全局提升拦截敏感度（所有规则从严）
     → 输出: "⚡ 检测到赶工模式（连续跳步骤），全局拦截敏感度已提升。"

3. 轻量模式切换:
   - 读取 rules/ 目录 → 统计规则总数
   - 规则数 > 20 条 → 切换轻量模式: 只跑 BanInterceptor（第一层），跳过 Fabrication / StepCompleteness / SkillLoad / Clarify
     → 输出: "💡 规则库 {N} 条（>20），已切换轻量模式（仅精确匹配拦截）。"

4. 用户豁免检测:
   - 用户输入含「跳过检查」「免检」「skip guard」「不用检查」→ 本次会话临时放行
   - 写入 state.json: exemptions.active = true, exemptions.expires_at = session_end
     → 输出: "⏸️ 本次会话 Guard 拦截已暂停（用户豁免）。"
```

**降级：** intercept_log.jsonl 不存在 → 跳过重复错误检测和赶工检测。规则数统计失败 → 不切换轻量模式。

### 5. 动态清单生成（G2 · v4.5.0）

**每次加载时自动执行。** 不再依赖静态 `checklists/*.yaml` 文件——直接从 `errors.jsonl` 实时生成。

**执行步骤：**

```
1. 读取 errors.jsonl → 提取所有错误记录
2. 按任务类型分类:
   - 论文类: 搜索"论文/essay/字数/文献/引用/格式/abstract"关键词
   - 代码类: 搜索"代码/code/PR/commit/test/CI"关键词
   - 通用类: 不匹配以上两类的归入
3. 每类提取高频遗漏（同一错误 ≥ 3 次）→ 生成动态检查项
4. 补充默认项（最近 7 天 errors.jsonl 中首次出现的错误类型）
5. 注入系统提示作为检查清单

生成示例:
  动态清单 - 论文类:
    1. [高频] 论文字数检查（近7天遗漏3次）
    2. [高频] 参考文献格式验证（近7天遗漏3次）
    3. [新增] 摘要字数限制（首次出现于05-20）
    4. [默认] 文件保存确认

  动态清单 - 通用类:
    1. [高频] Skill 加载检查（近7天遗漏5次）
    2. [新增] 版本号同步验证（首次出现于05-19）
```

**降级：** errors.jsonl 不存在或为空 → 回退静态清单（如果 `checklists/` 目录有 YAML 文件），否则输出 "无可用的检查清单（errors.jsonl 为空且无静态清单）。"

### 6. 初始化拦截日志

如 `~/.hermes/self-reflection/intercept_log.jsonl` 不存在则创建空文件。

### 7. 输出激活状态

**必须输出**: "Guard v4.6.0 已激活。读取 Canon {N} 条规则。效能分析: {X} 条规则正常 / {Y} 条降级 / {Z} 条过期。上下文感知: {重复检测/赶工检测/轻量模式} 就绪。动态清单: {论文类K项/代码类L项/通用类M项}。"

---

## 五层拦截器 — 运行时执行

> **每次行动前强制执行。** 以下检查不是规格文档——是必须执行的步骤。跳过任一步骤即违规。

### 执行流程（不可跳过）

```
每个动作前:
  1. 读取 Canon rules/ 目录 → 构建关键词匹配表
  2. 逐条执行以下五层检查
  3. 任一层命中 → 拦截 + 写入 intercept_log.jsonl + 更新 Canon 评分
  4. 全部通过 → 放行
```

### 轻量模式（G3 · v4.5.0）

当规则数 > 20 条时自动激活：只跑第一层 BanInterceptor，跳过其余四层。拦截日志中标注 `mode: lightweight`。

---

### 第一层：BanInterceptor — 精确关键词匹配

**检查方法：** 当前思考/输出文本 → 逐条比对 patterns.json 中 ban 类所有 keywords → 任一命中即拦截。

**执行步骤：**
```
1. 读取 ~/.hermes/self-reflection/patterns.json → 提取 ban.keywords 列表
2. 将当前准备输出的文本与 keywords 逐条比对
3. 命中 → 拦截，输出: "⛔ 拦截。命中规则: [{rule}]。"
4. 写入 intercept_log.jsonl: {\"interceptor\":\"Ban\",\"action\":\"block\",\"rule_id\":\"...\",\"reason\":\"关键词匹配: {keyword}\"}
5. 回写 Canon rules/ 中对应规则的 hit_count += 1
```

### 上下文升级拦截（G3 · v4.5.0）

同一 rule_id 在 5 分钟内已被拦截 ≥ 2 次（即本次为第 3 次）→ 升级 action：
- 第 1-2 次: `action: warn`
- 第 3+ 次: `action: block`（强制阻断，不可跳过）

intercept_log.jsonl 中标注 `context_level: escalated`。

---

### 第二层：FabricationInterceptor — 防幻觉声称

**检查方法：** 识别"声称型语句"，逐条核实是否真实存在。

**触发词：** 我能 / 我有 / 我会 / 已经创建了 / 存在 / 已安装 / 已完成 / 已验证 / 确认无误

**执行步骤：**
```
1. 扫描即将输出的文本，匹配触发词
2. 对每一条声称:
   - 声称 Skill → 调用 skills_list 核实是否存在
   - 声称 API → 调用 web_search 或查 memory 核实
   - 声称数据 → 查原始 source 核实
3. 任一条无法核实 → 拦截: "⛔ 拦截。声称 [{claim}] 无法核实。"
4. 写入 intercept_log.jsonl
```

---

### 第三层：StepCompletenessInterceptor + 典忆卫・闭环校验器

> **v4.6.0: 拦截 + 监工一体化。** 不再只拦——剩余步骤 ≥ 2 时，自动进入逐步骤催办模式，直到全部闭环。

**检查方法：** 用户原始指令拆解为步骤列表，对比已完成步骤。

**执行步骤：**

```
1. 提取用户原始指令 → 拆解为步骤列表(编号)
2. 从上下文提取已完成步骤
3. 对比: 未完成步骤 = 全部步骤 - 已完成步骤
4. 有未完成步骤 → 拦截
5. 写入 intercept_log.jsonl

拦截后的分支:

  ├── 剩余步骤 = 1 步
  │   → 输出: "⚠️ 还有 1 步未完成: {step}。执行后继续。"
  │
  └── 剩余步骤 ≥ 2 步
      → 启动「典忆卫・闭环校验器」:
```

#### 典忆卫・闭环校验器

**触发条件：** StepCompletenessInterceptor 拦截 + 剩余步骤 ≥ 2。

**核心原则：** 不依赖外部工具、不写文件、不委派子 Agent。典忆卫用自己的规则体系和会话上下文，逐条引导 Agent 完成剩余步骤。

**执行流程：**

```
1. 宣告进入监工模式:
   "⛔ 典忆卫规则: 任务必须完整执行。
    当前检测到 {N} 步未完成:
      1. {步骤一}
      2. {步骤二}
      ...
    进入逐步骤闭环校验——每步执行后验证，全部通过才放行。"

2. 逐步骤催办 (for i = 1 to N):
   ┌─────────────────────────────────────────┐
   │ [{i}/{N}] {步骤描述}                     │
   │                                         │
   │ 典忆卫指令: 请执行以上步骤，完成后明确    │
   │ 说明「步骤 {i} 已完成」并附验证证据。     │
   │                                         │
   │ Agent 执行 → Guard 核查:                 │
   │   - 该步骤确有产出？                     │
   │   - 有验证证据？（文件存在/测试通过/...） │
   │   ✅ 通过 → 标记完成，进入下一步          │
   │   ❌ 未通过 → "步骤 {i} 验证未通过。      │
   │               缺少: {验证项}。请补充。"    │
   └─────────────────────────────────────────┘

3. 全部通过:
   "✅ 典忆卫闭环校验: {N}/{N} 步骤全部完成。
    任务完整闭环，放行。"
```

**闭环校验器的验证标准：**

| 步骤类型 | 验证要求 |
|---------|---------|
| 写代码 | 文件存在 + 语法检查通过 |
| 写文档 | 文件存在 + 字数/格式达标 |
| 搜索/查询 | 返回了实际结果（非编造） |
| 安装/配置 | 命令执行成功（exit code 0） |
| 分析/计算 | 计算过程可追溯 + 结果明确 |

**与 ralph-loop 的关系：**

典忆卫内置的闭环校验器处理**当前会话的单任务步骤遗漏**——从对话上下文直接提取，零配置，即时生效。

当任务规模超出单会话范围（跨会话项目、多文件迁移、批量重构），推荐搭配 `ralph-loop` 使用。ralph-loop 提供项目级任务队列、持久化进度、子 Agent 委派等进阶能力。

> **设计声明：** 典忆卫・闭环校验器是完全原生的监工机制。它使用典忆卫自己的规则体系、拦截器框架和对话上下文分析能力。不依赖、不复用、不兼容 ralph-loop 的数据结构或执行模型——两者是独立设计、各自完整的系统。ralph-loop 作为可选进阶工具，仅推荐给有复杂项目管理需求的用户。

### 赶工模式联动（G3 · v4.5.0）

全局赶工模式激活时（启动检测到连续 ≥ 4 次 StepCompleteness 命中），闭环校验器升级：
- 正常: 逐步骤催办，每步等待 Agent 确认
- 赶工: 「🛑 赶工模式：剩余步骤全部并行催办。不得跳过任何一步。」

---

### 第四层：SkillLoadInterceptor — 防偷懒

**检查方法：** 当前任务领域是否加载了对应 Skill。

**执行步骤：**
```
1. 提取当前任务领域关键词(论文→学术,代码→开发,金融→数据…)
2. 扫描 skills_list → 匹配领域 Skill
3. 检查是否已通过 skill_view 加载
4. 0 个匹配 Skill 已加载 → 拦截: "⚠️ 领域 Skill 未加载。搜索可用 Skill 并加载。"
5. 写入 intercept_log.jsonl
```

---

### 第五层：ClarifyInterceptor — 防瞎猜

**检查方法：** 多选项场景是否调用了 clarify。

**执行步骤：**
```
1. 判断: 当前步骤是否 ≥2 个可选项且需用户决策
2. 检查: 是否已调用 clarify
3. 未调用 → 拦截: "⚠️ 需用户决策，调用 clarify。"
4. 写入 intercept_log.jsonl
```

---

## 评分计数器

每次拦截检查后，更新 Canon rules/ 目录中对应规则的 frontmatter：

```
命中时: hit_count += 1, last_triggered = now()
误报时: false_positives += 1 (用户说「这不是错误」后回调写入)
```

Canon 固化引擎运行时读取 hit_count / false_positives 计算评分。高分规则严格拦截，低分规则降级为提醒。

### 效能分析自动调优（G4 · v4.5.0）

Guard 加载时已执行效能分析。运行时额外：

- 拦截命中时 → 检查该规则是否在「降级列表」中 → 如果是，仍输出但标注 `downgraded: reminder_only`
- 拦截命中时 → 检查该规则是否在「过期列表」中 → 如果是，仍输出但标注 `stale: may_be_outdated`

---

## 拦截日志

每次拦截写入 `intercept_log.jsonl`：

```json
{"ts":"ISO8601","interceptor":"Ban","rule_id":"rule_001","action":"block","reason":"关键词匹配: 虚构","context":"用户要求输出一个不存在的API","mode":"full","context_level":"normal"}
```

v4.5.0 新增字段:
- `mode`: `full`（五层全跑）或 `lightweight`（仅第一层）
- `context_level`: `normal` / `escalated`（上下文升级）

---

## 与 Canon / Mnemonic 联动

```
Canon (producer, system_anchor)
    │  生产 rules/*.md + patterns.json + errors.jsonl
    ▼
Guard (guard, pre_action)
    │  读取 Canon 规则 → 五层拦截 → 命中/误报计数
    │  写入 intercept_log.jsonl
    ▼
Mnemonic (memory, background)
    │  读取 intercept_log.jsonl → 自动模式识别 → 推送规则草稿至 Canon
    ▼
Canon 固化引擎 → 去重 → 写入 rules/
```

---

## 安装

```bash
npx skills add guard --yes --global
```

或从 Canon Mnemonic Guard 仓库独立获取。

---

## 常见坑点

### 坑点 1: Guard 不会自动加载

Hermes 的技能系统靠任务匹配加载——没有「always-load」概念。用户安装 Guard 后，Guard 不会在每次对话中自动出现。必须通过以下方式之一激活：

1. **SOUL 激活标记**（推荐）— CMG init 写一行到 SOUL.md
2. `/skill guard` 手动触发
3. `hermes -s guard` 启动参数

**检测：** 查看 SOUL.md 中是否有 `[CMG v` 标记。没有 → Guard 未自动激活。

### 坑点 2: 不要给模糊结论

Guard 加载后必须输出确凿的激活状态。「应该已激活」「可能生效了」这类表述本身就是 Guard 要拦截的模式（ban_vague_answers 规则）。验证到确定为止。

### 坑点 3: intercept_log 需要有效 timestamp

手工填充的测试数据（timestamp=?）会导致效能分析（G4）全部失败。intercept_log 的每条记录必须有真实 ISO8601 时间戳。

### 坑点 4: 版本号变更必须四包同步 grep

CMG 四包制（canon/guard/mnemonic/canon-mnemonic-guard）升版时，只改 frontmatter `version:` 字段远远不够。散布在 SKILL.md 中的激活消息、注入消息、当前标记、标题全部含硬编码版本号。v5.2.0→v5.2.1 再次验证了这一点：注入消息「三省引擎 v5.2.0」、激活消息「v5.2.0 已激活」滞后。

**正确做法：** 升版后跑 `grep -rn 'v[0-9]\.[0-9]\.[0-9]'` 四包全部 SKILL.md，确保只出现新版本号。

### 坑点 5: Guard 功能验证必须实际触发

文档写完不等于功能通。v5.2.1 发布前 Guard 的五层拦截器有完整规格但从未在真实对话中拦截过。端到端测试方法：

```
BanInterceptor:        让 Agent 说「编造一个不存在的 Skill」→ 应拦截
FabricationInterceptor: 让 Agent 声称「已全部完成」但实际有未完成项 → 应拦截
StepCompleteness:      指令含多步骤，Agent 跳过一步 → 应拦截
```

每次发布前必须跑一遍这三项。v5.2.1 发布时终于跑了前两项并通过。
