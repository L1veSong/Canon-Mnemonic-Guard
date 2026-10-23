# sentinel v1.4.0 — 平台适配 · 任务计划

> 日期：2026-06-04 | 触发：Hermes Desktop 试用暴露出跨平台兼容问题
> 前置调研：Doubao + DeepSeek + Hermes 三方交叉验证（findings Section 4）

---

## 一、背景

### 1.1 触发事件

用户试用 Hermes Desktop（官方 v0.15.1），sentinel 插件导致三项致命问题：

| # | 问题 | 根因 |
|---|------|------|
| 1 | CMG 自噬循环 | ban 规则 `cmg-declaration-without-load` 关键词含"激活"，CMG 自己的激活消息被拦 |
| 2 | Desktop 输出死锁 | `transform_llm_output` 替换输出 → Desktop 直接渲染拦截消息，无 AI 重试 |
| 3 | 哨兵劫持用户消息 | `pre_llm_call` sentinel 注入 `[CMG-SENTINEL]` → Desktop 消息流被破坏 |

### 1.2 为什么 CLI 没问题

CLI 有 AI 自我修正循环：输出被拦 → AI 看到拦截 → 重试 → 用户看到干净回复。Desktop/Web/API/Gateway 没有这个循环——拦截消息直接渲染给用户。

### 1.3 为什么现在才暴露

CLI 一直有自我修正遮丑。用户用的飞书/微信平台在 `skill_autoload.per_platform` 里配了 `[]`（不加载 CMG），所以也避开了。Desktop 是第一个同时开启 CMG + 无重试循环的平台。

---

## 二、目标

sentinel 在**所有 Hermes 平台**上可用，不破坏用户体验。

| 平台 | 输出替换 | 哨兵检测 | 哨兵注入 | 工具拦截 |
|------|:--:|:--:|:--:|:--:|
| CLI | ✅ | ✅ | ✅ | ✅ |
| Desktop | ❌ | ✅ 静默 | ❌ | ✅ |
| Web Dashboard | ❌ | ✅ 静默 | ❌ | ✅ |
| Gateway（飞书/微信等） | ❌ | ✅ 静默 | ❌ | ✅ |
| API Server | ❌ | ✅ 静默 | ❌ | ✅ |

---

## 三、方案

### 3.1 核心逻辑

不判断"是什么平台"，判断**"有没有 AI 自愈循环"**。

```
sentinel 启动 → 检测平台能力
  ├─ 有自愈循环（CLI）→ interactive 模式
  │    ├─ transform_llm_output: ON（输出替换 + AI 重试）
  │    ├─ pre_llm_call sentinel: ON（注入 [CMG-SENTINEL]）
  │    └─ pre_llm_call 任务推荐: ON
  │
  └─ 无自愈循环（Desktop/Web/API/Gateway）→ direct 模式
       ├─ transform_llm_output: OFF（不替换输出）
       ├─ pre_llm_call sentinel: 静默（检测 + 写 errors.jsonl，不注入上下文）
       └─ pre_llm_call 任务推荐: OFF
       
所有平台：pre_tool_call: ON（工具层拦截，跨平台兼容）
```

### 3.2 平台检测

```python
def _detect_platform_capability() -> str:
    """返回 'interactive' 或 'direct'"""
    # Desktop 后端有 HERMES_DESKTOP_CHILD_PID
    if os.environ.get("HERMES_DESKTOP_CHILD_PID"):
        return "direct"
    # CLI（无特殊信号 → 默认 interactive，向后兼容）
    return "interactive"
```

**为什么不是完整平台枚举？** Hermes 没有统一的平台标识机制。未来如果 Hermes 框架加了 `HERMES_PLATFORM` 环境变量，再切换为精确检测。当前用"能力检测"更鲁棒。

### 3.3 配置

```yaml
sentinel:
  output_mode: auto    # auto | interactive | direct
  
  # auto（默认）: 自动检测。Desktop → direct，其他 → interactive
  # interactive: 强制全开。CLI 用户无需改配置
  # direct: 强制静默。给已知有问题的平台用，或用户主动关闭
```

### 3.4 哨兵静默模式

哨兵在 direct 模式下仍然运行（检测纠正 + 写 errors.jsonl + escalation），但 `_pre_llm_call` 不返回 `{"context": flag}`。

**为什么保留哨兵检测？** 用户纠正 → 写入 errors.jsonl → 触发 solidify → CMG 规则库增长。这是 CMG 的核心记忆循环，不能因为 Desktop 就丢掉。

---

## 四、改动清单

### Phase 1：平台检测 + 钩子分流（当前会话）

| # | 文件 | 改动 | 状态 |
|---|------|------|:--:|
| 1 | `sentinel/__init__.py` | 新增 `_detect_platform_capability()` | ✅ 已做 |
| 2 | `sentinel/__init__.py` | `_hook_enabled()` 加平台门控 | ✅ 已做 |
| 3 | `sentinel/__init__.py` | `_pre_llm_call()` 哨兵静默模式 | ✅ 已做 |
| 4 | `~/.hermes/config.yaml` | 恢复 CLI 默认（全部 ON） | ✅ 已做 |
| 5 | `~/.hermes/self-reflection/rules/ban/` | 修复两个误伤规则 | ✅ 已做 |

### Phase 2：验证 + 文档（待做）

| # | 内容 | 说明 |
|---|------|------|
| 6 | CLI 回归测试 | 发送"好问题" → sentinel 拦截 → AI 自修正 → 用户看到干净回复 |
| 7 | Desktop 回归测试 | 重启 Desktop → 正常对话 → 无拦截消息 → 哨兵静默记录 |
| 8 | 更新 CHANGELOG | sentinel v1.4.0 变更记录 |
| 9 | 更新 findings/progress | 记录 Desktop 试用教训 |

### Phase 3：未来（待 Hermes 框架支持）

| # | 内容 | 前置条件 |
|---|------|---------|
| 10 | 精确平台检测 | Hermes 注入 `HERMES_PLATFORM=cli|desktop|web|gateway|api` |
| 11 | Gateway 平台适配 | 飞书/微信等消息平台是否需要 output_mode 调整 |
| 12 | output_mode 细粒度控制 | 每个钩子独立开关，而非全局 interactive/direct |

---

## 五、验证标准

### CLI（interactive 模式）

```
1. 发送"好问题！我很乐意帮你" → transform_llm_output 拦截
   → AI 看到 [CMG 拦截] → 重新生成干净回复 → ✅
2. 发送"你又犯了这个" → pre_llm_call sentinel 触发
   → 注入 [CMG-SENTINEL] → errors.jsonl 追加 → ✅
3. 发送"打包发布" → pre_llm_call 任务推荐触发
   → 推荐 ralph-loop + VBC + authoring → ✅
4. 直接 patch SKILL.md → pre_tool_call 拦截 → ✅
```

### Desktop（direct 模式）

```
1. 正常对话 → 无 [CMG 拦截] 消息 → ✅
2. 发送"你又犯了这个" → 哨兵静默检测 → errors.jsonl 追加
   → 对话不受影响 → ✅
3. 直接 patch SKILL.md → pre_tool_call 拦截 → ✅
```

---

## 六、风险

| # | 风险 | 概率 | 缓解 |
|---|------|:--:|------|
| R1 | 未知平台被误判为 interactive | 低 | `output_mode: direct` 手动覆盖 |
| R2 | `HERMES_DESKTOP_CHILD_PID` 改名 | 低 | 代码回退到直接 interactive |
| R3 | Gateway 平台有自愈循环但被标为 direct | 低 | 每个 Gateway 平台独立验证后再开 |
| R4 | 哨兵静默后用户不知道纠正被记录了 | 中 | 在 `!log` / `!diagnose` 里显示静默记录数 |

---

## 七、不做的事（延期）

| # | 事项 | 原因 | 前置条件 | 目标版本 |
|---|------|------|---------|:--:|
| 1 | Gateway 平台逐个验证 | 飞书/微信已关 CMG，其他平台未启用 | 用户启用某个 Gateway 平台 + 反馈问题 | v1.5.0 |
| 2 | 精确平台枚举（`HERMES_PLATFORM`） | 需要 Hermes 框架支持 | Hermes 官方加环境变量 | v2.0 |
| 3 | 每个钩子独立开关 | 复杂度高，边际收益低 | 有具体场景需要差异化 | v2.0 |
| 4 | RAG 知识注入（v1.4.0 原计划） | 本次 Desktop 修复优先级更高 | 平台适配稳定后 | v1.4.1 |

---

## 八、Desktop 试用教训（写入 CMG 规则）

| # | 教训 | 状态 |
|---|------|:--:|
| 1 | `transform_llm_output` 输出替换仅在 AI 自愈循环存在时安全 | findings 记录 |
| 2 | ban 规则关键词不能是通用单字/双字词（"激活""CMG""打包"等） | findings 记录 |
| 3 | 任何新平台接入前，必须先验证 sentinel 兼容性 | findings 记录 |
| 4 | CLI 的 AI 自我修正循环掩盖了 Plugin 设计缺陷——不能假设所有平台都有 | findings 记录 |

---

## 九、关联文档

- `cmg-next-iteration_findings.md` — 防幻觉三源分析 + Desktop 发现
- `cmg-next-iteration_progress.md` — 进度日志
- `cmg-antihallucination-v1.4.0_plan.md` — v1.4.0 原计划（防幻觉，本次平台适配插入为前置 Phase）
