# Public-Facing Naming Convention

> Source: CMG Dashboard development (2026-05-30) · Extended 2026-06-15 to cover all project abbreviations

## Rule

In public-facing text, **all project abbreviations are forbidden**. Full names only:

| Abbreviation | Full Name (English) | Full Name (Chinese) |
|-------------|---------------------|---------------------|
| CMG | Canon-Mnemonic-Guard | 三省引擎 |
| Smart Skill Router | Smart Skill Router | 智配路由 |
| IF | Idea Foundry | Idea Foundry |
| RTK | RTK Rewrite | RTK Rewrite |
| VBC | Verification Before Completion | — |
| CoVe | Chain-of-Verification | — |

## Scope

"Public-facing" means any text seen by anyone other than the developer:
- README.md / CHANGELOG.md
- Dashboard and other UI surfaces
- GitHub release announcements
- Sub-component SKILL.md description fields
- Companion skill tables
- Any document pushed to public repositories

## Exception

Internal session dialogue between AI and developer may use abbreviations — this is private communication.

## Verification

Pre-release scan across all public files:
```bash
grep -rn '\bSSR\b\|\bIF\b\|\bRTK\b\|\bVBC\b\|\bCoVe\b\|\bCMG\b' README.md CHANGELOG.md SKILL.md 2>/dev/null | grep -v 'CMG_\|Canon-Mnemonic-Guard\|Smart Skill Router\|Idea Foundry\|RTK Rewrite\|Chain-of-Verification'
```
Replace any hits with full names.

## Related

- SKILL.md Pitfall 32
- hermes-agent-skill-authoring SKILL.md
- CMG ban rule `ban_no_project_abbreviations` (rules/ban/)
