# 三省引擎 CMG v5.2.1 发布公告

> Canon-Mnemonic-Guard · 典忆卫 · AI 的错题本 + 免疫系统

---

## v5.2.1 核心突破：「安装即生效」

在 SOUL.md 末尾写入一行 `[CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则`，Hermes 每次新会话读到这行自动激活护栏。删掉即停用，用户完全可控。

---

## 新特性

- **SOUL 一行激活**: init.py 选 Y → 自动写入。扫盘时检测标记存在+版本匹配
- **推荐列表自动扫描**: 9 项推荐工具（ralph-loop/VBC/diagnose/idea-foundry/rtk-rewrite/plur/obsidian/karpathy/skill-authoring），init 自动检测安装状态
- **init.py 一键初始化**: 目录创建→配置生成→状态初始化→推荐扫描→询问激活

---

## 四包版本

| 包 | 版本 |
|----|------|
| canon-mnemonic-guard | v5.2.1 |
| canon | v2.5.2 |
| guard | v4.5.1 |
| mnemonic | v3.3.0 |

---

## 快速开始

```bash
npx skills add canon-mnemonic-guard --yes --global
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

---

## 链接

- GitHub: https://github.com/L1veSong/Canon-Mnemonic-Guard
- License: MIT
