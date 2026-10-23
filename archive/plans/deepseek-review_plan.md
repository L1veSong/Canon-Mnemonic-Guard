# CMG — DeepSeek 评审行动清单

> 2026-06-09。来源：DeepSeek 评审 图1（CMG开发方向）+ 图3（生态8项目）+ 图5（隐私声明）

---

## ✅ 已完成

- ✅ IF/SSR emoji 清除（跨项目，不属 CMG）

---

## 待执行

### P0: 30秒示例 + 隐私声明

**改 README。纯文档，不发版。**

1. README 开头加一段可复制对话示例（"记住，禁止 xxx" → "已记录规则#N" → 下次自动遵守）
2. 隐私声明："CMG 不会上传规则数据，所有文件存本地 `~/.hermes/self-reflection/`"

**工作量:** 10分钟 | **目标:** 下次提交

---

### P1: !lint 命令

**规则语法/冲突/冗余一键检查。**

- YAML frontmatter 语法（复用 check-frontmatter.py）
- 冲突检测（封装已有 v2.3.1 逻辑）
- 冗余检测：关键词重叠 >70% 提示合并
- 入口：`!lint` / `!rule-check`

**文件:** 新建 `scripts/lint-rules.py`，改 SKILL.md 加触发词
**工作量:** 1-2天 | **目标:** v5.7.0

---

### P2: 傻瓜/专家模式

**降低非技术用户门槛。**

- 傻瓜（默认）：自动记录 → 阈值提示固化
- 专家：每次 clarify 确认，可编辑
- 入口：`!mode simple|expert`

**文件:** 改 SKILL.md + config.json
**工作量:** 2-3天 | **目标:** v5.8.0 | **前置:** 取决于分发计划

---

### P3: Example Hub

**5 个完整可复制场景示例。**

1. CMG 安全规则记录+验证拦截
2. IF+CMG 协同：想法→代码→规则固化
3. CMG 学术写作
4. CMG 金融分析
5. Dashboard 演示

**文件:** 新建 GitHub 仓库 `cmg-example-hub`
**工作量:** 4-5天 | **前置:** 公开发布前

---

## ❌ 不做

| 建议 | 原因 |
|------|------|
| GIF/asciinema 录屏 | 费时，30秒文字够用 |
| v4 集成 ESLint/Black | 已走 sentinel Plugin 路线 |
| Rule Bazaar | 无用户基础 |
| Skill Config Manager | 过度设计 |
| Skill Logger | !log 已够用 |
| Skill RPC | 文件接口已够用 |
