# CMG 生态系统更新日志

## v5.5.4 (2026-05-28) — cmg-guard v1.2.0

### cmg-guard v1.1.0 → v1.2.0
- **步骤完整性检查**：pre_llm_call 新增 4 条强制规则（链接完整阅读、文件覆盖度校验、Orchestrator clarify、Skill workflow 执行）
- **分阶段升级系统**：同一错误逐步升级（第1次标记→第2次警告→第3次推草稿→第5次黑名单）
- **新增 post_llm_call 钩子**：AI 回复后二次黑名单扫描
- 哨兵正则优化

### 子包版本
- canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3（无变更）
- canon-mnemonic-guard v5.5.4（版本号跟踪）
- skill-autoload v1.0.1（无变更）

---

## v5.5.3 (2026-05-26) — 哨兵 + 一键部署

### 新增

- **双层哨兵**：A 层（cmg-guard Plugin）正则广撒网 + B 层（CMG Skill）LLM 语义判断，关键词漏网率从 80% 降至接近零
- **意图识别优先规则**（rule_meta_001）：用户纠正自动触发 CMG 三步走，不等追问
- **init.py 自动配置**：安装时自动写入 config.yaml（启用插件 + 自动加载），零手动
- **一键卸载**：`python3 init.py --uninstall` 恢复安装前状态，不碰其他配置

### 变更

- cmg-guard v1.0.0 → v1.1.0：新增 `pre_llm_call` sentinel hook（默认开启），三组正则覆盖 80%+ 纠正句式
- skill-autoload v1.0.0 → v1.0.1：`pre_system_prompt` → `pre_llm_call`，适配 Hermes ≥v0.14.0
- init.py：+Phase 7.5 自动配置 config.yaml，+--uninstall/--purge 卸载支持
- README：重写为完整安装指南 + 兼容性矩阵

### 兼容性

- Hermes ≥v0.14.0：三层全开
- Hermes ≤v0.13.x：skill-autoload 需降级到 v1.0.0（pre_system_prompt）
- 其他 Agent：Skill 层可用，Plugin 层不可用

### 子包版本

- canon v2.7.2 / guard v4.8.2 / mnemonic v3.5.3（无变更）
- canon-mnemonic-guard v5.5.3（+init.py 增强）

---

## v5.5.1 (2026-05-25) — 三层闭环首次发布

### 新增插件

- skill-autoload v1.0.0：pre_system_prompt 自动加载 CMG
- cmg-guard v1.0.0：transform_llm_output 硬拦截

### canon-mnemonic-guard v5.5.1

- README 更新为三层闭环说明
- 配套生态加入两个新插件

---

## v5.5.0 (2026-05-25) — 微型调度器

- 微型调度器：Guard 拦截自动匹配配套 skill
- P1-P4 全部完成

---

## v5.4.0 (2026-05-24) — 大更

- P1: 同会话升级 + P3: 用户纠正提升 + P4: 误报降级
- Mnemonic v3.5.0: 上下文保留

---

## v5.3.0 (2026-05-23) — 风险分级

- Guard 风险分级（不可逆操作暂停确认）

---

## v5.2.0 (2026-05-22) — 四包制

- 定时扫盘 + 协调日志 + 一键诊断
- !scan-recommendations

---

## v5.1.0 (2026-05-21) — 四包分装

- Canon / Guard / Mnemonic 物理拆分

---

## v5.0.0 (2026-05-20) — 三线合一

- 典则 + 护栏 + 忆存 → 三省引擎
