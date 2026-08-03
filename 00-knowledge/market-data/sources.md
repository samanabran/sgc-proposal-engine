# Sources

Every benchmark in `benchmarks.yaml` traces to one of these two documents,
archived in `_source-documents/`. Refresh external figures before public
release or use in a major enterprise tender — see the Research Standards
Note in the pricing playbook.

| Ref | Source | Date | Status |
|---|---|---|---|
| Commercial rate card | `commercial-pricing-revised-v2.xlsx` ("SGC-TECH-AI-Commercial-Export-v2_REVISED.xlsx") | v1→v2 revision, 22 Jul 2026 | VERIFIED — internal, current operating pricing |
| Pricing & proposal playbook | "Odoo Implementation Pricing Strategy, Proposal Architecture, and Market Benchmarks for Dubai & the Middle East (2025–2026)" | v1.0, 18 Jul 2026 | Mixed — see per-claim labels below |
| [S1] | Odoo official partner directory, UAE | live snapshot 18 Jul 2026 | VERIFIED |
| [S2] | Odoo official partner directory, Saudi Arabia | live snapshot 18 Jul 2026 | VERIFIED |
| [S3]–[S6] | Odoo official partner directory, Qatar/Bahrain/Oman/Kuwait | live snapshot 18 Jul 2026 | VERIFIED |
| [S11] | Singapore SMB Odoo implementation pricing references | 2025–2026 | MARKET BENCHMARK |
| [S12] | Australia SME Odoo implementation pricing references | 2025–2026 | MARKET BENCHMARK |
| [S13] | United States Odoo implementation pricing references | 2025–2026 | MARKET BENCHMARK |
| [S14] | Europe Odoo implementation pricing references | 2025–2026 | MARKET BENCHMARK |
| [S15] | Cross-region consultant hourly-rate references | 2025–2026 | MARKET BENCHMARK |
| [S16] | SGCTECH.AI field brief + playbook synthesis (UAE quote variance, compliance cost drivers, industry pricing bands) | 2025–2026 | MARKET BENCHMARK |
| [S17] | Post-go-live support/maintenance revenue-share references | 2025–2026 | MARKET BENCHMARK |

## Update checklist

Before quoting any figure from `benchmarks.yaml` in a client-facing
document, or before a knowledge-layer version bump that touches
`market-data/`:

1. Confirm the source document is still the latest revision (check
   `CHANGELOG.md`).
2. For VERIFIED partner-directory figures: these are point-in-time
   snapshots and drift over months, not days — re-verify if the cited date
   is more than one quarter old.
3. For MARKET BENCHMARK figures: treat as directional, not contractual. Do
   not present a MARKET BENCHMARK number to a client as if it were VERIFIED.
4. Log any correction as a new `CHANGELOG.md` entry, not a silent edit.
