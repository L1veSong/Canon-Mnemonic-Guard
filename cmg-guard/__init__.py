"""
cmg-guard v1.3.0: Full hook coverage + pre_tool_call + completion-evidence + external-claim check.

v1.3.0: + pre_tool_call SKILL.md edit gate (default ON)
        + post_llm_call completion-without-evidence check (default ON)
        + session state tracking for authoring skill detection
        + configurable hook system (17 hooks, 4 default ON, 13 opt-in)
        + hook-enable check via config.yaml cmg_guard.hooks.*

v1.2.0: + pre_llm_call step-completeness checker + global blacklist.
v1.1.0: + sentinel regex + escalation system.
v1.0.0: + transform_llm_output ban keyword scanner.

Unlike the CMG skill (AI reads rules and self-polices), this plugin runs
inside Hermes — the AI has no opportunity to skip or rationalise past it.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

_CONFIG_CACHE: Optional[dict] = None
_SESSION_FLAGS: Dict[str, dict] = {}
_BLACKLIST_CACHE: Optional[Set[str]] = None


def _load_cmg_config() -> dict:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE
    try:
        from hermes_cli.config import load_config
        raw = load_config()
        cfg: dict = raw.get("cmg_guard", {})
    except Exception:
        cfg = {}
    _CONFIG_CACHE = cfg
    return _CONFIG_CACHE


def _hook_enabled(hook_name: str) -> bool:
    """Check if a specific hook is enabled. CORE hooks default ON, others OFF."""
    cfg = _load_cmg_config()
    hooks_cfg = cfg.get("hooks", {})
    core_defaults = {
        "pre_tool_call": True,
        "pre_llm_call": True,
        "post_llm_call": True,
        "transform_llm_output": True,
    }
    if hook_name in core_defaults:
        return hooks_cfg.get(hook_name, core_defaults[hook_name])
    return hooks_cfg.get(hook_name, False)


def _intercept_notice_mode() -> str:
    """silent (default) or visible — how to display interception notices."""
    cfg = _load_cmg_config()
    return cfg.get("intercept_notice", "silent")


def _sentinel_enabled() -> bool:
    cfg = _load_cmg_config()
    if "lightweight_sentinel" not in cfg:
        return True
    return bool(cfg["lightweight_sentinel"])


def _step_check_enabled() -> bool:
    cfg = _load_cmg_config()
    if "step_check" not in cfg:
        return True
    return bool(cfg["step_check"])


# ---------------------------------------------------------------------------
# Session state tracking (NEW v1.3.0)
# ---------------------------------------------------------------------------

def _get_session(session_id: str) -> dict:
    """Get or create per-session state dict."""
    if session_id not in _SESSION_FLAGS:
        _SESSION_FLAGS[session_id] = {
            "authoring_seen": False,
            "writing_seen": False,
            "authoring_loaded": False,
        }
    return _SESSION_FLAGS[session_id]


# ---------------------------------------------------------------------------
# Escalation system
# ---------------------------------------------------------------------------

ESCALATION_FILE = os.path.expanduser("~/.hermes/self-reflection/escalation.json")
BLACKLIST_FILE = os.path.expanduser("~/.hermes/self-reflection/blacklist.json")


def _load_escalation() -> dict:
    try:
        if os.path.exists(ESCALATION_FILE):
            with open(ESCALATION_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"patterns": {}, "last_updated": ""}


def _save_escalation(data: dict) -> None:
    data["last_updated"] = "2026-05-30"
    os.makedirs(os.path.dirname(ESCALATION_FILE), exist_ok=True)
    with open(ESCALATION_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _record_correction(pattern: str) -> int:
    data = _load_escalation()
    now = time.time()
    entry = data["patterns"].get(pattern, {"count": 0, "first_seen": now, "last_seen": now, "level": 0})
    entry["count"] += 1
    entry["last_seen"] = now
    entry["level"] = _calc_level(entry["count"])
    data["patterns"][pattern] = entry
    _save_escalation(data)
    logger.info("[cmg-guard] escalation: '%s' count=%d level=%d", pattern[:80], entry["count"], entry["level"])
    return entry["level"]


def _calc_level(count: int) -> int:
    if count <= 1: return 1
    elif count == 2: return 2
    elif count <= 4: return 3
    else: return 4


def _load_blacklist() -> Set[str]:
    global _BLACKLIST_CACHE
    if _BLACKLIST_CACHE is not None:
        return _BLACKLIST_CACHE
    try:
        if os.path.exists(BLACKLIST_FILE):
            with open(BLACKLIST_FILE) as f:
                data = json.load(f)
            _BLACKLIST_CACHE = set(data.get("permanent_errors", []))
        else:
            _BLACKLIST_CACHE = set()
    except Exception:
        _BLACKLIST_CACHE = set()
    return _BLACKLIST_CACHE


def _maybe_add_to_blacklist(pattern: str, level: int) -> None:
    if level < 4:
        return
    bl = _load_blacklist()
    bl.add(pattern)
    data = {"permanent_errors": list(bl), "updated": "2026-05-30"}
    os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    global _BLACKLIST_CACHE
    _BLACKLIST_CACHE = bl
    logger.warning("[cmg-guard] BLACKLISTED permanently: '%s' (level 4)", pattern[:80])


def _scan_blacklist(message: str) -> Optional[str]:
    bl = _load_blacklist()
    if not bl:
        return None
    lower = message.lower()
    for pattern in bl:
        if pattern.lower() in lower:
            logger.warning("[cmg-guard] blacklist hit: '%s'", pattern[:80])
            return f"[CMG-BLACKLIST] 此行为已被永久禁止: {pattern}"
    return None


# ---------------------------------------------------------------------------
# Ban rule loading
# ---------------------------------------------------------------------------

_BAN_KEYWORDS: Optional[Dict[str, Tuple[str, List[str]]]] = None


def _load_ban_keywords() -> Dict[str, Tuple[str, List[str]]]:
    global _BAN_KEYWORDS
    if _BAN_KEYWORDS is not None:
        return _BAN_KEYWORDS
    rules_dir = Path(os.path.expanduser("~/.hermes/self-reflection/rules/ban"))
    if not rules_dir.is_dir():
        _BAN_KEYWORDS = {}
        return _BAN_KEYWORDS
    result: Dict[str, Tuple[str, List[str]]] = {}
    for md_file in sorted(rules_dir.glob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
            m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
            if not m:
                continue
            fm_text = m.group(1)
            rule_id = md_file.stem
            keywords: List[str] = []
            in_kw = False
            buf = ""
            for line in fm_text.split("\n"):
                s = line.strip()
                if s.startswith("id:"):
                    rule_id = s[3:].strip().strip('"').strip("'")
                elif s.startswith("keywords:"):
                    in_kw = True
                    buf = s[9:].strip()
                    if buf.endswith("]"):
                        in_kw = False
                        buf = buf[:-1]
                elif in_kw:
                    buf += " " + s
                    if s.endswith("]"):
                        in_kw = False
                        buf = buf.rstrip("]")
            if buf:
                raw = buf.strip().lstrip("[").rstrip("]")
                for p in raw.split(","):
                    kw = p.strip().strip("'").strip('"').lower()
                    if kw and len(kw) >= 2:
                        keywords.append(kw)
            if keywords:
                result[rule_id] = (md_file.stem, keywords)
        except Exception:
            pass
    _BAN_KEYWORDS = result
    logger.info("[cmg-guard] loaded %d ban rules", len(result))
    return _BAN_KEYWORDS


def _scan_text(text: str) -> Optional[str]:
    rules = _load_ban_keywords()
    if not rules:
        return None
    lower = text.lower()
    for rule_id, (stem, keywords) in rules.items():
        for kw in keywords:
            if kw in lower:
                logger.warning("[cmg-guard] rule %s hit: '%s'", rule_id, kw)
                return (
                    f"[CMG 拦截] 你的回答命中了规则 \"{stem}\"（关键词: \"{kw}\"）。"
                    f"请遵守 CMG 规则重新回答。"
                )
    return None


# ---------------------------------------------------------------------------
# Sentinel — negation regex scanner
# ---------------------------------------------------------------------------

_SENTINEL_PATTERN_1 = re.compile(
    r"(不|别|不能|别再|不要|不该|不许|怎么又|又忘了|又犯|又偷|又懒|"
    r"你总[是说]|你咋|你又|别再|不准)"
    r".{0,15}"
    r"(你|我|这么|这样|那么|那|这|还|再|老|了|啦|吧|啊)"
)
_SENTINEL_PATTERN_2 = re.compile(r"^(别|不要|不能|不许|不该|别再|不准)")
_SENTINEL_PATTERN_3 = re.compile(
    r"(记住[了没]?|明白[了没]|懂[了没]|"
    r"下次还|以后还|还敢|还能不能|"
    r"说了多少次|能不能|好了再说|"
    r"长点记性|长记性)"
)


def _scan_user_message(user_message: str) -> Optional[str]:
    if not user_message or len(user_message) < 2:
        return None
    if (_SENTINEL_PATTERN_1.search(user_message) or
            _SENTINEL_PATTERN_2.search(user_message) or
            _SENTINEL_PATTERN_3.search(user_message)):
        logger.debug("[cmg-guard] sentinel matched: %s", user_message[:80])
        words = re.findall(r"[\u4e00-\u9fff\w]+", user_message)
        pattern_key = " ".join(words[:5]) if words else user_message[:30]
        level = _record_correction(pattern_key)
        _maybe_add_to_blacklist(pattern_key, level)
        if level >= 4:
            return f"[CMG-BLACKLIST-PERMANENT] 此错误已反复出现{level}次，永久禁止"
        elif level >= 3:
            return f"[CMG-SENTINEL-L3] 此错误已出现{level}次，建议固化规则"
        elif level >= 2:
            return f"[CMG-SENTINEL-L2] 此错误已出现{level}次，警告拦截"
        else:
            return "[CMG-SENTINEL] suspected_correction"
    return None


# ---------------------------------------------------------------------------
# Step-completeness checker
# ---------------------------------------------------------------------------

_STEP_RULES = [
    {
        "id": "link_complete_reading",
        "trigger": re.compile(r"https?://[^\s]+"),
        "description": "链接必须完整阅读（含图片、附件、代码块）",
        "required_tools": ["web_extract", "vision_analyze"],
    },
    {
        "id": "file_coverage_check",
        "trigger": re.compile(r"(write_file|write_to_file|创建了.*文件|写入了.*文件)"),
        "description": "创建文件后必须做覆盖度校验（逐条核对）",
        "required_pattern": r"(覆盖度|逐条核对|N/N|全部覆盖)",
    },
    {
        "id": "orchestrator_clarify",
        "trigger": re.compile(r"(IF|idea-foundry|orchestrator|Phase -[0-9])"),
        "description": "Orchestrator流程每阶段必须用clarify()确认",
        "required_tools": ["clarify"],
    },
    {
        "id": "skill_workflow_execution",
        "trigger": re.compile(r"(跑|走|过).{0,5}(一遍|一下).{0,10}(IF|idea-foundry|brainstorming|planning)"),
        "description": "说'跑Skill'必须执行完整workflow，不能只读文档",
        "required_pattern": r"(Phase -[0-9].*完成|质量预检|策略选择)",
    },
    {
        "id": "evidence_for_claims",
        "trigger": re.compile(r"(通过|完成|成功|已安装|存在|无冲突|全部.*[过绿]|✅|PASS|生效|可用|已修复|已解决|没问题)"),
        "description": "断言性结论必须附带验证证据（终端输出/文件列表/命令结果）",
        "required_pattern": r"(验证|实测|输出|grep|wc -l|ls |cat |curl|exit_code|diff|find.*SKILL|python3.*check)",
    },
]


def _get_recent_context() -> str:
    try:
        from hermes_cli.session import get_current_session
        session = get_current_session()
        if session and hasattr(session, "messages"):
            messages = getattr(session, "messages", [])
            recent = messages[-10:] if len(messages) > 10 else messages
            parts = []
            for msg in recent:
                content = getattr(msg, "content", "") or str(msg)
                if content and len(str(content)) < 2000:
                    parts.append(str(content)[:500])
            return " ".join(parts)
    except Exception:
        pass
    return ""


def _check_step_completeness(user_message: str, **kwargs) -> Optional[str]:
    if not _step_check_enabled():
        return None
    recent_context = _get_recent_context()
    combined = f"{recent_context} {user_message}"
    violations = []
    for rule in _STEP_RULES:
        if not rule["trigger"].search(combined):
            continue
        if "required_tools" in rule:
            tools_called = all(tool in recent_context for tool in rule["required_tools"])
            if not tools_called:
                violations.append(rule["description"])
                continue
        if "required_pattern" in rule:
            if not re.search(rule["required_pattern"], combined, re.IGNORECASE):
                violations.append(rule["description"])
    if violations:
        msg = (
            "[CMG-STEP-CHECK] 以下步骤未完成，禁止回复：\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\n\n请先完成上述步骤后再回复。"
        )
        logger.warning("[cmg-guard] step check failed: %s", violations)
        return msg
    return None


# ===========================================================================
#  HOOK HANDLERS (v1.3.0 — 17 hooks, 4 core ON, 13 configurable OFF)
# ===========================================================================

# ── Core: transform_llm_output ───────────────────────────────────────────

def _transform_llm_output(response_text: str = "", **kwargs) -> Optional[str]:
    if not _hook_enabled("transform_llm_output"):
        return None
    block_msg = _scan_text(response_text)
    if block_msg:
        if _intercept_notice_mode() == "visible":
            return f"⚠️ [CMG拦截] {block_msg}"
        return block_msg
    bl_msg = _scan_blacklist(response_text)
    if bl_msg:
        if _intercept_notice_mode() == "visible":
            return f"⚠️ [CMG拦截] {bl_msg}"
        return bl_msg
    return None


# ── Core: pre_llm_call ───────────────────────────────────────────────────

# Task-type → recommended CMG companion tools
_TASK_RECOMMENDATIONS = {
    "打包|发布|部署|zip|上传|release|桌面": [
        "ralph-loop（闭环验证，逐项核对不漏组件）",
        "verification-before-completion（证据先于断言）",
        "hermes-agent-skill-authoring（发布自检清单）",
    ],
    "写代码|开发|实现|重构|build|新建|创建.*项目": [
        "tdd / test-driven-development（先写测试）",
        "brainstorming（先想清楚再动手）",
        "planning-with-files（文件持久化进度）",
    ],
    "调试|修复|bug|报错|不工作": [
        "diagnose（四阶段根因调试）",
        "systematic-debugging（理解bug再修复）",
    ],
    "测试|验证|test": [
        "tdd / test-driven-development（RED-GREEN-REFACTOR）",
        "verification-before-completion（完成前必须验证）",
    ],
    "写.*(文章|论文|文档|报告)": [
        "planning-with-files（大纲持久化）",
        "verification-before-completion（字数/格式校验）",
    ],
}

_REC_SESSION_CACHE: Dict[str, set] = {}


def _check_task_recommendations(user_message: str, session_id: str = "") -> Optional[str]:
    """Scan user message for task keywords, suggest CMG companion tools.

    Only fires once per session per task type to avoid spam.
    """
    if len(user_message) < 5:
        return None

    cache = _REC_SESSION_CACHE.setdefault(session_id, set())

    suggestions = []
    for pattern, tools in _TASK_RECOMMENDATIONS.items():
        if re.search(pattern, user_message, re.IGNORECASE):
            task_key = pattern[:20]
            if task_key in cache:
                continue
            cache.add(task_key)
            suggestions.extend(tools)

    if not suggestions:
        return None

    tool_list = "\n".join(f"  • {t}" for t in suggestions)
    msg = (
        "[CMG 配套工具建议]\n"
        "检测到任务类型，推荐启用以下 CMG 配套工具以确保质量：\n"
        f"{tool_list}\n"
        "以上为一次性提示，本会话内不再重复。"
    )
    logger.info("[cmg-guard] task recommendation: %d tools suggested", len(suggestions))
    return msg


def _pre_llm_call(user_message: str = "", session_id: str = "", **kwargs) -> Optional[dict]:
    if not _hook_enabled("pre_llm_call"):
        return None
    bl_msg = _scan_blacklist(user_message)
    if bl_msg:
        logger.info("[cmg-guard] blacklist intercept")
        return {"context": f"[CMG-BLACKLIST-BLOCK] {bl_msg}"}
    if _sentinel_enabled():
        flag = _scan_user_message(user_message)
        if flag:
            logger.info("[cmg-guard] sentinel: flagged suspected correction")
            return {"context": flag}
    rec_msg = _check_task_recommendations(user_message, session_id)
    if rec_msg:
        return {"context": rec_msg}
    step_fail = _check_step_completeness(user_message, **kwargs)
    if step_fail:
        logger.info("[cmg-guard] step check: blocking LLM call")
        return {"context": step_fail}
    return None


# ── Core: post_llm_call ──────────────────────────────────────────────────

# Completion-claim patterns
_COMPLETION_CLAIM = re.compile(
    r"(完成[了啦]?|好了|搞定|做完了|已创建|已写入|已更新"
    r"|已修复|已打包|已发布|已部署|就绪|全部.*[过绿]"
    r"|一切.*正常|到此.*结束|以上.*就是)",
    re.IGNORECASE,
)
# Minimal data token: any digit, emoji marker, or path separator
_DATA_TOKEN = re.compile(r"[\d✅❌⏳⚠️/~]")


def _check_completion_evidence(response_text: str) -> Optional[str]:
    """Detect task-completion claims with nothing substantive following them.

    Abstract rule: after declaring something done, what's left?
    If the reply ends right after the claim (or fills the rest with
    vague words only), there's no evidence.  If there's substance —
    numbers, paths, markers, anything specific — it passes.

    Works for any task type because it doesn't enumerate valid evidence.
    It checks whether the AI put anything verifiable after the claim.
    """
    # Find the last completion claim position
    match = None
    for m in _COMPLETION_CLAIM.finditer(response_text):
        match = m
    if match is None:
        return None

    after_claim = response_text[match.end():].strip()
    # Strip whitespace-only content
    after_meaningful = re.sub(r"\s+", "", after_claim)

    # If no data token anywhere after the claim → intercept
    # (removed length check — the issue is falsifiability, not brevity)
    if not _DATA_TOKEN.search(after_claim):
        logger.warning("[cmg-guard] completion claim with no substance after: %s", match.group())
        return (
            "[CMG-GUARD post_llm_call] 检测到任务完成声明"
            f"（{match.group()}）但后面没有实质内容。\n"
            "请在声明完成后附上可核对的具体数据。\n"
            "禁止只报结论不报证据。"
        )

    return None


# Claims-about-external-source patterns (post_llm_call v1.3.0)
_EXTERNAL_CLAIM = re.compile(
    r"(我看了|我确认|我读到|里面说|那边说|说了|讨论了|同意|验证过)"
    r"|(三个AI|三方|交叉验证|两边都|都.*[同确])",
    re.IGNORECASE,
)
# Must have actual quoted text, not just a claim about it
_QUOTED_EVIDENCE = re.compile(
    r"([「『\"'“].{3,}[」』\"'”)]"
    r"|原文[:：].{3,}"
    r"|摘录[:：].{3,})",
)


def _check_external_claims(response_text: str) -> Optional[str]:
    """Detect claims about external-source content without actual quotes.

    If AI says "I read link X / they discussed Y / three AIs agreed"
    but doesn't include any actual quoted text from those sources,
    the claim is unverifiable → intercept.
    """
    if not _EXTERNAL_CLAIM.search(response_text):
        return None
    if _QUOTED_EVIDENCE.search(response_text):
        return None
    logger.warning("[cmg-guard] external-source claim without quoted evidence")
    return (
        "[CMG-GUARD post_llm_call] 检测到对外部来源内容的主张"
        "但未附带原文摘录。\n"
        "如需引用外部链接/素材的内容，请附上具体摘录文字。\n"
        "如链接无法访问，请明确说明「无法读取」，禁止猜测内容。"
    )


def _post_llm_call(response_text: str = "", **kwargs) -> Optional[str]:
    if not _hook_enabled("post_llm_call"):
        return None
    bl_msg = _scan_blacklist(response_text)
    if bl_msg:
        return bl_msg
    evidence_fail = _check_completion_evidence(response_text)
    if evidence_fail:
        return evidence_fail
    external_fail = _check_external_claims(response_text)
    if external_fail:
        return external_fail
    return None


# ── Core (NEW v1.3.0): pre_tool_call ─────────────────────────────────────

def _pre_tool_call(
    tool_name: str = "",
    args: dict = None,
    session_id: str = "",
    **kwargs,
) -> Optional[dict]:
    """Block SKILL.md edits without authoring skills loaded."""
    if not _hook_enabled("pre_tool_call"):
        return None

    args = args or {}
    path = str(args.get("path", "") or args.get("file_path", ""))

    # 1. Detect: loading authoring skills → set session flag
    if tool_name == "skill_view":
        skill_name = str(args.get("name", ""))
        if skill_name in ("hermes-agent-skill-authoring", "writing-skills"):
            session = _get_session(session_id)
            if "hermes-agent" in skill_name:
                session["authoring_seen"] = True
            if "writing" in skill_name:
                session["writing_seen"] = True
            if session.get("authoring_seen") and session.get("writing_seen"):
                session["authoring_loaded"] = True
                logger.info("[cmg-guard] session %s: authoring skills loaded ✓", session_id[:12])
            return None

    # 2. Block: SKILL.md edits without authoring skills loaded
    if tool_name in ("patch", "skill_manage") and "SKILL.md" in path:
        session = _get_session(session_id)
        if not session.get("authoring_loaded"):
            logger.warning("[cmg-guard] BLOCK: %s on SKILL.md without authoring (session %s)", tool_name, session_id[:12])
            return {
                "action": "block",
                "message": (
                    "[CMG-GUARD pre_tool_call] 修改 SKILL.md 前必须先加载 skill 编写规范。\n"
                    "请先执行: skill_view('hermes-agent-skill-authoring')\n"
                    "      然后: skill_view('writing-skills')\n"
                    "加载后根据规范选择适合你的工具和流程。"
                ),
            }

    return None


# ── Optional: post_tool_call ─────────────────────────────────────────────

def _post_tool_call(**kwargs) -> None:
    if not _hook_enabled("post_tool_call"):
        return None
    # Reserved for tool-audit logging
    return None


# ── Optional: transform_tool_result ──────────────────────────────────────

def _transform_tool_result(result_text: str = "", tool_name: str = "", **kwargs) -> Optional[str]:
    if not _hook_enabled("transform_tool_result"):
        return None
    # Reserved: detect fake success (e.g. "✅ installed" but actually failed)
    return None


# ── Optional: transform_terminal_output ──────────────────────────────────

def _transform_terminal_output(output_text: str = "", **kwargs) -> Optional[str]:
    if not _hook_enabled("transform_terminal_output"):
        return None
    # Reserved: CLI output filtering
    return None


# ── Optional: pre_api_request ────────────────────────────────────────────

def _pre_api_request(payload: dict = None, **kwargs) -> Optional[dict]:
    if not _hook_enabled("pre_api_request"):
        return None
    # Reserved: inject hard constraints into LLM API request
    return None


# ── Optional: post_api_request ───────────────────────────────────────────

def _post_api_request(response: dict = None, **kwargs) -> None:
    if not _hook_enabled("post_api_request"):
        return None
    # Reserved: validate LLM response compliance
    return None


# ── Optional: on_session_start ───────────────────────────────────────────

def _on_session_start(session_id: str = "", **kwargs) -> None:
    if not _hook_enabled("on_session_start"):
        return None
    _get_session(session_id)  # init fresh session state
    logger.info("[cmg-guard] session started: %s", session_id[:12])
    return None


# ── Optional: on_session_end ─────────────────────────────────────────────

def _on_session_end(session_id: str = "", **kwargs) -> None:
    if not _hook_enabled("on_session_end"):
        return None
    if session_id in _SESSION_FLAGS:
        del _SESSION_FLAGS[session_id]
    return None


# ── Optional: on_session_finalize / on_session_reset ─────────────────────

def _on_session_finalize(**kwargs) -> None:
    if not _hook_enabled("on_session_finalize"):
        return None
    return None


def _on_session_reset(**kwargs) -> None:
    if not _hook_enabled("on_session_reset"):
        return None
    return None


# ── Optional: pre_gateway_dispatch ───────────────────────────────────────

def _pre_gateway_dispatch(event=None, **kwargs) -> Optional[dict]:
    if not _hook_enabled("pre_gateway_dispatch"):
        return None
    # Reserved: scan outbound messages on WeChat/Feishu/etc.
    return None


# ── Optional: pre_approval_request / post_approval_response ──────────────

def _pre_approval_request(command: str = "", **kwargs) -> None:
    if not _hook_enabled("pre_approval_request"):
        return None
    # Reserved: monitor dangerous command approvals
    return None


def _post_approval_response(choice: str = "", **kwargs) -> None:
    if not _hook_enabled("post_approval_response"):
        return None
    return None


# ── Optional: subagent_stop ──────────────────────────────────────────────

def _subagent_stop(**kwargs) -> None:
    if not _hook_enabled("subagent_stop"):
        return None
    return None


# ===========================================================================
#  REGISTRATION
# ===========================================================================

def register(ctx) -> None:
    """Register all 17 hooks. Only enabled hooks execute logic."""

    # ── Core (always registered, enabled by default) ──
    ctx.register_hook("transform_llm_output", _transform_llm_output)
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_hook("pre_tool_call", _pre_tool_call)

    # ── Core (registered if supported) ──
    for hook, handler in [
        ("post_llm_call", _post_llm_call),
        ("post_tool_call", _post_tool_call),
        ("transform_tool_result", _transform_tool_result),
        ("transform_terminal_output", _transform_terminal_output),
        ("pre_api_request", _pre_api_request),
        ("post_api_request", _post_api_request),
        ("on_session_start", _on_session_start),
        ("on_session_end", _on_session_end),
        ("on_session_finalize", _on_session_finalize),
        ("on_session_reset", _on_session_reset),
        ("pre_gateway_dispatch", _pre_gateway_dispatch),
        ("pre_approval_request", _pre_approval_request),
        ("post_approval_response", _post_approval_response),
        ("subagent_stop", _subagent_stop),
    ]:
        try:
            ctx.register_hook(hook, handler)
        except Exception:
            logger.debug("[cmg-guard] hook '%s' not available, skipping", hook)

    rules = _load_ban_keywords()
    sentinel = _sentinel_enabled()
    step_check = _step_check_enabled()
    bl_size = len(_load_blacklist())

    active = [h for h in [
        "pre_tool_call", "pre_llm_call", "post_llm_call", "transform_llm_output",
        "post_tool_call", "transform_tool_result", "transform_terminal_output",
        "pre_api_request", "post_api_request", "on_session_start", "on_session_end",
        "on_session_finalize", "on_session_reset", "pre_gateway_dispatch",
        "pre_approval_request", "post_approval_response", "subagent_stop",
    ] if _hook_enabled(h)]

    logger.info(
        "[cmg-guard] v1.3.0 registered (%d rules, sentinel=%s, step-check=%s, blacklist=%d, hooks=%s)",
        len(rules),
        "ON" if sentinel else "OFF",
        "ON" if step_check else "OFF",
        bl_size,
        "+".join([h.split("_")[-1][:4] for h in active]) if active else "none",
    )
