# Networking Fundamentals (IP · TCP · TLS · DNS · HTTP)

> **Role:** Prerequisite plumbing — *the layer every other SD answer silently stands on* · **Filed under:** SD concepts (underpins load balancers, CDNs, TLS termination, timeouts, retries).
> **You'll want this when:** you say "the load balancer terminates TLS" or "we'll keep the connection alive" or "add a retry" — and someone asks *what actually happens on the wire*. Also whenever a design's latency budget needs RTTs counted.
> **Drill:** answer the [Recall Card](#-recall-card-the-rep) cold, then unfold to check.

## 🦴 The spine — everything else derives from this

> **Layers nest like envelopes. Each layer knows only its own job and treats everything above it as
> opaque payload it must not read.**

Three facts. Everything below is a consequence of one of them.

| Fact | What it means | What it buys you |
|---|---|---|
| **IP** moves packets between **machines**, best-effort | may drop, duplicate, reorder, and never tells you | it is *allowed* to fail silently — every guarantee above is built on this admission |
| **TCP** runs on top of IP, between **ports**, and adds back what IP lacks | ordering, delivery, dedup, flow control | "reliable byte stream" is software at the two ends, not a property of the network |
| A **connection** is *state at both endpoints*, not a wire | nothing in the middle is obliged to remember it | this is why a proxy can terminate, pool, and re-originate connections at all |

## 🔤 The acronyms, expanded

Kept at the top on purpose — these get used unexpanded everywhere, and half of them are named after
something other than what they do.

| | Stands for | What it actually is |
|---|---|---|
| **IP** | **I**nternet **P**rotocol | addresses + routing between *machines*. Best-effort: may drop/dupe/reorder |
| **TCP** | **T**ransmission **C**ontrol **P**rotocol | reliable ordered byte stream between *ports*, built on top of IP |
| **UDP** | **U**ser **D**atagram **P**rotocol | the no-guarantees alternative to TCP — fire and forget |
| **TLS** | **T**ransport **L**ayer **S**ecurity | encryption + server identity, between TCP and HTTP. Formerly **SSL** (**S**ecure **S**ockets **L**ayer) — you'll still hear "SSL" for TLS everywhere |
| **HTTP** | **H**yper**T**ext **T**ransfer **P**rotocol | the request/response text format: method, path, headers, body |
| **HTTPS** | HTTP **S**ecure | *not a separate protocol* — it is plain HTTP running inside a TLS tunnel |
| **DNS** | **D**omain **N**ame **S**ystem | name → IP address lookup. A distributed database, queried before you can connect at all |
| **SNI** | **S**erver **N**ame **I**ndication | a TLS handshake field naming the host you want, sent **in the clear** |
| **RTT** | **R**ound-**T**rip **T**ime | one there-and-back trip. The unit latency budgets are actually counted in |
| **CDN** | **C**ontent **D**elivery **N**etwork | caches placed near users, mostly to cut RTTs |
| **L3 / L4 / L7** | **L**ayer 3 / 4 / 7 of the OSI model | shorthand for *which header a box reads*: L3 = IP, L4 = TCP/UDP ports, L7 = HTTP itself |
| **OSI** | **O**pen **S**ystems **I**nterconnection (model) | the 7-layer teaching diagram the layer numbers come from |
| **LB** | **L**oad **B**alancer | the box spreading requests across backends |
| **VPC** | **V**irtual **P**rivate **C**loud | your isolated private network inside a cloud provider. Servers get private addresses unreachable from the internet; only what you expose (usually the LB) faces outward. "Inside the VPC" = on the trusted side |
| **QPS** | **Q**ueries **P**er **S**econd | request rate. (Also seen: RPS, requests per second) |
| **TTL** | **T**ime **T**o **L**ive | how long a cached answer stays valid — used by DNS records and HTTP caches alike |

**On "L7":** the OSI model is a 7-layer teaching diagram from the 1980s that the real internet never
matched. Almost nobody uses layers 5 and 6. In practice the numbers survive only as jargon for how
deep a middlebox looks:

- **L3 switch/router** — reads IP addresses. Picks a next hop.
- **L4 load balancer** — reads TCP ports. Can balance connections, but has no idea what a URL is.
- **L7 load balancer** — reads the HTTP request. Can route by path/header/cookie, retry a failed
  request, and terminate TLS.

## 👁 What the middle can see

**"Stateless about you" ≠ "can't read you."** A router keeps no memory of your connection, but the
packet is in its buffer and it may read as deep as it likes. It stops at the IP header because that
is its *job*, not because of any barrier.

| Over | A middlebox can read | It cannot read |
|---|---|---|
| `http://` | everything — method, path, headers, body, cookies | *(nothing — it's all plaintext)* |
| `https://` | IP addresses, ports, packet sizes/timing, **the hostname via TLS SNI** | method, **path**, headers, body, cookies |

Two consequences that come up constantly in design:

- **Deep reading is a feature, not just a threat.** An **L7 load balancer** routing `/api` to one pool
  and `/images` to another is doing exactly this on purpose. So is a CDN keying its cache on the URL.
- **HTTPS hides the path, not the destination.** `https://example.com/secret-report` leaks
  `example.com` to anyone on the path (SNI is sent in the clear during the handshake, and the DNS
  lookup leaked it a moment earlier). It does *not* leak `/secret-report`. ECH and DNS-over-HTTPS
  close those two gaps respectively; assume neither unless told otherwise.

## 🔐 TLS termination — the word that confuses everyone

**"Terminate" does not mean "stop using TLS." It means "be one of the two ends."**

The apparent paradox: an L7 load balancer routes by URL path, but under HTTPS the path is encrypted.
Resolution — the client is not talking *through* the LB, it is talking **to** it:

```
client ──── TLS session #1 ────▶ load balancer ──── connection #2 ────▶ backend
       (LB holds the cert +                    (separate connection,
        private key for the domain;             LB re-sends the request)
        to the client, the LB *is* example.com)
```

The LB completes the handshake, decrypts, and holds plaintext HTTP — so it can route on path, retry,
add headers, and log. This is only possible because **a connection is state at its two endpoints**
(spine fact 3): anything holding the keys is allowed to *be* an endpoint.

**The second hop is a separate decision**, and it's the one people forget:

| Second hop | What it means | When |
|---|---|---|
| **Terminate** (plain HTTP to backend) | LB→backend is unencrypted | inside a trusted VPC; cheapest, most common |
| **Re-encrypt** (a.k.a. TLS bridging) | LB decrypts, then opens its own TLS to the backend | regulated data, zero-trust networks |
| **Passthrough** | LB does *not* decrypt; forwards TCP bytes | end-to-end encryption required — but then it is an **L4** balancer and **cannot** route by path |

> **The tradeoff to say out loud in an interview:** you cannot have both end-to-end encryption *and*
> path-based routing at the same box. Passthrough buys secrecy and costs you L7 features. That is a
> real fork, not a detail.

## ⏱ The cold-start ladder — what one URL actually costs

**Nothing about HTTP has happened yet.** Before the first byte of `GET /foo` can leave your machine,
three separate conversations must complete, each costing at least one **RTT (round-trip time)**.

| # | Step | Cost | What it's doing |
|---|---|---|---|
| 1 | **DNS lookup** | ~1 RTT (cached) · up to 4 (cold) | `example.com` → `93.184.216.34`. You cannot open a socket to a name |
| 2 | **TCP handshake** | **1 RTT** | SYN → SYN-ACK → ACK. Both ends agree on starting sequence numbers. *This is the moment the "connection" (state at both ends) comes into existence* |
| 3 | **TLS handshake** | **1 RTT** (TLS 1.3) · **2 RTT** (TLS 1.2) | agree on ciphers, server proves it owns the certificate, derive session keys |
| 4 | **HTTP request finally sent** | 1 RTT to first byte back | `GET /foo HTTP/1.1` |

**Cold start on TLS 1.3 ≈ 3 RTTs before you have even asked for anything**, then a 4th to get it.

### Run it with real numbers

RTT is dominated by physical distance — light in fibre is ~200,000 km/s, and packets don't travel in
straight lines.

| Path | Typical RTT | Cold start (3 RTT) | + first byte |
|---|---|---|---|
| Same datacenter | ~0.5 ms | ~1.5 ms | ~2 ms |
| Same city | ~5 ms | 15 ms | 20 ms |
| US coast to coast | ~70 ms | 210 ms | **280 ms** |
| US → Europe | ~100 ms | 300 ms | **400 ms** |
| US → Australia | ~200 ms | 600 ms | **800 ms** |

> **The punchline:** for a user in Sydney hitting a server in Virginia, roughly *three quarters of a
> second* elapses before a single byte of your page arrives — and your server code hasn't run yet.
> None of that is your application's fault, and none of it is fixable by making the server faster.

### Latency vs bandwidth vs RTT — the distinction that decides the fix

| Term | What it measures | Analogy |
|---|---|---|
| **Latency** | delay for data to travel one way | how long the truck takes to arrive |
| **RTT** | there *and back* — roughly 2× latency | round trip of the truck |
| **Bandwidth** | how much data per second once flowing | how big the truck is |

**They are independent, and this is the single most useful consequence in the whole card:**

- **Bandwidth cannot fix RTT.** A 10 Gbps link between Sydney and Virginia still has ~200 ms RTT. The
  handshakes above take exactly as long on a fat pipe as a thin one — they're waiting on *distance*.
- So for **many small requests**, you are latency-bound → the fix is *fewer round trips* or *shorter
  distance*: connection reuse, HTTP/2 multiplexing, a **CDN (Content Delivery Network)** that moves
  the endpoint near the user.
- For **few large transfers**, you are bandwidth-bound → the fix is compression, a smaller payload,
  or a fatter pipe.
- Diagnosing one as the other is the classic wrong turn: buying bandwidth to fix a chatty API does
  nothing at all.

### Design consequences

- **Keep-alive / connection pooling is not a micro-optimisation.** Reusing a warm connection skips
  steps 1–3 entirely — that's 3 RTTs saved *per request*. This is why every HTTP client library
  pools, and why creating a new client per request is a real bug.
- **A CDN's main product is fewer milliseconds of distance**, not just caching. Terminating TLS at an
  edge node 5 ms away turns a 300 ms cold start into 15 ms even on a cache miss.
- **TLS 1.3 removed a full round trip** vs 1.2, and its 0-RTT resumption can send data on the *first*
  packet to a previously-visited server (at the cost of replay risk — not for non-idempotent requests).
- **DNS TTL (time to live) is a failover lever.** A 60-second TTL means clients re-resolve quickly
  when you move an IP; a 24-hour TTL means some clients keep hitting a dead address all day.

## 🧭 DNS — you make one query; someone else makes four

**You parse the URL locally.** `https://example.com/foo` → scheme `https`, host `example.com`, path
`/foo`. **Only the host is looked up.** The path never leaves your machine until the HTTP request
itself — which is exactly why TLS protects the path but not the hostname.

**Your machine asks exactly one server: a recursive resolver.** Default is your **ISP (Internet
Service Provider)**'s; you can point at a public one (`8.8.8.8` Google, `1.1.1.1` Cloudflare). Your
home router usually just *forwards* to it, which is why it looks like the router answered.

If the resolver has the answer cached, that's your ~1 RTT and you're done. If not, **it** does the
walking — you still made only one query:

```
you ──▶ recursive resolver ──▶ root server        "who handles .com?"
                          ──▶ .com TLD server     "who handles example.com?"
                          ──▶ authoritative NS    "what is example.com?"  → 93.184.216.34
        ◀── answer ───────
```

- **Root servers** (13 logical, anycast to hundreds of physical) know only where the TLDs are.
- **TLD (Top-Level Domain) servers** — `.com`, `.org`, `.io` — know which nameserver is authoritative
  for each domain under them.
- **Authoritative nameserver** — the one you configure when you buy a domain — holds the real record.

**Every level caches, governed by TTL (time to live).** In practice roots and TLDs are almost always
cached, so a cold lookup is 1–2 RTTs, not 4.

### Design consequences

- **TTL is your failover speed.** See the box below — this is the one people get bitten by.
- **DNS is a load-balancing layer.** Returning different IPs per region (GeoDNS) is how a CDN sends
  you to a nearby edge. It's coarse — DNS can't see health or load mid-connection — so it's usually
  paired with a real load balancer behind it.
- **DNS is plaintext by default** (UDP port 53), so your ISP and anyone on the path sees every
  hostname you resolve. DoH (DNS over HTTPS) and DoT (DNS over TLS) close that.
- **A failed resolve looks like a total outage to users** while your servers sit perfectly healthy.
  DNS is a genuine single point of failure and belongs on your dependency list.

### ⏳ TTL, concretely — why your DNS change "didn't work"

**TTL (time to live) is a permission slip attached to the answer:** *"you may reuse this for N seconds
before asking me again."* The authoritative server doesn't just return `example.com → 1.1.1.1`; it
returns `example.com → 1.1.1.1, TTL 3600`. Every resolver that sees it serves from memory for an hour.

```
10:00  resolver asks, gets 1.1.1.1 with TTL 3600  → caches until 11:00
10:15  you change the record to 2.2.2.2 at your registrar
10:16  user asks their resolver → still cached    → gets 1.1.1.1   ✗
10:59  still 1.1.1.1                                                ✗
11:00  cache expires; next query re-asks          → gets 2.2.2.2   ✓
```

Your change was live and correct at 10:15 and made **no difference** to those users for 45 minutes.
If the old IP is dead, that is 45 minutes of outage you cannot shorten by fixing anything on your
side — you are waiting on caches you do not control to expire.

**So the migration procedure is three steps, not one:**

1. **A day ahead**, lower the TTL 3600 → 60. *(You must wait out the old 3600 for this to take hold
   everywhere — that's why it's a day ahead, not an hour.)*
2. **Then** flip the IP. Clients pick it up within a minute.
3. Raise the TTL back once it's settled.

**Why not just leave TTL at 60 permanently?** Resolvers then re-ask constantly: more DNS load, more
cache misses, and a DNS round trip added back onto requests that could have skipped it. It is the
ordinary cache trade — **freshness vs. traffic** — and DNS is just a cache like any other.

## 🔌 Ports, and what a "connection" actually is

**IP gets you to the machine. The port gets you to the program on it.** One server at one IP runs a
web server on 443, SSH on 22, and Postgres on 5432 — same address, three doors.

A TCP connection is identified by a **4-tuple**:

```
(source IP, source port, destination IP, destination port)
```

Your browser opens three tabs to the same site: same destination IP and port, but three *different*
source ports, so they're three distinct connections. This is also why one server can hold hundreds of
thousands of connections on port 443 — the port isn't consumed, the tuple is.

> **Well-known ports:** 80 HTTP · 443 HTTPS · 53 DNS · 22 SSH. The `https://` in a URL is what implies
> 443; `https://example.com:8443/foo` overrides it.

**The connection is that 4-tuple plus the sequence-number state at each end — and nothing else.** No
router in between allocates anything or agrees to anything. "Establishing a connection" is two machines
writing down numbers about each other.

### The three port bands

| Range | Name | Who uses it |
|---|---|---|
| **0–1023** | **well-known** | HTTP 80 · HTTPS 443 · DNS 53 · SSH 22 · SMTP 25. **The one band every OS agrees on**, and on Unix-likes **binding here requires root** |
| 1024–49151 | registered | vendor defaults — Postgres 5432 · MySQL 3306 · Redis 6379 · Kafka 9092 · Mongo 27017 · Elasticsearch 9200 |
| 49152–65535 | **ephemeral** | throwaway source ports your OS picks per connection. ⚠️ **OS-dependent** — Linux actually uses **32768–60999**, so "49152+" is IANA's recommendation, not a rule |

Two consequences that look like mysteries when you meet them cold:

- **Apps run on 8080 behind a proxy holding 443** because of the root rule — not ceremony. The privileged
  port is held by the load balancer; the app runs unprivileged behind it.
- **A machine tops out around 28k outbound connections to a *single* destination** (Linux's ephemeral range
  is ~28,000 wide) — each needs a distinct source port. A busy gateway hammering one backend hits this and
  starts failing to connect. **The fix is more source IPs or a wider range, not a bigger machine.**

## 🏠 Private vs public addressing, and NAT

*Added Aug 8, 2026 — this was missing from the card entirely and came up immediately on first contact.*

**Every device on your network has its own address, but a *private* one** — `192.168.1.5`, `192.168.1.6`.
Unique inside that network, meaningless outside it, and the same numbers exist in millions of homes at once.
The whole network shares **one public address**, held by the router. **The router is a member of both
networks — that is the only reason it can pass traffic between them.**

```
        HOME NETWORK (private)                    │        INTERNET (public)
 ┌────────────────────┐                           │
 │ Laptop             │                           │
 │ 192.168.1.5 :51204 │───────────┐               │
 └─────────┬──────────┘           │               │
           │ local traffic        ▼               │
           │ (AirDrop, casting)  ┌──────────────────┐
           │ never leaves the    │     ROUTER       │
           │ house               │ priv 192.168.1.1 │
 ┌─────────┴──────────┐          │ pub  203.0.113.9 │───┼──▶ 93.184.216.34:443
 │ Phone              │──────────▶     NAT table    │   │
 │ 192.168.1.6 :52117 │          │ .1.5:51204⇄:62311│   │
 └─────────┬──────────┘          │ .1.6:52117⇄:62312│   │
 ┌─────────┴──────────┐          └──────────────────┘   │
 │ Smart TV           │───────────▲                     │
 │ 192.168.1.7 :58330 │───────────┘                     │
 └────────────────────┘                                 │
```

**Why the split exists — two reasons, and both still matter:**

1. **Scarcity.** IPv4 has ~4.3 billion addresses, fewer than there are devices. Private ranges let a whole
   household consume **one** public address.
2. **Nothing on the internet can address your laptop directly.** It has no globally routable address, so
   unsolicited inbound traffic reaches the router and has nowhere to go. A firewall for free, as a side
   effect of the addressing. *(IPv6 removes reason 1; reason 2 is valuable enough that the boundary usually
   stays.)*

### Follow one packet — only the SOURCE changes

```
 ① laptop ──▶ router      SRC 192.168.1.5:51204    DST 93.184.216.34:443
 ② router ──▶ internet    SRC 203.0.113.9:62311    DST 93.184.216.34:443   ← NAT rewrote SRC
 ③ server ──▶ back        SRC 93.184.216.34:443    DST 203.0.113.9:62311   ← reply swaps halves
 ④ router ──▶ laptop      SRC 93.184.216.34:443    DST 192.168.1.5:51204   ← NAT reversed it
```

> **The two ends disagree about what the connection is — and nothing breaks.** The server's 4-tuple names
> `203.0.113.9:62311`; the laptop's names `192.168.1.5:51204`. Each end only has to be self-consistent.
> That is spine fact 3 (*a connection is state at its two endpoints*) doing real work, and it is the same
> permission that lets a load balancer terminate TLS and re-originate the request.

**NAT rewrites the port, not just the IP, and it must.** Two devices can easily pick the same ephemeral
source port; if only the IP were swapped, both connections would look identical from outside and the
replies would be indistinguishable. **The public port is the disambiguator.**

### The NAT table is state, and it expires

One row per active connection, written on the first outbound packet, read on every reply. **It is the only
thing in existence linking the internal device to the traffic the server sees** — lose it and every open
connection dies at once, with neither end told.

⚠️ **Rows are evicted after an idle timeout, often just a few minutes.** A silent connection has its row
dropped and the next packet is discarded. **This is why long-lived connections (WebSockets, DB pools) send
keepalives** — not to check liveness, but to stop a middlebox forgetting they exist. Debugging "the
connection works, then dies after five idle minutes" starts here.

### Why this is not just home-network trivia

**A VPC (Virtual Private Cloud) is the same shape.** App servers hold private addresses, talk to each other
directly with no NAT and no public exposure, and only the load balancer has a public address. *"Inside the
VPC"* means exactly what *"inside the house"* means above — which is why TLS termination at the LB with
plain HTTP to the backend is the common, cheap choice.

## 🤝 What TCP actually guarantees (and what it doesn't)

TCP is the layer that turns IP's "best effort, no promises" into something you can build on.

| Guarantee | How | Consequence |
|---|---|---|
| **Delivery** | receiver ACKs each byte range; sender retransmits what isn't ACKed | a lost packet costs you a *timeout*, not an error |
| **Ordering** | every byte has a sequence number; receiver reassembles | you never see data out of order — you just wait |
| **No duplicates** | sequence numbers let the receiver discard repeats | IP may duplicate freely; you never notice |
| **Flow control** | receiver advertises a *window* = "I have room for N more bytes" | a fast sender can't drown a slow receiver |
| **Congestion control** | sender backs off on packet loss (loss ≈ congestion signal) | TCP is *polite* — it deliberately slows down under strain |

**What TCP does NOT give you — each of these is a real design trap:**

- **Not "the other side processed it."** An ACK means the bytes reached the receiver's OS buffer. The
  application may crash before reading them. **Application-level acknowledgement is a separate thing
  you must design**, which is the whole reason message queues have explicit acks.
- **Not message boundaries.** See framing below.
- **Not timeliness.** TCP will happily spend 30 seconds retransmitting. Reliability is bought *with
  latency* — which is exactly the trade the next section is about.
- **Not security.** Anyone on the path reads it. That's TLS's job, not TCP's.

### ⚠️ Head-of-line blocking — the cost of ordering

Ordering is a guarantee with a bill. If packet #2 of 10 is lost, packets #3–10 may have already
arrived — but TCP **cannot** hand them to your application, because that would break ordering. They
sit in a buffer until #2 is retransmitted. **One lost packet stalls everything behind it.**

This is why HTTP/2, which multiplexes many requests over one TCP connection, still stalls *all* of
them on a single lost packet — and why **HTTP/3 abandoned TCP for QUIC on top of UDP**, so each stream
can advance independently.

## ⚖️ TCP vs UDP — the question is "is a late packet still worth anything?"

**UDP (User Datagram Protocol) is IP with ports bolted on and nothing else.** No handshake, no
retransmission, no ordering, no congestion control. You hand it a datagram; it tries once.

| | TCP | UDP |
|---|---|---|
| Setup cost | 1 RTT handshake | **zero** — first packet carries data |
| Lost data | retransmitted (adds latency) | **gone**, silently |
| Order | guaranteed | not guaranteed |
| Head-of-line blocking | yes | no |
| Congestion control | built in | you build it or you don't |
| Message boundaries | none (stream) | preserved (datagrams) |

**The decision rule, and it's one sentence:**

> **Ask whether a late packet is still valuable.** If yes → TCP; retransmission is a gift. If a late
> packet is *worthless* → UDP; the retransmission would arrive after you needed it and cost you
> latency for nothing.

- **Voice/video call** — a 200 ms-late audio frame is garbage; the conversation moved on. Drop it and
  keep going. UDP.
- **Live game state** — position update #47 is obsolete the moment #48 arrives. UDP.
- **File download, API call, database query** — every byte matters whenever it lands. TCP.
- **DNS** — one small request, one small answer, retrying is trivial and cheaper than a handshake. UDP
  (falls back to TCP for large responses).
- **QUIC / HTTP/3** — UDP underneath, then rebuilds reliability *per stream* in userspace, keeping
  TCP's guarantees without its head-of-line blocking. The point wasn't "UDP is faster"; it was
  "we want to choose our own reliability rules."

## 📏 Framing — TCP gives you a stream, not messages

TCP delivers an **ordered byte stream with no message boundaries**. `send()` calls do not map 1:1 to
`recv()` calls: one request can arrive split across three packets, and two requests can arrive in one.
So every protocol on top of TCP must frame itself. HTTP does it twice:

- **Headers** end at the first blank line (`\r\n\r\n`) — a *delimiter*.
- **Body** length comes from `Content-Length: N` — a **length prefix**, exactly the trick in
  [271 Encode and Decode Strings](../../../../dsa/leetcode/arrays_and_hash/271_encode_and_decode_string.py).
  When the length isn't known up front (streaming), `Transfer-Encoding: chunked` sends a length prefix
  per chunk and a `0` chunk to terminate.

> **Why it matters in design:** "the request is slow" and "the request never framed" look identical to
> a client. A truncated body with no `Content-Length` hangs until timeout rather than erroring — which
> is why timeouts are mandatory, not optional, on every network call.

---

# HTTP semantics — the four clusters that change an architecture

*Admitted to this card under one rule: **only if picking it differently changes an architecture.***

## ↪️ 301 vs 302 — who remembers the redirect

Both say "it's at a different URL." The difference is **who caches that fact.**

| | **301** Moved Permanently | **302** Found (temporary) |
|---|---|---|
| Client caches it | **yes — often indefinitely** | no |
| Your server sees later requests | **no — it's bypassed** | yes, every one |
| Load / latency after first hit | ~zero | one hop through you, always |
| Change the destination later | **effectively impossible** | instantly |
| Analytics on later clicks | blind | full |

> **This is not a detail — it decides whether a subsystem exists.** In a URL shortener, 301 means
> clicks bypass you and there is *nothing to log*; 302 means every click is a request you serve, which
> is the only reason a `ClickEvent` table can exist. Same product, different data model, because of a
> three-digit number.

⚠️ **A 301 is nearly impossible to retract.** It lives in browser caches you don't control; no deploy
reaches it. **Ship 302 first, confirm the target, harden to 301 only when certain.**

**Method preservation (the historical wart):** clients have long been allowed to turn a POST into a
GET when following 301/302. If the method must survive, use **308** (permanent) or **307** (temporary)
— same caching semantics, method preserved.

## 🃏 Recall Card (the rep)
*Answer each from memory before unfolding. Miss one → it's not 🟢.*

> ⚠️ **Covers the Aug 3 session + the Aug 8 addressing/NAT section.** The remaining HTTP clusters
> (`304`/`ETag`/`Cache-Control`, method idempotency, 429-vs-503-vs-500) are not yet written and are
> **not** on this card. Extend it when they land.
>
> 🛑 **This card has NOT been measured.** Aug 8's session was **teaching, unrated** — the learner asked to
> stop the blind sprint after Q1 (*"I'm a complete novice at this"*), which was the right call: rating a
> sprint on never-bootstrapped material measures the explanation, not retention. **The rated sprint needs
> a real gap after the teaching finishes.** Do not log a comfort rating off a session where the material
> was explained the same day.

<details><summary><b>1. Name the three layers of a normal web request and what each one is responsible for.</b></summary>

**IP** — gets packets to the right *machine*; best-effort, may drop/duplicate/reorder and never says so.
**TCP** — on top of IP, between *ports*; adds back delivery, ordering, dedup, flow and congestion control.
**HTTP** — text riding inside; assumes a working byte stream and says nothing about delivery.
Each layer treats the one above as opaque payload.
</details>

<details><summary><b>2. Over <code>https://example.com/secret</code>, what can a middlebox on the path see, and what can't it?</b></summary>

**Can see:** IP addresses, ports, packet sizes and timing, and **the hostname** (`example.com`) via TLS SNI, sent in the clear during the handshake. The DNS lookup leaked it a moment earlier too.
**Cannot see:** method, **path**, headers, body, cookies.
So HTTPS hides *what you asked for*, not *who you're talking to*.
</details>

<details><summary><b>3. "Stateless" vs "can't read" — why doesn't a router act on your URL path?</b></summary>

Because reading the IP header is its *job*, not because it's unable. Over plain HTTP the request text is in its buffer in the clear. Middleboxes read deeper all the time when you want them to — that's exactly what an L7 load balancer does.
</details>

<details><summary><b>4. What does "TLS termination" mean, and how can an L7 load balancer route by path if the path is encrypted?</b></summary>

**Terminate = be one of the two ends**, not "stop using TLS." The LB holds the cert and private key for the domain, so the client's TLS session ends *at the LB*. It decrypts, reads plaintext HTTP, routes on path, then opens a **separate** connection to the backend. Possible only because a connection is state at its two endpoints — anything with the keys can be an endpoint.
</details>

<details><summary><b>5. Name the three options for the LB→backend hop, and the tradeoff you must state out loud.</b></summary>

**Terminate** (plain HTTP inside a trusted VPC — cheapest, most common) · **Re-encrypt / bridging** (LB opens its own TLS to the backend — regulated or zero-trust) · **Passthrough** (LB never decrypts).
**The tradeoff:** passthrough gives end-to-end encryption but makes the box an **L4** balancer — it *cannot* route by path. You can't have both at the same box.
</details>

<details><summary><b>6. Cold start on <code>https://</code>: how many round trips before the first byte of HTTP leaves? Name them.</b></summary>

**3 RTTs** (TLS 1.3): DNS lookup (1) → TCP handshake (1) → TLS handshake (1). A 4th to get the first byte back. TLS 1.2 adds one more.
At 200 ms RTT (Sydney→Virginia) that's ~800 ms before any page content arrives, with your server code not yet run.
</details>

<details><summary><b>7. Latency vs bandwidth vs RTT — and why can't buying bandwidth fix a chatty API?</b></summary>

**Latency** = one-way delay · **RTT** = there and back (~2× latency) · **Bandwidth** = data per second once flowing.
They're independent. Handshakes wait on *distance*, not pipe width — a 10 Gbps link between Sydney and Virginia still has ~200 ms RTT. Many small requests = latency-bound → fix with fewer round trips (connection reuse, HTTP/2) or less distance (CDN). Few large transfers = bandwidth-bound → compress or shrink.
</details>

<details><summary><b>8. You ask one DNS question. Who does the walking, and what are the three tiers?</b></summary>

Your **recursive resolver** (ISP's by default, or `8.8.8.8`/`1.1.1.1`) does it. **Root** servers know where each TLD lives → **TLD servers** (`.com`) know which nameserver owns each domain → the **authoritative nameserver** holds the record. Every tier caches, so a real lookup is usually 1–2 RTTs, not 4.
</details>

<details><summary><b>9. You changed your DNS record 45 minutes ago and users still hit the old server. Why — and what's the correct migration procedure?</b></summary>

The old answer was cached with its **TTL** (say 3600s). Resolvers serve from memory until it expires; your change is live and irrelevant to them until then.
**Procedure:** (1) a day ahead, lower TTL 3600→60 — you must wait out the *old* TTL for that to take hold; (2) then flip the IP; (3) raise TTL back after.
Not always-60 because short TTLs mean constant re-queries: more load, more cache misses, a DNS RTT added back. Freshness vs traffic.
</details>

<details><summary><b>10. What identifies a TCP connection, and why can one server hold 100k connections on port 443?</b></summary>

The **4-tuple**: `(source IP, source port, dest IP, dest port)` — plus sequence-number state at each end, and nothing in the middle. The port isn't consumed; the *tuple* is, so distinct source ports make distinct connections.
</details>

<details><summary><b>10b. Name the three port bands. Which is the one every OS agrees on, and what does binding there require?</b></summary>

**0–1023 well-known** (HTTP 80 · HTTPS 443 · DNS 53 · SSH 22) — the universally agreed band; **on Unix-likes, binding requires root**. **1024–49151 registered** — vendor defaults (Postgres 5432, Redis 6379, Kafka 9092). **49152–65535 ephemeral** — throwaway source ports, but **OS-dependent**: Linux really uses 32768–60999.
Two consequences: apps run on **8080 behind a proxy holding 443** because of the root rule; and a machine tops out near **28k outbound connections to one destination**, since each needs its own source port.
</details>

<details><summary><b>10c. Your laptop is 192.168.1.5. What does the web server think your address is, and what single thing connects the two views?</b></summary>

The server sees the **router's public address and a public port it invented** — `203.0.113.9:62311`. Your laptop's own view is `192.168.1.5:51204`. **The two ends disagree about the connection's identity and nothing breaks**, because each end only has to be self-consistent (spine fact 3).
The **NAT table** in the router is the only record linking them: one row per connection, written outbound, read on every reply.
**NAT rewrites the port as well as the IP, and must** — two devices can pick the same ephemeral source port, so the public port is the disambiguator.
</details>

<details><summary><b>10d. A WebSocket sits idle for ten minutes and then stops working, with no error at either end. Why?</b></summary>

A **NAT (or firewall) table row was evicted on an idle timeout** — often just a few minutes. The mapping is gone, the next packet has nowhere to go, and it's discarded silently; neither end is told.
**That's why long-lived connections send keepalives** — not to test liveness, but to stop a middlebox forgetting they exist.
</details>

<details><summary><b>11. What does TCP guarantee — and name three things it does NOT.</b></summary>

**Guarantees:** delivery (retransmit un-ACKed), ordering (sequence numbers), no duplicates, flow control (receiver window), congestion control.
**Does not:** that the *application processed* it (an ACK means it reached the OS buffer — app-level acks are yours to design) · message boundaries · timeliness (it will retransmit for 30s rather than fail) · security.
</details>

<details><summary><b>12. What is head-of-line blocking, and why did HTTP/3 abandon TCP?</b></summary>

Ordering means a lost packet #2 blocks already-arrived packets #3–10 from being delivered — handing them over would break the ordering promise. One loss stalls everything behind it.
HTTP/2 multiplexes many requests over one TCP connection, so one lost packet stalls *all* of them. HTTP/3 runs QUIC on **UDP** and rebuilds reliability per-stream, so streams advance independently.
</details>

<details><summary><b>13. TCP or UDP — state the decision rule in one sentence, with an example each way.</b></summary>

**Is a late packet still worth anything?** Yes → TCP (retransmission is a gift). No → UDP (the retransmission arrives after you needed it, and you paid latency for nothing).
Voice/video, live game state → UDP. File download, API call, DB query → TCP. DNS → UDP (small, retry is cheaper than a handshake).
</details>

<details><summary><b>14. TCP hands you a byte stream with no message boundaries. How does HTTP know where a message ends?</b></summary>

Two mechanisms: headers end at the first blank line (`\r\n\r\n`) — a **delimiter**; the body length comes from `Content-Length: N` — a **length prefix** (same trick as LC 271). When the length isn't known up front, `Transfer-Encoding: chunked` sends a length prefix per chunk and a `0` chunk to end.
</details>

<details><summary><b>15. 301 vs 302 — which lets you keep click analytics, and why? What's the trap with the other one?</b></summary>

**302** (temporary) — not cached, so every click comes back through your server, which is the only reason a click-event log can exist. **301** (permanent) is cached by the client, often indefinitely, so later clicks bypass you entirely: cheap and fast, but blind and **effectively impossible to retract** — no deploy reaches a browser cache. Ship 302 first, harden to 301 only when certain. Use **307/308** if the HTTP method must be preserved.
</details>
