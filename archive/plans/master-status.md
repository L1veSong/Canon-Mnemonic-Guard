# CMG 总状态追踪

> 最后更新: 2026-09-16 | 版本基线: CMG v5.7.0 + sentinel v2.0.2

---

## 一、当前基线

| 组件 | 版本 | 状态 |
|------|------|:--:|
| canon | 2.7.2 | ✅ |
| guard | 4.8.3 | ✅ |
| mnemonic | 3.5.3 | ✅ |
| canon-mnemonic-guard | 5.6.0 | ✅ |
| sentinel | 2.0.1 | ✅ | v2.0.0 行为级检测器 + v2.0.1 热修复（2026-09-13，timezone import）；原名 cmg-guard |
| skill-autoload | 1.0.1 | ✅ |
| 规则库 | 52 ban / 6 gap / 3 lazy / 2 meta (63 条) | ✅ | M2 去重 77→63（2026-09-07，§八）|
| C/G/M/E 序列 | 18/18 完成 | ✅ |
| P 系列 | P1-P4 完成；P5 评估不实施（2026-09-16） | ✅ |
| Dashboard | v1.0.1 已发布 | ✅ |

---

## 二、已完成事项

| # | 事项 | 日期 | 说明 |
|:--:|------|:--:|------|
| 1 | C/G/M/E 18 项全部闭环 | 2026-05-30 | |
| 2 | P1-P4 增强全部落地 | 2026-05-30 | |
| 3 | sentinel v1.3.2 读写分流修复 | 2026-05-30 | |
| 4 | post_llm_call 两层校验 | 2026-05-30 | |
| 5 | pre_llm_call 任务推荐系统 | 2026-05-30 | |
| 6 | Dashboard v1.0.0 | 2026-05-30 | |
| 7 | 平台适配（Desktop端兼容） | 2026-06-04 | cmg-platform-adaptation |
| 8 | SSR v0.3.0 发布 | 2026-06-05 | |
| 9 | ban_skill_install_fabrication 规则强化 | 2026-06-07 | 新增"手写→源码安装"子规则 |
| 10 | sentinel v1.4.0 平台检测已部署 | 2026-06-11 | `_detect_platform()` + auto-hook-skip |
| 11 | 最优升级方案定稿 | 2026-06-14 | optimal-upgrade_plan.md |
| 12 | sentinel v2.0.0 行为级检测器 | 2026-09-03 | gap/lazy/meta 8/9 规则机器执行: inject/toolseq/output/path_write, 配置驱动 detector 字段 |

---

## 三、本次对话决策（2026-06-14）

| # | 决策 | 结论 |
|:--:|------|------|
| D1 | CMG 架构 | 三条核心线（Canon+Guard+Mnemonic）+ 一条外观（CMG）+ 两个插件（sentinel+skill-autoload） |
| D2 | 规则覆盖度 | 60 ban 有硬拦 / 9 gap+lazy+meta 无硬拦 = 核心矛盾（v5.6.0 清理后 82→69） |
| D3 | CLI/GUI 不等效 | 事后拦截依赖 CLI 交互循环，GUI 无法重试 → v2.0.0 自动重试闭环根治 |
| D4 | sentinel 改名 | ✅ 已完成。全链路：目录/plugin.yaml/config.yaml/__init__.py/SKILL.md/references/plan/CHANGELOG/memory/rules |
| D5 | guard-merge | ❌ 否决。sentinel 并入 Guard = 架构杂交 |
| D6 | 两插件合并 | 💤 可做但不急。skill-autoload 10行代码并入 sentinel，下次顺手 |
| D7 | Plan 文件 | ✅ 已更新。规则数 82→69 修正，版本号/CHANGELOG 同步 |

### 跨项目决策

> 详见各项目 master-status

| # | 决策 | 结论 |
|:--:|------|------|
| X1 | 三项目联动 | SSR→IF 已自然运行。CMG-IF 联动否决（过度设计） |
| X2 | 链路闭环 ✅ | SSR 降噪 → CMG !review → IF gap 报告（三项全部完成，2026-09-16） |

---

## 四、进行中

| # | 事项 | 优先级 | 难度 | 估时 | 阻塞项 | 状态 |
|:--:|------|:--:|:--:|:--:|------|:--:|
| 12 | sentinel v1.4.0 防幻觉收尾发布 | 🔴 高 | 中 | ~3h | — | ✅ 已完成 |
| 12a | ├─ register API 迁移 (旧→新 ctx API) | — | — | — | ✅ 已修复 | 2026-06-14 |
| 12b | ├─ 全量代码审计 (子agent, 发现 2HIGH+5MEDIUM+3LOW) | — | — | — | ✅ 已审计 | 2026-06-14 |
| 12c | ├─ 审计修复 (去重/None防护/日期/死代码/正则) | — | — | — | ✅ 已修复 | 2026-06-14 |
| 12d | ├─ 重启验证 (活跃规则注入✅+URL检测✅) | — | — | — | ✅ 已通过 | 2026-06-14 |
| 12e | ├─ sentinel 全链路改名 (cmg-guard→sentinel) | — | — | — | ✅ 已完成 | 2026-06-14 |
| 12f | ├─ Dashboard 七项修复 (时区/DPR/i18n/自适应) | — | — | — | ✅ 已完成 | 2026-06-14 |
| 12g | ├─ CHANGELOG 补全 (CMG v5.6.0 + sentinel v1.4.0) | — | — | — | ✅ 已完成 | 2026-06-14 |
| 12h | └─ 打包 + 发布审计 (9/9 全绿) | — | — | — | ✅ 已审计 | 2026-06-14 |
| 13 | gap/lazy→ban 升级（3-5条规则） | 🔴 高 | 低 | ~1h | ✅ v2.0.0 行为级检测器替代（2026-09-03，比升级 ban 更优：保留 advisory + 机器执行双模式） |
| 14 | !review 规则减负实施 | ✅ 已完成（2026-09-16 核实接入） | 低 | 已上线 | — |

---

## 五、下一版本

| # | 事项 | 目标版本 | 前提 |
|:--:|------|:--:|------|
| 15 | pre_llm_call 活跃规则结构化注入 | sentinel v1.5.0 | v1.4.0 发布 |
| 16 | 哨兵跨会话提醒（GUI端补齐） | sentinel v1.5.0 | 同上 |
| 17 | P5: !mode simple\|expert | ❌ 评估不实施（2026-09-16） | 需求从未明确 |
| 18 | 行为级检测器（gap/lazy/meta） | sentinel v2.0.0 | ✅ 已完成 2026-09-03 |
| 19 | 自动重试闭环 | sentinel v2.0.0 | 行为级检测器就绪 |
| 20 | 三层验证管线 | sentinel v2.0.0 | 自动重试验证通过 |
| 21 | !lint 规则冲突检测命令 | ❌ 评估不实施（2026-09-16） | 目标已被 !review 体检覆盖 |
| 22 | Example Hub（规则示例库） | ❌ 评估不实施（2026-09-16） | 对内零收益；_TEMPLATE.md 已够用 |

### 远期项目编号（独立序号，不与上面重叠）

| 23 | RAG 知识库 | v1.4.0 跑稳 + 检索命中率不够 |
| 24 | 多 Agent 验证 | Hermes 支持免费模型做验证 Agent |
| 25 | 双模型自动分流 | Hermes 暴露模型路由 hook |

---

## 六、已知问题

| # | 问题 | 影响 | 计划解决 |
|:--:|------|------|:--:|
| 1 | gap/lazy/meta 不被 sentinel 拦截 | 9 条规则靠 AI 自觉 | ✅ v2.0.0 已解决：8/9 机器执行（007/008/009 toolseq；skip_web_extract/lazy_010/lazy_011/meta_reasonix inject；lazy_012 path_write 硬拦）；gap_ssr_report 待 ssr.report 配置 |
| 2 | _index.md 与实际文件数漂移 | diagnose 报不一致 | 下次 !solidify 同步修复 |
| 3 | CLI/GUI CMG 功能不等效 | GUI 无输出替换+无重试 | v2.0.0 自动重试闭环 |

---

## 七、相关文件

| 文件 | 内容 |
|------|------|
| `optimal-upgrade_plan.md` | ★ 最优升级方案（本文档的详细版） |
| `antihallucination-v1.4.0_plan.md` | v1.4.0 防幻觉完整实现计划 |
| `platform-adaptation_task_plan.md` | Desktop 兼容（已完成） |
| `dashboard_task_plan.md` | Dashboard 四期规划 |
| `rule-governance_task_plan.md` | !review 规则减负设计 |
| `deepseek-review_plan.md` | DeepSeek 外部评审对照 |
| `guard-merge_task_plan.md` | ⚠️ 过期：sentinel并入Guard（15天无进展） |

---

## 八、2026-09-07 状态自动化改造（维护记录，非升版）

| # | 事项 | 结果 |
|:--:|------|------|
| M1 | 状态维护机械化 | `~/.hermes/self-reflection/maintain.py` + cron `cmg-state-maintain`(每日9:00, no_agent) → state/index 自动同步，根治 state 冻结 |
| M2 | 规则库去重 | 77→63 (ban 52 / gap 6 / lazy 3 / meta 2)；12 组合并 + 2 条空占位归档 → rules/dead/；keywords 并入保留规则；备份 rules.bak.09071932 |
| M3 | 绝对化规则豁免 | 8 条规则加豁免句（用户明确要求省略或成本/时间优先时可跳过，须说明原因） |
| M4 | 行为分级澄清 | SKILL.md 明确 hard=硬拦 / soft=注入提醒 / monitor=仅记录；自觉层=提示层，非拦截层 |
| M5 | 体检脚本 | `scripts/review-rules.py`（!review 可接入） |
| M6 | errors.jsonl 清理 | 3 条损坏行隔离至 errors.jsonl.corrupt，95 条可解析 |
| M7 | 版本同步 | sentinel 描述 v1.4.0→v2.0.0；历史记载逐一核对无误伤 |
| M8 | 关键词精确化（2026-09-08） | ban_dashboard_dev_without_skills / ban_act_before_verify / ban_format_migration_must_grep_all 裸词(dashboard/开发/验证/假设/v3/迁移) → 行为短语；修掉「讨论 Dashboard 也被拦」的误杀；备份 rules.bak.09081158 |
| M9 | 体检集成 | review-rules.py +宽泛关键词检测([5] 候选)；!review 命令文档更新 |
| M10 | sentinel 拦截语义修复（2026-09-08） | ①`_scan_text` 实为子串匹配(kw in lower)非正则→全库 36 个 `.*` 死关键词改写为真实子串 ②插件 `_load_ban_keywords` 现解析 level 字段，soft/monitor 仅记录不替换输出（40+8 条不再打断对话）③全库 frontmatter 规范化（keywords 单行 flow 格式，sentinel 手写解析器只认此格式；yaml.dump 多行格式丢失 14 条加载，52/52 全量恢复）④裸词精确化：dashboard/开发/验证/假设/素材/发布/上传/备份/CMG 等 → 行为短语 ⑤真实 sentinel 模块 12/12 测试通过。备份 rules.bak.09081158 + __init__.py.bak.09081220 |
| M11 | sentinel v2.0.1 热修复（2026-09-13） | timezone NameError 修复（_save_escalation/_maybe_add_to_blacklist import 补全）；pyflakes 静态扫描 0 undefined；重启 gateway + desktop 后端加载验证 |
| M12 | sentinel v2.0.2 契约修复 + 误伤清理（2026-09-15） | pre_tool_call 三处契约迁移（`{"action":"block"}`，此前全通道失效）；skill/终端写入判定收窄；_scan_user_message 系统前缀豁免+模式收窄；post_llm_call 改仅记录（核心不消费返回值）；词表批次1（10 条规则）+ 批次2（真实语料回扫，清 skill_manage/自动归档/不要再/不备份就 等裸词）；黑名单移除误伤项。备份 sentinel *.bak.09151830 + rules.bak.09151830。回归测试：`python3 ~/.hermes/plugins/sentinel/tests/test_contract.py` |
| M13 | Mnemonic 线评估（2026-09-15） | 纸面空转（recognized_patterns=0，冻结自 5/30）；职能已被 sentinel P1/P3 覆盖 → 标停用，不投工开发 |
| M14 | 全量 grep 审计（2026-09-16，用户指令） | CMG：reference 死链 2 处重命名对齐（cmg-guard-v1.3.2→sentinel- / v5.4.0→v5.5.0）、hermes-desktop 技能内跨平台文档重命名（cmg-guard-cross-platform→sentinel-cross-platform）、future-release-plan 陈旧路径修正、cmg-audit 版本引用同步 v2.0.2；Dashboard：server.py 旧 key cmg_guard→sentinel ×7 + generate.py 版本 badge v5.5.5→v5.6.0 ×2（6/14 改名欠账，记录在案但代码未落地），备份 .bak.09160927；规则词表收窄 11 处（工程用语电池：硬编码/白名单/炒股/越权/wechat/cookie/retina/hotkey/双击/单击/Bearer）；SSR 版本面断层 → 已同步（SSR v3.0.1 于当日发布，见 ssr master-status §十三/§十四） |
| M15 | GitHub 发布 v5.7.0（2026-09-16） | 仓库 L1veSong/Canon-Mnemonic-Guard 推送 v5.7.0（commit d9096a2，28 文件 +1273/−333）：sentinel v2.0.2（契约修复 + 回归测试）+ Dashboard v1.0.1 + 技能文档全量升版（SKILL.md / README / CHANGELOG / ROADMAP：注入消息、诊断样例、init.py 三处、审计基线）+ references 对齐（2 改名 / 2 新增 / 5 更新）；Release + 资产 CMG-Ecosystem-v5.7.0.zip（2.0MB）；隐私终扫零命中。遗留：本地 skill 根目录 3 文档（README / CHANGELOG / ROADMAP）位于工具夹缝，已同步（2026-09-16，见 M19） |
| M16 | 收款码素材清理（2026-09-16） | 用户确认收款码为弃用方案：canon-mnemonic-guard/assets/ 两张图片（1.7MB，idea-foundry 素材副本、CMG 文档零引用）从仓库移除并推送；v5.7.0 Release 资产替换为轻量版（不含图，约 300KB）；本地 skill 本就无 assets 无需同步；历史提交未做改写。 |
| M17 | 文档链接卫生（2026-09-16） | 全量扫描三仓库+两本地副本：SSR 0 处；CMG 30 处（21 本地文档 / 5 跨技能 / 2 本机路径 / 1 全外链 404 / 1 死链）→ 全部去链接化 + 提交推送 + 资产刷新（commit 见仓库）；IF 1 处同修 |
| M18 | 挂账清算（2026-09-16，用户委托评估） | ①`!review`：核实早已接线（命令表 + 脚本实测通过），清掉重复行 + 补数据时效注释 ②P5 / !lint / Example Hub：评估不实施——P5 需求从未明确；!lint 目标被 !review 体检覆盖；Example Hub 对内零收益、模板已够用 |
| M19 | 本地同步验收（2026-09-16） | 用户执行 sync-all.sh；11/11 cmp 全过（CMG 3 + IF 8，时间戳 10:42）；技能版本库已收录（a39d272）；IF 两个模板测试 issue 经用户决定保留不动 |
| M20 | 三面对账 + 副本漂移修复（2026-09-16） | 全量对账：远端=克隆 3/3 ✓｜克隆=本地实体 109/109 ✓（含模板嵌套文件）｜youhong 副本查出 8 处漂移（CMG 根文档×3 / SSR 引擎 / sentinel 引擎+README+CHANGELOG+测试文件）→ 全部补齐复验 12/12 ✓（备份 youhong-bak-0916-2）；skill-autoload / rtk-rewrite 副本核验一致；技能版本库残余 0 |

未做（有意保留）：
- `!solidify`：95 条 errors 均为 AI 执行错误，按规则不固化（rule_070）
- #19 自动重试闭环 / #20 三层验证管线：延期至 sentinel v2.1（收益/成本未达标）
- #14 !review：✅ 已接入（2026-09-16 核实：命令表 + `scripts/review-rules.py` 实测通过）
- P5 / !lint / Example Hub：✅ 评估完成（2026-09-16）→ 三项均不实施（理由见规划表 17 / 21 / 22 行）
- 已知问题 2（_index 漂移）：由 M1 cron 每日自动修复，问题已闭环
