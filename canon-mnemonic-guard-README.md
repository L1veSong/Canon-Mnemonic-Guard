# 三省引擎 (CMG) — Canon-Mnemonic-Guard v5.2.1

> AI 的错题本 + 免疫系统。你只需指出一次错误，它从此记住。
>
> 取自「吾日三省吾身」。也可昵称「典忆卫」。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.2.1-blue)]()

---

## 这是什么

三省引擎 (CMG) 是一个 AI 行为自省系统，由三条独立线路 + 外观索引层组成：

| 线路 | 版本 | 定位 | 一句话 |
|------|------|------|--------|
| **典则线** Canon | v2.5.2 | 规则生产库 | 你说「记住」→ 写入规则 → 去重固化 |
| **护栏线** Guard | v4.5.1 | 规则执行器 | 五层拦截 → 动态清单 → 上下文感知 |
| **忆存线** Mnemonic | v3.3.0 | 状态记忆层 | 读拦截日志 → 自动模式识别 → 推送规则草稿 |
| **外观层** CMG | v5.2.1 | 四包索引 | init 脚本 + SOUL 激活标记 + 推荐列表扫描 |

**三线联动：** Canon 生产规则 → Guard 执行拦截 → Mnemonic 识别模式 → Canon 固化升级

---

## v5.2.1 新特性

### ⚡ SOUL 激活机制

安装后运行 `init.py`，选 Y → 在 SOUL.md 末尾写入一行 `[CMG v5.2.1]`。Hermes 每次对话读到这行自动加载护栏规则。

- **一行激活**，删掉即停用
- 扫盘时自动检测标记存在 + 版本匹配
- 标记丢失 → 提醒恢复（数据不丢）

### 📋 推荐列表自动扫描

`init.py` 初始化时自动扫描 9 项推荐工具，检测安装/配置状态。`!scan-recommendations` 随时手动补扫。`!scan` 扫盘时自动包含推荐检测。

| 类别 | 推荐工具 |
|------|---------|
| 护栏执行 | ralph-loop · verification-before-completion · diagnose |
| 调度联动 | idea-foundry（CMG 规则集注入代码生成） |
| 成本优化 | rtk-rewrite（压缩 60-90% token） |
| 规则扩展 | plur |
| 跨线共享 | obsidian · karpathy-coding-guidelines |
| 开发者 | hermes-agent-skill-authoring |

---

## 快速开始

```bash
# 安装
npx skills add canon-mnemonic-guard --yes --global

# 初始化（自动扫描推荐列表 + 询问 SOUL 激活）
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

各线也可独立安装：

```bash
npx skills add canon --yes --global
npx skills add guard --yes --global
npx skills add mnemonic --yes --global
```

### 命令速查

| 命令 | 功能 |
|------|------|
| `!remember 禁止xxx` | 记录规则 |
| `!scan` | 手动扫盘（含推荐检测） |
| `!scan-recommendations` | 仅扫描推荐列表 |
| `!solidify` | 手动触发固化 |
| `!export` | 导出规则为 ZIP |
| `!import <path>` | 从 ZIP 导入规则 |
| `!log` | 三线协调日志 |
| `!diagnose` | 一键诊断 |

---

## 功能一览

| 功能 | 所属 | 版本 |
|------|------|------|
| 三类错误系统 (ban/gap/lazy) | Canon | v1.0 |
| 固化引擎 + 去重合并 | Canon | v1.0 |
| Obsidian 结构化 rules/ | Canon | v2.0 |
| 扫盘提取 (4 源) | Canon | v2.2 |
| 可配置扫描源 + 白名单 | Canon | v2.3 |
| 规则冲突检测与裁决 | Canon | v2.3 |
| 规则效果评分 | Canon | v2.4 |
| 角色声明制 | Canon | v2.4 |
| 定时扫盘 (C1) | Canon | v2.5 |
| 推荐列表自动扫描 | Canon | v2.5.1 |
| SOUL 激活机制 | Canon | v2.5.2 |
| 五层拦截器 | Guard | v4.0 |
| 动态清单生成 (G2) | Guard | v4.5 |
| 拦截效能分析 (G4) | Guard | v4.5 |
| 上下文感知拦截 (G3) | Guard | v4.5 |
| 自动模式识别 | Mnemonic | v3.1 |
| 数据源降级链 (M1) | Mnemonic | v3.3 |
| 独立持久化 (M2) | Mnemonic | v3.2 |
| 健康检查 (E1) | Engine | v5.0.2 |
| 协调日志 (E2) | Engine | v5.2.0 |
| 一键诊断 (E3) | Engine | v5.2.0 |
| 四包制分装 (E4) | Engine | v5.1.0 |
| init 脚本 | Engine | v5.2.1 |

---

## 架构

```
三省引擎 (CMG) v5.2.1 — 外观模式
对外: role: guard, stage: pre_action
内部:
  ┌────────┐  ┌────────┐  ┌───────┐
  │ 典则线  │  │ 护栏线  │  │ 忆存线 │
  │Canon   │  │Guard   │  │Mnemonic│
  │生产规则 │  │执行拦截 │  │模式识别 │
  └────────┘  └────────┘  └───────┘
  四模块严格独立，互不混合
```

全部配套采用添加式集成 — CMG 只读不写，第三方行为不受影响。

---

## License

MIT © [L1veSong](https://github.com/L1veSong)
