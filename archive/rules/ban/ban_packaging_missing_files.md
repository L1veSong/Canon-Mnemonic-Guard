---
type: ban
id: ban_packaging_missing_files
date: 2026-05-23
last_triggered: 2026-09-08
hit_count: 4
hits_block: 4
hits_record: 0
telemetry_synced: 2026-09-22
false_positives: 0
keywords: [打包发布, 缺文件, 漏文件, 漏组件]
tags: [发布流程, 打包]
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: "发布打包时必须包含 references/ 和 assets/ 目录。用 find 对比源目录和桌面包，确保所有子目录和文件完整无遗漏。"
---

# 发布打包不得遗漏 references/ 和 assets/

**规则：** 打包桌面 ZIP 时，必须包含完整的 references/ 目录（所有 .md 参考文档 + templates/ 模板）和 assets/ 目录。

**禁止：** 只复制 SKILL.md/README.md/CHANGELOG.md/LICENSE/init.py 就声称打包完成。

**检查清单：**
- [ ] SKILL.md · README.md · CHANGELOG.md · LICENSE · init.py
- [ ] references/ 下所有 .md 文件
- [ ] references/templates/ 完整
- [ ] assets/ 目录
- [ ] canon/ · guard/ · mnemonic/ 三线子包

v5.2.1 开始丢失 references/ 和 assets/，直到 v5.3.0 用户指出才发现——跨了三个版本。
