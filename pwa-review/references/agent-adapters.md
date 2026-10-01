---
description: "How Grok, Codex, Hermes, and Claude fetch PWA evidence without Claude-only tools."
connections: [checklist, report-template]
---

# Agent adapters

Use `scripts/collect_pwa.py` first. Fall back to the row for the host agent. Never require `WebFetch` or `/pwa-review`.

| Agent | Fetch HTML | Fetch manifest / SW | Shell |
|---|---|---|---|
| Grok | `browse_page` with instruction to return raw HTML head, or run the script | `browse_page` on the absolute manifest and SW URLs | `bash` + `python3 scripts/collect_pwa.py URL` |
| Codex | shell `curl -fsSL` or built-in web fetch if present | same, absolute URL | `python3 scripts/collect_pwa.py URL` |
| Hermes / OpenClaw | browser tool or shell curl | browser tool or shell curl | same script |
| Claude Code | WebFetch is allowed, not required | WebFetch or curl | same script |
| Any other | HTTP GET of the page | HTTP GET of discovered URLs | same script |

## Fetch contract

Return these three bodies, or an explicit failure:

1. Page HTML (head is required; body if present).
2. Web app manifest JSON.
3. Service worker source.

Also note response URL after redirects, status code, and `content-type`.

## Discovery

- Manifest: `<link rel="manifest" href="...">`. Resolve against the final page URL.
- Service worker: `navigator.serviceWorker.register("...")` or `register('...')` in HTML or linked classic scripts. Do not execute the page.
- If missing, try `/manifest.webmanifest`, `/manifest.json`, `/sw.js`, `/service-worker.js` on the same origin. Label those as probes, not as declared.

## Failure map

| Failure | Score |
|---|---|
| No manifest link and probes 404 | Manifest categories 0. Critical. |
| Manifest 404, CORS, or invalid JSON | Manifest categories 0. Name the status. |
| No SW registration and probes 404 | SW category 0. Critical. |
| SW fetch fails | SW and offline checks that need SW source score 0. |
| Page is an app shell that loads the manifest from JS only | Say so. Score only what you fetched. |

## Output

Write the report in the host agent's normal channel (chat, file, or PR comment). Do not wrap it in `<pwa-review>` tags. Do not depend on a slash command.
