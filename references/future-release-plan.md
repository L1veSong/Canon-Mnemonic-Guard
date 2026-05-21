# 未来发布计划

本文档定义 Hermes Canon Mnemonic Guard 从当前典则线 (v2.x) 到最终统一引擎 (v5.0.0) 的完整发布路线。

---

## 发布清单

## 发布清单（三省引擎 CMG = Canon-Mnemonic-Guard）

| 阶段 | Skill 包名 | 版本系列 | 状态 | 配套推荐 |
|------|-----------|---------|------|---------|
| 1 | `canon-mnemonic-guard` | v5.0.0 | ✅ 已发布 | 三省引擎统一外观（典则·护栏·忆存三线合一） |
| 2 | `guard` | v4.3.0 | ✅ 已发布 | ralph-loop / verification-before-completion / diagnose |
| 3 | `mnemonic` | v3.1.0 | ✅ 已发布 | 内置 memory + 待 Guard 拦截数据积累后激活模式识别 |
| 4 | （已合并至 canon-mnemonic-guard） | — | ✅ 完成 | 三线独立迭代，v5.0.0 外观模式统一对外 |

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
## 阶段 1: 三省引擎 (v5.0.0) — 已完成

**包名：** `canon-mnemonic-guard`

**架构：** 外观模式。对外 `role: guard, stage: pre_action`。内部三模块独立：Canon(典则·规则生产) + Guard(护栏·拦截执行) + Mnemonic(忆存·模式识别)。

**当前版本：** v5.0.0

**闭环验证：** 10 次拦截→2 个草稿→2 条固化，数据流全线贯通。

---

## 阶段 2-4: 三线各自独立迭代

三条线已全部独立发布。后续每个模块只修自己的 SKILL.md，通过标准化接口联动。16 条未来优化方向已入库（详见主 SKILL.md「未来更新方向」章节）。

**架构：** 外观模式

```
对外: role: guard, stage: pre_action (唯一契约)
内部: Canon (producer) → Mnemonic (memory) → Guard (guard)
```

**文件位置：** `~/.hermes/skills/software-development/self-reflection-engine/`
