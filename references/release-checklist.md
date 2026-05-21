# 版本发布自检清单

> 每次版本号变更后必须逐条执行。CMG 实战教训：v2.2.9 发布时 README 标题仍写 v2.2.6；v2.3.0 发布时注入/激活消息仍写 v2.2.3；v5.0.0 发布时多处滞留 v2.4.1。此后每次漏改都被用户指出。

---

## 全文件 grep 验证（发布最后一步，不可跳过）

```bash
grep -rn "v[0-9]\.[0-9]\.[0-9]" SKILL.md README.md CHANGELOG.md
```

确保所有出现处一致。

---

## 逐文件检查清单

### SKILL.md (8 处)

| # | 位置 | 格式 |
|---|------|------|
| 1 | frontmatter `version:` | `version: X.Y.Z` |
| 2 | frontmatter `_comment:` | 内部子模块版本引用（如 Guard v4.3.1） |
| 3 | 标题 `# Canon Mnemonic Guard` | `# Canon Mnemonic Guard vX.Y.Z` |
| 4 | 版本变更表 | 新增一行 |
| 5 | 注入格式 `三省引擎 vX.Y.Z` | 第 ~103 行 |
| 6 | 激活消息 `三省引擎 vX.Y.Z` | 第 ~143 行 |
| 7 | 典则线当前标记 `vX.Y.Z (当前)` | 第 ~780 行 |
| 8 | 三线路线图中的版本标注 | 如有 GUI 相关更新需同步 |
| 9 | 架构 `_comment` 中 Guard/Mnemonic 版本引用 | 子模块升级时必查 |

### README.md (3 处)

| # | 位置 | 格式 |
|---|------|------|
| 1 | 标题 `# 三省引擎 (CMG) — Canon-Mnemonic-Guard vX.Y.Z` | 第 1 行 |
| 2 | badge `[![Version](https://img.shields.io/badge/version-X.Y.Z-blue)]()` | 第 7 行附近 |
| 3 | 三线架构表版本号 | 如有更新 |

### CHANGELOG.md (1 处)

| # | 位置 | 格式 |
|---|------|------|
| 1 | 新增版本条目 | `## [X.Y.Z] — YYYY-MM-DD` |

### 子模块 SKILL.md（Guard / Mnemonic 单独发布时）

| # | 位置 | 格式 |
|---|------|------|
| 1 | frontmatter `version:` | 各模块独立版本号 |
| 2 | 标题 | `# Guard 护栏线 vX.Y.Z` |
| 3 | description | 如有 CMG 引用需同步 |
| 4 | CHANGELOG | 新增版本条目 |

---

## 发布后清理

- [ ] 删除旧版桌面 ZIP（避免混淆）
- [ ] 重新生成 `~/Desktop/Canon-Mnemonic-Guard-vX.Y.Z.zip`
- [ ] `skill_view` 验证加载正常 + 版本号一致

---

## 历史翻车记录

| 版本 | 遗漏 | 发现方式 |
|------|------|---------|
| v2.2.9 | README 标题仍写 v2.2.6 | 用户指出 |
| v2.2.9 | 注入/激活消息仍写 v2.2.3 | 自查发现 |
| v2.3.0 | README 标题/注入/激活消息多版本混乱 | 用户指出 |
| v5.0.0 | README 标题仍写 v2.4.1 | 用户指出 |
| v5.0.0 | 创建了错误的 `self-reflection-engine` 独立 Skill | 用户指出 |
| v5.0.1 | README 标题/CHANGELOG 未更新 | 用户指出 |
