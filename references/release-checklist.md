# 版本发布检查清单

每次版本号变更后强制执行。跳过任何项 = 发布失败。

---

## 全文件同步验证

```bash
# 必须输出 0 残留（历史 changelog 条目除外）
grep -rn "v[0-9]\.[0-9]\.[0-9]" SKILL.md README.md CHANGELOG.md
```

**检查点：**

| 文件 | 位置 | 必须同步 |
|------|------|---------|
| SKILL.md | frontmatter `version:` | ✅ |
| SKILL.md | 标题 `# Canon Mnemonic Guard vX.Y.Z` | ✅ |
| SKILL.md | 注入格式 `自省引擎 vX.Y.Z` | ✅ |
| SKILL.md | 激活消息 `自省引擎 vX.Y.Z 已激活` | ✅ |
| SKILL.md | 典则线当前标记 `vX.Y.Z (当前)` | ✅ |
| SKILL.md | 版本变更表第一行 | ✅ |
| README.md | 标题 `# Canon Mnemonic Guard — 典则线 vX.Y.Z` | ✅ |
| README.md | badge `version-X.Y.Z` | ✅ |
| CHANGELOG.md | 最新条目 `## [X.Y.Z]` | ✅ |

---

## 内容自洽检查

- [ ] role/stage 声明与头部描述一致（如 `role: producer` → 头部写 `producer (规则生产锚点)`）
- [ ] 推荐列表无重复/遗漏
- [ ] 交叉引用 Skill 名全部为 `canon-mnemonic-guard`（不含 hermes 前缀）
- [ ] 无外部 Skill 内部版本号引用（如 Idea Foundry 的 v8/v9）
- [ ] 未来规划只在「版本路线」章节，不混入设计哲学/推荐列表/激活消息

---

## 文件完整性

- [ ] `references/guard-spec.md` 存在（v2.4.1+）
- [ ] `references/companion-skills-research.md` 存在
- [ ] `references/future-release-plan.md` 存在
- [ ] `~/.hermes/self-reflection/config.json` 与 SKILL.md 的描述一致
- [ ] 桌面 ZIP 文件名含正确版本号

---

## 功能验证

- [ ] `skill_view("canon-mnemonic-guard")` → `readiness_status: available`
- [ ] `setup_needed: false`
- [ ] `missing_required_commands: []`

---

## 实战教训

**v2.2.9 发布时：** README 标题仍写 v2.2.6；注入消息和激活消息仍写 v2.2.3。全因跳过了全文件 grep。

**v2.3.2 发布时：** README 标题仍写 v2.3.0。badge 更新了但标题没同步。

**v2.4.0→v2.4.1：** role 从 guard→producer 后，头部描述行仍写 `角色: guard`。role 字段改了但描述行没改。
