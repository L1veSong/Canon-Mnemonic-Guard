# Canon-Mnemonic-Guard 三省引擎 v5.5.1

> **典则·忆存·护栏** — AI 的错题本、免疫系统、监工。取自「吾日三省吾身」。
> 你只需指出一次错误，它从此记住。**v5.5.1：skill-autoload 插件自动加载，零手动。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.5.1-blue)]()

---

```
                         +------------------+
                         |    CMG  v5.5.1    |
                         +--------+---------+
                                  |
             +--------------------+--------------------+
             |                    |                    |
     +----------------+  +----------------+  +----------------+
     |     Canon      |  |     Guard      |  |    Mnemonic    |
     |     v2.7.1     |  |     v4.8.1     |  |     v3.5.2     |
     +-------+--------+  +-------+--------+  +-------+--------+
             |                   |                   |
        规则生产              拦截执行              模式识别
    你说「记住」→写入     五层前置→命中就拦     从日志学→推草稿

    微型调度 + 四包索引 + 自动加载
```

### 🆕 v5.5.1 新特性

**skill-autoload 插件自动加载。** 不用再手动 `/skill` 或依赖 SOUL 标记——CMG 每次会话自动生效。

```yaml
# ~/.hermes/config.yaml
skill_autoload:
  skills:
    - canon-mnemonic-guard
```

配合 [skill-autoload](https://github.com/L1veSong/skill-autoload) 插件（本合集自带），配置即生效。飞书/微信等平台可单独关闭。

---

## 它解决什么

和 AI 协作时，最烦的不是犯错——是**同一个错误反复犯**。

"别编造 API""加载 skill 再干活""发布前检查版本号"……你说了十遍，它还是忘。

三省引擎让你**只说一遍**。说完，它写入规则。下次，它自动拦截。再下次，它从拦截日志中学到新模式，推给你确认。

```
  你纠正一次  ──▶  Canon 写入规则
  下次自动拦  ──▶  Guard 五层拦截
  从日志中学  ──▶  Mnemonic 发现模式 ──▶ 推草稿 ──▶ 你确认 ──▶ 规则+1
```

54 条规则，没有一条是预设的。全部从你的实际使用中生长出来。

---

## 怎么跑起来的

> 框内英文仅为对齐，对应中文见框外说明。

```
  +------------------------------------------------------+
  |                                                      |
  |  Make a mistake --> Say "remember this"              |
  |    |                                                 |
  |    v                                                 |
  |  Canon: write rule, dedup, conflict check, score     |
  |    |                                                 |
  |    v                                                 |
  |  Guard: 5-layer interception                         |
  |    |  . Ban          --> keyword match --> block     |
  |    |  . Fabrication  --> verify claim  --> block     |
  |    |  . StepComplete --> check remaining steps       |
  |    |  . SkillLoad    --> remind to load skill        |
  |    |  . Clarify      --> ask user first              |
  |    v                                                 |
  |  Write intercept_log.jsonl                           |
  |    |                                                 |
  |    v                                                 |
  |  Mnemonic: analyze patterns                          |
  |    |  . Same session >= 2 hits --> draft rule        |
  |    |  . Cross-session >= 2 hits --> draft rule       |
  |    v                                                 |
  |  Confirm --> Canon solidify --> +1 rule               |
  |                                                      |
  +------------------------------------------------------+
```

> 犯错 → 说「记住」→ Canon 写规则（去重/冲突检测/评分）→ Guard 五道闸拦截（Ban 关键词/Fabrication 防幻觉/StepComplete 催办/SkillLoad 提醒/Clarify 先问）→ 写入拦截日志 → Mnemonic 分析（同会话≥2次推草稿/跨会话≥2次推草稿）→ 确认 → 固化 → 规则+1

---

## 四个组件

### 📜 Canon 典则线 — 规则生产库

> "你说 '记住'，我把它变成规则。"

| 能力 | 说明 |
|------|------|
| 规则分级 | hard / soft / monitor 三级，含修正模板（告诉 AI 怎么改） |
| 误报降级 | 连续否决 ≥ 3 次 → 自动降为 soft |
| 规则有效期 | `!remember --expires 7d` → 到期自动归档 |
| 扫盘提取 | 自动扫描 SOUL.md / Obsidian / Memory 中的准则 |
| 定时扫盘 | 每 7 天自动触发，新装 skill 准则自行纳入 |

### 🛡️ Guard 护栏线 — 规则执行器

> "每次行动前查五道闸，命中就拦。"

```
  AI 准备行动
    |
    +-- 1. Ban           --> 关键词命中？拦
    +-- 2. Fabrication   --> 幻觉声称？核实 --> 拦
    +-- 3. StepComplete  --> 还有步骤没做？催
    +-- 4. SkillLoad     --> skill 没加载？提醒
    +-- 5. Clarify       --> 该问用户没问？拦
    |
    v
  全部通过 --> 放行
```

- 同会话第 2 次命中 → 直接 block（原 3 次），24h 半衰期防误伤
- 你说「记住」「别再犯」→ 规则自动升一级
- 闭环重试：拦截 → 注入修正方向 → AI 重生成 → 再检 → 合格放行
- 风险分级：删文件 / 覆盖 → 暂停确认。格式错误 → 自动修。

### 🧠 Mnemonic 忆存线 — 模式识别

> "我从拦截日志里发现规律。"

```
  intercept_log.jsonl
    |
    v
  按 session_id 分组统计
    |
    +-- 同会话 >= 2 次     --> 立即推草稿 (置信度 0.7)
    +-- 跨会话 >= 2 次     --> 推草稿     (置信度 0.5)
    +-- 置信度 < 0.5       --> 只记录，不推送
    |
    v
  你确认 --> Canon 固化 --> 新规则诞生
```

`!patterns` 随时查看当前识别到的模式。`!datasource` 看数据源健康状态。

### 🎯 CMG 外观层 — 微型调度器

> "拦截了 → 告诉你该加载哪个配套 skill。"

| 拦截场景 | 自动推荐 |
|----------|----------|
| 过设计 / 复杂化 | karpathy-coding-guidelines |
| 跳步骤 / 没闭环 | ralph-loop |
| "已经完成了"（没验证） | verification-before-completion |
| 同一规则连续命中 ≥ 3 次 | diagnose |

已装未加载 → 提醒加载。没装 → 提醒安装。已加载 → 安静。

---

## ⚡ 自动加载（推荐）

安装 skill-autoload 插件，CMG 在每次会话自动生效：

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - skill-autoload

skill_autoload:
  skills:
    - canon-mnemonic-guard
  per_platform:
    feishu: []
    weixin: []
```

> 需要 Hermes 包含 `pre_system_prompt` 钩子。PR 已提交至 NousResearch/hermes-agent，合入前可本地 patch。

---

## 装起来

```bash
# 一行安装
npx skills add canon-mnemonic-guard --yes --global
npx canon-mnemonic-guard init

# init 最后一步：
#   "是否在 SOUL.md 写入激活标记？[Y/n]"
#   选 Y → 每次对话自动生效
#   选 N → 手动 /skill canon-mnemonic-guard 触发
```

```
安装后 ~/.hermes/self-reflection/ 长这样：

  rules/
  ├── ban/     ←  36 条禁止项
  ├── gap/     ←   8 条缺失项
  └── lazy/    ←   9 条偷懒项
  errors.jsonl           ← 原始错误记录
  patterns.json          ← 匹配模式库
  state.json             ← 跨会话状态
  intercept_log.jsonl    ← Guard 拦截日志
  mnemonic_state.json    ← Mnemonic 记忆
  config.json            ← 用户配置
```

规则全是 `.md` 文件，直接用 Obsidian 浏览、Dataview 查询、图谱链接。

---

## 口中念念有词

| 念什么 | 出什么 |
|--------|--------|
| `!remember "禁止xxx"` | 记一条规则（支持 --hard / --soft / --expires 7d） |
| `!scan` | 扫一遍 SOUL / Obsidian / Memory，提取准则 |
| `!patterns` | 规则 / 本会话命中 / 7天 / 置信度 / 该不该固化 |
| `!datasource` | 当前数据源是谁、健康吗、切换过几次 |
| `!solidify` | 把 errors.jsonl 固化成 rules/ 里的规则 |
| `!log` | Canon + Guard + Mnemonic 三线日志一张表 |
| `!diagnose` | 五阶段深度体检：文件 → 规则 → 引用 → 数据 → 版本 |
| `!export` / `!import` | 打包规则 ZIP / 从 ZIP 导入（含冲突检测） |

---

## 带上这些更强

**护栏线（拦截执行 · 验证闭环）**

| 推荐 | 增强点 |
|------|--------|
| skill-autoload | 自动加载 CMG，零手动 |
| ralph-loop | 跳步骤 → 闭环验证 |
| verification-before-completion | 声称完成 → 证据协议 |
| diagnose | 连续命中 → 根因诊断 |
| karpathy-coding-guidelines | 进攻型行为准则（已双向认可） |

**典则线（规则扩展 · 可视化）**

| 推荐 | 增强点 |
|------|--------|
| plur | 扩展规则来源 |
| obsidian | rules/ 可视化浏览 |

**跨线共享（基础设施）**

| 推荐 | 增强点 |
|------|--------|
| rtk-rewrite | 压缩 token 60-90%（Gateway 插件） |
| hermes-agent-skill-authoring | 13 项发布自检清单 |

**参考模式** — gstack/careful、gstack/guard（命令层安全，Hermes hook 限制）

---

## 走过的路

```
  v5.0.0 ── 三线合一
  v5.1.0 ── 四包制分装
  v5.2.0 ── 定时扫盘 + 协调日志 + 一键诊断
  v5.3.0 ── Guard 风险分级
  v5.4.0 ── P1+P3+P4 + 上下文保留           ← 大更
  v5.4.1 ── P2 补全（Mnemonic 加速）
  v5.4.2 ── M3 清零（!patterns + !datasource）
  v5.5.0 ── 微型调度器
  v5.5.1 ── skill-autoload + 生态合集发布     ← 当前
  ─────────────────────────────────────────
  未来    ── 完整中央调度器（独立项目）
```

**P 系列全家福：** P1 同会话升级 ✅ · P2 加速模式识别 ✅ · P3 用户纠正提升 ✅ · P4 误报降级+有效期 ✅ · P5 傻瓜/专家模式 ⏳

---

## 你可能想问

**规则库跟 ZIP 一起发布吗？**

不。`rules/` 在 `~/.hermes/self-reflection/` 下，是你本地的，不打包。别人装了 CMG，规则库从零开始，踩自己的坑，长自己的记性。

**跟我已装的 skill 会打架吗？**

不会。CMG 用 stage 声明制排队——按"锚点 → 护栏 → 调度 → 执行"的固定顺序。CMG 在 pre_action 位置，在所有 skill 干活之前检查。

**规则太多会不会卡？**

规则超过 20 条自动切轻量模式——只跑第一道闸（精确匹配），跳过后面四道。54 条规则不影响速度。

---

MIT · [L1veSong](https://github.com/L1veSong)
