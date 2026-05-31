# Canon-Mnemonic-Guard Dashboard v1.0.0

Web 可视化仪表盘，为 [Canon-Mnemonic-Guard 三省引擎](https://github.com/L1veSong/canon-mnemonic-guard) 提供规则浏览、引擎配置、配套技能监控和规则增删改查功能。

## 快速开始

```bash
# 安装依赖
pip install pyyaml

# 启动
python3 server.py
# 浏览器打开 http://localhost:8765
```

在 Hermes Agent 对话中直接说 `!dashboard` 即可触发。

## 功能概览

### 规则库
- 76+ 条规则，支持搜索、按类型筛选（禁止/缺失/偷懒/元规则）
- 列排序不抖动（table-layout:fixed + 箭头旋转动画）
- 点击展开查看详情（创建日期、最后触发、误报、来源）
- 关键词 tooltip 悬停弹簧动画
- 悬浮窗编辑关键词和描述
- 删除确认弹窗

### 引擎配置
- 17 个 cmg-guard Hook 可视化开关
- 拦截通知模式：静默替换 / 前置说明
- 配套技能总开关 + 各技能独立开关
- 实时检测安装状态（扫描 Hermes / Claude Code / gstack / OpenClaw / Codex 五个技能目录）
- 刷新按钮重新扫描
- 按模块独立保存，不串扰

### 添加规则
- 四种类型选择（ban / gap / lazy / meta）
- 写入 `rules/<type>/` 目录，自动生成 frontmatter

### 主题与语言
- 暗色/亮色双主题，跟随系统 + localStorage 记忆
- 完整中/英文切换，覆盖所有 UI 文本

### 动画
- 统计卡片 hover 上浮 + 阴影
- Toast 从底部滑入
- 保存按钮按下缩放
- Tab 切换淡入
- 排序箭头旋转
- 弹窗淡入 + 背景锁定

## 架构

```
server.py               # 单文件：HTTP 服务器 + HTML + CSS + JS（零外部 web 依赖）
~/.hermes/self-reflection/   # 数据源（rules/ 目录）
~/.hermes/config.yaml        # 配置源（cmg_guard 段）
```

## 配套技能检测路径

| Agent | 路径 |
|-------|------|
| Hermes | `~/.hermes/skills/` |
| Claude Code | `~/.claude/skills/` |
| gstack | `~/.agents/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.codex/skills/` |
| Hermes 插件 | `~/.hermes/plugins/` |

通过扫描 SKILL.md frontmatter 的 `name:` 字段匹配（正则，不 YAML 解析——避免特殊字符崩溃）。

## 依赖

- Python 3.7+
- PyYAML

## 常见问题

1. **后台启动卡死** — `server.py` 的 `webbrowser.open()` 在无桌面环境卡住。改用 `python3 -c "import http.server,server;s=http.server.HTTPServer(('127.0.0.1',8765),server.DashboardHandler);s.serve_forever()"` 后台启动。
2. **配置修改后需重启 Hermes** — cmg-guard 插件只在启动时读取 config.yaml。
3. **端口冲突** — `lsof -ti:8765 | xargs kill` 杀旧进程。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
