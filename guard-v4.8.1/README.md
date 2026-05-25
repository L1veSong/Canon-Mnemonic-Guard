# Guard 护栏线 — v4.8.1

> 三省引擎(CMG) 护栏线。读取 Canon 规则库，独立执行五层 pre_action 前置拦截。
> **v4.8.1 P2补全：session_id追踪 + Mnemonic联动钩子。** v4.8.0 上下文升级增强 + 用户纠正自动提升。

## 核心能力

| 层级 | 拦截器 | 检查内容 |
|------|--------|---------|
| 1 | BanInterceptor | 精确关键词匹配 |
| 2 | FabricationInterceptor | 防幻觉声称 |
| 3 | StepCompletenessInterceptor | 步骤完整性 + 闭环校验器 |
| 4 | SkillLoadInterceptor | 防偷懒（Skill是否加载） |
| 5 | ClarifyInterceptor | 防瞎猜（是否调用clarify） |

## v4.8.1 补全

### P2 补全：session追踪 + Mnemonic联动
- intercept_log.jsonl 新增 session_id 字段
- Guard 拦截后自动通知 Mnemonic 同会话计数
- 与 Mnemonic v3.5.1 P2 session追踪联动

## v4.8.0 新增（已发布）

### 上下文升级增强
- 同会话第2次命中即升级为 block（原3次）
- 24h半衰期衰减，防历史积累误升级
- `repeat_tolerance` 可配置

### 用户纠正自动提升
- 你说「记住」「别再犯」→ 规则自动提升（monitor→soft→hard）
- 与 Canon level_history 联动追踪

## 已有能力

- **闭环重试引擎**：拦截→修正→重试→放行
- **风险分级**：不可逆操作暂停确认，可自动修复自动重试

## 安装

```bash
npx skills add guard --yes --global
```

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v4.0.0 | 独立化拆分 + 角色声明制 |
| v4.6.0 | 典忆卫・闭环校验器 |
| v4.7.0 | 闭环重试引擎 |
| v4.7.1 | 风险分级 |
| **v4.8.0** | **上下文升级增强 + 用户纠正提升** |
| **v4.8.1** | **P2补全：session追踪 + Mnemonic联动** |

MIT · [L1veSong](https://github.com/L1veSong)
