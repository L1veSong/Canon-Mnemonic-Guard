# Changelog

## v1.0.0 (2026-05-30)

Initial release of Canon-Mnemonic-Guard Dashboard.

### Features
- Rule browsing with search, type filter (ban/gap/lazy/meta), and sortable columns
- Expandable rule detail rows with edit modal for keywords and description
- Rule deletion with confirmation dialog
- 17 cmg-guard hook toggles (core + extended)
- Intercept notice mode (silent/visible)
- Auto-recommend companion tools master switch
- Companion skills list with per-skill toggles and real-time install detection
- Companion detection across 5 agent directories + plugins
- Add rule form with type selector and frontmatter generation
- Dark/light theme with system detection and localStorage
- Full Chinese/English i18n
- Animations: card lift, toast slide, button press, tab fade, sort rotate, row hover, modal fade
- Fixed table layout: no column shift on sort, uniform padding
- meta rule type (teal badge, rules/meta/ directory)
- Refresh button for companion skill re-scan
- Config save per module (no cross-contamination)
- Deep-merge config writes (partial payload safe)
- Body scroll lock on modal open

### Technical
- Single-file Python HTTP server (stdlib + PyYAML)
- Rule CRUD via REST API (GET/POST/PUT/DELETE)
- Config read/write with deep-merge
- Skill install detection via regex frontmatter parsing (avoids YAML parse crashes)
- i18n via data-i18n/data-i18n-col/data-i18n-ph attributes
