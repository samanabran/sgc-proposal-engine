# The 12 Commercial Rules

Source: `commercial-pricing-revised-v2.xlsx`, sheet "Commercial Rules"
(unchanged across the v1 → v2 pricing revision — see `CHANGELOG.md`).
These apply across every segment. Discount and segment selection do not
waive them.

| # | Rule | Note |
|---|---|---|
| 1 | Implementation always calculated before discount. | Full effort-based price first, then discount line. |
| 2 | Discount never changes estimated hours. | Hours = genuine effort, fixed. |
| 3 | Hours must remain auditable. | Every hour traces to task × module × complexity in the service catalog (`pricing/hour-lookup.yaml`). |
| 4 | Every custom feature includes documentation hours. | No dev item shipped without docs. |
| 5 | Every development includes QA. | QA = % of dev effort, never waived. |
| 6 | Every implementation includes PM. | 15% standard, 10% Startup segment. |
| 7 | Startup segment = AED 280/hr revised (was 300/hr at L0). | PM 10%, contingency 5%. |
| 8 | Training billed once. | No overhead percentage stacked on top. |
| 9 | Every proposal includes assumptions. | Protects both SGC and client. |
| 10 | Every proposal includes exclusions. | No expectation gaps, no scope creep. |
| 11 | Every proposal generates a professional quotation. | Standalone PDF + commercial summary. |
| 12 | Every proposal generates a commercial summary. | One-page financial overview attached. |

These 12 rules are the constitution; `subscription-guardrails.md` (G1–G10)
is how they get enforced mechanically against a specific worksheet.
