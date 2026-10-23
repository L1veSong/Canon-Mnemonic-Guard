# CMG 规则治理：!review 命令

> **来源：** Google/UIUC/MIT SkillOS 论文启发（2026-06-13）
>
> **核心洞察：** SkillOS 的「技能治理器」不光会加规则，还会根据效果数据删除不生效的。CMG 已经有 hit_count 数据，只是从未用于减负。
>
> **目标：** 给 CMG 加 `!review` 命令，利用已有 frontmatter 数据做规则减负。

---

## 当前数据（2026-06-13）

| 命中率 | 数量 | 典型规则 |
|--------|:--:|------|
| hit=0, >30天 | 9 条 | 女娲生成Skill先审查、强制联网搜索、禁止企业化套路等 |
| hit=0, ≤30天 | 2 条 | 版本号变更必须全文件同步、用户纠错必须立刻固化 |
| hit=1, >14天未触发 | 29 条 | 各类 ban 规则，触发一次后再无命中 |

---

## !review 命令设计

### 触发词
`!review` 或「审查规则」「规则减负」「清理规则」

### 执行流程

```
1. 遍历 rules/ban/ rules/gap/ rules/lazy/ rules/meta/
2. 读取每条规则的 frontmatter: hit_count, date, last_triggered
3. 按活跃度排序，生成审查列表

【输出格式】
╭─────────────────────────────────╮
│      CMG 规则治理 · 审查        │
╰─────────────────────────────────╯

  规则                            命中  创建   最后触发
  ────────────────────────────────────────────────
  女娲生成Skill先审查.md           0    23天   从未
  强制联网搜索.md                  0    23天   从未
  禁止企业化套路.md                0    23天   从未
  ...

  🔴 建议归档（hit=0 且 >30天）: 9 条
  🟡 待审查（hit=1 且 >14天未触发）: 29 条
  🟢 活跃规则: 22 条

  处理方式：
  A) 归档所有 🔴 (9条 → _archive/)
  B) 逐条选择
  C) 保留全部
  D) 先看详情再决定
```

### 归档逻辑

- 目标路径: `~/.hermes/self-reflection/rules/_archive/`
- 保留原始 .md 文件（含 frontmatter），不修改内容
- 更新 `rules/_index.md`（移除归档条目）
- 更新 `state.json`（total_rules 递减）
- 归档目录可随时恢复（手动移回原目录）

### 不自动归档的原因

CMG 是交互式系统，不是 RL 训练。规则删错一次比规则冗余更危险。SkillOS 用 GRPO 奖励信号做自动筛选—— CMG 用人工审查达到同样效果。

---

## 实施

| 改动 | 文件 | 行数 |
|------|------|:--:|
| `!review` 命令解析 | SKILL.md 新增章节 | ~15 |
| 审查列表生成逻辑 | references/review-spec.md | ~40 |
| 归档 CLI 脚本 | scripts/review-and-archive.py | ~60 |

---

## 参考

- SkillOS 论文: Google/UIUC/MIT, 2026-06
- 核心论点: 冻结执行器 + 训练治理器 → 自进化 Agent
- 可迁移点: 规则治理器不光加规则，还基于效果数据减规则

---

> **记录时间：** 2026-06-13
>
> **触发对话：** 用户分享 SkillOS 豆包链接 → 分析 → 提取可借鉴点 → 落地为 CMG 功能
>
> **下一步：** 用户确认后实施

---

# CMG 对外分发问题（2026-06-13）

## 问题一：四包制外泄

**症状：** 别人装 CMG 后 skill 列表出现四个东西——canon、guard、mnemonic、canon-mnemonic-guard。开发者架构暴露给使用者，困惑"到底用哪个"。

**修法：** 三子包 SKILL.md 加 `visibility: internal`

```yaml
# ~/.hermes/skills/software-development/canon/SKILL.md
# ~/.hermes/skills/software-development/guard/SKILL.md
# ~/.hermes/skills/software-development/mnemonic/SKILL.md
# 各加一行:
visibility: internal
```

Hermes 加载时跳过 internal skill → 用户只看到 canon-mnemonic-guard 一个入口。内部三线照常联动。

**发布自检追加：** 发布 CMG 前 grep 确认三子包 visibility 已设。

## 问题二：CMG vs Hermes Desktop 不兼容

**症状：** 装 CMG 后 Hermes Desktop 任何回复都被拦截，一句都出不来。

**根因：** sentinel 的 `transform_llm_output` 钩子替换输出后依赖 AI 自修正循环——CLI 有、Desktop 没有。Desktop 渲染单向，替换即最终结果 → 用户看到空白或 `[CMG 拦截]`。

**历史：** 坑点 39（2026-06-04）修过一次——Desktop 端关掉 pre_llm_call + post_llm_call。但只修了本机 config.yaml，其他人装 CMG 时仍全开。

**修法（两步）：**

### 2a. sentinel 内置平台检测

```python
# ~/.hermes/plugins/sentinel/__init__.py → register()

import os

def _detect_platform() -> str:
    """检测运行平台：desktop | cli | web | api"""
    # Desktop 特征: 存在 _HERMES_DESKTOP 环境变量
    if os.environ.get("HERMES_DESKTOP") or os.environ.get("HERMES_GUI"):
        return "desktop"
    # CLI 特征: TERM 存在且是交互式
    if os.environ.get("TERM") and os.environ.get("HERMES_INTERACTIVE"):
        return "cli"
    return "unknown"

PLATFORM = _detect_platform()

# Desktop 平台：自动禁用 transform_llm_output + pre_llm_call + post_llm_call
if PLATFORM == "desktop":
    config["hooks"]["transform_llm_output"] = False
    config["hooks"]["pre_llm_call"] = False
    config["hooks"]["post_llm_call"] = False
    logger.info("sentinel: Desktop 平台检测，自动禁用输出修改钩子")
```

### 2b. 安装脚本加 Desktop 检测

```bash
# scripts/init.py 安装时检测
if [ -n "$HERMES_DESKTOP" ]; then
    echo "Desktop 环境检测: 自动设置 sentinel.hooks（仅保留 pre_tool_call）"
    hermes config set sentinel.hooks.transform_llm_output false
    hermes config set sentinel.hooks.pre_llm_call false
    hermes config set sentinel.hooks.post_llm_call false
    hermes config set sentinel.hooks.pre_tool_call true
fi
```

**验证：** 在 Hermes Desktop 上安装 CMG → 发消息 → 正常回复，不被拦截。

## 问题三（不需要做）：静默模式

CMG 已有静默/非静默切换。本次不需要改。

---

> **记录时间：** 2026-06-13
>
> **下一步：** 实施 2a + 2b（Desktop 兼容）+ 问题一（四包制 visibility）
