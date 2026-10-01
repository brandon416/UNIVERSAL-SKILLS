# Changelog

## 2026-09-30

- Ported NexFabric/pwa-review-skill (MIT, Copyright 2025 Emrah) to an agent-neutral skill.
- Removed Claude Code-only contract: `WebFetch`, `/pwa-review`, `user_invocable` args, `<pwa-review>` wrapper, `.claude/skills` as the only install path.
- Added Grok, Codex, Hermes, Claude adapters.
- Split rubric, report template, and iOS limits into `references/`.
- Added `scripts/collect_pwa.py` so scoring evidence does not depend on a vendor fetch tool.
- Point values and grade bands unchanged (192 total).
