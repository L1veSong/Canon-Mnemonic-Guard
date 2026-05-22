# 三省引擎 (CMG) — Canon-Mnemonic-Guard v5.3.0

> AI 的错题本 + 免疫系统 + 监工。你只需指出一次错误，它从此记住。
> 取自「吾日三省吾身」。也可昵称「典忆卫」。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.3.0-blue)]()

---

## 这是什么

三省引擎 (CMG) 是一个 AI 行为自省系统，由三条独立线路 + 外观索引层组成：

| 线路 | 版本 | 定位 | 一句话 |
|------|------|------|--------|
| **典则线** Canon | v2.5.2 | 规则生产库 | 你说「记住」→ 写入规则 → 去重固化 |
| **护栏线** Guard | v4.6.0 | 规则执行器 + 监工 | 五层拦截 → 闭环校验器逐步骤催办 |
| **忆存线** Mnemonic | v3.3.0 | 状态记忆层 | 读拦截日志 → 自动模式识别 → 推送规则草稿 |
| **外观层** CMG | v5.3.0 | 四包索引 | init 脚本 + SOUL 激活标记 + 推荐列表扫描 |

---

## v5.3.0 新特性：典忆卫・闭环校验器

**Guard 不再只是一个红灯。它是监工。**

当 Agent 跳过步骤想交差时，闭环校验器自动接管：

```
Agent: "差不多了，完成了"
Guard:  ⛔ 拦截。剩余 3 步未完成。

       进入典忆卫・闭环校验器:
       [1/3] 补充参考文献 → Agent执行 → ✅
       [2/3] 格式检查     → Agent执行 → ✅
       [3/3] 最终验证     → Agent执行 → ✅

       3/3 全部闭环，放行。
```

- **零外部依赖** — 不用 ralph-loop、不写文件、不委派子 Agent
- **典忆卫原生** — 用自己的规则体系、对话上下文、拦截器框架实现
- **2 步以上自动触发** — 剩余步骤 ≥ 2 时进入逐步骤催办

---

## ⚡ SOUL 一行激活

```bash
python3 init.py
# 选 Y → SOUL.md 写入: [CMG v5.3.0] 加载 canon-mnemonic-guard 护栏规则
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
python3 init.py
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
