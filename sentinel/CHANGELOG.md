# CHANGELOG

## v2.0.2 (2026-09-15) — 契约修复 + 误伤清理（审计驱动）

### 修复
- **pre_tool_call 双契约错位（三处，全通道此前从未生效）**：①返回值——核心现收 `{"action": "block", "message"}`，旧 `{"block": True, "reason"}` 被静默忽略；②入参——核心以 `args=`/`assistant_response=` 传参，旧代码收 `tool_args=`/`response_text=` 永远为空。两处均已对齐（双命名兼容），实测探针验证。
- **判定收窄**：skill 写入按 `.hermes/skills/`、`.agents/skills/`、`SKILL.md` 精确匹配（此前"路径含 skill 字样"连 /tmp 都拦）；终端写入门正则同步收窄。
- **_scan_user_message 误报治理**：新增系统消息前缀豁免（[IMPORTANT/[SYSTEM/cron skill 激活注入）；P1/P3 模式收窄（删"不…了/吧"噪声组合与裸"能不能"）；黑名单移除误伤项 `IMPORTANT The user has invoked`。
- **path_guard 终端判定收窄**：`2>&1` 等纯重定向不再触发 Desktop/保护路径拦截（验收时自测抓出的误伤，回归用例已入契约测试）。
- **post_llm_call 死通道处置**：核心不消费返回值（实测确认）→ 改 record-only，不再声称改写输出。
- **真实语料回扫批次 2**：新建「拿最近真实输出当靶」扫描法（38 条语料一次审出 7 处）；清理 ban_skill_edit_use_right_tool（skill_manage 等裸词——曾吃掉一条验收报告）、禁止自动归档改写铁则库（自动归档裸词）、用户纠错规则（不要再/说清楚等口语片段）、ban_no_backup_before_write（不备份就 收窄为三种具体行为）。违规精确词（如 我瞎编）保留，改写作侧规避引用。
- **词表批次 1（10 条规则）**：瞎编→我瞎编；规则库/cmg规则→行为短语；密钥/明文→行为短语；restore/golden→绑定 a_rules；changelog/隐私/上传前/发布前/全量检查→行为短语或删除；那边说/里面说→移除；不一致/矛盾/模糊→收窄。备份 rules.bak.09151830。
- **词表批次 3（工程用语电池，2026-09-16）**：11 处裸词收窄或移除（硬编码/白名单/炒股/越权/wechat/cookie/retina/hotkey/双击/单击/Bearer），保留精确违规复合形态。

## v2.0.1 (2026-09-13) — 热修复

### 修复
- `_save_escalation` / `_maybe_add_to_blacklist` 缺少 `timezone` 导入 → 纠正识别命中时 `name 'timezone' is not defined`，pre_llm_call 回调中断（escalation/blacklist 不落盘 + 同轮后续子检查全部跳过）。补全 `from datetime import datetime, timezone`。

## v2.0.0 (2026-09-03) — 行为级检测器（gap/lazy/meta 硬拦/注入）

### 新增
- **行为级规则引擎**：规则文件 frontmatter 新增 `detector` 字段（inject/toolseq/output/path_write），sentinel 仅对声明 detector 的规则做机器执行——配置驱动，新增规则零代码
- **inject**（pre_llm_call）：行为规则触发词匹配 → 注入修正提示（会话级去重）——覆盖 gap_skip_web_extract/lazy_010/lazy_011/meta_reasonix
- **toolseq**（pre_llm_call）：任务触发 + 会话工具轨迹缺必需工具 → 流程检查警告——覆盖 gap_007/gap_008/gap_009；pre_tool_call 记录"工具名::关键参数"轨迹（如 skill_view::tdd）
- **output**（post_llm_call）：回复缺必需格式 → 追加格式提醒（预留，当前无规则启用）
- **path_write**（pre_tool_call）：写路径命中保护规则 → 硬阻断——覆盖 lazy_012（桌面目录写入）
- 配置开关 `sentinel.behavior_check`（默认 true）
- _detect_urls 模板更新：不再强制 web_extract，按站点类型提示（对齐坑点 59）

### 修复
- 工具轨迹带参存储（_tool_entry），skill_view::xxx 可区分加载了哪个 skill

### 规则覆盖变化
- 9 条无硬拦规则中 8 条具备机器执行（007/008/009 toolseq，skip_web_extract/lazy_010/lazy_011/meta_reasonix inject，lazy_012 path_write 硬拦）
- gap_ssr_report 保持 advisory（等待 ssr.report 配置）；gap_ssr_no_limit 属 SSR 程序侧；meta_001 已由哨兵扫描覆盖

## v1.4.0 (2026-06-14) — 活跃规则注入 + URL 检测 + 改名

### 新增
- pre_llm_call：活跃规则注入（按任务匹配 5-10 条最相关 ban 规则）
- pre_llm_call：URL 检测提示（检测用户消息中的链接，建议 web_extract）
- post_llm_call：CoVe 自检薄层（Chain-of-Verification 提示）
- 平台检测：Desktop/GUI 自动跳过 pre_llm_call/post_llm_call 不兼容钩子

### 重大变更
- **插件改名**：cmg-guard → sentinel（全链路同步：目录/配置/日志前缀）

### 修复
- register() 迁移到 Hermes 新插件 API
- 审计修复：会话去重、None 防护、时区处理、死代码清理

## v1.3.0 (2026-05-30)

### 新增：17 Hook 全阶段覆盖 + pre_tool_call 阻断 + 自披露闭环

**核心升级：** 从 3 个 hook 扩展到 17 个，覆盖工具调用层 / LLM 层 / 会话层 / 网关层 / 子 Agent 层全部五个阶段。

**新增功能：**

- **pre_tool_call 硬阻断**
  - 直接调用 patch 工具修改 SKILL.md → 内核拦截，要求先加载 hermes-agent-skill-authoring + writing-skills
  - 加载 authoring 后用 skill_manage 操作 → 放行
  - 治本方案：不再依赖 AI 自觉遵守规则

- **自披露闭环** (`post_llm_call`)
  - AI 断言「测试通过了」但未附具体证据 → 拦截，要求补充验证结果
  - 杜绝「张嘴就来」式结论
- **任务完成声明验证** (`post_llm_call` · v1.3.0 同版追加)
  - AI 声称「完成/搞定/好了/就绪/已打包」→ 检查输出后是否有实质内容
  - 无数据 → 拦截
  - 一条规则覆盖所有任务类型
- **外部来源主张验证** (`post_llm_call` · v1.3.0 同版追加)
  - AI 声称「我看了/里面说/三个AI都同意/交叉验证了」
  - 但未附带原文摘录 → 拦截
  - 彻底杜绝「没读到链接却编造链接内容」的臆断行为

- **拦截通知 visible 模式**
  - 用户可选择 visible 模式，拦截详情透明输出

- **17 Hook 全阶段覆盖**

| 阶段 | Hook | 用途 |
|------|------|------|
| 工具调用 | `pre_tool_call` | SKILL.md 修改门禁 |
| 工具调用 | `post_tool_call` | 工具调用后审计 |
| 工具调用 | `transform_tool_result` | 工具假报检测 |
| LLM | `pre_llm_call` | 步骤完整性 + 哨兵 + 黑名单 |
| LLM | `post_llm_call` | 自披露闭环 + 二次黑名单 |
| LLM | `pre_api_request` | API 请求前拦截 |
| LLM | `post_api_request` | API 响应后审计 |
| 输出 | `transform_llm_output` | 关键词硬拦截 |
| 输出 | `transform_terminal_output` | 终端输出拦截 |
| 会话 | `on_session_start` | 会话启动检查 |
| 会话 | `on_session_end` | 会话结束审计 |
| 会话 | `on_session_finalize` | 最终化检查 |
| 会话 | `on_session_reset` | 重置检查 |
| 网关 | `pre_gateway_dispatch` | 网关分发前拦截 |
| 网关 | `pre_approval_request` | 审批请求前拦截 |
| 网关 | `post_approval_response` | 审批响应后审计 |
| 子 Agent | `subagent_stop` | 子 Agent 停止拦截 |

**改进：**
- Hook 从 3 个扩展到 17 个，默认开启 4 个核心 hook，其余按需配置
- 拦截能力从「输出层事后」延伸到「调用层事前 + 全链路审计」

## v1.2.0 (2026-05-28)

### 新增：步骤完整性检查 + 分阶段升级

**核心升级：** 从"输出层事后检查"升级为"调用层事前拦截"。AI 跳步骤时 sentinel 在 LLM 调用前就拦截，不再等输出后再补救。

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
