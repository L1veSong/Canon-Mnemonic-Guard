---
type: ban
id: rule_incomplete_readme_before_conclusion
date: 2026-05-23
last_triggered: 2026-09-22
hit_count: 8
hits_block: 2
hits_record: 6
telemetry_synced: 2026-09-22
false_positives: 0
level: soft
source_ids: [err_incomplete_readme_001]
correction_template: "安装评估前必须完整阅读官方 README + 搜索目标平台关键词 + 先跑官方安装命令。请先完成以上步骤再下结论。"
keywords: [readme没读, 没查官方文档, install.sh, 平台支持, 没查文档, 跳步, 下结论]
tags: [information-gathering, skill-installation]
---

# 禁止：不读完官方文档就下结论

## 触发场景

用户要求安装/评估某个工具，打开 GitHub 仓库后。

## 规则

**安装或评估任何第三方工具前，必须完整执行以下步骤，不得跳步：**

1. 阅读 README 全文（不是摘要）
2. 搜索关键词（目标平台名：hermes、openclaw 等）
3. 检查 install.sh 或 setup 脚本是否列出目标平台
4. 先运行官方安装命令，失败后再判断是否需要适配

## 错误模式

```
打开仓库 → 看到 CLAUDE.md → "这是 Claude Code 插件" → 结论"需要适配"
                    ↑
              跳过了 README 的 Multi-Platform Installation
              跳过了 install.sh 里的 hermes 条目
              跳过了 grep hermes
```

## 正确流程

```bash
# 1. 完整读 README
web_extract(urls=["仓库地址"])

# 2. 搜索目标平台
grep -i hermes README.md install.sh

# 3. 先试官方安装
bash install.sh hermes

# 4. 失败后再说"需要适配"
```

## 拦截行为

检测到"这是 XX 插件，需要适配才能用"结论，但在对话中未出现 install.sh / Multi-Platform / grep 搜索结果 → 拦截，要求先跑官方安装流程。
