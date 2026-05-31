# CMG Dashboard 开发记录

> 2026-05-30 | 来源: CMG v5.5.5 Dashboard 全流程开发

## 架构决策

- **Python HTTP 服务器 + 单 HTML 前端** — 零外部依赖
- **服务端渲染** — 每次请求实时读取 `~/.hermes/self-reflection/` 数据，不缓存
- **API 端点**: `GET /api/rules` `GET /api/stats` `GET /api/config` `POST /api/config` `POST /api/rules`
- **配置修改** — 通过 API POST 写回 `config.yaml`，重启 Hermes 生效

## 文件

```
~/.hermes/dashboard/
├── server.py     # HTTP 服务器 (localhost:8765)
└── generate.py   # 静态 HTML 生成器（备用，file:// 打开用）
```

## 触发方式

- Hermes 对话中: `!dashboard`
- CLI: `python3 ~/.hermes/dashboard/server.py`

## 功能

| Tab | 功能 |
|-----|------|
| 规则库 | 75 条规则可搜索/排序/筛选，6 张统计卡片，关键词悬停气泡展开 |
| 引擎配置 | 17 个 Hook 可视化开关 + 拦截通知模式切换 + 保存到 config.yaml |
| 添加规则 | Web 表单创建新规则，自动生成 .md 文件到 rules/<type>/ |

## 踩坑

1. **Python 三重引号内嵌 JS 的转义陷阱** — `toggleHook(\''+h+'\')` 被 Python 吃掉反斜杠。修复：用 `data-*` 属性。详见 `hermes-agent-skill-authoring/references/python-js-escaping-pitfall.md`
2. **POST 测试冲掉 config.yaml** — 测试时只传了 1 个 hook，覆盖了全部 17 个。修复：前端传完整对象。
3. **`days_since` 计算失败** — naive vs timezone-aware datetime 减法抛异常。修复：`parse_days_since()` 多格式兼容 + 强制 UTC。
