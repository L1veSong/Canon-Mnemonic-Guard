---
type: ban
id: ban_assume_tool_installed
date: 2026-05-30
last_triggered: 2026-05-30
hit_count: 1
false_positives: 0
source_ids: [err_20260530111454]
keywords: [假设已安装, 以为装好了, 默认工具可用, 不验证安装状态, 推荐工具前不检查, vault≠app]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
tags: [基础设施验证, 推荐流程]
correction_template: |
  推荐/使用任何工具前，先实测安装状态（ls / which / --version），
  不复用记忆假设、不凭文件存在推断（数据文件存在 ≠ 应用已装）。
---

# 禁止推荐/使用工具前不验证安装状态

**规则：** 推荐工具、讨论功能、指导使用前，先验证是否已安装。

**案例（2026-05-29）：** CMG推荐列表里obsidian在典则线数周，多次讨论图谱视图，用户问「在哪打开图谱视图」才发现 /Applications/Obsidian.app 不存在。vault文件存在≠应用安装。

**正确做法：** ls验证比「看起来有文件」可靠。
