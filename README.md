# Canon-Mnemonic-Guard 三省引擎 v5.6.0

取自「吾日三省吾身」—— AI 自我反思引擎。规则生产（典则）、状态记忆（忆存）、行为拦截（护栏）、反思提示、Web 仪表盘，五线协作。

## 组件

| 组件 | 版本 | 类型 | 说明 |
|------|------|------|------|
| canon | 2.7.2 | Skill | 典则线 — 规则生产库 |
| guard | 4.8.3 | Skill | 护栏线 — 五层拦截执行器（精简版） |
| mnemonic | 3.5.3 | Skill | 忆存线 — 模式识别 + 草稿推送 |
| canon-mnemonic-guard | 5.6.0 | Skill | 外观层 — 反思提示 + 微型调度器 |
| canon-mnemonic-guard-dashboard | 1.0.0 | 工具 | Web 可视化仪表盘 |
| skill-autoload | 1.0.1 | Plugin | 自动加载插件 |
| cmg-guard | 1.3.1 | Plugin | 全工具全路径硬拦截 + 反思门禁 |

## v5.6.0 新功能

**Dashboard** — 单文件 Python 服务器，`python3 server.py` 一键启动：
- 规则浏览/搜索/筛选/排序，展开详情，编辑关键词和描述
- Hook 开关、拦截通知、配套技能实时状态
- 规则导出 ZIP、拦截趋势图、批量操作
- 中英文切换、亮暗主题、虚拟滚动

**反思提示** — CMG 加载后每次行动前提醒检查配套 skill，所有平台生效。

**规则类型互转** — 编辑弹窗可修改规则类型，自动迁移文件目录。

## 安装

```bash
# 一键安装
./install.sh

# 或手动：
cp -r canon guard mnemonic canon-mnemonic-guard ~/.hermes/skills/software-development/
cp -r skill-autoload cmg-guard ~/.hermes/plugins/
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

## Dashboard

```bash
pip install pyyaml
python3 canon-mnemonic-guard-dashboard/server.py
# 浏览器打开 http://localhost:8765
# 或在 Hermes 对话中说 !dashboard
```

## 许可证

MIT License
