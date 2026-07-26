# Quorum Math (R + W > N)

> **Role:** Replication tuning — *one inequality that generates consistency-vs-latency on demand* · **Filed under:** SD concepts (underpins Cassandra/DynamoDB, replication deep-dives, CAP in practice).
> **You'll want this when:** you're asked **"how do you keep replicas consistent?"** or **"what happens if a replica is down?"** — or you're setting a consistency level on a Dynamo-style store.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this
> **If your write set and read set are big enough that they must overlap, the read is guaranteed to see the write. That's the pigeonhole principle, and it's the whole idea.**

Three facts. Everything else is a consequence of one of them.

| Fact | What you get | What it costs |
|---|---|---|
| `R + W > N` forces the read and write sets to **share at least one node** | the read always touches a replica holding the newest write | you must wait on more nodes → higher latency |
| **W and R are independent dials** on the same budget | tune per workload: cheap writes *or* cheap reads, your choice | making one cheap makes the other expensive |
| Overlap gives you **the newest value is present**, not **the newest value is returned** | a strong foundation for consistency | you still need versioning + read-repair to *pick* it |

## 🎯 In one line
With `N` replicas, requiring `W` acknowledgements to write and `R` responses to read, the condition
`R + W > N` guarantees the read quorum intersects the write quorum — so at least one responding node has
the latest value, and consistency becomes a **tunable latency tradeoff** rather than a fixed property.

## 🔢 Why it works (30 seconds of pigeonhole)
`N = 3`, `W = 2`, `R = 2`. The write landed on some 2 of the 3 nodes; the read asks some 2 of the 3. Two
sets of size 2 drawn from 3 elements **cannot be disjoint** — that would need 4 distinct nodes. So the
read set contains at least one node from the write set. Generally: `W + R > N` ⟹ overlap.

## 🎛️ The dial (N = 3, the default in practice)

| W | R | Overlap? | Character |
|---|---|---|---|
| 1 | 1 | ❌ | Fastest both ways, **eventual** only. Fine for caches, metrics, feeds. |
| **2** | **2** | ✅ | **Balanced quorum** — the standard default. Survives 1 node down for both reads and writes. |
| 3 | 1 | ✅ | Fast reads, slow/fragile writes — **any** node down blocks writes. Read-heavy, rarely written data. |
| 1 | 3 | ✅ | Fast writes, fragile reads. Write-heavy ingest where reads are rare. |

**Availability reading:** you tolerate `N − W` node failures for writes and `N − R` for reads. `W = N` is
the trap — it maximizes durability per write but means *zero* fault tolerance for writes.

**Latency reading:** waiting for `W` acks means waiting for the `W`-th **fastest** node — so raising W
pushes you further into the tail. Connects directly to
[percentiles & tail latency](percentiles_and_tail_latency.md): `W=3` waits on the slowest of 3.

## ⚠️ The honest caveats (say these before you're asked)
`R + W > N` is a **necessary** condition, not a sufficient one. It guarantees you *see* a node with the
latest write; it does not by itself give you linearizability.

- **You still need versioning to pick a winner.** The read gets multiple values back — resolve by version
  vector / timestamp / last-write-wins. LWW **silently drops** concurrent writes; vector clocks surface
  them as siblings for the application to merge.
- **Writes aren't rolled back on partial failure.** If a write reaches 1 of the required 2 and fails, that
  node keeps the value — the "failed" write may still be read later.
- **Sloppy quorums break the guarantee.** Dynamo-style systems accept writes on *any* N healthy nodes
  during a partition (with **hinted handoff** to deliver later) — great for availability, but the
  overlap argument no longer holds while nodes are displaced.
- **Concurrent writes race.** Two clients writing at the same time both satisfy W, and quorum math says
  nothing about which wins.
- **Read repair / anti-entropy is required** to converge the stale replicas the quorum didn't touch —
  otherwise a node can stay stale indefinitely and low-R reads keep hitting it.

## 🌐 Where you'll cite this
- **Cassandra** consistency levels: `ONE`, `QUORUM`, `LOCAL_QUORUM`, `ALL` — set **per query**, which is
  the whole point (analytics reads at ONE, account reads at QUORUM). `LOCAL_QUORUM` keeps the quorum
  inside one datacenter to avoid cross-region latency.
- **DynamoDB** exposes it as a simplified toggle: eventually-consistent reads (cheaper, faster) vs
  strongly-consistent reads (≈2× the read capacity cost).
- **CAP/PACELC in practice** — this is the concrete dial behind the abstraction. During a partition,
  lowering W/R chooses availability; keeping `R+W>N` chooses consistency. **PACELC's "else" half is the
  interesting one:** even with no partition, higher quorums cost latency.

---

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

<details><summary><b>1. State the quorum condition and the one-line reason it works.</b></summary>

`R + W > N`. By pigeonhole, two subsets of an N-node set whose sizes sum to more than N cannot be disjoint — so the read quorum must include at least one node from the write quorum, which therefore holds the latest value.
</details>

<details><summary><b>2. N=3. Give the settings for balanced quorum, and how many failures each side tolerates.</b></summary>

`W=2, R=2`. Writes tolerate `N−W = 1` node down; reads tolerate `N−R = 1` node down. It's the standard default because both sides survive a single failure.
</details>

<details><summary><b>3. When would you deliberately choose W=1, R=1?</b></summary>

When eventual consistency is acceptable and latency/availability dominate — caches, metrics, activity feeds, view counts. No overlap, so a read can miss a recent write, but both operations are as fast and as available as possible.
</details>

<details><summary><b>4. Why is W=N (write to all) a trap?</b></summary>

It gives zero write fault-tolerance — any single node down blocks all writes — and forces every write to wait on the *slowest* replica, putting you deep in the latency tail.
</details>

<details><summary><b>5. Does R + W > N give you linearizability? Explain.</b></summary>

No — it's necessary, not sufficient. It guarantees a latest-value replica *responds*; you still need versioning (vector clocks / timestamps) to decide which returned value wins, plus read-repair to converge. Partial failed writes aren't rolled back, concurrent writes still race, and **sloppy quorums** with hinted handoff void the overlap argument entirely.
</details>

<details><summary><b>6. What is a sloppy quorum and what does it buy?</b></summary>

During a partition, the write is accepted by any N *healthy* nodes rather than the N designated home nodes, with **hinted handoff** delivering it to the rightful owners once they return. It buys write availability under partition, at the cost of the strict overlap guarantee.
</details>

<details><summary><b>7. How does this map onto Cassandra, and why is LOCAL_QUORUM notable?</b></summary>

Cassandra sets consistency **per query** (`ONE` / `QUORUM` / `LOCAL_QUORUM` / `ALL`), so one cluster serves both weak and strong workloads. `LOCAL_QUORUM` confines the quorum to a single datacenter — you keep quorum semantics without paying cross-region round-trip latency.
</details>
