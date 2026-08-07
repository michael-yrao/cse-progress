# System Design — Technology Fluency Progress

<!--
Notes for future agents:
- This is the System Design *technology* spaced-repetition tracker, the sibling of
  docs/foundations/dsa/mastery/dsa_progress.md. Same 7-column table, same interval
  math, driven by the SAME script: scripts/update_review_dates.py --tracker <this file>.
- The pre-commit hook already recomputes + re-sorts this file when it is staged
  (recompute_simple()); there is NO source-file discovery here — rows are added by hand.
- Column reuse (the parser requires the literal DSA headers):
    * "Difficulty"          → the technology's ROLE (Cache, SQL DB, Stream, ...), or the
                              literal "Concept" for a ../concepts/ card.
    * "Problem"             → the technology, linked to its note in ../technologies/,
                              or the concept, linked into ../concepts/.
- Rows with role "Concept" are drilled by lane ② as its fallback when the pull queue is
  empty (see ../study_guide.md "The concepts lane"). Same blind-sprint format, same math.
- Rows with role "Design (Easy|Med|Hard|V.Hard)" are the end-to-end DESIGN reps, reseeded
  Aug 6, 2026 to the systemdesign.io catalog + its difficulty tiers. The "Problem" links to
  the systemdesign.io question (the LeetCode-equivalent anchor), + a local note link once
  work exists. **One design = one row = one session** (the old multi-day "Weekly Design
  Question Loop" is retired). Do them in tier order — finish open arcs first (URL Shortener
  in flight, Rate Limiter arc at 🟡), then Easy → Med → Hard. Queued designs sit 🔴/blank
  (inert, no review load) until their session. Rate the ~45-min cold mock on the senior_ramp
  7-point rubric (#5 forks / #6 failure modes / #7 evolve-operate) — see ../senior_ramp.md.
- The REP is a "blind sprint": open the technology's Recall Card, answer every prompt
  from memory, unfold to check, then rate:
    * 🟢 Clean  — every card answered cold, correctly.            +30d (streak2 +60, retire@3 +180)
    * 🟡 Shaky  — got most, needed a nudge or missed a follow-up. +10d, streak → 0
    * 🔴 Blank  — couldn't recall the shape of it.                +2d,  streak → 0
- To log a rep: set Comfort, add today's date to Attempt Dates + Latest Attempt Date,
  then stage this file and commit (or run the script) — Next Review Date recomputes.
- Undrilled technologies sit in the backlog with empty dates until their first sprint.
-->

> **Auto-refresh note:** regenerated when this file is staged for commit, or when
> `python scripts/update_review_dates.py --tracker docs/foundations/system_design/mastery/design_progress.md` runs.

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Cache | [Redis](../technologies/redis.md) | 🟡 | 0 | 2026-08-15 | 2026-08-05 | 2026-07-13, 2026-07-19, 2026-07-21, 2026-08-05 |
| SQL DB | [PostgreSQL](../technologies/postgresql.md) | 🔴 | 0 |  |  |  |
| Wide-column NoSQL | [Cassandra](../technologies/cassandra.md) | 🔴 | 0 |  |  |  |
| Managed NoSQL | [DynamoDB](../technologies/dynamodb.md) | 🔴 | 0 |  |  |  |
| Streaming log | [Kafka](../technologies/kafka.md) | 🔴 | 0 |  |  |  |
| Stream processing | [Flink](../technologies/flink.md) | 🔴 | 0 |  |  |  |
| Search | [Elasticsearch](../technologies/elasticsearch.md) | 🔴 | 0 |  |  |  |
| Edge / gateway | [API Gateway](../technologies/api_gateway.md) | 🔴 | 0 |  |  |  |
| Coordination | [ZooKeeper](../technologies/zookeeper.md) | 🔴 | 0 |  |  |  |
| Concept | [Networking fundamentals](../concepts/networking_basics.md) | 🔴 | 0 |  |  |  |
| Concept | [Percentiles & tail latency](../concepts/percentiles_and_tail_latency.md) | 🔴 | 0 |  |  |  |
| Concept | [Little's Law](../concepts/littles_law.md) | 🔴 | 0 |  |  |  |
| Concept | [Utilization & queueing](../concepts/utilization_and_queueing.md) | 🔴 | 0 |  |  |  |
| Concept | [Probabilistic sketches (HLL, Count-Min)](../concepts/probabilistic_sketches.md) | 🔴 | 0 |  |  |  |
| Concept | [Retry storms & stampedes](../concepts/retry_storms_and_stampedes.md) | 🔴 | 0 |  |  |  |
| Concept | [Quorum math (R + W > N)](../concepts/quorum_math.md) | 🔴 | 0 |  |  |  |
| Concept | [Zipfian distribution](../concepts/zipfian_distribution.md) | 🔴 | 0 |  |  |  |
| Concept | [Bloom filter](../concepts/bloom_filter.md) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Pastebin](https://systemdesign.io/question/design-pastebin) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Instagram](https://systemdesign.io/question/design-instagram) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Twitter](https://systemdesign.io/question/design-twitter-for-millions-of-users) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Top-K (App Store Rankings)](https://systemdesign.io/question/top-k-elements-app-store-rankings-amazon-bestsellers) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Job Scheduler](https://systemdesign.io/question/design-a-job-scheduler) | 🔴 | 0 |  |  |  |
| Design (Easy) | [Document Mgmt (Notion/Wikipedia)](https://systemdesign.io/question/create-a-document-management-system-like-wikipedia-or-notion) | 🔴 | 0 |  |  |  |
| Design (Easy) | [FB Likes w/ Live Updates](https://systemdesign.io/question/design-facebook-likes-feature-with-live-updates) | 🔴 | 0 |  |  |  |
| Design (Med) | [Dropbox / Google Drive](https://systemdesign.io/question/design-dropbox-or-google-drive) | 🔴 | 0 |  |  |  |
| Design (Med) | [Messenger / WhatsApp](https://systemdesign.io/question/design-facebook-messenger-or-whatsapp) | 🔴 | 0 |  |  |  |
| Design (Med) | [YouTube / Netflix](https://systemdesign.io/question/design-youtube-or-netflix) | 🔴 | 0 |  |  |  |
| Design (Med) | [Key-Value Store](https://systemdesign.io/question/design-a-keyvalue-store) | 🔴 | 0 |  |  |  |
| Design (Med) | [Web Crawler](https://systemdesign.io/question/design-web-crawler) | 🔴 | 0 |  |  |  |
| Design (Med) | [News Feed](https://systemdesign.io/question/design-facebooks-news-feed) | 🔴 | 0 |  |  |  |
| Design (Med) | [Google Calendar](https://systemdesign.io/question/design-google-calendar) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Typeahead / Autocomplete](https://systemdesign.io/question/design-typeahead-suggestion-autocomplete) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Notification Service](https://systemdesign.io/question/design-a-notification-service-at-scale) | 🔴 | 0 |  |  |  |
| Design (Hard) | [Metrics Collection](https://systemdesign.io/question/system-to-collect-metrics-from-thousands-of-servers) | 🔴 | 0 |  |  |  |
| Design (V.Hard) | [Yelp / Nearby Friends](https://systemdesign.io/question/design-yelp-or-nearby-friends) | 🔴 | 0 |  |  |  |
| Design (V.Hard) | [Credit-Card Processing (fintech waypoint — deprioritized)](https://systemdesign.io/question/design-a-credit-card-processing-system) | 🔴 | 0 |  |  |  |
| Design (Easy) | [URL Shortener (TinyURL)](https://systemdesign.io/question/design-url-shortening-service-like-tinyurl) · [wip](../case_studies/url_shortener.md) | 🔴 | 0 |  |  |  |
| Design (Hard) | [API Rate Limiter](https://systemdesign.io/question/design-an-api-rate-limiter) · [arc](../components/rate_limiter.md) | 🟡 | 0 | 2026-08-05 | 2026-07-26 | 2026-07-05, 2026-07-12, 2026-07-26 |
