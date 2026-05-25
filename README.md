# CMG 三省引擎 生态系统 v5.5.2

> **典则·忆存·护栏 + 自动加载 + 硬拦截。** 六合一完整包。AI 的错题本、免疫系统、监工。
> 你指出一次错误，它从此记住。**v5.5.2：默认固化阈值10→3，修复init.py版本号滞后。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.5.2-blue)]()

---

## 包里有什么

```
                         +------------------+
                         |   CMG  v5.5.2    |  ← 外观层·微型调度器
                         +--------+---------+
                                  |
             +--------------------+--------------------+
             |                    |                    |
     +----------------+  +----------------+  +----------------+
     |     Canon      |  |     Guard      |  |    Mnemonic    |
     |    v2.7.2      |  |     v4.8.2     |  |     v3.5.3     |
     +-------+--------+  +-------+--------+  +-------+--------+
             |                   |                   |
          规则生产              拦截执行              模式识别
      你说「记住」→写入       五层前置→命中就拦       从日志学→推草稿

    +------------------+                +------------------+
    |  skill-autoload  |                |    cmg-guard     |
    |     v1.0.0       |                |     v1.0.0       |
    +-------+----------+                +-------+----------+
            |                                   |
     会话开始强制加载 CMG                    AI 输出前硬拦截替换
    (pre_system_prompt)                (transform_llm_output)
```

**六组件分工：**

| 组件 | 版本 | 类型 | 职责 |
|------|------|------|------|
| canon-mnemonic-guard | v5.5.2 | Skill | 三省引擎主包 · 微型调度器 · 四包索引 |
| canon | v2.7.2 | Skill | 典则线 — 规则生产 · 固化引擎 · 扫盘 |
| guard | v4.8.2 | Skill | 护栏线 — 五层拦截 · 闭环重试 · 风险分级 |
| mnemonic | v3.5.3 | Skill | 忆存线 — 模式识别 · 自动推草稿 · 数据源管理 |
| skill-autoload | v1.0.0 | Plugin | 会话开始时强制加载 CMG（pre_system_prompt 钩子） |
| cmg-guard | v1.0.0 | Plugin | AI 输出前硬拦截（transform_llm_output 钩子） |

---

## 它解决什么

和 AI 协作时，最烦的不是犯错——是**同一个错误反复犯**。

"别编造 API""加载 skill 再干活""发布前检查版本号"……你说了十遍，它还是忘。

三省引擎让你**只说一遍**。说完，它写入规则。下次，它自动拦截。再下次，它从拦截日志中学到新模式，推给你确认。

而插件层让这一切**不可绕过**——skill-autoload 保证 CMG 不被遗忘，cmg-guard 保证违规内容到不了你的眼睛。

```
  你纠正一次  ──▶  Canon 写入规则
  下次自动拦  ──▶  Guard 五层拦截
  从日志中学  ──▶  Mnemonic 发现模式 ──▶ 推草稿 ──▶ 你确认 ──▶ 规则+1

  每次会话    ──▶  skill-autoload 自动加载 CMG
  每次输出    ──▶  cmg-guard 扫描，违规就替换
```

---

## 怎么跑起来的 — 三层闭环

```
  Layer 1: skill-autoload (Plugin)
    pre_system_prompt 钩子 → 系统提示词注入 MUST-LOAD 指令
    → AI 在每个会话开始时自动加载 CMG 四包
                ↓
  Layer 2: CMG 四包 (Skills)
    Canon    → 你说「记住」→ 写入 rules/ban/*.md
    Guard    → 每次行动前查五道闸 → 命中就拦
    Mnemonic → 从 intercept_log.jsonl 学 → 推草稿
    调度器   → 拦截了 → 告诉你该加载哪个配套 skill
                ↓
  Layer 3: cmg-guard (Plugin)
    transform_llm_output 钩子 → AI 回复后扫描全文
    → 命中 ban 关键词 → 直接替换为拦截消息
    → 用户看到的是修正后的输出，违规内容不存在
```

**为什么需要三层？**

Skill 层靠 AI 自觉——可以绕过。Plugin 层在 Hermes 内核执行——AI 没有机会跳过。

cmg-guard 已实测：AI 想说"好问题"，被 `禁止废话开头` 规则命中 → 输出被替换为 `[CMG 拦截] 请遵守规则重新回答` → AI 下一轮自动修正。

---

## 六组件详解

### 📜 Canon 典则线 v2.7.2 — 规则生产库

> "你说 '记住'，我把它变成规则。"

| 能力 | 说明 |
|------|------|
| 规则分级 | hard / soft / monitor 三级，含修正模板（告诉 AI 怎么改） |
| 误报降级 | 连续否决 ≥ 3 次 → 自动降为 soft |
| 规则有效期 | `!remember --expires 7d` → 到期自动归档 |
| 扫盘提取 | 自动扫描 SOUL.md / Obsidian / Memory 中的准则 |
| 定时扫盘 | 每 7 天自动触发，新装 skill 准则自行纳入 |
| 冲突检测 | 新规则写入前自动检测与已有规则冲突 |
| 导入导出 | `!export` / `!import` 打包规则 ZIP |

### 🛡️ Guard 护栏线 v4.8.2 — 规则执行器

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

- 同会话第 2 次命中 → 直接 block（24h 半衰期防误伤）
- 你说「记住」「别再犯」→ 规则自动升一级
- 闭环重试：拦截 → 注入修正方向 → AI 重生成 → 再检 → 合格放行
- 风险分级：删文件/覆盖 → 暂停确认。格式错误 → 自动修。

### 🧠 Mnemonic 忆存线 v3.5.3 — 模式识别

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

`!patterns` 看当前识别到的模式。`!datasource` 看数据源健康状态。

### 🎯 CMG 外观层 v5.5.2 — 微型调度器

> "拦截了 → 告诉你该加载哪个配套 skill。"

| 拦截场景 | 自动推荐 |
|----------|----------|
| 过设计 / 复杂化 | karpathy-coding-guidelines |
| 跳步骤 / 没闭环 | ralph-loop |
| "已经完成了"（没验证） | verification-before-completion |
| 同一规则连续命中 ≥ 3 次 | diagnose |

### 🔌 skill-autoload v1.0.0 — 自动加载

> "每次会话开始时，强制加载 CMG。"

注册 `pre_system_prompt` 钩子。在系统提示词构建后、发送给 LLM 前，注入 MUST-LOAD 指令。按平台配置，飞书/微信可单独关闭。

```yaml
# ~/.hermes/config.yaml
skill_autoload:
  skills:
    - canon-mnemonic-guard
  per_platform:
    feishu: []
    weixin: []
```

### 🚫 cmg-guard v1.0.0 — 硬拦截

> "AI 的输出不经过检查到不了你的眼睛。"

注册 `transform_llm_output` 钩子。每次 AI 生成回复后，扫描输出全文，命中 ban 规则关键词 → 直接替换。AI 绕不过去——这是在 Hermes 内核层执行的。

- 读取 `~/.hermes/self-reflection/rules/ban/*.md` 的关键词
- 37 条 ban 规则自动加载
- 命中 → 替换为 `[CMG 拦截] 请遵守 CMG 规则重新回答`

---

## 装起来

### 完整安装（六合一）

```bash
# 1. 安装 Skill 包
npx skills add canon-mnemonic-guard --yes --global
npx canon-mnemonic-guard init

# 2. 安装 Plugin（从本合集复制）
cp -r skill-autoload ~/.hermes/plugins/
cp -r cmg-guard ~/.hermes/plugins/
```

### 配置

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - skill-autoload
    - cmg-guard

skill_autoload:
  skills:
    - canon-mnemonic-guard
  per_platform:
    cli: [canon-mnemonic-guard]
    feishu: []
    weixin: []
```

> Plugin 需要 Hermes 包含 `pre_system_prompt` / `transform_llm_output` 钩子。

### init 后长这样

```
~/.hermes/self-reflection/
  rules/
  ├── ban/     ←  禁止项（你的规则在这）
  ├── gap/     ←  缺失项
  └── lazy/    ←  偷懒项
  errors.jsonl           ← 原始错误记录
  patterns.json          ← 匹配模式库
  state.json             ← 跨会话状态
  intercept_log.jsonl    ← Guard 拦截日志
  mnemonic_state.json    ← Mnemonic 记忆
  config.json            ← 你的配置
```

规则全是 `.md` 文件，直接 Obsidian 浏览、Dataview 查询、图谱链接。

---

## 口中念念有词

| 念什么 | 出什么 |
|--------|--------|
| `!remember "禁止xxx"` | 记一条规则（支持 --hard / --soft / --expires 7d） |
| `!scan` | 扫一遍 SOUL / Obsidian / Memory，提取准则 |
| `!patterns` | 当前识别的重复模式 / 命中次数 / 置信度 |
| `!datasource` | 数据源是谁、健康吗、切换过几次 |
| `!solidify` | 把 errors.jsonl 固化成 rules/ 里的规则 |
| `!log` | Canon + Guard + Mnemonic 三线日志一张表 |
| `!diagnose` | 五阶段深度体检：文件 → 规则 → 引用 → 数据 → 版本 |
| `!export` / `!import` | 打包规则 ZIP / 从 ZIP 导入（含冲突检测） |

---

## 带上这些更强

**护栏线（拦截执行 · 验证闭环）**

| 推荐 | 增强点 |
|------|--------|
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
  v5.5.1 ── 三层闭环 (skill-autoload + cmg-guard 首次发布)
  v5.5.2 ── 默认固化阈值10→3，修复init.py版本号滞后  ← 当前
  ─────────────────────────────────────────
  未来    ── 完整中央调度器（独立项目）
```

**P 系列全家福：** P1 同会话升级 ✅ · P2 加速模式识别 ✅ · P3 用户纠正提升 ✅ · P4 误报降级+有效期 ✅ · P5 傻瓜/专家模式 ⏳

---

## 你可能想问

**规则库跟 ZIP 一起发布吗？**

不。`rules/` 在 `~/.hermes/self-reflection/` 下，是你本地的，不打包。别人装了三省引擎，规则库从零开始——踩自己的坑，长自己的记性，每个人的规则库都是独一无二的。

**Skill 层和 Plugin 层有什么区别？**

Skill 层靠 AI 读取指令并自觉遵守——可以被绕过。Plugin 层在 Hermes 内核执行——AI 没有机会跳过。三层闭环：skill-autoload 保证加载 → Skill 层引导行为 → cmg-guard 拦截输出。

**跟我已装的 skill 会打架吗？**

不会。CMG 用 stage 声明制排队——按"锚点 → 护栏 → 调度 → 执行"的固定顺序。CMG 在 pre_action 位置，在所有 skill 干活之前检查。

**规则太多会不会卡？**

规则超过 20 条自动切轻量模式——只跑第一道闸（精确匹配），跳过后面四道。54 条规则不影响速度。

**两个 Plugin 能单独用吗？**

skill-autoload 可以独立使用，加载任意 Skill。cmg-guard 依赖 CMG 提供 ban 规则库——没有 CMG，规则库为空，插件无操作。

---

MIT License · GitHub: [L1veSong/CMG](https://github.com/L1veSong/CMG)
