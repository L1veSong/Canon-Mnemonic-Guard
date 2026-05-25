"""cmg-guard: Hard-enforce CMG ban rules at the Hermes kernel level.

Registers ``transform_llm_output`` to scan AI responses for ban-rule
violations.  When a violation is detected, the response is replaced with a
correction directive before the user ever sees it.

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
# Hook
# ---------------------------------------------------------------------------

def _transform_llm_output(response_text: str, **kwargs) -> Optional[str]:
    block_msg = _scan_text(response_text)
    if block_msg is not None:
        return block_msg
    return None


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    ctx.register_hook("transform_llm_output", _transform_llm_output)
    rules = _load_ban_keywords()
    logger.info("[cmg-guard] registered (%d rules)", len(rules))
