# System Design — Technology Fluency Progress

<!--
Notes for future agents:
- This is the System Design *technology* spaced-repetition tracker, the sibling of
  docs/foundations/dsa/mastery/dsa_progress.md. Same 7-column table, same interval
  math, driven by the SAME script: scripts/update_review_dates.py --tracker <this file>.
- The pre-commit hook already recomputes + re-sorts this file when it is staged
  (recompute_simple()); there is NO source-file discovery here — rows are added by hand.
- Column reuse (the parser requires the literal DSA headers):
    * "Difficulty"          → the technology's ROLE (Cache, SQL DB, Stream, ...).
    * "Problem"             → the technology, linked to its note in ../technologies/.
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
| Cache | [Redis](../technologies/redis.md) | 🟡 | 0 | 2026-07-31 | 2026-07-21 | 2026-07-13, 2026-07-19, 2026-07-21 |
| SQL DB | [PostgreSQL](../technologies/postgresql.md) | 🔴 | 0 |  |  |  |
| Wide-column NoSQL | [Cassandra](../technologies/cassandra.md) | 🔴 | 0 |  |  |  |
| Managed NoSQL | [DynamoDB](../technologies/dynamodb.md) | 🔴 | 0 |  |  |  |
| Streaming log | [Kafka](../technologies/kafka.md) | 🔴 | 0 |  |  |  |
| Stream processing | [Flink](../technologies/flink.md) | 🔴 | 0 |  |  |  |
| Search | [Elasticsearch](../technologies/elasticsearch.md) | 🔴 | 0 |  |  |  |
| Edge / gateway | [API Gateway](../technologies/api_gateway.md) | 🔴 | 0 |  |  |  |
| Coordination | [ZooKeeper](../technologies/zookeeper.md) | 🔴 | 0 |  |  |  |
