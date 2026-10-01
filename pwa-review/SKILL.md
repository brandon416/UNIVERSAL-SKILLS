---
name: pwa-review
description: "192-point PWA audit beyond Lighthouse. Use when reviewing a PWA, manifest, service worker, installability, offline behavior, or iOS PWA compatibility. Not for general web perf or Lighthouse-only runs."
type: workflow
lifecycle: active
---

# PWA Review — agent-neutral 192-point audit

Audit a Progressive Web App across 11 categories (192 points). Origin: NexFabric/pwa-review-skill (MIT, Copyright 2025 Emrah). This copy drops Claude Code-only tools (`WebFetch`, `/pwa-review`, `.claude/skills`).

Works in Grok, Codex, Hermes, Claude, and any agent with fetch or a shell. Same rubric, same report.

## When to use

- User gives a URL and asks for a PWA review, install check, manifest audit, service-worker audit, or iOS PWA check.
- Do not use for generic Lighthouse, Core Web Vitals-only, or non-PWA site reviews.

## Workflow

1. Take the URL. If missing, ask once. Require `https://`.
2. Collect evidence. Prefer the script so every agent scores the same inputs:

```bash
python3 scripts/collect_pwa.py "https://example.com" --out /tmp/pwa-evidence.json
```

3. If the script cannot run, fetch with the agent adapter in `references/agent-adapters.md`. Minimum set: HTML, manifest JSON, service worker source. Resolve relative URLs against the page URL.
4. Read `references/checklist.md`. Score only with evidence. Missing file = 0 for that category, not a guess.
5. Read `references/ios-limits.md` when the page is mobile, installable, or the user mentions iOS.
6. Write the report from `references/report-template.md`. Lead with grade, score, and the top 3 fixes.

## Grades

| Grade | Points | Share |
|---|---|---|
| A+ | 173+ | 90%+ |
| A | 154–172 | 80–89% |
| B | 135–153 | 70–79% |
| C | 116–134 | 60–69% |
| D | 77–115 | 40–59% |
| F | <77 | <40% |

| Category | Points |
|---|---|
| Manifest compliance | 20 |
| Advanced manifest | 15 |
| Service worker and caching | 33 |
| Offline capability | 24 |
| Installability | 13 |
| Security | 16 |
| Performance signals | 17 |
| UX and accessibility | 29 |
| SEO and discoverability | 7 |
| PWA advanced | 17 |
| iOS compatibility bonus | 1 |

Critical blockers: no manifest = 0/20 on manifest compliance. No service worker = 0/33 on service worker and caching.

## Scoring rules

- Full points only when the check is present in fetched HTML, manifest, service worker, or a linked app script you actually opened.
- Partial points only where the checklist says partial.
- If a check lives in a bundled JS file you did not fetch, mark `unverified` and score 0. Say which URL to open next.
- Do not invent icons, CSP, or splash screens.
- Script output is evidence, not the final report. Apply the checklist, then write the report.

## References

- `references/checklist.md` — point tables. Read before scoring.
- `references/report-template.md` — issue classes and report shape.
- `references/ios-limits.md` — iOS/Safari limits and fetch failures.
- `references/agent-adapters.md` — Grok, Codex, Hermes, Claude fetch map.
- `scripts/collect_pwa.py` — fetch HTML, manifest, SW; emit evidence JSON.

## Install

Drop this folder on the agent skill path. No runtime deps beyond Python 3.

| Agent | Path |
|---|---|
| Grok | skills directory that already loads `SKILL.md` |
| Codex | `.agents/skills/pwa-review/` or `~/.codex/skills/pwa-review/` |
| Hermes / OpenClaw | skills path that loads `SKILL.md` |
| Claude Code | `.claude/skills/pwa-review/` |

Invoke in plain language: "pwa review https://example.com". Slash commands are optional.
