---
type: lazy
id: rule_lazy_012_桌面文件被write_file清空
date: 2026-05-23
hit_count: 1
severity: high
detector: path_write
protection_paths: ["/Desktop/", "/桌面/"]
keywords: [桌面文件被write_file清空]
level: hard
correction_template: "write_file 会完全覆盖目标文件。写入前先确认目标路径正确、内容完整。写入后立即 read_file 验证文件大小 > 0 且内容正确。"
---

# 桌面文件被write_file清空

多次使用write_file写入README/CHANGELOG时覆盖了整个桌面目录,导致SKILL.md/JSON文件丢失。需重新从工作副本rsync恢复。

触发 1 次 | 严重度: high
