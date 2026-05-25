# 配套 Skill 协同测试指南

四步检测法，验证第三方 skill 与 CMG 的兼容性。

## 步骤

### 1. 相互认可检查

- CMG SKILL.md 是否提及该 skill？
- 该 skill SKILL.md 是否提及 CMG？
- 如 karpathy 已双向声明"防守+进攻互补"。

### 2. 指令冲突检测

- 该 skill 的准则与 CMG ban/gap/lazy 规则是否矛盾？
- 例：karpathy "Simplicity First" vs CMG 是否有"禁止简化"规则？→ 无冲突。

### 3. 层级隔离检查

- 该 skill 的 stage/role 声明是否与 CMG 的 `stage: pre_action` 冲突？
- gstack/careful 用 PreToolUse hooks（命令层）vs CMG 用 pre_action（行为层）→ 不同层，不冲突。
- 特别注意：Claude Code 特有 hook（CLAUDE_SKILL_DIR）在 Hermes 下不生效。

### 4. 能力互补评估

- 该 skill 提供的能力是 CMG 的补充还是重叠？
- 重叠 → 可能冲突。互补 → 推荐配套。
- gstack/guard（命令安全）+ CMG Guard（行为拦截）= 互补，两层过滤。

## 测试结果（2026-05-25）

| Skill | 认可 | 冲突 | 层级 | 互补 | 结论 |
|-------|:--:|:--:|:--:|:--:|------|
| karpathy | ✅双向 | 无 | 无 | 防守+进攻 | ✅ 强烈推荐 |
| gstack/careful | ❌ | 无 | 不同层 | 命令+行为 | ⚠️ Hermes hook 限制 |
| gstack/guard | ❌ | 无 | 不同层 | 三层过滤 | ⚠️ 同 careful |

## 规则

- 通过全部四项 → 入推荐列表
- 层级隔离但 hook 不兼容 → 入参考模式，标注限制
- 有冲突 → 不推荐，说明原因
