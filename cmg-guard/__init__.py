"""
cmg-guard v1.2.0: System-level step enforcement.

v1.2.0: + pre_llm_call step-completeness checker + global blacklist.
         The AI can no longer skip steps — cmg-guard blocks LLM calls
         until all required checks are completed.

Unlike the CMG skill (AI reads rules and self-polices), this plugin runs
inside Hermes — the AI has no opportunity to skip or rationalise past it.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

_CONFIG_CACHE: Optional[dict] = None
_SESSION_STATE: Dict[str, any] = {}
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


def _sentinel_enabled() -> bool:
    cfg = _load_cmg_config()
    if "lightweight_sentinel" not in cfg:
        return True
    return bool(cfg["lightweight_sentinel"])


def _step_check_enabled() -> bool:
    """Step-completeness checker is ON by default."""
    cfg = _load_cmg_config()
    if "step_check" not in cfg:
        return True
    return bool(cfg["step_check"])


# ---------------------------------------------------------------------------
# Escalation system (NEW v1.2.0) — 分阶段升级，不搞一刀切黑名单
# ---------------------------------------------------------------------------

ESCALATION_FILE = os.path.expanduser("~/.hermes/self-reflection/escalation.json")
BLACKLIST_FILE = os.path.expanduser("~/.hermes/self-reflection/blacklist.json")

# Escalation levels (track HOW MANY TIMES the same error was corrected)
#   Note: this is separate from CMG rule levels (monitor/soft/hard),
#   which define rule SEVERITY. The two work together:
#     monitor rule + L1 escalation = just record, no action
#     soft rule    + L2 escalation = warn, remind
#     hard rule    + L3 escalation = draft a new rule
#     hard rule    + L4 escalation = permanent blacklist


def _load_escalation() -> dict:
    try:
        if os.path.exists(ESCALATION_FILE):
            with open(ESCALATION_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"patterns": {}, "last_updated": ""}


def _save_escalation(data: dict) -> None:
    data["last_updated"] = "2026-05-28"
    os.makedirs(os.path.dirname(ESCALATION_FILE), exist_ok=True)
    with open(ESCALATION_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _record_correction(pattern: str) -> int:
    """Record a correction event. Returns new escalation level (0-4)."""
    import time
    data = _load_escalation()
    now = time.time()

    entry = data["patterns"].get(pattern, {"count": 0, "first_seen": now, "last_seen": now, "level": 0})
    entry["count"] += 1
    entry["last_seen"] = now
    entry["level"] = _calc_level(entry["count"])
    data["patterns"][pattern] = entry
    _save_escalation(data)
    logger.info("[cmg-guard] escalation: '%s' count=%d level=%d", pattern, entry["count"], entry["level"])
    return entry["level"]


def _calc_level(count: int) -> int:
    """Calculate escalation level from hit count."""
    if count <= 1:
        return 1  # sentinel
    elif count == 2:
        return 2  # warn
    elif count <= 4:
        return 3  # draft
    else:
        return 4  # harden → permanent blacklist


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
    """Only add to blacklist at level 4 (harden)."""
    if level < 4:
        return
    bl = _load_blacklist()
    bl.add(pattern)
    data = {"permanent_errors": list(bl), "updated": "2026-05-28"}
    os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    global _BLACKLIST_CACHE
    _BLACKLIST_CACHE = bl
    logger.warning("[cmg-guard] BLACKLISTED permanently: '%s' (level 4, count>=5)", pattern)


def _scan_blacklist(message: str) -> Optional[str]:
    """Check user message against permanent blacklist (level 4 only)."""
    bl = _load_blacklist()
    if not bl:
        return None
    lower = message.lower()
    for pattern in bl:
        if pattern.lower() in lower:
            logger.warning("[cmg-guard] blacklist hit: '%s'", pattern)
            return f"[CMG-BLACKLIST] 此行为已被永久禁止: {pattern}"
    return None


# ---------------------------------------------------------------------------
# Ban rule loading (unchanged from v1.1.0)
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
# Blacklist scan — check user message against permanent errors
# ---------------------------------------------------------------------------

def _scan_blacklist(message: str) -> Optional[str]:
    """Check if user message indicates a previously-blacklisted error pattern."""
    bl = _load_blacklist()
    if not bl:
        return None
    lower = message.lower()
    for pattern in bl:
        if pattern.lower() in lower:
            logger.warning("[cmg-guard] blacklist hit: '%s'", pattern)
            return f"[CMG-BLACKLIST] 此行为已被永久禁止: {pattern}"
    return None


# ---------------------------------------------------------------------------
# Sentinel — negation regex scanner (unchanged from v1.1.0)
# ---------------------------------------------------------------------------

_SENTINEL_PATTERN_1 = re.compile(
    r"(不|别|不能|别再|不要|不该|不许|怎么又|又忘了|又犯|又偷|又懒|"
    r"你总[是说]|你咋|你又|别再|不准)"
    r".{0,15}"
    r"(你|我|这么|这样|那么|那|这|还|再|老|了|啦|吧|啊)"
)

_SENTINEL_PATTERN_2 = re.compile(
    r"^(别|不要|不能|不许|不该|别再|不准)"
)

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
        # Extract a stable pattern key (first 3 non-trivial words)
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
# Step-completeness checker (NEW in v1.2.0)
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
]


def _get_recent_context() -> str:
    """Attempt to retrieve recent conversation context for step checking.
    Returns empty string if unavailable."""
    try:
        # Try to access session context through Hermes internals
        from hermes_cli.session import get_current_session
        session = get_current_session()
        if session and hasattr(session, "messages"):
            messages = getattr(session, "messages", [])
            recent = messages[-10:] if len(messages) > 10 else messages
            context_parts = []
            for msg in recent:
                content = getattr(msg, "content", "") or str(msg)
                if content and len(str(content)) < 2000:
                    context_parts.append(str(content)[:500])
            return " ".join(context_parts)
    except Exception:
        pass
    return ""


def _check_step_completeness(user_message: str, **kwargs) -> Optional[str]:
    """Check if all required steps have been completed before allowing LLM response."""
    if not _step_check_enabled():
        return None

    recent_context = _get_recent_context()
    combined = f"{recent_context} {user_message}"

    violations = []
    for rule in _STEP_RULES:
        if not rule["trigger"].search(combined):
            continue

        # Check if required tools were called
        if "required_tools" in rule:
            tools_called = all(
                tool in recent_context
                for tool in rule["required_tools"]
            )
            if not tools_called:
                violations.append(rule["description"])
                continue

        # Check if required pattern was matched
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


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def _transform_llm_output(response_text: str, **kwargs) -> Optional[str]:
    # 1. Ban keyword check
    block_msg = _scan_text(response_text)
    if block_msg is not None:
        return block_msg

    # 2. Blacklist check on AI output too
    bl_msg = _scan_blacklist(response_text)
    if bl_msg is not None:
        return bl_msg

    return None


def _pre_llm_call(
    user_message: str = "",
    **kwargs,
) -> Optional[dict]:
    """A-layer sentinel + step completeness check + blacklist scan."""

    # 1. Blacklist scan — highest priority
    bl_msg = _scan_blacklist(user_message)
    if bl_msg is not None:
        logger.info("[cmg-guard] blacklist intercept")
        return {"context": f"[CMG-BLACKLIST-BLOCK] {bl_msg}"}

    # 2. Sentinel — suspected correction detection
    if _sentinel_enabled():
        flag = _scan_user_message(user_message)
        if flag is not None:
            logger.info("[cmg-guard] sentinel: flagged suspected correction")
            return {"context": flag}

    # 3. Step completeness check — block if steps skipped
    step_fail = _check_step_completeness(user_message, **kwargs)
    if step_fail is not None:
        logger.info("[cmg-guard] step check: blocking LLM call")
        return {"context": step_fail}

    return None


def _post_llm_call(response_text: str = "", **kwargs) -> Optional[str]:
    """Post-LLM call check — verify the AI actually completed required steps."""
    # Check if AI tried to skip steps in its response
    bl_msg = _scan_blacklist(response_text)
    if bl_msg is not None:
        return bl_msg
    return None


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    ctx.register_hook("transform_llm_output", _transform_llm_output)
    ctx.register_hook("pre_llm_call", _pre_llm_call)

    # Register post_llm_call if Hermes supports it
    try:
        ctx.register_hook("post_llm_call", _post_llm_call)
    except Exception:
        logger.debug("[cmg-guard] post_llm_call hook not available, skipping")

    rules = _load_ban_keywords()
    sentinel = _sentinel_enabled()
    step_check = _step_check_enabled()
    bl_size = len(_load_blacklist())
    logger.info(
        "[cmg-guard] v1.2.0 registered (%d rules, sentinel=%s, step-check=%s, blacklist=%d)",
        len(rules),
        "ON" if sentinel else "OFF",
        "ON" if step_check else "OFF",
        bl_size,
    )
