---type: ban
id: ban_lazy_scanning
date: 2026-05-30
last_triggered: 2026-05-30
hit_count: 3
false_positives: 0
source_ids:
- err_20260530112931
keywords:
- 扫描偷懒
- 路径太窄
- 只搜顶层
- 没递归
- 假警报
- 不验证就说缺
tags:
- 基础设施验证
- 扫描
correction_template: '验证安装状态必须递归搜索：find ~/.hermes/skills -name "SKILL.md" -maxdepth
  5 | xargs grep -l "name: xxx"

  禁止只检查固定路径（如 ~/.hermes/skills/xxx/SKILL.md）——文件可能在子目录下。

  '
superseded: rule_ban_verify_install_path
superseded_date: '2026-09-07'
---

# 禁止扫描时路径不递归

**规则：** 验证文件/工具是否存在时，必须递归搜索，不能假设固定路径。

**违反记录（3次）：**
- 2026-05-25：CMG规则数 33/8/9 错报为 10/2/2（没数实际文件）
- 2026-05-29：三个已安装skill误报为缺失（只搜了顶层目录）
- 根因：偷懒——用最简单的路径假设代替实际搜索

**正确做法：** find -maxdepth 5 递归 + grep 验证，不行就多种路径都试。
