# Changelog

## v5.6.0 (2026-05-31)

### 新增
- **Dashboard v1.0.0**: 配套 Web 可视化仪表盘。规则浏览/搜索/筛选/排序，Hook 开关 + 拦截通知管理，7 个配套技能实时状态监控，中英文切换，亮暗主题，16 种交互动画，编辑悬浮窗，规则增删改查
- **反思提示**: CMG 加载后自动注入 `[CMG 反思]` 提醒——每次行动前检查是否有更好的配套 skill。任何平台生效，无需 Plugin
- **meta 类型**: 新增第四种规则类型"元规则"（rules/meta/ 目录），用于管 CMG 引擎自身的系统级规则

### 更新
- **guard v4.8.3**: 文档精简，从 686 行压缩到 77 行。保留五层拦截器规格、cmg-guard 插件 Hook 表、安装命令和常见坑点
- **cmg-guard v1.3.1**: 拦截范围从 patch/skill_manage + ~/.hermes/skills/ 扩展到 write_file/terminal/execute_code + 任意路径（含桌面）。每次拦截提示具体替代工具
- **canon-mnemonic-guard 外观**: 新增 meta 类型目录、Dashboard 引用、反思提示注入、guard 版本号更新

### 修复
- Dashboard: 配套技能检测覆盖 5 个 Agent 目录 + 插件目录（Hermes / Claude Code / gstack / OpenClaw / Codex）
- Dashboard: 配套技能列表排除个人工具，只保留公开推荐技能
- Dashboard: 亮色主题圆角变量补全
- Dashboard: `table-layout:fixed` + `padding:14px` 排序不抖不挤
- Dashboard: Hook 保存独立按钮，按模块隔离不串扰

## v5.5.5 (2026-05-30)

cmg-guard v1.3.0 + 四名冲突检测。详见 v5.5.5 发布说明。
