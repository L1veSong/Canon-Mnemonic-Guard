---
type: gap
id: rule_gap_skill_verify_before_recommend
date: 2026-06-08
hit_count: 0
keywords: [skills_list, 推荐, 安装skill, 这个skill, 建议装, 可以装, 你缺, 需要装]
level: hard
correction_template: |
  检测到正在推荐或建议安装某个 skill。
  必须先用 skill_view(name) 验证该 skill 可加载（返回 success: true）。
  skills_list 中有条目 ≠ SKILL.md 可加载。
  验证失败 → 如实报告，不推荐该 skill，寻找替代方案。
source: 2026-06-08 audiocraft/sd两个skill列表有但加载失败
---

# 推荐 skill 前必须验证可加载性

禁止仅凭 `skills_list` 返回结果推荐 skill。

## 为什么

`skills_list` 展示的是 skill 注册表索引，不等于 SKILL.md 实际文件存在且可解析。索引与文件可能不同步——skill 名在注册表中但实际文件已损坏/缺失。

## 验证流程

1. 确定要推荐的 skill 名称
2. 调用 `skill_view(name)` → 检查返回的 `success` 字段
3. `success: true` → 可安全推荐
4. `success: false` 或 `not found` → 不可推荐，如实告知用户

## 实战案例

2026-06-08：向李吉扬推荐 `audiocraft-audio-generation` 和 `stable-diffusion-image-generation`，两者在 skills_list 中显示正常，但 skill_view 均返回 "not found"。导致推荐了两个不可用的 skill，需要临时找替代方案（comfyui 覆盖 SD、freesound 替代 AudioGen）。
