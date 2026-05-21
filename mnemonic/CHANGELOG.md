# Changelog — Mnemonic 忆存线

## [3.0.0] — 2026-05-21

### 初始发布 — 状态记忆层独立 Skill

**自动模式识别**
- 读取 Guard intercept_log.jsonl，按关键词分组统计
- 同一关键词 7 天内 ≥ 3 次 → 自动生成规则草稿
- 推送至 Canon 固化引擎，不直接写入 rules/

**CLI 命令**
- `hermes reflect status` — 规则库状态
- `hermes reflect add` — 手动添加规则
- `hermes reflect scan` — 手动扫盘
- `hermes reflect patterns` — 高频模式查看

**角色声明**
- `role: memory, stage: background`
- 独立进程模式：不作为 Skill 加载，作为 Hermes 守护进程常驻

**三线联动**
- 读取 Guard intercept_log.jsonl + Canon errors.jsonl
- 推送规则草稿至 Canon 固化引擎
- 不生产规则、不执行拦截
