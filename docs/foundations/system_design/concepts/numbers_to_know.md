# Numbers to Know — SOURCE DATA (card not yet written)

> ⚠️ **This is not a concept card yet, and it has NO tracker row.** It is the raw figure set, captured
> Aug 12 2026 so a perishable paste isn't lost. The card — spine, fork-keyed bindings, Recall Card — is
> **agenda item 9(d) at the Aug 17 build**, held there because it is a fourth bidder for lane ②'s one
> midweek slot and that conflict is being resolved as a single decision.
>
> **Deliberately no `Concept` row in [`design_progress.md`](../mastery/design_progress.md).** A row means
> drillable, and the scheduler would place it. Add the row in the same edit that writes the card — the
> [`coverage_map.md`](../coverage_map.md) maintenance rule.
>
> **Source:** [HelloInterview → Core Concepts → Numbers to Know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know).
> Free tier fetched directly; the component table pasted by the learner from premium, Aug 12 2026.

## Free tier — the physical ceilings of one box

| | |
|---|---|
| **Memory, one box** | 512 GiB / 128 vCPU is *common* (M6i.32xlarge) · 4 TB (X1e.32xlarge) · **24 TB** (U-24tb1.metal) |
| **Local storage, one box** | **60 TB SSD** (i3en.24xlarge) · **336 TB HDD** (D3en.12xlarge) |
| **Network** | 25 Gbps in-datacenter is common · 50–100 Gbps on high-perf instances |
| **Latency ladder** | same AZ **sub-1ms** · cross-AZ, same region **1–2ms** · **cross-region 50–150ms** |

## Premium tier — per component (verbatim)

| Component | Key metrics | Scale triggers |
|---|---|---|
| **Caching** | ~1 ms latency · 100k+ ops/sec · memory-bound (up to 1 TB) | hit rate < 80% · latency > 1 ms · memory > 80% · cache churn/thrashing |
| **Databases** | up to 50k transactions/sec · sub-5ms read latency (cached) · 64 TiB+ storage | write throughput > 10k TPS · read latency > 5 ms uncached · geographic distribution needs |
| **App servers** | 100k+ concurrent connections · 8–64 cores @ 2–4 GHz · 64–512 GB RAM standard, up to 2 TB | CPU > 70% utilization · response latency > SLA · connections near 100k/instance · memory > 80% |
| **Message queues** | up to 1M msgs/sec per broker · sub-5ms end-to-end · up to 50 TB storage | throughput near 800k msgs/sec · partition count ~200k per cluster · growing consumer lag |

---

## ⭐ The finding — read the two columns as ONE rule, not sixteen numbers

**Every scale trigger fires at 70–80% of its stated ceiling, never at 100%.** Cache memory > 80% of 1 TB ·
app-server CPU > 70% · app-server memory > 80% · queue throughput at 800k of 1M · connections *near* 100k.
That is not four independent ops conventions — it is
[`utilization_and_queueing.md`](utilization_and_queueing.md)'s knee restated as practice: queueing delay
runs away as ρ → 1, so the usable ceiling sits well below the physical one.

**Which collapses the whole sheet into something memorable:** *one rule you already know, plus a short list
of ceilings.* Build the card on that spine. Sixteen flat figures will not survive to the interview; "80% of
whatever the ceiling is" plus five ceilings will.

**And it reprices the free-tier column.** 24 TB of RAM on one box is not a 24 TB budget — it is ~19 TB. Quote
the derated number *and the reason* in one breath; that is the senior signal, and the bare spec-sheet number
is the junior one.

## Bindings to write when the card is built — fork first, number second

[`framework.md`](../framework.md) §1: *"a number that doesn't change a decision is theater."* So every entry
gets keyed by the fork it resolves, not by the fact it states.

| Number | Fork it kills | Binds to |
|---|---|---|
| DB **64 TiB+** capacity vs the **> 10k TPS** write trigger | ⭐ *"the data is big, so we shard."* HelloInterview's own two columns say capacity is enormous and **writes bind first** — the trigger is a TPS number, not a size | **S** · Scaling Writes pattern · sharding (a Core Concept gap) |
| Latency ladder, **50–150 ms** cross-region | a p99 < 100 ms budget survives ~**one** cross-region hop and no more — this is what *prices* cross-region strong consistency | **L** + **C** · the CAP deep dive |
| Cache **~1 ms**, hit rate **< 80%** is a problem | ⭐ an 80% floor is only reachable *because* access is Zipfian — the number and the reason live in different files today | [`caching.md`](../components/caching.md) · [`zipfian_distribution.md`](zipfian_distribution.md) |
| App server **100k concurrent connections** | ⭐ this is `L`. With a latency it yields the QPS ceiling for free — the sheet supplies the constant the operator has been missing | [`littles_law.md`](littles_law.md) |
| CPU **> 70%** | the knee, not a round number | [`utilization_and_queueing.md`](utilization_and_queueing.md) |
| Sub-5ms cached vs **> 5 ms uncached** | the cache-or-not fork, with both branches quantified | [`percentiles_and_tail_latency.md`](percentiles_and_tail_latency.md) |
| **25 Gbps** ≈ 3 GB/s ≈ ~3M × 1 KB msg/s | whether one node can physically carry the fan-out | high-level design — "load each component absorbs" |
| **60 TB SSD / 336 TB HDD** | row-store vs blob store | Handling Large Blobs pattern · blob storage (a Key Technology gap) |
| Queue **1M msgs/sec per broker** | when one broker stops being enough → partitioning | Managing Long-Running Tasks pattern · the *queue role* gap |

**Three of these bind straight onto cards that already exist and are currently unusable for want of a
constant** — Little's Law, utilization & queueing, Zipf. That is the argument for pulling this forward: it
is the missing **input** to machinery already built, not another standalone fact.
