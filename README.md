# 三省引擎 (CMG) — Canon-Mnemonic-Guard v5.0.1

> AI 的错题本 + 免疫系统。你只需指出一次错误，它从此记住。
>
> 取自「吾日三省吾身」。也可昵称「典忆卫」。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.0.1-blue)]()

---

## 这是什么

三省引擎 (CMG) 是一个 AI 行为自省系统，由三条独立线路组成：

| 线路 | 版本 | 定位 | 一句话 |
|------|------|------|--------|
| **典则线** Canon | v2.4.1 | 规则生产库 | 你说「记住」→ 写入规则 → 去重固化 |
| **护栏线** Guard | v4.3.0 | 规则执行器 | 五层拦截 → 动态清单 → 上下文感知 |
| **忆存线** Mnemonic | v3.1.0 | 状态记忆层 | 读拦截日志 → 自动模式识别 → 推送规则草稿 |

**三线联动：** Canon 生产规则 → Guard 执行拦截 → Mnemonic 识别模式 → Canon 固化升级

---

## 架构

```
三省引擎 (CMG) v5.0.0 — 外观模式
对外: role: guard, stage: pre_action
内部:
  ┌────────┐  ┌────────┐  ┌───────┐
  │ 典则线  │  │ 护栏线  │  │ 忆存线 │
  │Canon   │  │Guard   │  │Mnemonic│
  │生产规则 │  │执行拦截 │  │模式识别 │
  └────────┘  └────────┘  └───────┘
  四模块严格独立，互不混合
```

---

## 快速开始

### 安装

```bash
npx skills add canon-mnemonic-guard --yes --global
```

三模块也可独立安装：

```bash
npx skills add guard --yes --global
npx skills add mnemonic --yes --global
```

### 使用

```
"记住，以后禁止虚构 Skill。"
"固化规则"
"扫盘"
```

### 规则类型

| 类型 | 触发词 | 行为 |
|------|--------|------|
| 🚫 `ban` | "禁止" "不要" | 拦截 |
| ⚠️ `gap` | "不够" "没达标" | 补齐 |
| 😴 `lazy` | "跳过" "没做" | 追加 |

---

## 功能一览

| 功能 | 所属 |
|------|------|
| 三类错误系统 (ban/gap/lazy) | Canon v1.0 |
| 固化引擎 + 去重合并 | Canon v1.0 |
| Obsidian 结构化 rules/ | Canon v2.0 |
| 扫盘提取 (4 源) | Canon v2.2 |
| 可配置扫描源 + 白名单 | Canon v2.3 |
| 规则冲突检测与裁决 | Canon v2.3 |
| 规则效果评分 | Canon v2.4 |
| 角色声明制 | Canon v2.4 |
| 简化命令 (!remember/!solidify/!scan) | Canon v2.4 |
| 五层拦截器 | Guard v4.0 |
| 动态清单生成 | Guard v4.1 |
| 拦截效能分析 | Guard v4.2 |
| 上下文感知拦截 | Guard v4.3 |
| 自动模式识别 | Mnemonic v3.1 |

---

## 配套生态（推荐，非必需）

| 类别 | 工具 |
|------|------|
| 护栏执行 | ralph-loop · verification-before-completion · diagnose |
| 调度联动 | idea-foundry（CMG 规则集注入代码生成） |
| 成本优化 | rtk-hermes（压缩 60-90% token） |
| 规则扩展 | plur |
| 跨线共享 | obsidian · karpathy-coding-guidelines |

全部采用添加式集成 — CMG 只读不写，第三方行为不受影响。

---

## 未来方向

16 条优化项已入库：典则 4 条 · 护栏 5 条 · 忆存 4 条 · 引擎 3 条。详见 SKILL.md。

---

## 💡 建议与反馈

- 有 Bug？[提交 Issue](https://github.com/L1veSong/Canon-Mnemonic-Guard/issues/new?template=bug_report.md)
- 有想法？[提交 Feature Request](https://github.com/L1veSong/Canon-Mnemonic-Guard/issues/new?template=feature_request.md)

## License

MIT © [L1veSong](https://github.com/L1veSong)
