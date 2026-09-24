# LinkedIn copy — Sep 24, 2026

Paste-ready text matching the Sep 23 one-pager. Every claim here was confirmed in the Sep 23–24 resume
session; nothing is added beyond the resume except the Skills list, which carries the AI terms the
one-pager had no room for. Character limits are LinkedIn's as of 2026: Headline 220, About 2,600,
each Experience description 2,000, Skills 100 entries.

Before posting: Morgan Stanley's external-communications policy may restrict naming an internal
program (Finance Command Center), an internal user (the WM CFO), or pre-GA status. The sections below
name them because the resume does; drop them here if the policy says so.

---

## Headline (≤ 220 chars)

Senior Full-Stack Developer & Squad Lead @ Morgan Stanley | Shipping production LLM agents with real evals | Snowflake Cortex · FastAPI · React · .NET · ETL

---

## About (≤ 2,600 chars)

I build financial systems end to end, and lately that means LLM agents that finance leadership actually uses.

I lead the WM Finance slice of Finance Command Center at Morgan Stanley: a Snowflake platform, containerized with Podman and fronted by ReactJS/FastAPI, that reports Return on Assets and Assets under Management across ~$3 trillion in client assets to WM leadership and the CFO organization. It retired a manual, Excel-driven process.

On top of it sits a Snowflake Cortex AI agent. Eleven finance users, including the WM CFO, ask ROA and AUM questions in natural language instead of requesting reports. It runs on Semantic Views, Skills, and Dynamic Tables, with guardrails that decline out-of-scope and restricted-data questions.

What I care most about is that it ships behind real evals. I built the harness with guidance from Snowflake's FDEs: a 68-question golden set with reference SQL and expected figures, LLM-as-judge grading, and finance SME review. It re-runs on every semantic-model, Skill, or prompt change, and GA is gated on a 0.70 F1 score tuned for precision over recall plus 100% groundedness.

Before the agent work, nine years of the data plumbing underneath it:
• Integrated EquityZen's books into Morgan Stanley's general ledger, leading the squad and building the Teradata/Python journal-ingestion ETL with simulation and posting modes, plus reconciliation that brought every accounting break to zero before cutover.
• Built the Canadian extension of the ASP.NET FA Notes platform: loan lifecycle engine, Canadian regulatory and compensation rules, audit logging, and payroll, GL, and HR integrations.
• Decommissioned three acquired general ledgers (E*TRADE, Eaton Vance, Shareworks) with automated journal-ingestion pipelines and an audited, approval-gated C# posting tool.

I manage four engineers and own delivery for WM Financial Technology. Stack: Python, C#/.NET, TypeScript, SQL, ReactJS, FastAPI, Snowflake, Teradata, DB2, Podman.

---

## Experience

### Morgan Stanley — Senior Full-Stack Developer, Squad Lead
New York, NY · Oct 2023 – Present

Manages 4 engineers; delivery owner for WM Financial Technology.

Finance Command Center — WM Finance Cortex AI Agent (Snowflake)
• Retired a manual Excel-driven EUC process by designing and building a Podman-containerized ReactJS/FastAPI/Snowflake platform reporting Return on Assets (ROA) and Assets under Management (AUM) across ~$3 trillion in client assets to WM leadership and the CFO organization
• Layered a Snowflake Cortex Agent chat on the platform so 11 finance users, including the WM CFO, self-serve ROA and AUM questions in natural language instead of requesting reports — built on Semantic Views, Skills, and Dynamic Tables, with guardrails that decline out-of-scope and restricted-data questions
• Built the agent's eval harness with guidance from Snowflake FDEs: a 68-question golden set with reference SQL and expected figures, LLM-as-judge grading, and finance SME review — re-run on every semantic-model, Skill, or prompt change, with GA gated on a 0.70 F1 score tuned for precision over recall plus 100% groundedness

EquityZen Acquisition
• Led the squad integrating EquityZen's books into Morgan Stanley's general ledger — built the Teradata/Python journal-ingestion ETL on Autosys and the in-house framework with simulation and posting modes, plus Python reconciliation that reconciled every accounting break to zero before cutover
• Built a C# .NET WPF trial-balance application where Finance Controllers review the simulated EquityZen numbers and adjust account mappings before the ETL posts them to the GL

FA Notes System — Canadian Expansion (MSWC)
• Built the Canadian extension of the ASP.NET FA Notes platform — loan lifecycle engine, Canadian regulatory and compensation rules, audit logging, reporting feeds, and payroll, GL, and HR integrations — enabling MSWC's first Canadian FA Recruit onboarding

### Progressive Overflow — Owner & Developer
Remote · Apr 2023 – Sep 2023

• Designed an offline-first Flutter mobile app (BLoC state management) with local Realm persistence synced to MongoDB Atlas — works fully offline, changes reconciling automatically on reconnect

### Career Break
Mar 2022 – Apr 2023

Planned time off — self-directed study and open-source development, leading into Progressive Overflow.

### Morgan Stanley — Senior Full-Stack Developer
New York, NY · Mar 2017 – Mar 2022

• General Ledger Integration — Led GL decommissioning across three acquisitions — E*TRADE ($13B), Eaton Vance ($7B), Shareworks (~$900M) — building automated journal-ingestion pipelines in Teradata, Shell, and Python via Autosys and an in-house ETL framework, plus a C# .NET WPF migration tool with audited, approval-gated posting
• Manual Automation Delivery (MAD) — Eliminated a recurring monthly EUC process across fees and billing, automating tens of thousands of journal entries per month and replacing hundreds of hours of manual Operations effort with structured logging, persistent archival, and completion/failure notifications
• Retail Inventory Application (RETINA) — Delivered a C# .NET WPF (MVVM) hub for inventory maintenance, approval-gated position adjustments, and finance reporting (~15 daily users), backed by DB2 stored procedures computing real-time Balance Sheet and P&L positions at near-zero latency

---

## Education

Stony Brook University — B.S. Computer Science & Applied Mathematics and Statistics · Dec 2016 · Dean's List (4 semesters)

---

## Skills (order matters: LinkedIn shows the top three on the profile card)

AI / LLM (the terms the one-pager has no room for; each is backed by the Finance Command Center bullets)
1. LLM Agents
2. LLM Evaluation (LLM-as-judge, golden sets)
3. Snowflake Cortex
4. AI Guardrails
5. Semantic Layer Design (Semantic Views, Dynamic Tables)

Languages
6. Python · 7. C# · 8. TypeScript · 9. SQL · 10. Java · 11. Shell

Frameworks & tools
12. FastAPI · 13. ReactJS · 14. .NET · 15. ASP.NET · 16. WPF · 17. Node.js · 18. Flutter · 19. Podman

Data & cloud
20. Snowflake · 21. Teradata · 22. DB2 · 23. MongoDB · 24. AWS · 25. Autosys · 26. Git

Domain & practices
27. ETL Pipeline Design · 28. General Ledger Integration · 29. Financial Reconciliation · 30. Agile/Scrum · 31. CI/CD · 32. MVVM · 33. Trunk-Based Development · 34. Engineering Management

Not listed on purpose: RAG, LangChain, vector databases — the agent runs on Snowflake's semantic layer, not a retrieval stack, and nothing in the session backs those terms.
