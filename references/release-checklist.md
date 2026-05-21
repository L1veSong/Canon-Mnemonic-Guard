# 发布检查清单

每次版本发布前逐条验证。跳过任何一步即为未完成发布。

---

## 版本号自洽

```bash
grep -rn "v[0-9]\.[0-9]\.[0-9]" SKILL.md README.md CHANGELOG.md
```

确保所有出现处同步到新版本号。以下位置最容易遗漏：

| 位置 | 检查项 |
|------|--------|
| SKILL.md frontmatter | `version:` 字段 |
| SKILL.md 标题 | `# Canon Mnemonic Guard vX.X.X` |
| SKILL.md 注入格式 | `三省引擎 vX.X.X · 永久规则` |
| SKILL.md 激活消息 | `三省引擎 vX.X.X 已激活` |
| SKILL.md 版本变更表 | 新增版本条目 |
| SKILL.md 典则线当前标记 | `vX.X.X (当前):` |
| README.md 标题 | `# 三省引擎 (CMG) — ... vX.X.X` |
| README.md 徽章 | `version-X.X.X-blue` |
| CHANGELOG.md 标题 | `## [X.X.X]` |
| 路线图三线表 | 正确标注 ✅ |

---

## 内容自洽

| 检查项 | 方法 |
|--------|------|
| 所属模块版本号（guard/mnemonic） | grep 确认引用版本与实际一致 |
| GitHub 链接 | 确认 `L1veSong/Canon-Mnemonic-Guard`，非旧名 `hermes-canon-mnemonic-guard` |
| 交叉引用 Skill 名 | 确认 `canon-mnemonic-guard`，非 `hermes-self-reflection` |
| 三省引擎 / 典忆卫 | 正式名和昵称在文档中协调使用 |
| 三线状态 | v3/v4 标注 ✅ 已发布，非 📋 规划中 |

---

## 功能测试

| 检查项 | 命令 |
|--------|------|
| Skill 可加载 | `skill_view("canon-mnemonic-guard")` |
| readiness_status | 必须为 `available` |
| setup_needed | 必须为 `false` |
| missing_required_commands | 必须为空 |
| 子模块可加载 | `skill_view("software-development/guard")` + `skill_view("mnemonic")` |
| 数据文件存在 | `~/.hermes/self-reflection/rules/` 目录非空 |
| state.json 可读 | `python3 -c "import json; json.load(open('...'))"` |

---

## 交付物

| 文件 | 路径 |
|------|------|
| CMG ZIP | `~/Desktop/Canon-Mnemonic-Guard-vX.X.X.zip` |
| Guard ZIP | `~/Desktop/Guard-vX.X.X.zip` |
| Mnemonic ZIP | `~/Desktop/Mnemonic-vX.X.X.zip` |

---

## 禁止事项

- ❌ 版本号改了 frontmatter 但漏了 README 标题
- ❌ README 徽章更新但正文说「v3/v4 规划中」
- ❌ 新建独立 engine Skill 而非升版主 Skill
- ❌ 回退到旧名 `self-reflection-engine` 或 `hermes-self-reflection`
