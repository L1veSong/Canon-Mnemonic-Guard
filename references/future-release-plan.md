# 未来发布计划

本文档定义 Hermes Canon Mnemonic Guard 从当前典则线 (v2.x) 到最终统一引擎 (v5.0.0) 的完整发布路线。

---

## 发布清单

| 阶段 | Skill 包名 | 版本系列 | 状态 | 配套推荐 |
|------|-----------|---------|------|---------|
| 1 | `canon` | v2.x | ✅ 已发布 v2.4.1 | obsidian（rules/ 可视化） |
| 2 | `mnemonic` | v3.x | ✅ 已发布 v3.1.0 | memory (内置) + 自动模式识别 |
| 3 | `guard` | v4.x | ✅ 已发布 v4.3.0 | ralph-loop / verification-before-completion / diagnose |
| 4 | `self-reflection-engine` | v5.0.0 | 📋 规划 | 继承全部推荐，外观模式统一对外 |

---

## 铁律

1. **物理隔离：** 三个阶段的 Skill 包各自独立，不共享 SKILL.md，不互相寄生
2. **标准化接口联动：** 运行时通过 `rules/*.md` / `errors.jsonl` / `state.json` 通信，不直接调用
3. **前向兼容：** v5.0.0 对外 `role: guard, stage: pre_action` 与当前 v2.2.x 完全一致
4. **渐进发布：** 每个 Skill 独立迭代、独立测试、独立发布，不等其他线

---

## 阶段 1: 典则线 (v2.x) — 当前

**包名：** `canon`（当前在 `canon-mnemonic-guard` 目录内）

**职责：** 规则来源、固化、扫描、效果评分。纯静态规则层。

**当前版本：** v2.3.2

**Phase 1 完成（v2.3.x）：**
- ✅ v2.3.0 依赖解耦：RuleReader 接口 + 7 个适配器 + 可配置扫描源
- ✅ v2.3.1 规则冲突检测与裁决
- ✅ v2.3.2 Idea Foundry 规则集联动

**Phase 2 待办（v2.4.0）：** 规则效果评分 + 角色声明制 + init/export 命令

---

## 阶段 2: 忆存线 (v3.x) — 待启动

**包名：** `mnemonic`

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

**文件位置：** `~/.hermes/skills/software-development/mnemonic/`

---

## 阶段 3: 护栏线 (v4.x) — 待启动

**包名：** `guard`

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

**文件位置：** `~/.hermes/skills/software-development/guard/`

---

## 阶段 4: 统一引擎 (v5.0.0) — 未来

**包名：** `self-reflection-engine`

**前置条件：** 三条线各自成熟并稳定运行

**架构：** 外观模式

```
对外: role: guard, stage: pre_action (唯一契约)
内部: Canon (producer) → Mnemonic (memory) → Guard (guard)
```

**文件位置：** `~/.hermes/skills/software-development/self-reflection-engine/`
