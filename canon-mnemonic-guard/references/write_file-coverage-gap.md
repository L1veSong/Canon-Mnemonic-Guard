# sentinel write_file 覆盖缺口

> 2026-06-24 实战：dashboard.html 两次被 write_file 覆写，sentinel 未拦截。

## 缺口

sentinel 的 `pre_tool_call` 钩子拦截以下操作：
- `patch` 操作 SKILL.md
- `skill_manage` 操作 SKILL.md
- `terminal` 含写操作符（sed, >, >>, tee, mv, cp, rm）

**不拦截：** `write_file` 工具。无论写的是 `.html`、`.py`、`.md`，sentinel 全部放行。

## 影响

单文件 HTML（含内联 CSS/JS）被 `write_file` 覆写时：
- 无备份检查
- 无内容完整性验证
- 无回滚路径

## 当前缓解

CMG ban 规则 `ban_no_backup_before_write`（hard）要求：
- write_file/patch 前必须 `cp backup`
- 备份文件命名: `<原文件名>.bak.<MMDDHHMM>`

但此规则仅靠 AI 自觉（sentinel 不拦 write_file）。

## 长期方向

sentinel `pre_tool_call` 扩展 `write_file` 检测：
- HTML/py/md 文件 → 检查最近备份是否存在
- 无备份 → 拦截并提示
- 有备份 → 放行

归入 sentinel v2.0 架构升级。
