# 三省引擎 (CMG) — Canon-Mnemonic-Guard v5.5.0

> AI 的错题本 + 免疫系统 + 监工。你只需指出一次错误，它从此记住。
> **v5.5.0 微型调度器：Guard 拦截→自动匹配配套 skill。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.5.0-blue)]()

---

## 这是什么

三省引擎 (CMG) 是一个 AI 行为自省系统，由三条独立线路 + 外观索引层组成：

| 线路 | 版本 | 定位 | 一句话 |
|------|------|------|--------|
| **典则线** Canon | v2.7.1 | 规则生产库 | 你说「记住」→ 写入规则 |
| **护栏线** Guard | v4.8.1 | 规则执行器 | 五层拦截 + 闭环重试 |
| **忆存线** Mnemonic | v3.5.2 | 记忆状态层 | 模式识别 + !patterns/!datasource |
| **外观层** CMG | v5.5.0 | 四包索引 + 微型调度 | init + SOUL激活 + 场景→配套映射 |

## v5.5.0：微型调度器

Guard 拦截时自动匹配配套 skill，提示加载：

| 拦截场景 | 推荐加载 |
|---------|---------|
| 过设计/复杂化 | karpathy-coding-guidelines |
| 跳步骤 | ralph-loop |
| 声称完成但未验证 | verification-before-completion |
| 同规则连续命中≥3次 | diagnose |

## ⚡ SOUL 一行激活

```bash
python3 init.py
# 选 Y → SOUL.md: [CMG v5.5.0] 加载 canon-mnemonic-guard 护栏规则
```

## 📋 配套生态

| 推荐 | 作用 | 验证 |
|------|------|:--:|
| **karpathy-coding-guidelines** | 进攻型行为准则，防守+进攻互补 | ✅ |
| rtk-rewrite | 压缩终端输出 60-90% token | ✅ |
| plur | 扩展规则来源 | ✅ |
| verification-before-completion | 证据先于断言 | ✅ |
| diagnose | 五阶段诊断 + 根因分析 | ✅ |
| ralph-loop | 跨会话项目级任务队列 | ✅ |

参考: gstack/careful, gstack/guard (命令层安全模式，Hermes hook限制)

## 快速开始

```bash
npx skills add canon-mnemonic-guard --yes --global
npx canon-mnemonic-guard init
```

## 命令速查

| 命令 | 功能 |
|------|------|
| `!remember 禁止xxx` | 记录规则 |
| `!scan` | 手动扫盘 |
| `!patterns` | 查看识别模式 |
| `!datasource` | 数据源状态 |
| `!log` | 协调日志 |
| `!diagnose` | 一键诊断 |

## License

MIT © [L1veSong](https://github.com/L1veSong)
