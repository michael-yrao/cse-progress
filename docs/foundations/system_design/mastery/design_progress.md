# System Design — Mock Interview Progress

<!--
Notes for future agents:
- This is the System Design spaced-repetition tracker, the sibling of
  cse-progress's docs/foundations/dsa/mastery/dsa_progress.md. Same 7-column table, same interval
  math, driven by the SAME script: scripts/update_review_dates.py --tracker <this file>.
- The pre-commit hook already recomputes + re-sorts this file when it is staged
  (recompute_simple()); there is NO source-file discovery here — rows are added by hand.
- ⚠️ REBUILT Aug 13, 2026 for the MOCK-INTERVIEW MODEL. The learner studies system design
  on their own via HelloInterview; the coach's entire job is running mock interviews on
  HelloInterview's question breakdowns and scoring them. Read
  ../study_guide.md (mechanics) and ../senior_ramp.md (sequence + rubric) before touching
  this file.
- Column reuse (the parser requires the literal DSA headers):
    * "Difficulty" → "Design (Easy|Med|Hard)", carrying HelloInterview's own tier for
                     that question. The tier is theirs, not a local judgement.
    * "Problem"    → the question, linked to its HelloInterview breakdown, plus a
                     "· debrief" link to ../mocks/<date>_<slug>.md once one exists.
- THE ROW IS A MOCK. One question = one row = one ~45-min cold mock = one rating.
  A question is 🔴/blank and inert (no review load) until its first mock runs.
- Rating is the 7-point rubric in ../senior_ramp.md, scored right after the mock:
    * 🟢 Clean  — #1–4 solid AND #5 forks, #6 failure modes, #7 evolve/operate all pass.
                                                              +30d (streak2 +60, retire@3 +180)
    * 🟡 Shaky  — skeleton (#1–4) solid, #5–7 shaky.           +10d, streak → 0
    * 🔴 Blank  — couldn't drive the framework cold.           +2d,  streak → 0
- To log a mock: write the debrief to ../mocks/, set Comfort, add today's date to Rep
  Dates + Latest Rep Date, then stage this file and commit (or run the script).
- The technology / concept / component cards are NO LONGER on the review engine — see
  "Reference cards" below. They were a study lane; studying is the learner's side of the
  split now, so they stopped being reps and stopped billing review load.
-->

> **Auto-refresh note:** regenerated when this file is staged for commit, or when
> `python scripts/update_review_dates.py --tracker mastery/design_progress.md` runs.

⚠️ **The board is entirely 🔴 and inert on purpose (Aug 13, 2026).** Rate Limiter's three 2026-07 reps
were cleared with the rest of the old apparatus at the learner's request: those were staged sessions
against a different rubric on a different source, and carrying a 🟡 forward would have priced a re-mock
against a rating no mock produced. **The arc note ([`../components/rate_limiter.md`](../components/rate_limiter.md))
keeps the content.** Nothing on this board bills review load until its first mock runs.

**The board is HelloInterview's own list: [31 question breakdowns](https://www.hellointerview.com/learn/system-design/in-a-hurry/problem-breakdowns) + the 4 *More Practice* questions that ship without a write-up — 35 rows, at HelloInterview's own tiers** (4 Easy · 18 Medium · 13 Hard). Order of attack, and the few that are trigger-gated rather than in the rotation, are owned by [`../senior_ramp.md`](../senior_ramp.md).

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |
|---|---|---|---|---|---|---|
| Design (Easy) | [Bitly](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly) | 🔴 | 0 |  |  |  |
| Design (Med) | [Rate Limiter](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Dropbox](https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Yelp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Local Delivery (GoPuff)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff) | 🔴 | 0 |  |  |  |
| Design (Med) | [Ticketmaster](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster) | 🔴 | 0 |  |  |  |
| Design (Med) | [Instagram](https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram) | 🔴 | 0 |  |  |  |
| Design (Med) | [FB News Feed](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed) | 🔴 | 0 |  |  |  |
| Design (Med) | [Tinder](https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder) | 🔴 | 0 |  |  |  |
| Design (Med) | [LeetCode](https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode) | 🔴 | 0 |  |  |  |
| Design (Med) | [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp) | 🔴 | 0 |  |  |  |
| Design (Med) | [Strava](https://www.hellointerview.com/learn/system-design/problem-breakdowns/strava) | 🔴 | 0 |  |  |  |
| Design (Med) | [Distributed Cache](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache) | 🔴 | 0 |  |  |  |
| Design (Med) | [Online Auction](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction) | 🔴 | 0 |  |  |  |
| Design (Med) | [YouTube](https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube) | 🔴 | 0 |  |  |  |
| Design (Med) | [Job Scheduler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler) | 🔴 | 0 |  |  |  |
| Design (Med) | [FB Live Comments](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments) | 🔴 | 0 |  |  |  |
| Design (Med) | [News Aggregator (Google News)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-news) | 🔴 | 0 |  |  |  |
| Design (Med) | [Price Tracking (camelcamelcamel)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/camelcamelcamel) | 🔴 | 0 |  |  |  |
| Design (Med) | [Notification System](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system) | 🔴 | 0 |  |  |  |
| Design (Hard) | [YouTube Top K](https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Uber](https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Google Docs](https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Web Crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Ad Click Aggregator](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator) | 🔴 | 0 |  |  |  |
| Design (Hard) | [FB Post Search](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Metrics Monitoring](https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring) | 🔴 | 0 |  |  |  |
| Design (Hard) | [ChatGPT](https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Online Chess](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Payment System](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Robinhood](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood) | 🔴 | 0 |  |  |  |
| Design (Med) | [Food Review App — no write-up](https://www.hellointerview.com/practice/system-design) | 🔴 | 0 |  |  |  |
| Design (Med) | [Game Leaderboard (Google) — no write-up](https://www.hellointerview.com/practice/system-design) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Donations Website — no write-up](https://www.hellointerview.com/practice/system-design) | 🔴 | 0 |  |  |  |
| Design (Hard) | [GitHub Actions — no write-up](https://www.hellointerview.com/practice/system-design) | 🔴 | 0 |  |  |  |

⭐ **The last four are HelloInterview's *More Practice* set — real reported interview questions with no
written breakdown.** That makes them **permanently cold-eligible**: there is no worked answer to read, so
they can never become a prepared mock, and they are the only rows on this board that can be re-mocked at
full 🟢 weight later. Treat them as the calibration reps and **do not spend them early** — hold them for
Phase C, where the question is whether the framework transfers to something you have never seen written
up. Sourced from the [practice hub](https://www.hellointerview.com/practice/system-design), which is the
link they carry because they have no page of their own.

⚠️ **Three rows are trigger-gated, not queued** — Payment System and Robinhood on
`waypoint_loop:fintech`, Online Chess as the lowest-ceiling Hard on the board. They hold rows because
they are on HelloInterview's list and a row costs nothing at 🔴; they are **not** in the rotation.
Reasons in [`../senior_ramp.md`](../senior_ramp.md).

---

## 📚 Reference cards — off the review engine (Aug 13, 2026)

**These were tracker rows until Aug 13, 2026 and are not any more.** They were the *study* lane —
technology fluency (lane ①), building blocks and concepts (lane ②) — and study is now the learner's
own side of the split, done in HelloInterview's Key Technologies / Core Concepts / Patterns material.
Cards written here stay as **remediation reference**: when a mock exposes a gap, the debrief points at
the card that covers it, or at the HelloInterview page if no card exists.

**They carry no comfort, no streak, and no review date.** The last rating each one held is recorded
below purely so the history isn't destroyed — do not read it as current state, and do not re-add these
rows. What measures whether Redis is understood is now a mock that reaches for Redis and gets probed
on it.

| Card | Last rating before retirement | Rep dates |
|---|---|---|
| [Redis](../technologies/redis.md) | 🟡 (teach Aug 10, rated sprint was scheduled Aug 15) | 2026-07-13, 2026-07-19, 2026-07-21, 2026-08-05 |
| [PostgreSQL](../technologies/postgresql.md) | never drilled | — |
| [Caching](../components/caching.md) · [Load balancer](../components/load_balancer.md) · [Rate limiter](../components/rate_limiter.md) | never drilled (rate limiter's arc is the design row above) | — |
| [Networking basics](../concepts/networking_basics.md) · [Percentiles & tail latency](../concepts/percentiles_and_tail_latency.md) · [Little's Law](../concepts/littles_law.md) · [Utilization & queueing](../concepts/utilization_and_queueing.md) · [Probabilistic sketches](../concepts/probabilistic_sketches.md) · [Retry storms & stampedes](../concepts/retry_storms_and_stampedes.md) · [Quorum math](../concepts/quorum_math.md) · [Zipfian distribution](../concepts/zipfian_distribution.md) · [Bloom filter](../concepts/bloom_filter.md) | never drilled | — |

**The nine `concepts/` cards are the one part of the old apparatus worth actively keeping.** They are
the *quantitative* foundations — Little's Law, percentiles, queueing, Zipf, quorum math — and
HelloInterview has **no equivalent**; its Core Concepts are structural (sharding, CAP, consistent
hashing), not numeric. They are what a "quantify every claim" push runs on mid-mock, so they stay,
indexed by their "You'll want this when…" trigger lines.

**Rows removed here are not deleted anywhere else.** Seven of the nine technologies had a row but no
note; those rows are simply gone, and HelloInterview's Key Technologies deep-dives cover the same
ten technologies with better material than an unwritten local file.

---

## 📋 Not on HelloInterview's board — kept so nothing was silently dropped

The board used to be [systemdesign.io](https://systemdesign.io/)'s 55 questions, triaged Aug 8, 2026.
Reseeding to HelloInterview replaced that list. **Most of the old core set maps straight across**
(URL shortener → Bitly, Messenger → WhatsApp, Doc Mgmt → Google Docs, Top-K → YouTube Top K, Metrics →
Metrics Monitoring, Nearby → Yelp, Ads → Ad Click Aggregator). These do **not** map, and are parked
here with a trigger rather than deleted — schedule-integrity rule: nothing leaves without a home.

| Question | Why it's parked | Trigger |
|---|---|---|
| Typeahead / autocomplete | Genuinely absent from HelloInterview. Real L6 round; FB Post Search is search, not prefix-completion | `board:hard-tier-open` — pull as a self-directed mock once the Hard tier is in rotation |
| Key-value store | Distributed Cache is adjacent but not the same rep (durability, partitioning, consistency knobs) | same |
| Google Calendar | Scheduling/conflict domain; nothing on the HelloInterview board teaches it | same |
| Distributed tracing · A/B testing | Observability + experimentation platform rounds, both real at L6, both absent | same |
| Data migration to cloud (zero-downtime cutover) | **Rubric #7 as an entire design**, and #7 is what the L6 rating hinges on | same — protect this one when it fires |
| Stream-processing system (design Kafka itself) | HelloInterview has Kafka as a *technology* deep-dive, not as a design | same |
| Twitter · Pastebin | Declined, not parked — Instagram + FB News Feed cover the first, Bitly covers the second | none; redundant |

**Everything below the old ROI line stays below it.** The 25 systemdesign.io questions triaged out on
Aug 8 keep their written reasons in [`../senior_ramp.md`](../senior_ramp.md); reseeding the board did
not re-open them.
