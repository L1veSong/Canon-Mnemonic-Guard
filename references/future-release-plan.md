# 未来发布计划

本文档定义 Hermes Canon Mnemonic Guard 从当前典则线 (v2.x) 到最终统一引擎 (v5.0.0) 的完整发布路线。

---

## 发布清单

| 阶段 | Skill 包名 | 版本系列 | 状态 | 说明 |
|------|-----------|---------|------|------|
| 1 | `hermes-canon` | v2.x | ✅ 当前 | 典则线独立 Skill，规则生产库 |
| 2 | `hermes-mnemonic` | v3.x | 📋 规划 | 忆存线独立 Skill，状态记忆层 |
| 3 | `hermes-guard` | v4.x | 📋 规划 | 护栏线独立 Skill，规则执行器 |
| 4 | `hermes-self-reflection-engine` | v5.0.0 | 📋 规划 | 三合一统一引擎，外观模式 |

---

## 铁律

1. **物理隔离：** 三个阶段的 Skill 包各自独立，不共享 SKILL.md，不互相寄生
2. **标准化接口联动：** 运行时通过 `rules/*.md` / `errors.jsonl` / `state.json` 通信，不直接调用
3. **前向兼容：** v5.0.0 对外 `role: guard, stage: pre_action` 与当前 v2.2.x 完全一致
4. **渐进发布：** 每个 Skill 独立迭代、独立测试、独立发布，不等其他线

---

## 阶段 1: 典则线 (v2.x) — 当前

**包名：** `hermes-canon`（当前在 `hermes-canon-mnemonic-guard` 内）

**职责：** 规则来源、固化、扫描、效果评分。纯静态规则层。

**当前版本：** v2.2.7

---

## 阶段 2: 忆存线 (v3.x) — 待启动

**包名：** `hermes-mnemonic`

**前置条件：** 典则线 v2.4.0 完成角色声明制引入后

**职责：**
- 会话记忆管理
- 错误模式自动识别
- 自动规则草稿生成并推送至典则线固化引擎

**角色声明：**
```yaml
role: memory
stage: background
```

**文件位置：** `~/.hermes/skills/software-development/hermes-mnemonic/`

---

## 阶段 3: 护栏线 (v4.x) — 待启动

**包名：** `hermes-guard`

**前置条件：** 典则线 v2.4.0 + 忆存线 v3.0.0 完成角色声明制引入后

**职责：**
- 前置拦截（从典则线剥离）
- 动态清单生成
- 拦截效能分析
- 上下文感知拦截

**角色声明：**
```yaml
role: guard
stage: pre_action
```

**文件位置：** `~/.hermes/skills/software-development/hermes-guard/`

---

## 阶段 4: 统一引擎 (v5.0.0) — 未来

**包名：** `hermes-self-reflection-engine`

**前置条件：** 三条线各自成熟并稳定运行

**架构：** 外观模式

```
对外: role: guard, stage: pre_action (唯一契约)
内部: Canon (producer) → Mnemonic (memory) → Guard (guard)
```

**文件位置：** `~/.hermes/skills/software-development/hermes-self-reflection-engine/`
