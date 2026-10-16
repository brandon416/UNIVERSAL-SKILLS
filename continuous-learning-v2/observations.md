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

## 2026-10-16 — Early morning (all-nighter aftermath, ~5 AM PT)

- [workflow] User walked to car after all-nighter, wants 2–3 hours max then workout. Best move: eat first, one highest-leverage task, hard stop, lift. The all-nighter habit is the target, not the to-do list.
- [workflow] Time-sensitive triage from Fleet Board (read-only): payroll Gusto cutoff 4 PM PT (~$1,742), Steffi 1 PM Acuity deadline (DW-009), Vianey 2 PM family emergency draft (DW-011), Camille approved-but-unsent text (DW-010), Richard broken 9-digit Acuity phone. Everything else waits for 8:02 PM batch.
- [preference] When user says a name that ASR renders as "Catherine" in fleet context, it means Captain (Chief of Staff bot). Confirm by context, don't ask.
- [preference] User said "Captain" to correct me, then immediately said don't dispatch Captain — he wants to be with Captain directly. Supersede any bot prompt the moment Brandon says he'll handle it himself.
- [safety] Read-only session rule: when Brandon says read-only / tools-only / don't write, ALL connectors are read-only — no Sheet writes, no sends, no Acuity mutations, no payroll entry, no draft approvals. Ask before any mutation even if it seems helpful. This killed my instinct to offer queuing approvals.
- [workflow] Continuous-learning request pattern: Brandon asks to log what was learned into a doc, frames it as CEO-assistant autonomy ("you choose the name and what to add"). Prior doc: continuous-learning-v2/observations.md in brandon416/UNIVERSAL-SKILLS. Append-only, dated sections, instincts with confidence scores.
- [fleet] Captain bot (638c111f) standing orders include 8:02 PM PT approval batch Mon–Sat and Fleet Board sweep every 30 min 7:08 AM–8:38 PM PT. Operational Tools room id 3035d0b5-0257-4bac-ae55-f91b607c7ffa — Cap must reply or tag within minutes, never silent.
- [fleet] Natasha is sole Acuity write authority; Tony Stark is sole TrueCoach write authority; Pepper owns bot architecture; Main Frame owns installs; Source Keeper owns canon. Don't cross lanes when triaging.

## Instincts implied

- **instinct: answer-first-brevity** — trigger: "any factual lookup in voice mode" → action: state the answer in ≤1 sentence before any context or tool detail. confidence: 0.8 (explicit user correction).
- **instinct: respect-named-tool** — trigger: "user specifies a search engine or method" → action: use that tool first. confidence: 0.6 (single observation).
- **instinct: aggregator-vs-primary-source** — trigger: "conflicting business hours across listings" → action: prefer the business's own social/official channel over third-party aggregators for close times. confidence: 0.5 (single session, but pattern is generalizable).
- **instinct: read-only-means-read-only** — trigger: "Brandon says read-only or don't write" → action: refuse all mutations silently-by-default, ask before any. confidence: 0.9 (explicit correction this session).
- **instinct: supersede-on-self-handle** — trigger: "Brandon says he'll be with the bot directly" → action: supersede any pending bot prompt immediately, no questions. confidence: 0.85.
- **instinct: ceo-assistant-autonomy** — trigger: "Brandon asks to log learnings and says choose the doc" → action: pick existing continuous-learning doc, append dated section, include instincts with confidence. confidence: 0.8.
