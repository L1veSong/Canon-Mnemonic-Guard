# Guard 护栏线 — v4.8.0

> 三省引擎(CMG) 护栏线。读取 Canon 规则库，独立执行五层 pre_action 前置拦截。
> **v4.8.0 上下文升级增强 + 用户纠正自动提升。**

## 核心能力

| 层级 | 拦截器 | 检查内容 |
|------|--------|---------|
| 1 | BanInterceptor | 精确关键词匹配 |
| 2 | FabricationInterceptor | 防幻觉声称 |
| 3 | StepCompletenessInterceptor | 步骤完整性 + 闭环校验器 |
| 4 | SkillLoadInterceptor | 防偷懒（Skill是否加载） |
| 5 | ClarifyInterceptor | 防瞎猜（是否调用clarify） |

## v4.8.0 新增

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

MIT · [L1veSong](https://github.com/L1veSong)
