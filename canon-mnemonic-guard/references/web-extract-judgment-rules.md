# web_extract 判断规则 v2026-06-28

> 用户 2026-06-28 纠正：不要每次都先 web_extract。自行判断站点类型。

## 规则
遇到外部 URL 时自行判断站点类型选择工具。禁止不加判断就调用 web_extract。

## 判断表
| 站点类型 | 工具 | 原因 |
|---------|------|------|
| raw.githubusercontent.com / .md / .json / .txt | web_extract | 纯文本，快省 token |
| API 裸接口 | web_extract | 结构化数据 |
| 官网/文档站/博客 | browser | JS 渲染 |
| GitHub 页面 | browser | JS 渲染 |
| 高德/大众点评/抖音等 SPA | browser | web_extract 必失败 |
| 用户报错/问进度/问配置 | 不验证 | 直接回答 |

## 相关
- CMG SKILL.md 坑点 52: Gaode web_extract 不可用
- CMG SKILL.md 坑点 59: web_extract 前置浪费 80%
- SOUL.md 铁则第 6 条
