# Changelog — Guard 护栏线

## [4.0.0] — 2026-05-21

### 初始发布 — 从 Canon v2.4.1 剥离独立

**五层拦截器**
- BanInterceptor: 精确关键词匹配拦截
- FabricationInterceptor: 防幻觉声称核实
- StepCompletenessInterceptor: 指令步骤完整性检查
- SkillLoadInterceptor: 领域 Skill 加载检测
- ClarifyInterceptor: 多选项强制 clarify

**评分计数器**
- 命中自动 `hit_count += 1, last_triggered = now()`
- 误报回调写入 `false_positives += 1`
- 数据回写 Canon rules/ 目录 frontmatter

**拦截日志**
- `intercept_log.jsonl`: 每次拦截的完整记录
- 供 Mnemonic v3.0.0 自动模式识别消费

**三线联动**
- 读取 Canon rules/ + patterns.json + errors.jsonl
- 读取 Mnemonic state.json
- 单向消费，不反向污染
