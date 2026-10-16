# Session Observations — 2026-10-16

Append-only log. Format: `- YYYY-MM-DD [domain] observation`

---

## 2026-10-16 — Superbloom Cafe hours (San Diego)

- [research] Superbloom Coffee & Juice, 2688 E Mission Bay Dr, Mission Bay Beach Club. Opens 7:00 AM daily. Mon–Thu closes 6:30 PM; Fri–Sun closes 7:00 PM. Instagram (@superbloomcafemissionbay) is closest to a primary source: "Hours: 7am-7pm."
- [research] Outliers claiming 8 PM close (Checkle, Franki) are likely Moonlight Bar hours bleeding into the listing after Superbloom wraps.
- [research] DuckDuckGo HTML search (duckduckgo.com/html) works as a no-JS fallback when regular web_search results are noisy. Browser-fetching the official site (missionbaybeachclub.com) returned no hours text — site is JS-heavy or hours live elsewhere.
- [research] Multiple listing sites (Yelp, Restaurant Guru, Yahoo Local, MapQuest, Apple Maps, Opulist, Snapchat) all agree on 7 AM open; closing times vary 6:30–8:00 PM across sources. When sources conflict on close time, trust the business's own channel (Instagram) over aggregators.
- [workflow] For a single factual lookup, answer in one sentence first. User explicitly corrected a multi-paragraph, tool-heavy response as overwhelming. Default to: fact → one line of context max → stop. No tool narration, no "I checked X and Y" preamble.
- [workflow] User asked to "Google it" / use DuckDuckGo specifically. When a user names a search engine or tool, use that tool (or the closest equivalent) rather than defaulting to web_search. Respect the named method.
- [preference] User dislikes dense, multi-clause spoken answers. Break complex findings into short beats. One fact per sentence. If it can't be said in under ~15 seconds aloud, it's too long.

## Instincts implied

- **instinct: answer-first-brevity** — trigger: "any factual lookup in voice mode" → action: state the answer in ≤1 sentence before any context or tool detail. confidence: 0.8 (explicit user correction).
- **instinct: respect-named-tool** — trigger: "user specifies a search engine or method" → action: use that tool first. confidence: 0.6 (single observation).
- **instinct: aggregator-vs-primary-source** — trigger: "conflicting business hours across listings" → action: prefer the business's own social/official channel over third-party aggregators for close times. confidence: 0.5 (single session, but pattern is generalizable).
