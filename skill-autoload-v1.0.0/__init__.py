"""skill-autoload: Inject skill loading directives into system prompt at session start.

Reads ``skill_autoload`` configuration from Hermes config.yaml:

.. code-block:: yaml

    skill_autoload:
      skills:
        - canon-mnemonic-guard
        - karpathy-coding-guidelines
      per_platform:
        cli: [canon-mnemonic-guard]
        feishu: []
        telegram: [canon-mnemonic-guard]

- ``skills``: default list for all platforms (used when no per_platform match).
- ``per_platform.<platform>``: override for a specific platform.  Empty list
  means no auto-load on that platform.

If ``skill_autoload`` is missing or empty, the plugin is a no-op.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

_CONFIG_CACHE: Optional[dict] = None


def _load_config() -> dict:
    """Read ``skill_autoload`` from Hermes config.yaml.  Result is cached."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE
    try:
        from hermes_cli.config import load_config
        raw = load_config()
        cfg: dict = raw.get("skill_autoload", {})
    except Exception:
        cfg = {}
    _CONFIG_CACHE = cfg
    logger.debug("[skill-autoload] config loaded: %s", bool(cfg))
    return _CONFIG_CACHE


def _get_skills_for_platform(platform: str) -> List[str]:
    """Return the skill list for *platform*, falling back to defaults."""
    cfg = _load_config()
    if not cfg:
        return []

    per_platform: Dict[str, list] = cfg.get("per_platform", {})
    if platform and platform in per_platform:
        skills = per_platform[platform]
        logger.debug("[skill-autoload] platform=%s → per_platform override: %s", platform, skills)
        return list(skills) if isinstance(skills, list) else []

    default_skills: list = cfg.get("skills", [])
    logger.debug("[skill-autoload] platform=%s → default skills: %s", platform, default_skills)
    return list(default_skills) if isinstance(default_skills, list) else []


# ---------------------------------------------------------------------------
# Hook
# ---------------------------------------------------------------------------

_MUST_LOAD_PREFIX = (
    "\n\n"
    "[MUST-LOAD] 以下技能已配置为自动加载。"
    "每个会话开始后，使用 skill_view(name='<skill>') 逐个加载它们。"
    "这是强制性指令，不可跳过。\n"
)


def _pre_system_prompt(
    system_prompt: str,
    session_id: str = "",
    model: str = "",
    platform: str = "",
) -> str | None:
    skills = _get_skills_for_platform(platform)
    if not skills:
        return None

    lines = [_MUST_LOAD_PREFIX]
    for s in skills:
        lines.append(f"  必须加载: {s}")
    lines.append("")
    directive = "\n".join(lines)

    logger.info("[skill-autoload] injecting auto-load for: %s (platform=%s)", skills, platform)
    return system_prompt + directive


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    ctx.register_hook("pre_system_prompt", _pre_system_prompt)
    skills = _get_skills_for_platform("")  # default list
    logger.info("[skill-autoload] plugin registered (default skills: %s)", skills or "none")
