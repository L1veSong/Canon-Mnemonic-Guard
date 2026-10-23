# Sentinel v2.0 行为级检测器 · 实施计划

> 目标版本: sentinel v2.0.0 | 关联: CMG v5.6.0 / master-status 第 18 项
> 背景: 规则库 69 条中 9 条(4 gap + 3 lazy + 2 meta)无硬拦, 全靠 AI 自觉。sentinel 只扫 ban/
> 缺口确认: 2026-09-03 代码审计 _load_ban_keywords/_inject_active_rules 仅覆盖 rules/ban

## 一、设计

规则文件 frontmatter 新增 `detector` 字段(配置驱动, 新增规则零代码):

| detector | hook | 行为 | 对应规则 |
|----------|------|------|---------|
| inject | pre_llm_call | 关键词/URL 匹配 → 注入该规则 correction_template 提示 | gap_skip_web_extract, lazy_011, meta_reasonix, lazy_010 |
| output | post_llm_call | 回复缺少必需格式 → 追加提醒 | gap_ssr_report |
| toolseq | pre_llm_call | 任务触发词命中 + 会话工具轨迹缺必需工具 → 注入缺失警告(soft) | gap_007, gap_008, gap_009 |
| path_write | pre_tool_call | 写路径命中危险规则 → **硬阻断**(block) | lazy_012 |

已覆盖无需改造: meta_001(纠正识别,_scan_user_message 已管), gap_ssr_no_limit(SSR 程序侧)

## 二、改动清单

1. `~/.hermes/plugins/sentinel/__init__.py`
   - `_load_behavior_rules()` — 泛化加载 gap/lazy/meta 目录 + detector 字段(复用 _parse_fm)
   - `_behavior_check_enabled()` — config.yaml sentinel.behavior_check 开关(默认 true)
   - `_behavior_inject()` / `_behavior_output_check()` / `_behavior_toolseq()` / `_behavior_path_check()`
   - `_pre_llm_call` / `_post_llm_call` / `_pre_tool_call` 三处接入
   - `register()` 日志加 behavior=ON/OFF
   - 会话工具轨迹: 复用 `_get_session()` 记录已用工具名
2. 9 条规则文件 frontmatter 补 detector + detector_args(触发词/必需工具/参考路径)
3. `~/.hermes/config.yaml` sentinel 段加 `behavior_check: true`
4. 版本号: __init__.py / plugin.yaml / README / CHANGELOG → v2.0.0
5. master-status: 第 18 项 行为级检测器 → 已完成; 19/20(自动重试闭环/三层验证管线) → 下一版本

## 三、验证

- 重启 Hermes → grep agent.log 注册行含 behavior=ON
- 单测: _behavior_inject("写skill") 触发 gap_007; _behavior_output_check 无[SSR 使用]触发; _behavior_path_check(~/Desktop/x.md); _behavior_toolseq(发布无 grep)
- 确认不误伤: 常规消息零注入

## 四、风险

- toolseq 为 soft(注入警告)非 hard(拦截) — 工具轨迹可能因会话轮转不完整, 硬拦会误杀
- path_write 为 soft — 桌面写入在部分场景合法, 只提醒不阻断
- inject 频率控制: 同一规则同一会话只注入一次(session cache)

## 五、延期(非本次)

- 行为级 hard 拦截(B 层 LLM 语义判断): 需要 LLM 端点, 单发
- 自动重试闭环 / 三层验证管线: v2.1.0+ 按 master-status 19/20

## 六、热修复 v2.0.1（2026-09-13）

- 症状: 每小时 cron tick + 疑似纠正消息 → gateway 日志 `Hook 'pre_llm_call' callback _pre_llm_call raised: name 'timezone' is not defined`
- 根因: `_save_escalation` / `_maybe_add_to_blacklist` 使用 `datetime.now(timezone.utc)`，但 import 仅有 `datetime`
- 影响: `_scan_user_message` 命中纠正模式 → `_record_correction` 抛异常 → 整个 pre_llm_call 回调中断（活跃规则/URL 注入之后全部跳过；escalation/blacklist 不落盘）
- 修复: `from datetime import datetime, timezone`（单行）
- 验证: pyflakes 0 undefined；隔离单测 _record_correction/_maybe_add_to_blacklist 通过；重启后注册日志 v2.0.1
