---type: ban
id: rule_ban_004_ZIP不验证
date: 2026-05-23
hit_count: 1
severity: critical
keywords:
- ZIP不验证
level: hard
correction_template: 声称 ZIP 已更新前必须先 unzip -l 验证内容。ZIP 必须从桌面包直接压缩。验证通过前不许说'可以发布'。
superseded: rule_066_zip_clean_before_pack
superseded_date: '2026-09-07'
---

# ZIP不验证

声称'ZIP已更新可以发布'但ZIP实际是旧版v8.2.0,包含过时内容,未包含assets/.github等新文件。重复2次。

触发 1 次 | 严重度: critical
