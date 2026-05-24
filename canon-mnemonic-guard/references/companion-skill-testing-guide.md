# 配套 Skill 协同测试指南

对 CMG 推荐列表中候选第三方 skill 的系统测试框架。

---

## 四步检测法

### 1. 相互认可检查

双方的 SKILL.md 是否声明彼此为配套？

- CMG 推荐列表是否提及对方
- 对方 `related_skills` / 配套章节是否提及 CMG
- 缺失 → 单向认可，推荐前先补齐

### 2. 指令冲突检查

逐条对比双方的指令/规则，看是否有逻辑矛盾。

| 检查项 | 方法 |
|--------|------|
| 行为准则 vs CMG ban规则 | 是否一方说"做X"另一方说"禁止X" |
| 拦截目标重叠 | 是否拦截同一类操作但策略相反 |
| 兼容而非冲突 | 是否一方的"简化"会被另一方判为"偷懒" |

### 3. 层级隔离检查

双方运行在不同层级即为安全。

| CMG 运行层 | 第三方运行层 | 结论 |
|-----------|------------|------|
| pre_action (AI行为) | PreToolUse (OS命令) | ✅ 不冲突 |
| pre_action (AI行为) | pre_action (AI行为) | ⚠️ 需深入检查 |
| background (记忆) | 任意 | ✅ 不冲突 |

### 4. 能力互补检查

双方是否提供 CMG 不具备的能力？

| 模式 | 示例 |
|------|------|
| 进攻+防守互补 | karpathy(进攻型准则) + CMG(防守型拦截) |
| 基础+进阶 | CMG典忆卫(基础任务监控) + ralph-loop(跨会话项目管理) |
| 命令层+行为层 | gstack/careful(命令安全) + CMG Guard(行为安全) |

---

## 推荐等级

| 等级 | 条件 | 示例 |
|------|------|------|
| ✅ 强烈推荐 | 4/4通过 + 双向认可 + 双向生效 | karpathy |
| ⚠️ 参考模式 | 无冲突但功能受限(Hermes不兼容hook) | gstack/careful, gstack/guard |
| ❌ 不推荐 | 有冲突或CMG无法感知调用 | shotguncode, MemPalace |

---

## 实测案例

### karpathy-coding-guidelines (8/8 ✅)

- 双向认可 ✅
- 指令无冲突 [防守+进攻互补]
- 层级隔离 ✅ (karpathy无stage声明)
- 能力互补 ✅ (进攻型行为准则)

### gstack/careful (5/6 ⚠️)

- 单向认可 (CMG提及，careful未提及)
- 指令无冲突 ✅
- 层级隔离 ✅ (Bash PreToolUse vs AI pre_action)
- 能力互补 ✅ (命令层保底)
- **问题：** Claude Code hook (`CLAUDE_SKILL_DIR`) 在 Hermes 下不生效

### gstack/guard (6/6 ⚠️)

- 实质=careful+freeze
- 与careful相同结论
- 三层过滤(careful→freeze→CMG)互补

---

## 更新记录

| 日期 | 事件 |
|------|------|
| 2026-05-25 | 创建：四步检测法 + 三组实测 (karpathy 8/8, gstack/careful 5/6, gstack/guard 6/6) |
