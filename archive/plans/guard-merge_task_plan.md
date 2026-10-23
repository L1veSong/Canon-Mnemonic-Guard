# Guard 合并优化 — 任务计划

> 目标：sentinel 插件代码迁入 Guard 目录，Guard 从「纯文档」变为「文档 + 内核执行」统一体

## Phase 1: 结构准备

- [ ] Guard 目录新增 plugin.yaml（声明为 skill + plugin 双角色）
- [ ] sentinel `__init__.py` → Guard `__init__.py`（改名、改注释）
- [ ] sentinel CHANGELOG 并入 Guard CHANGELOG
- [ ] sentinel README 关键内容并入 Guard README
- [ ] Guard SKILL.md 重写（去规格化，留精炼版）

## Phase 2: SKILL.md 优化目标

当前 686 行 → 目标 ~200 行。砍掉：
- 五层拦截器的详细执行步骤（现在代码里有了）
- 上下文感知检测步骤（代码里或砍掉）
- 动态清单生成规格（未实现，砍）
- 闭环重试引擎详细规格（代码里或砍）
- 版本变更表（移到 CHANGELOG）

保留：
- Guard 是什么（一句话）
- 能力清单（表格）
- 安装/配置
- 常见坑点
- 参考文件链接

## Phase 3: 代码优化

- `__init__.py` 更名为 Guard 统一执行体
- 合并 Skill 层尚有用的逻辑（如有）
- 清理冗余注释和预留空函数

## Phase 4: 生态适配

- CMG SKILL.md 更新 Guard 版本号和描述
- CMG README 更新架构（Guard = skill + plugin）
- CMG CHANGELOG 记录合并事件
- config.yaml 更新（sentinel 插件路径改为 Guard）
- 删除独立的 sentinel 插件目录

## Phase 5: 验证与打包

- 重启 Hermes 验证 Guard 插件加载
- 验证 pre_tool_call / post_llm_call 仍生效
- 桌面重新打包（5 组件）
- 推 GitHub
