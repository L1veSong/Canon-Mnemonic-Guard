# Canon-Mnemonic-Guard Dashboard v1.0.0

Web 可视化仪表盘，单文件 Python 服务器，零外部 web 依赖。

## 启动

```bash
pip install pyyaml
python3 server.py
# http://localhost:8765
```

## 功能

- 规则库：搜索/筛选/排序，展开详情，编辑关键词和描述，添加/删除
- 引擎配置：17 Hook 开关，拦截通知，配套技能实时状态
- 规则导出 ZIP
- 30 天拦截趋势柱状图
- 批量操作（Shift+范围选中、批量删除）
- 规则类型互转
- 虚拟滚动（200+ 规则流畅）
- 中英文切换、亮暗主题

## 配套检测

Dashboard 自动扫描以下目录：
- `~/.hermes/skills/`（Hermes）
- `~/.claude/skills/`（Claude Code）
- `~/.agents/skills/`（gstack）
- `~/.openclaw/skills/`（OpenClaw）
- `~/.codex/skills/`（Codex）

## 依赖

Python 3.7+, PyYAML
