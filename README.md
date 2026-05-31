# Canon-Mnemonic-Guard 三省引擎 v5.6.0

取自「吾日三省吾身」—— AI 自我反思引擎。规则生产（典则）、状态记忆（忆存）、行为拦截（护栏）、反思提示，四线协作。

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

## v5.6.0 更新

- **Dashboard v1.0.0**: 规则浏览/搜索/筛选/排序，引擎配置管理，7 个配套技能状态监控，中英文切换，亮暗主题，16 种交互动画
- **guard v4.8.3**: 文档精简，从 686 行压缩到 77 行
- **cmg-guard v1.3.1**: 拦截范围扩展到 write_file/terminal/execute_code + 任意路径
- **反思提示**: CMG 激活后自动注入 [CMG 反思] 提醒——每次行动前检查是否有更好的配套 skill
- **meta 类型**: 第四种规则类型"元规则"（rules/meta/ 目录）

## 安装

```bash
git clone https://github.com/L1veSong/Canon-Mnemonic-Guard.git
cd Canon-Mnemonic-Guard

# 四线 Skill
cp -r canon guard mnemonic canon-mnemonic-guard ~/.hermes/skills/software-development/

# 插件
cp -r skill-autoload cmg-guard ~/.hermes/plugins/

# 一键初始化
python3 ~/.hermes/skills/software-development/canon-mnemonic-guard/scripts/init.py
```

## Dashboard

```bash
pip install pyyaml

# 方式一：CLI 命令
./canon-mnemonic-guard-dashboard/cmg dashboard

# 方式二：直接启动
python3 canon-mnemonic-guard-dashboard/server.py

# 浏览器打开 http://localhost:8765
```

从 Hermes 对话中直接说 `!dashboard` 即可触发。

Dashboard 是单文件架构：`server.py` 内含 HTTP 服务器 + HTML 页面 + CSS 样式 + JavaScript 逻辑。无需额外 HTML 文件。

## 许可证

MIT License
