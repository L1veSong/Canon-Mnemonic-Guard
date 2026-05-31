# Changelog

## v5.6.0 (2026-05-31)

### 新增
- **Dashboard v1.0.0**: Web 可视化仪表盘，单文件 Python 服务器。规则浏览/搜索/筛选/排序，引擎配置管理，配套技能实时状态监控，规则增删改查，中英文切换，亮暗主题，16 种交互动画
- **规则导出 ZIP**: 一键导出全部规则为 ZIP 文件
- **拦截趋势图**: 30 天拦截柱状图（Canvas 渲染），无数据时显示提示
- **规则类型互转**: 编辑弹窗支持修改规则类型（ban/gap/lazy/meta），自动迁移文件
- **虚拟滚动**: 表格容器限高 600px，表头固定，按需渲染可见行，200+ 规则不卡
- **批量操作**: 批量模式支持 Shift+点击范围选中、全选、批量删除
- **一键安装**: `install.sh` 脚本，自动安装全部组件
- **反思提示**: CMG 激活后注入 `[CMG 反思]` 提醒——每次行动前检查是否有更好的配套 skill

### 更新
- **guard v4.8.3**: 文档精简，从 686 行压缩到 77 行，保留核心规格和常见坑点
- **cmg-guard v1.3.1**: pre_tool_call 拦截扩展到 write_file/terminal/execute_code + 任意路径
- **canon-mnemonic-guard 外观**: 新增 meta 类型目录、Dashboard 引用、反思提示、版本号更新

### 修复
- Dashboard: 配套技能检测覆盖 5 个 Agent 目录 + 插件目录
- Dashboard: 亮色主题圆角变量补全
- Dashboard: table-layout:fixed 排序不抖，padding 统一不挤

## v5.5.5 (2026-05-30)

cmg-guard v1.3.0 + 四名冲突检测。
