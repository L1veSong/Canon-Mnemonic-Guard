# 发布自检清单

每次版本发布前，逐项确认。跳过任一项即视为未完成发布。

---

## 版本号同步（6 处）

- [ ] `SKILL.md` frontmatter `version`
- [ ] `SKILL.md` 标题（`# 三省引擎 (CMG) vX.X.X`）
- [ ] `SKILL.md` 注入格式消息（`三省引擎 vX.X.X · 永久规则`）
- [ ] `SKILL.md` 激活消息（`三省引擎 vX.X.X 已激活`）
- [ ] `README.md` 标题
- [ ] `README.md` Badge 版本号

**验证命令：**
```bash
grep -rn "v[0-9]\.[0-9]\.[0-9]" SKILL.md README.md CHANGELOG.md
```
确保所有出现处为同一版本号。

---

## 内容自洽（4 处）

- [ ] `SKILL.md` 版本变更表新增当前版本条目
- [ ] `SKILL.md` 典则线「当前」标注更新
- [ ] `CHANGELOG.md` 新增当前版本条目
- [ ] `README.md` 内容反映当前版本状态（非旧版「规划中」等描述）

---

## 测试（3 项）

- [ ] `skill_view` 加载成功
- [ ] `readiness_status: available`
- [ ] `setup_needed: false`

---

## 打包

- [ ] `zip -r ~/Desktop/Canon-Mnemonic-Guard-vX.X.X.zip . -x ".git/*"`
- [ ] 确认 ZIP 文件存在且大小 > 1KB

---

## 历史教训

> 本清单之所以存在，是因为 v2.2.9 → v5.0.0 期间多次发布时 README 标题、注入/激活消息、CHANGELOG 滞后。纯粹靠脑子记不可靠，必须逐项打勾。
