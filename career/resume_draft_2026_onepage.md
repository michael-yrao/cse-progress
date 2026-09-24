# MICHAEL RAO
(646) 240-1135 | yao.michael.rao@gmail.com | New York, NY

---

## SUMMARY

Senior full-stack developer and squad lead shipping production LLM agents. Leads WM Finance's slice of Finance Command Center, a Snowflake Cortex AI agent gated by a golden set, LLM-as-judge grading, and a precision-weighted F1 score. 9+ years at Morgan Stanley building the reporting platforms and ETL it runs on.


---

## SKILLS

**Languages:** C#, Python, Java, TypeScript, SQL, Shell
**Frameworks & Tools:** .NET, ReactJS, Node.js, FastAPI, Podman, Flutter, WPF, ASP.NET
**Data & Cloud:** Snowflake, DB2, Teradata, MongoDB, AWS, Autosys, Git
**Practices:** Agile/Scrum, CI/CD, MVVM, ETL pipeline design, trunk-based development

---

## EXPERIENCE

### Morgan Stanley — Senior Full-Stack Developer, Squad Lead
New York, NY | Oct 2023 – Present · *Manages 4 engineers; delivery owner for WM Financial Technology.*

**Finance Command Center — WM Finance Cortex AI Agent (Snowflake)**
- Retired manual Excel-driven EUC process by designing and building a Podman-containerized ReactJS/FastAPI/Snowflake platform reporting Return on Assets (ROA) and Assets under Management (AUM) across ~$3 trillion in client assets to WM leadership and the CFO organization <!-- METRIC: add one shipped number if any — e.g. "eliminating N monthly EUCs" / "adopted by N leaders" / "cutting reporting turnaround from X to Y" -->
- Layered a Snowflake Cortex Agent chat on the platform so 11 finance users, including the WM CFO, self-serve ROA and AUM questions in natural language instead of requesting reports — built on Semantic Views, Skills, and Dynamic Tables, with guardrails that decline out-of-scope and restricted-data questions <!-- swap "Piloting" -> "Delivered" once GA -->
- Built the agent's eval harness with guidance from Snowflake FDEs: a 68-question golden set with reference SQL and expected figures, LLM-as-judge grading, and finance SME review — re-run on every semantic-model, Skill, or prompt change, with GA gated on a 0.70 F1 Score tuned for precision over recall plus 100% groundedness

**EquityZen Acquisition**
- Led the squad integrating EquityZen's books into Morgan Stanley's general ledger — built the Teradata/Python journal-ingestion ETL on Autosys and the in-house framework with simulation and posting modes, plus Python reconciliation that reconciled every accounting break to zero before cutover
- Built a C# .NET WPF trial-balance application where Finance Controllers review the simulated EquityZen numbers and adjust account mappings before the ETL posts them to the GL

**FA Notes System — Canadian Expansion (MSWC)**
- Built the Canadian extension of the ASP.NET FA Notes platform — loan lifecycle engine, Canadian regulatory and compensation rules, audit logging, and reporting feeds — enabling MSWC's first Canadian FA Recruit onboarding

### Progressive Overflow — Owner & Developer
Remote | Apr 2023 – Sep 2023

- Designed an offline-first Flutter mobile app (BLoC state management) with local Realm persistence synced to MongoDB Atlas — works fully offline, changes reconciling automatically on reconnect

### Career Break
Mar 2022 – Apr 2023 · *Planned time off — self-directed study and open-source development, leading into Progressive Overflow*

### Morgan Stanley — Senior Full-Stack Developer
New York, NY | Mar 2017 – Mar 2022

- **General Ledger Integration** — Led GL decommissioning across three acquisitions — E*TRADE ($13B), Eaton Vance ($7B), Shareworks (~$900M) — building automated journal-ingestion pipelines in Teradata, Shell, and Python via Autosys and an in-house ETL framework, plus a C# .NET WPF migration tool with audited, approval-gated posting
- **Manual Automation Delivery (MAD)** — Eliminated a recurring monthly EUC process across fees and billing, automating tens of thousands of journal entries per month and replacing hundreds of hours of manual Operations effort with structured logging, persistent archival, and completion/failure notifications
- **Retail Inventory Application (RETINA)** — Delivered a C# .NET WPF (MVVM) hub for inventory maintenance, approval-gated position adjustments, and finance reporting (~15 daily users), backed by DB2 stored procedures computing real-time Balance Sheet and P&L positions at near-zero latency

---

## EDUCATION

**B.S. Computer Science & Applied Mathematics and Statistics** — Stony Brook University | Dec 2016 · Dean's List (4 semesters)
