# Changelog — Canon 典则线

## [2.4.1] — 2026-05-22

### 四包制独立发布
- 从 CMG v5.1.0 物理拆分，成为独立 `canon` Skill
- 保留全部 Canon 核心逻辑：扫盘提取、固化引擎、冲突检测、规则评分、动态阈值、导入导出、健康检查

## v2.6.0 — 规则分级 + 修正模板 (2026-05-23)

### 新增
- 规则分级: hard/soft/monitor 三级，Guard 根据级别决定拦截策略
- 修正模板 (correction_template): 每条 hard 规则配置具体修正方向
- frontmatter 新增字段: level, correction_template, level_history
- 用户纠正时的级别调整: monitor→soft→hard，当前会话强化、跨会话恢复
- !remember 增强: --hard/--soft 参数，!monitor 命令

### 修复
- 激活标记版本号: CMG v5.3.0 → v5.3.1
