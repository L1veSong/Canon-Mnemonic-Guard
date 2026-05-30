# cmg-guard v1.3.0

> Hermes 插件：CMG 规则系统级强制拦截。17 个 hook 全阶段覆盖，从"事后检查"升级为"全链路拦截"——AI 跳步骤直接阻断、未经授权修改 SKILL.md 内核拦截、断言须附证据。

---

## 定位

cmg-guard 是 CMG（三省引擎）的**配套硬拦截插件**，不是 CMG 核心四线。

CMG 核心四线：
```
Canon v2.7.2        → 典则线（规则生产库）
Mnemonic v3.5.3     → 忆存线（状态记忆层）
Guard v4.8.3        → 护栏线（规则执行器，77行精炼版）
canon-mnemonic-guard v5.5.5 → 外观层（四包索引 + 调度器 + 四名冲突检测）
```

配套插件：
```
skill-autoload → 自动加载 CMG Skill（加载辅助）
cmg-guard      → 系统级硬拦截（本插件）
```

和 CMG Skill 不同：Skill 层靠 AI 自觉遵守，可以被跳过。cmg-guard 在 Hermes 内核层拦截——AI 没有机会绕过去。

---

## 五层防护（v1.3.0 17hooks 全阶段）

```
pre_tool_call
  │  ① 直接 patch SKILL.md 未经 authoring → 内核拦截
  ▼

pre_llm_call
  │  ② 黑名单扫描 — 永久禁止的行为直接阻断
  │  ③ 哨兵检测   — 识别用户纠正意图
  │  ④ 步骤完整性 — 该做的事没做就拦截
  │  ⑤ 任务推荐   — 检测任务类型，建议配套工具（打包→ralph-loop+VBC，写代码→TDD，调试→diagnose）
  ▼

LLM 生成回复
  │
  ▼
transform_llm_output
  │  ⑥ 关键词扫描 — ban 规则命中 → 替换为拦截消息
  ▼

post_llm_call
  │  ⑦ 自披露闭环 — "测试通过"无证据 → 拦截
  │  ⑧ 任务完成验证 — "完成/搞定"无核对痕迹 → 拦截
  │  ⑨ 外部来源验证 — "我看了/三个AI同意"无原文摘录 → 拦截
  │  ⑩ 二次黑名单 — AI 回复后再扫一轮
  ▼

输出给用户（干净或拦截）
```

---

## v1.3.0 核心新特性

### pre_tool_call 硬阻断
直接调用 patch 工具修改 SKILL.md 未加载 hermes-agent-skill-authoring → 内核拦截。治本方案——不再依赖 AI 自觉。

### 自披露闭环（post_llm_call）
- **任务完成证据校验**：AI 声称"完成/搞定/已打包" → 检查后续输出有无实质内容 → 无数据拦截
- **外部来源主张验证**：AI 声称"我看了/三个AI都同意/交叉验证" → 无原文摘录 → 拦截
- **拦截通知 visible 模式**：用户可选择透明化拦截详情

### pre_llm_call 任务推荐
检测用户消息中的任务关键词（打包/写代码/调试/测试），自动推荐 CMG 配套工具。每会话每任务类型仅提醒一次，不刷屏。

---

## 步骤完整性检查

AI 准备回复时，cmg-guard 先检查该做的事做没做：

| 规则 | 触发条件 | 拦截条件 |
|------|---------|---------|
| 链接完整阅读 | 会话中出现了 HTTP 链接 | 未调用 web_extract + vision_analyze 看完所有内容（含图片） |
| 文件覆盖度校验 | 刚创建/修改了持久化文件 | 未逐条核对后输出 N/N 确认 |
| Orchestrator clarify | 正在执行 IF/planning 等流程 | 每阶段结束未用 clarify() 让用户确认 |
| Skill workflow 执行 | 用户说"跑一遍/走一遍 XX" | 只读了文档未执行完整 workflow |

任一条不满足 → LLM 调用被阻断，system prompt 注入强制补完指令。

---

## 分阶段升级系统

同一个错误不会立刻进黑名单。根据违规次数逐步升级：

| 次数 | 级别 | 行为 | 对应 CMG 规则级 |
|------|------|------|:--:|
| 第1次 | SENTINEL | 标记提醒，AI 注意即可 | monitor |
| 第2次(同会话) | SENTINEL-L2 | 警告拦截，必须纠正 | soft |
| 第3次(7天内) | SENTINEL-L3 | 建议固化规则，推 rule 草案 | hard |
| 第5次+ | BLACKLIST | 永久禁止，全链路拦截 | hard |

升级状态持久化到 `~/.hermes/self-reflection/escalation.json`，跨会话不丢失。

---

## 安装

```bash
cp -r cmg-guard ~/.hermes/plugins/
```

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - cmg-guard

# cmg-guard v1.3.0 配置（4 个核心默认开启，其余按需）
cmg_guard:
  intercept_notice: silent        # silent(静默) | visible(透明)
  hooks:
    pre_tool_call: true           # 堵 SKILL.md 直接改
    pre_llm_call: true            # 步骤检查 + 哨兵 + 黑名单 + 任务推荐
    post_llm_call: true           # 自披露闭环 + 来源验证
    transform_llm_output: true    # ban 关键词替换
    # 以下按需开启
    post_tool_call: false
    transform_tool_result: false
    transform_terminal_output: false
    pre_api_request: false
    post_api_request: false
    on_session_start: false
    on_session_end: false
    on_session_finalize: false
    on_session_reset: false
    pre_gateway_dispatch: false
    pre_approval_request: false
    post_approval_response: false
    subagent_stop: false
```

安装后重启 Hermes 生效。启动日志中看到 `[cmg-guard] v1.3.0 registered` 即成功。

---

## 所有 17 个 Hook

| 阶段 | Hook | 用途 | 默认 |
|------|------|------|:--:|
| 工具调用 | `pre_tool_call` | SKILL.md 修改门禁 | ✅ |
| 工具调用 | `post_tool_call` | 工具调用后审计 | |
| 工具调用 | `transform_tool_result` | 工具假报检测 | |
| LLM | `pre_llm_call` | 步骤完整性 + 哨兵 + 黑名单 + 任务推荐 | ✅ |
| LLM | `post_llm_call` | 自披露闭环 + 二次黑名单 | ✅ |
| LLM | `pre_api_request` | API 请求前拦截 | |
| LLM | `post_api_request` | API 响应后审计 | |
| 输出 | `transform_llm_output` | 关键词硬拦截 | ✅ |
| 输出 | `transform_terminal_output` | 终端输出拦截 | |
| 会话 | `on_session_start` | 会话启动检查 | |
| 会话 | `on_session_end` | 会话结束审计 | |
| 会话 | `on_session_finalize` | 最终化检查 | |
| 会话 | `on_session_reset` | 重置检查 | |
| 网关 | `pre_gateway_dispatch` | 网关分发前拦截 | |
| 网关 | `pre_approval_request` | 审批请求前拦截 | |
| 网关 | `post_approval_response` | 审批响应后审计 | |
| 子 Agent | `subagent_stop` | 子 Agent 停止拦截 | |

---

## 原理

### 规则加载
启动时读取 `~/.hermes/self-reflection/rules/ban/*.md`，提取每条规则的 frontmatter 中的 `keywords` 字段，构建关键词匹配库。

### 钩子执行流

**pre_tool_call**（每次工具调用前）：
1. 检测 patch/skill_manage 目标是否为 SKILL.md
2. 检查 hermes-agent-skill-authoring + writing-skills 是否已加载
3. 未加载 → 拦截，要求先加载 authoring

**pre_llm_call**（每次 LLM 调用前）：
1. 扫描用户输入 → 匹配黑名单（level 4 才命中）
2. 扫描用户输入 → 哨兵正则匹配（否定词模式）→ 匹配则记录升级
3. 检查会话上下文 → 是否有未完成的步骤 → 有则阻断
4. 检测任务关键词 → 推荐配套工具（每会话每类型仅一次）

**transform_llm_output**（每次 AI 回复后）：
1. 扫描 AI 输出全文 → 关键词匹配 ban 规则
2. 命中 → 输出替换为 `[CMG 拦截] 请遵守规则重新回答`
3. AI 下一轮看到拦截消息 → 自动修正

**post_llm_call**（v1.3.0 增强）：
1. 扫描 AI 回复 → 任务完成声明验证（"完成/搞定"无证据 → 拦截）
2. 扫描 AI 回复 → 外部来源主张验证（"我看了/三个AI同意"无引文 → 拦截）
3. 扫描 AI 回复 → 二次黑名单检查

---

## 配置参考

```yaml
cmg_guard:
  intercept_notice: silent        # silent(静默替换) | visible(拦截详情透明)
  hooks:
    pre_tool_call: true
    pre_llm_call: true
    post_llm_call: true
    transform_llm_output: true
    # 其余 13 个 hook 默认 false，按需开启
```

---

## 依赖

- **Hermes Agent**（需支持 pre_tool_call / pre_llm_call / transform_llm_output / post_llm_call 钩子）
- **CMG Skill**（提供 `rules/ban/*.md` 规则库——canon + guard + mnemonic）

---

## 文件结构

```
cmg-guard/
├── __init__.py        # 插件主逻辑（806行 v1.3.0）
├── plugin.yaml        # 插件元数据
├── README.md          # 本文件
├── CHANGELOG.md       # 版本历史
└── LICENSE            # MIT
```

运行时数据：
```
~/.hermes/self-reflection/
├── escalation.json     # 升级状态
├── blacklist.json      # 永久黑名单（自动生成，level≥4）
└── rules/ban/*.md      # ban 规则库（由 CMG Skill 维护）
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.3.0 | 2026-05-30 | 17hooks + pre_tool_call阻断 + 自披露闭环 + 任务推荐 |
| v1.2.0 | 2026-05-28 | 步骤完整性检查 + 分阶段升级 + post_llm_call |
| v1.1.0 | 2026-05-25 | 轻量哨兵（否定词正则） |
| v1.0.0 | 2026-05-20 | 初始发布，transform_llm_output 关键词拦截 |

详见 [CHANGELOG.md](CHANGELOG.md)

---

## License

MIT © 2026 L1veSong
