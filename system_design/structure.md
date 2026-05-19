```text
system_design/
│
├── 01_fundamentals/          # Core concepts and horizontal scaling rules
│   ├── scale_vs_efficiency.md
│   ├── load_balancing.md
│   └── replication_vs_sharding.md
│
├── 02_components/            # Deep-dives into individual system blocks
│   ├── api_gateway.md
│   ├── rate_limiter.md       <--- (Connects to Block 7: Communication)
│   ├── distributed_cache.md  <--- (Connects to Block 6: Storage)
│   └── message_queues.md
│
├── 03_databases/             # Understanding data models and trade-offs
│   ├── relational_sql.md
│   ├── nosql_key_value.md
│   └── vector_databases.md   <--- (Connects to Phase 3: AI Engineering)
│
├── 04_case_studies/          # Putting components together for real apps
│   ├── tinyurl_design.md
│   ├── notification_service.md
│   └── raw_video_streaming.md
│
└── 05_architectural_templates/ # Blank templates to fill out during practice
    ├── micro_system_template.md
    └── macro_system_template.md
