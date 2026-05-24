# 三省引擎 (CMG) — Canon-Mnemonic-Guard v5.4.0

> AI 的错题本 + 免疫系统 + 监工。你只需指出一次错误，它从此记住。
> 取自「吾日三省吾身」。也可昵称「典忆卫」。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.4.0-blue)]()

---

## 这是什么

三省引擎 (CMG) 是一个 AI 行为自省系统，由三条独立线路 + 外观索引层组成：

| 线路 | 版本 | 定位 | 一句话 |
|------|------|------|--------|
| **典则线** Canon | v2.7.0 | 规则生产库 | 你说「记住」→ 写入规则 → 去重固化 |
| **护栏线** Guard | v4.8.0 | 规则执行器 + 闭环重试 | 风险分级 + 2次升级 + 用户纠正提升 |
| **忆存线** Mnemonic | v3.5.0 | 记忆状态层 | 上下文保留 + 2次推草稿 |
| **外观层** CMG | v5.4.0 | 四包索引 | init 脚本 + SOUL 激活标记 |

---

## v5.4.0 新特性：四大增强

**P1 同会话重复快速升级：** 同一规则第2次命中直接 block（原3次），24h半衰期衰减防误升级。

**P3 用户纠正自动提升：** 你说「记住」「别再犯」→ 规则自动升级（monitor→soft→hard）。

**P4 误报自动降级 + 规则有效期：** 连续否决≥3次自动降级。`!remember --expires 7d` 支持临时规则。

**Mnemonic 上下文保留：** 每次命中记录触发场景，unknown 规则触发后自动还原。

---

## ⚡ SOUL 一行激活

```bash
python3 init.py
# 选 Y → SOUL.md 写入: [CMG v5.4.0] 加载 canon-mnemonic-guard 护栏规则
```

---

## 📋 推荐联动（全部验证通过）

| 推荐 | 作用 | 验证 |
|------|------|:--:|
| rtk-rewrite | 压缩终端输出 60-90% token | ✅ |
| plur | 扩展规则来源 | ✅ |
| verification-before-completion | 证据先于断言 | ✅ |
| diagnose | 五阶段诊断 + 根因分析 | ✅ |
| ralph-loop | 进阶：跨会话项目级任务队列 | ✅ |

---

## 快速开始

```bash
npx skills add canon-mnemonic-guard --yes --global
npx canon-mnemonic-guard init
```

首次 init 会自动检测子包（Guard/Canon/Mnemonic）是否已安装。未安装的子包会提示选择——默认全部安装，可跳过某个，后续补装自动检测。

也可分别安装子包：

```bash
npx skills add guard --yes --global
npx skills add canon --yes --global
npx skills add mnemonic --yes --global
```

---

## 命令速查

| 命令 | 功能 |
|------|------|
| `!remember 禁止xxx` | 记录规则 |
| `!scan` | 手动扫盘（含推荐检测） |
| `!scan-recommendations` | 仅扫描推荐列表 |
| `!solidify` | 手动触发规则固化 |
| `!export` / `!import` | 导入导出规则集 |
| `!log` | 三线协调日志 |
| `!diagnose` | 一键诊断 |

---

## License

MIT © [L1veSong](https://github.com/L1veSong)
