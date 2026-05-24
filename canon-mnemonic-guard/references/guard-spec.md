# Guard 护栏线规格 v4.0.0

> 从 Canon Mnemonic Guard v2.4.1 剥离。当前为规格文档，v4.0.0 实施为独立 Skill。

---

## 五层拦截器

```
Interceptor 接口       ← 每个拦截器独立开关、独立日志
  ├── BanInterceptor              精确匹配拦截
  ├── FabricationInterceptor      防幻觉拦截
  ├── StepCompletenessInterceptor 防跳步骤拦截
  ├── SkillLoadInterceptor        防偷懒拦截
  └── ClarifyInterceptor          防瞎猜拦截
```

---

## 拦截检查流程

### 1. ban_check — 精确匹配

```
当前思考文本 → 逐条比对 patterns.json 中所有 ban keywords
→ 命中 → 触发拦截 + hit_count += 1
→ 未命中 → 通过
```

### 2. no_fabrication — 防幻觉

```
当前输出文本 → 识别"声称型语句" (我能/我有/我会/已经创建了/存在...)
→ 每一条声称 → 核实:
  - 声称 Skill → 查 skills_list
  - 声称 API → 查 web_search 或 memory
  - 声称数据 → 查 source
→ 有 1 条无法核实 → 触发 action_on_fail
```

### 3. complete_steps — 防跳步骤

```
用户原始指令 → 拆解为步骤列表
→ 已完成步骤 → 从上下文提取
→ 未完成步骤 → 触发 action_on_fail (追加执行)
```

### 4. load_skills — 防偷懒

```
当前任务文本 → 提取领域关键词 (如 "论文"→学术, "代码"→开发, "金融"→数据)
→ 扫描 skills_list 输出 → 匹配领域 Skill
→ 检查是否已通过 skill_view 加载
→ 如果 0 个匹配 Skill 已加载 → 触发 action_on_fail
```

### 5. use_clarify — 防瞎猜

```
当前步骤 ≥ 2 个可选项 且 需要用户决策
→ 检查是否已调用 clarify
→ 未调用 → 触发 action_on_fail
```

---

## 评分计数器 (v2.4.1)

每次拦截检查后，更新 rules/ 目录中对应规则的 frontmatter：

```
命中时: hit_count += 1, last_triggered = now()
误报时: false_positives += 1 (用户说「这不是错误」后写入)
```

固化引擎运行时读取 hit_count / false_positives 计算评分。

---

## 运行时数据流

```
Canon 规则库 (rules/*.md)
        │
        ▼
  Guard 读取规则 → 五层拦截检查 → 命中/误报计数
        │
        ▼
  拦截日志 → intercept_log.jsonl
  评分更新 → rules/*.md frontmatter
```

---

## v4.0.0 实施规划

- 独立 Skill 包：`guard`
- 角色声明：`role: guard, stage: pre_action`
- 运行时读取 Canon rules/ 目录 + Mnemonic state.json
- 拦截日志独立记录到 `~/.hermes/self-reflection/intercept_log.jsonl`
