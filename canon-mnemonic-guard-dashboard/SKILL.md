---
name: canon-mnemonic-guard-dashboard
description: Use when the user says "dashboard", "仪表盘", "!dashboard", or wants to view/manage Canon-Mnemonic-Guard rules, config, or companion skills. Launches a local web dashboard at localhost:8765 with full rule browsing, config management, and skill status monitoring.
version: 1.0.0
author: L1veSong
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [dashboard, cmg, web, rules, config, companion]
    related_skills: [canon-mnemonic-guard]
---

# Canon-Mnemonic-Guard Dashboard

Web dashboard for the Canon-Mnemonic-Guard self-reflection engine. Visual rule browsing, engine configuration, companion skill monitoring, and rule CRUD — all in a single-file Python server with zero external dependencies beyond stdlib + PyYAML.

## When to Use

- User says "dashboard", "仪表盘", "!dashboard"
- Browse/search/filter CMG rules
- Toggle cmg-guard hooks or change intercept notice
- Add, edit, or delete rules via GUI
- Check companion skill install status and toggle them
- Switch between Chinese/English UI

## Quick Start

```bash
python3 ~/.hermes/dashboard/server.py
# Open http://localhost:8765
```

Or in Hermes: `!dashboard`

## Features

**Rules Tab** — 76+ rules searchable by ID/keywords, filterable by type (ban/gap/lazy/meta), sortable columns with rotating arrow indicators. Expand rows for metadata. Edit keywords/description via modal. Delete with confirmation.

**Engine Config** — 17 hook toggles (core + extended), intercept notice silent/visible, auto-recommend master switch, per-skill companion toggles with real-time install detection across Hermes/Claude Code/gstack/OpenClaw/Codex directories. Refresh button re-scans. Save per module.

**Add Rule** — Form with type selector, rule ID, keywords, description. Writes to `rules/<type>/` with proper frontmatter.

**Theme & i18n** — Dark/light with system detection + localStorage. Full zh/en coverage.

**Animations** — Card lift, toast slide, button press, tab fade, sort rotate, row hover, modal fade + scroll lock.

## Architecture

Single-file `server.py` reads `~/.hermes/self-reflection/rules/` and `~/.hermes/config.yaml`. Config writes use deep-merge. Rule edits use glob + frontmatter `id` matching (regex, never YAML-parse to avoid crashes on special characters).

## Companion Detection

Scans `~/.hermes/skills/`, `~/.claude/skills/`, `~/.agents/skills/`, `~/.openclaw/skills/`, `~/.codex/skills/`, and `~/.hermes/plugins/`. Matches by `name:` regex in SKILL.md frontmatter.

## Dependencies

Python 3.7+, PyYAML (`pip install pyyaml`).

## Common Pitfalls

1. **Server hangs in background** — `webbrowser.open()` blocks without display. Use `python3 -c` direct server start.
2. **Config changes need Hermes restart** — cmg-guard reads config on startup only.
3. **Port 8765 conflict** — `lsof -ti:8765 | xargs kill` before restart.
