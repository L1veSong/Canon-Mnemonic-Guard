# CHANGELOG

## v1.2.0 (2026-05-28)

### 新增：步骤完整性检查 + 分阶段升级

**核心升级：** 从"输出层事后检查"升级为"调用层事前拦截"。AI 跳步骤时 cmg-guard 在 LLM 调用前就拦截，不再等输出后再补救。

**新增功能：**

- **步骤完整性检查** (`pre_llm_call`)
  - 链接必须完整阅读（含图片、附件、代码块）
  - 创建文件后必须做覆盖度校验
  - Orchestrator 流程每阶段必须用 clarify() 确认
  - "跑 Skill" 必须执行完整 workflow，不只读文档

- **分阶段升级系统**
  - 第1次违规 → `[SENTINEL]` 标记提醒
  - 第2次同会话 → `[SENTINEL-L2]` 警告拦截
  - 第3次(7天内) → `[SENTINEL-L3]` 建议固化规则
  - 第5次+ → `[BLACKLIST]` 永久禁止
  - 状态持久化到 `escalation.json`，跨会话不丢失

- **新增 `post_llm_call` 钩子**
  - AI 回复后再次扫描黑名单和违规关键词

**改进：**

- 黑名单不再一刀切——只有反复犯 5 次以上才自动加入
- 升级链与 CMG 规则分级 (monitor/soft/hard) 配合工作
- 所有拦截日志通过 Python logging 输出

---

## v1.1.0 (2026-05-25)

### 新增：轻量哨兵

- **双钩子架构**: `transform_llm_output` + `pre_llm_call`
- **A 层哨兵**: 否定词正则扫描用户输入，标记 suspected_correction
- 哨兵默认开启，可在 config.yaml 关闭

---

## v1.0.0 (2026-05-20)

### 初始发布

- `transform_llm_output` 钩子扫描 AI 输出
- 读取 `rules/ban/*.md` 中的关键词
- 命中违规 → 直接替换为拦截消息
- 37 条 ban 规则自动生效
