# Changelog — Canon 典则线

## v2.6.0 — 规则分级 + 修正模板 (2026-05-23)

### 新增
- 规则分级: hard/soft/monitor 三级，Guard 根据级别决定拦截策略
- 修正模板 (correction_template): 每条 hard 规则配置具体修正方向
- frontmatter 新增字段: level, correction_template, level_history
- 用户纠正时的级别调整: monitor→soft→hard，当前会话强化、跨会话恢复
- !remember 增强: --hard/--soft 参数，!monitor 命令

## v2.5.2 — SOUL 激活 (2026-05-22)

- SOUL 激活机制: init 时询问写入激活标记到 SOUL.md
- 扫盘时检测标记存在 + 版本匹配
- 用户删标记即停用

## v2.5.1 — 推荐扫描 (2026-05-20)

- 推荐列表自动扫描 (!scan-recommendations)
- plugins 扫描源支持

## v2.5.0 — 定时扫盘 (2026-05-19)

- C1 定时扫盘: 加载时检查距上次扫盘天数
- 超阈值自动触发

## [2.4.1] — 2026-05-18

### 四包制独立发布
- 从 CMG v5.1.0 物理拆分，成为独立 `canon` Skill
