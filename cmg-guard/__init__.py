"""cmg-guard: Hard-enforce CMG ban rules at the Hermes kernel level.

Registers ``transform_llm_output`` to scan AI responses for ban-rule
violations.  When a violation is detected, the response is replaced with a
correction directive before the user ever sees it.

v1.1.0:  + lightweight_sentinel via ``pre_llm_call`` hook (negation regex
           scanner).  Defaults OFF; enable in config.yaml.  Marks suspected
           corrections for CMG Skill layer (B) to judge.

Unlike the CMG skill (AI reads rules and self-polices), this plugin runs
inside Hermes — the AI has no opportunity to skip or rationalise past it.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

_CONFIG_CACHE: Optional[dict] = None


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
    """Sentinel is ON by default.  Set ``cmg_guard.lightweight_sentinel: false``
    in config.yaml to explicitly disable."""
    cfg = _load_cmg_config()
    # Default ON — only disable when explicitly set to false
    if "lightweight_sentinel" not in cfg:
        return True
    return bool(cfg["lightweight_sentinel"])


# ---------------------------------------------------------------------------
# Rule loading — parse ban/*.md frontmatter for keywords
# ---------------------------------------------------------------------------

_BAN_KEYWORDS: Optional[Dict[str, Tuple[str, List[str]]]] = None


def _load_ban_keywords() -> Dict[str, Tuple[str, List[str]]]:
    global _BAN_KEYWORDS
    if _BAN_KEYWORDS is not None:
        return _BAN_KEYWORDS

    rules_dir = Path(os.path.expanduser("~/.hermes/self-reflection/rules/ban"))
    if not rules_dir.is_dir():
        logger.info("[cmg-guard] no ban rules directory")
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
# Lightweight Sentinel (A layer) — negation regex scanner for user input
# ---------------------------------------------------------------------------

# Broad negation patterns that catch most correction-like user messages
# Pattern 1: negation word + short gap + pronoun/demonstrative
_SENTINEL_PATTERN_1 = re.compile(
    r"(不|别|不能|别再|不要|不该|不许|怎么又|又忘了|又犯|"
    r"你总[是说]|你咋|你又|别再|不准)"
    r".{0,10}"
    r"(你|我|这么|这样|那么|那|这|还|再|老)"
)

# Pattern 2: sentence-starting negation commands
_SENTINEL_PATTERN_2 = re.compile(
    r"^(别|不要|不能|不许|不该|别再|不准)"
)

# Pattern 3: rhetorical questions / standalone correction signals
_SENTINEL_PATTERN_3 = re.compile(
    r"(记住[了没]吗|明白[了没]|懂[了没]|"
    r"下次还|以后还|还敢|还能不能|"
    r"说了多少次|能不能|好了再说|"
    r"长点记性|长记性)"
)


def _scan_user_message(user_message: str) -> Optional[str]:
    """Scan user input for suspected correction intent. Returns a flag string or None."""
    if not user_message or len(user_message) < 2:
        return None

    # Check all three pattern groups
    if (_SENTINEL_PATTERN_1.search(user_message) or
            _SENTINEL_PATTERN_2.search(user_message) or
            _SENTINEL_PATTERN_3.search(user_message)):
        logger.debug("[cmg-guard] sentinel matched: %s", user_message[:80])
        return "[CMG-SENTINEL] suspected_correction"

    return None


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def _transform_llm_output(response_text: str, **kwargs) -> Optional[str]:
    block_msg = _scan_text(response_text)
    if block_msg is not None:
        return block_msg
    return None


def _pre_llm_call(
    user_message: str = "",
    **kwargs,
) -> Optional[dict]:
    """A-layer sentinel: scan user input for suspected corrections."""
    if not _sentinel_enabled():
        return None

    flag = _scan_user_message(user_message)
    if flag is not None:
        logger.info("[cmg-guard] sentinel: flagged suspected correction")
        return {"context": flag}
    return None


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    ctx.register_hook("transform_llm_output", _transform_llm_output)
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    rules = _load_ban_keywords()
    sentinel = _sentinel_enabled()
    logger.info(
        "[cmg-guard] registered (%d rules, sentinel=%s)",
        len(rules), "ON" if sentinel else "OFF",
    )
