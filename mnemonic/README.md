# Mnemonic 忆存线 — v3.5.3

> 三省引擎(CMG) 状态记忆层。读取 Guard 拦截日志，自动识别高频错误模式。
> **v3.5.3 默认固化阈值10→3。** v3.5.2 M3清零：!patterns + !datasource。

## 核心能力

- **模式识别**：同会话 ≥2 次 → 自动推送规则草稿至 Canon（P2加速）
- **!patterns**：查看重复违规模式（本会话/7天/置信度/推荐操作）
- **!datasource**：查看数据源状态和切换历史
- **session追踪**：mnemonic_state.json 新增 session_tracking 去重
- **Guard联动**：接收 Guard 拦截后的同会话计数推送
- **数据源降级**：Guard拦截日志 → Canon错误记录 → 等待状态
- **误报率自适应**：置信度 ±0.1/0.2 浮动

## v3.5.2 补全

### M3 清零：!patterns + !datasource
- `!patterns`：表格展示本会话命中 / 7天命中 / 置信度 / 推荐操作
- `!datasource`：展示当前数据源 + 切换历史 + 降级链状态
- 零外部依赖，复用现有 ! 触发词机制
- CMG 待优化表 17 项全部完成

## v3.5.1 补全（已发布）

### P2 补全：session追踪 + Guard联动
- 同会话同一 rule_id ≥2次 → 立即推草稿（原7天3次）
- 跨会话7天内累计2次 → 推草稿
- mnemonic_state.json 新增 session_tracking 字段
- 与 Guard v4.8.1 P2联动钩子对接

## v3.5.0 新增（已发布）

### 命中上下文保留
- 每次 Guard 拦截命中记录触发场景（用户意图 + Agent操作）
- 解决 unknown 规则无法还原的问题
- 最近 100 条保留，每 rule_id 最多 5 条

### 已有能力
- 同会话 2 次推草稿（v3.4.0）
- 数据源降级链（v3.3.0）
- 独立持久化 + 误报率调节（v3.2.0）

## 安装

```bash
npx skills add mnemonic --yes --global
```

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v3.0.0 | CLI 规格 + 角色声明制 |
| v3.1.0 | 自动模式识别 |
| v3.3.0 | 数据源降级链 |
| v3.4.0 | 2次推草稿加速 |
| **v3.5.0** | **上下文保留** |
| **v3.5.1** | **P2补全：session追踪 + Guard联动** |

MIT · [L1veSong](https://github.com/L1veSong)
