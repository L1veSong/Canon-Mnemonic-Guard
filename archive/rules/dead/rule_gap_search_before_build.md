---
type: gap
id: rule_gap_search_before_build
date: 2026-06-08
hit_count: 0
keywords: [新建, 创建, 自建, 从零, 手写, 自己写, 做一个skill, 建一个, 造轮子]
level: soft
correction_template: |
  检测到准备新建/自建某个工具或 skill。
  建议先 web_search 确认是否存在现成可用的开源项目或社区 Skill。
  评估后决定：直接装 / 适配引用 / 确无现成→自建。
  本规则为 soft 级别：仅提醒，不阻断。
source: 2026-06-08 计划自建Skill A，搜索后发现Seedance+vlog可复用
---

# 新建前先搜索网上现成资源

声明「新建/自建/从零写」任何工具、Skill、脚本前，先用 `web_search` 确认是否存在现成可用的开源项目或社区资源。

## 为什么

不是所有东西都需要从零写。搜 5 分钟可能省下几天开发时间。能装就装，能引用就引用，只自建真正定制的部分。

## 搜索清单

1. 有没有现成的开源项目？（GitHub search）
2. 有没有 Hermes 社区已有的 Skill？（skills_list + web_search "hermes skill XXX"）
3. 有没有可以直接引用/适配/安装的参考资源？（文档、prompt 库、workflow 模板）

## 实战案例

2026-06-08：计划为 AI 短剧项目从零自建「剧本+分镜+提示词 Skill A」。在动手前 web_search 发现：
- `Seedance2.0-prompt-skill`（GitHub 开源，Z/Y/X/F 运镜代码 + 6 种剪辑节奏公式）→ 直接引用
- `vlog-auto-edit`（Hermes 社区 Skill，MIT 许可，ffmpeg 全流程已验证）→ 可直接安装

不搜就造 = 重复造轮子。搜后再造 = 站在已有的肩膀上。
