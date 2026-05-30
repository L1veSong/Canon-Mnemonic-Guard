# Guard 护栏线 — v4.8.3

> 三省引擎(CMG) 护栏线。读取 Canon 规则库，执行五层前置拦截。
> **v4.8.3 文档精简**：697→77 行，砍掉伪代码规格，保留核心内容。

## 核心能力

| 层级 | 拦截器 | 检查内容 | Hermes | 其他平台 |
|------|--------|---------|:------:|:------:|
| 1 | Ban | 精确关键词匹配 | ✅ 插件 | 自觉 |
| 2 | Fabrication | 防幻觉声称 | ✅ 插件 | 自觉 |
| 3 | StepCompleteness | 步骤完整性 | ✅ 插件 | 自觉 |
| 4 | SkillLoad | Skill 是否加载 | 自觉 | 自觉 |
| 5 | Clarify | 是否调用 clarify | 自觉 | 自觉 |

> Hermes 用户搭配 `cmg-guard` 插件获得 Ban/Fabrication/StepCompleteness 三层硬拦截。
> 非 Hermes 平台（OpenClaw/Claude Code/Codex）五层全凭 AI 自觉。

## 安装

```bash
# Skill 层（所有平台）
cp -r guard ~/.hermes/skills/software-development/

# Plugin 层（仅 Hermes）
cp -r cmg-guard ~/.hermes/plugins/

# 一键配置
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v4.0.0 | 独立化拆分 + 角色声明制 |
| v4.6.0 | 典忆卫・闭环校验器 |
| v4.7.0 | 闭环重试引擎 |
| v4.8.0 | 上下文升级 + 用户纠正提升 |
| v4.8.1 | P2 补全：session 追踪 + Mnemonic 联动 |
| **v4.8.3** | **文档精简：697→77 行** |

MIT · [L1veSong](https://github.com/L1veSong)
