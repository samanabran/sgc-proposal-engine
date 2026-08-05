# Verbal Promises Log — Prosper Intl Real Estate

Logged same-day per runbook §1. Each entry marked PRICED / DEFERRED /
EXCLUDED / NOT APPLIED.

| # | Promise / statement | Source | Classification |
|---|---|---|---|
| 1 | Field customization, no-extra-cost lead management, multiple admins with role-based access | CRM `x_bant_need` | PRICED — base scope: `crm_leads`, `users_roles_agent_perf` work packages |
| 2 | Listings/property register, tenancy tracking | Prior PRJ doc §07 (deferred there to its own Phase 2); reasonable core need for this vertical | PRICED — `property_unit_register`, `tenancies_contracts_reminders` included in base scope, consistent with the same vertical baseline (real-estate-brokerage-uae) established for Kallat, independent of the prior document's own phasing choice |
| 3 | Basic accounts/invoicing capability | CRM `x_bant_need` ("accounts integration"), prior PRJ doc | PRICED (partial) — `invoicing_trn` covers TRN-compliant invoicing only. Does **not** cover payroll or salary structure — see #5 |
| 4 | Sales agent check-in/check-out (attendance tracking, geolocation) | CRM `x_bant_need`; rehearsed in `call-transcript-2026-07-17-internal-demo-prep.md` | **NOT APPLIED — no priceable basis.** No HR/attendance work package exists anywhere in `hour-lookup.yaml`'s real-estate-brokerage-uae v2 catalogue (property/CRM/invoicing domains only). Escalate before ever quoting a delivery date or fee for this — do not estimate by analogy, per hour-lookup.yaml's own rule |
| 5 | Payroll / salary structure / WPS bulk submission | CRM `x_bant_need` ("including salary structure as well"); rehearsed in the same demo-prep call | **NOT APPLIED — no priceable basis.** Not in `hour-lookup.yaml` or `phase2-catalogue.yaml`. The prior PRJ doc itself placed this under its own unpriced Phase 3 ("custom quote... no price today") — independently reaching the same conclusion this repo's catalogue gap forces |
| 6 | ChatGPT/Copilot-style AI assistant | CRM `x_bant_need` | **NOT APPLIED — no equivalent priceable item.** Closest catalogue analog is `ai_lead_scorer_lite`/`ai_lead_scorer_standard` (lead scoring/matching/digest, Phase 2, from AED 495/mo) — a different capability from a conversational assistant. Not to be conflated or substituted silently in the draft |
| 7 | WhatsApp Business integration | Prior PRJ doc §08 | DEFERRED — same conclusion as Kallat: not in `phase2-catalogue.yaml` or `hour-lookup.yaml`, no priceable basis, escalate before quoting |
| 8 | Portal integration (Property Finder / Bayut) | Prior PRJ doc §08 | DEFERRED — Phase 2, `phase2-catalogue.yaml` (`portal_sync_property_finder` AED 3,900, `portal_sync_bayut_dubizzle` AED 3,400), conditional on the same 5 unconfirmed preconditions flagged for Kallat |
| 9 | **Native iOS/Android mobile app** ("Native Odoo app for updating leads and logging visits") | Prior PRJ doc §07, presented as a Phase 1 deliverable | **PRICED (equivalent capability)** — Community edition excludes `official_mobile_app` (`editions.yaml`), but delivers the same underlying use case (update leads, log visits, from any phone) via a fully responsive mobile-optimised browser experience, no install required. Presented in §07 as the mobile-access capability of this proposal, not framed as a gap against the prior document — 2026-08-05 user decision: keep Community, describe the browser experience on its own terms rather than as a shortfall |
| 10 | Payroll/commission engine, full accounting, board-ready BI | Prior PRJ doc §09 (its own unpriced Phase 3) | EXCLUDED — same conclusion independently reached via this repo's catalogue (no basis), consistent with the prior document's own phasing |

## Cross-reference note

Item #9's underlying use case (agents updating leads and logging visits
from mobile) is genuinely covered by this proposal via responsive browser
access — the earlier document's specific technical framing ("native app")
is not literally true under Community edition, but the capability the
client actually needs is delivered. Worth a quick, low-drama mention if
the client ever specifically asks whether it's an installable app, per
`deal-card.md`.
