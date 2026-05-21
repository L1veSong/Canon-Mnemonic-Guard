# 三省引擎 CMG v5.2.1 发布公告

> Canon-Mnemonic-Guard · 典忆卫 · AI 的错题本 + 免疫系统
> 取自「吾日三省吾身」

---

## 🎯 这个版本解决了什么

**v5.2.1 的核心突破：「安装即生效」。**

之前的版本，用户装完 CMG 后需要手动 `/skill` 加载才能触发护栏。v5.2.1 引入 SOUL 激活机制——安装时选 Y，在 SOUL.md 末尾写入一行标记，Hermes 每次新会话读到这行自动激活护栏规则。删掉这行就停用，完全用户可控。

---

## ✨ 新特性

### ⚡ SOUL 一行激活

```bash
python3 init.py
# 选 Y → SOUL.md 写入: [CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则
```

- **一行激活**，删掉即停用
- 扫盘时自动检测标记存在 + 版本匹配
- 标记被误删 → 自动提醒恢复（数据不丢）

### 📋 推荐列表自动扫描

`init.py` 初始化时自动扫描 9 项推荐工具的安装/配置状态。之后每次扫盘自动包含推荐检测。

| 类别 | 推荐工具 | 作用 |
|------|---------|------|
| 护栏执行 | ralph-loop · verification-before-completion · diagnose | 拦截违规后自动闭环、证据验证、根因分析 |
| 调度联动 | idea-foundry | CMG 规则集注入代码生成阶段 |
| 成本优化 | rtk-rewrite | 压缩终端输出 60-90% token |
| 规则扩展 | plur | 扩展记忆来源 |
| 跨线共享 | obsidian · karpathy-coding-guidelines | 可视化 + 行为准则 |
| 开发者 | hermes-agent-skill-authoring | 发布流程风控 |

### 🔧 init.py 一键初始化

一条命令完成：目录创建 → 配置生成 → 状态初始化 → 推荐扫描 → 询问 SOUL 激活。

---

## 📦 四包版本

| 包 | 版本 | 变更 |
|----|------|------|
| **canon-mnemonic-guard** | v5.2.1 | SOUL 激活 + init 脚本 + 推荐扫描 |
| **canon** | v2.5.2 | +推荐列表自动扫描 + SOUL 激活检测 |
| **guard** | v4.5.1 | +激活标记检测 + 三种激活方式文档化 |
| **mnemonic** | v3.3.0 | 数据源降级链（本次无变更） |

---

## 🚀 快速开始

```bash
# 安装四包
npx skills add canon-mnemonic-guard --yes --global
npx skills add canon --yes --global
npx skills add guard --yes --global
npx skills add mnemonic --yes --global

# 初始化（自动扫描推荐 + 询问 SOUL 激活）
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

---

## 📋 命令速查

| 命令 | 功能 |
|------|------|
| `!remember 禁止xxx` | 记录规则（你说一次，它从此记住） |
| `!scan` | 手动扫盘（含推荐检测） |
| `!scan-recommendations` | 仅扫描推荐列表 |
| `!solidify` | 手动触发规则固化 |
| `!export` / `!import` | 导入导出规则集 |
| `!log` | 三线协调日志 |
| `!diagnose` | 一键诊断（文件完整性 + 规则有效性 + 跨模块一致性） |

---

## 🔗 链接

- 仓库: [github.com/L1veSong/Canon-Mnemonic-Guard](https://github.com/L1veSong/Canon-Mnemonic-Guard)
- 桌面成品包: `~/Desktop/CMG-v5.2.1/` + `CMG-v5.2.1.zip`
- License: MIT

---

## 💡 反馈

有 Bug 或想法？[提交 Issue](https://github.com/L1veSong/Canon-Mnemonic-Guard/issues)。

---

**17 项路线图，16 项完成。仅剩 M3 CLI 命令（依赖 Hermes 内核支持），其余全部可用。**
