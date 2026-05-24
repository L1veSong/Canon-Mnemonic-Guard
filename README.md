# CMG 三省引擎 v5.4.0 — 完整包

> AI 的错题本 + 免疫系统 + 监工。取自「吾日三省吾身」。
> 四层完整发布：外观层 + 三条独立线路。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.4.0-blue)]()

---

## 目录结构

```
CMG-v5.4.0-full/
├── README.md                        # 本文件
├── canon-mnemonic-guard/            # 外观层（全家桶入口）
│   ├── SKILL.md                     # 四包索引 + 完整规格
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── scripts/init.py              # 一键初始化
│   ├── references/                  # 模板/设计文档/联动测试
│   └── assets/
├── guard/                           # Guard 护栏线 v4.8.0
│   ├── SKILL.md
│   ├── README.md
│   ├── CHANGELOG.md
│   └── references/
├── canon/                           # Canon 典则线 v2.7.0
│   ├── SKILL.md
│   ├── README.md
│   ├── CHANGELOG.md
│   └── references/
└── mnemonic/                        # Mnemonic 忆存线 v3.5.0
    ├── SKILL.md
    ├── README.md
    └── CHANGELOG.md
```

## 四层架构

| 线路 | 版本 | 角色 | 职责 |
|------|------|------|------|
| **Canon 典则线** | v2.7.0 | producer | 规则生产 + 固化引擎 + 误报降级 |
| **Guard 护栏线** | v4.8.0 | guard | 五层拦截 + 闭环重试 + 上下文升级 |
| **Mnemonic 忆存线** | v3.5.0 | memory | 模式识别 + 上下文保留 + 数据源降级 |
| **CMG 外观层** | v5.4.0 | facade | 四包索引 + 一键安装 + 协调日志 |

```
Canon (producer) → Guard (guard) → Mnemonic (memory)
      规则生产           拦截执行          记忆模式
```

## v5.4.0 四大增强

| 增强 | 模块 | 内容 |
|------|------|------|
| P1 | Guard | 同会话第2次命中直接 block，24h半衰期衰减 |
| P3 | Guard | 用户纠正自动提升规则级别（monitor→soft→hard） |
| P4 | Canon | 连续否决≥3次自动降级 + `!remember --expires 7d` |
| — | Mnemonic | 命中上下文保留，unknown规则自动还原 |

## 快速开始

```bash
cd canon-mnemonic-guard
python3 scripts/init.py
```

init 自动检测子包状态，提示安装缺失的线路。默认全部安装。

## 命令速查

| 命令 | 功能 |
|------|------|
| `!remember 禁止xxx` | 记录规则 |
| `!remember --expires 7d "xxx"` | 临时规则 |
| `!scan` | 手动扫盘 |
| `!solidify` | 固化规则 |
| `!log` | 三线协调日志 |
| `!diagnose` | 一键诊断 |
| `!export` / `!import` | 导入导出规则集 |

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v5.0.0 | 三线合一外观模式 |
| v5.1.0 | 四包制分装 |
| v5.2.0 | C1定时扫盘 + 协调日志 + 一键诊断 |
| v5.3.0 | Guard风险分级 |
| **v5.4.0** | **四大增强：上下文升级 + 用户纠正 + 误报降级 + 上下文保留** |

## License

MIT © [L1veSong](https://github.com/L1veSong)
