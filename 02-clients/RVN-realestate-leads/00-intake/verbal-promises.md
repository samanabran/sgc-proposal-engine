# Verbal Promises Log — RVN

Logged from the discovery call transcript/summary (source files file-dated
2026-08-15; see `client-brief.yaml: notes` for the call-date caveat). Each
entry marked PRICED / DEFERRED / EXCLUDED per SKILL.md §Stage 1.

| # | Promise (transcript ref) | Status | Notes |
|---|---|---|---|
| 1 | CRM demo tailored to RVN's workflows, delivered Monday (17:23-18:33; summary Action Items) | PRICED | Demo prep is pre-sales cost, not a billed line; covered by the draft's §01-§13 render and `monday-meeting-flow.md`. |
| 2 | Pricing/quotation delivered Monday, before/at the onsite meeting (13:43-14:39, 18:13-18:33) | PRICED | This worksheet + gate report + draft satisfy the commitment; quotation content is Option A / Option B per `02-calc/pricing-worksheet.yaml`. |
| 3 | Lead auto-distribution from Google Sheet into CRM, plus one-click manual assignment (15:17-15:56) | PRICED | Covered under `crm_leads` work package, Phase 1. |
| 4 | Manual call-outcome logging: answered / not answered / follow-up flag / conversation notes (09:31-10:34) | PRICED | Native Odoo Community CRM "Log an Activity" (Call type) functionality, covered under `crm_leads` work package. Manual entry by agents, not automated capture. |
| 5 | Reporting dashboard showing logged call activity vs. the stated 250-calls/agent/day target (06:59-08:39) | PRICED | Covered under `reports_dashboard` work package. Aggregates manually logged activity; does not auto-capture call events. |
| 6 | Automated call-analyzer / telephony integration for auto-captured call volume and pickup rate (06:59-07:37, 08:21-08:39, 12:03-12:34) | DEFERRED | No catalogue entry exists for telephony/dialer integration (see `client-brief.yaml: escalated_uncatalogued_requests`). Excluded from Phase 1 pricing. Logged as an open item requiring Commercial Desk scoping once RVN's phone/telephony stack is confirmed. Do NOT present as included or as a Phase 2 catalogue price — no catalogue price exists. |
| 7 | Attendance tracking: check-in/check-out and break times via RVN's existing sensor/badge system (10:34-11:45) | DEFERRED | No catalogue entry for third-party sensor/badge integration (see `client-brief.yaml: escalated_uncatalogued_requests`). Excluded from Phase 1 pricing pending sensor vendor/API identification. |
| 8 | Migration of existing Google Sheet lead records into the CRM (implied throughout; explicit at 15:17-15:31) | PRICED | Covered under `data_migration_500` + `migration_record_validation_signoff` work packages. Exact record count not confirmed on the call — flagged in `client-brief.yaml: scope_signals.migration_records` for verification before build kickoff. |
| 9 | No billing/invoicing functionality wanted (17:44-17:57) | EXCLUDED | Confirmed exclusion, not a gap. Odoo Community's invoicing app is available but out of scope for this build — do not include or bill for it. |
| 10 | CRM restricted to sales/telesales team + brokers (6-7 users); marketing team and the two owners excluded from CRM use (05:06-05:38) | PRICED | Sizing basis for `users_now: 7` in the worksheet. Owners are decision-makers, not licensed CRM seats. |
| 11 | Portal integrations (Property Finder, Bayut, Dubizzle) | EXCLUDED | Not requested on this call — leads come from Meta/Google Ads into Sheets, not a portal feed. Not included in Phase 1 or Phase 2 scope for this proposal; would require a separate scoping conversation if raised later. |
| 12 | Implementation target: September 2026 | DEFERRED | Contingent on Nazim's approval post-Monday demo — stated as a target, not a committed go-live date. Reflected in §13 Next Steps as a target, not a guarantee. |
| 13 | Follow-up decision meeting with Nazim + at least two other stakeholders, after Monday (summary Action Items) | PRICED | Reflected as the explicit close-the-loop ask in `monday-meeting-flow.md`. |

## Assumptions flagged for verification (not verbal promises, but load-bearing for pricing)

- `jurisdiction: mainland` — inferred from Burjuman Business Towers location, not confirmed by the client.
- `client_legal_name` — not stated on the call; "RVN" used as the working name throughout this client folder.
- Exact Google Sheet record count for migration — 400-600/month volume stated, but no total backlog count given; `data_migration_500` used as the nearest catalogue band.
- Entity age, VAT registration status, and trade licence validity — unknown, conservative assumptions used in `02-calc/risk-assessment.yaml`, flagged there for confirmation before issue.
