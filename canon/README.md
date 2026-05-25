# Canon 典则线 — v2.7.2

> 三省引擎(CMG) 规则生产库。你说「记住」→ 写入规则 → 去重固化。
> **v2.7.2 默认固化阈值10→3。** v2.7.1 P2补全：草稿快速通道。

## 核心能力

- **规则生产**：用户纠正 → 自动生成规则 → 写入 rules/ 目录
- **规则分级**：hard/soft/monitor 三级，含 correction_template
- **固化引擎**：errors.jsonl → 去重 → 写入结构化规则
- **扫盘提取**：自动扫描 SOUL.md/Obsidian/Memory 中的准则

## v2.7.1 补全

### P2 草稿快速通道
- 接收 Mnemonic 同会话推送的草稿，加速固化流程
- 与 Mnemonic v3.5.1 P2 session追踪联动

## v2.7.0 新增（已发布）

### 误报自动降级
- hard 规则被连续否决 ≥3 次 → 自动降为 soft
- 降级后 7 天观察期，期内再次违规恢复原级
- `downgrade_history` 追踪降级事件

### 规则有效期
- `!remember --expires 7d "临时规则"` → 到期自动归档
- `!remember --expires never` → 永久（默认）
- 到期规则移至 `rules/.expired/`

### 已有能力（v2.6.0）
- 规则分级 hard/soft/monitor + 修正模板
- 用户纠正级别调整 + level_history 追踪

## 安装

```bash
npx skills add canon --yes --global
```

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v2.0.0 | Obsidian 结构化 rules/ 目录 |
| v2.4.0 | 规则效果评分 + 角色声明制 |
| v2.5.0 | 定时扫盘 + SOUL 激活 |
| v2.6.0 | 规则分级 + 修正模板 |
| **v2.7.0** | **误报降级 + 规则有效期** |
| **v2.7.1** | **P2补全：草稿快速通道** |

MIT · [L1veSong](https://github.com/L1veSong)
