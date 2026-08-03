# Verbal Promises

Every item raised on the 2026-06-10 discovery call, classified PRICED
(in Phase 1 build) / DEFERRED (Phase 2, priced separately) / EXCLUDED
(written exclusion required). See `known-defects.md` #5 for what happens
when items like these are sold with zero hours allocated instead.

| Date | Item | Classification | Where it's reflected |
|---|---|---|---|
| 2026-06-10 | Adoption is the deal-breaker — must be addressed directly, not implied | **PRICED** | `clause-library/adoption.md` in §09, named data-entry owner + day-30/day-60 checkpoint |
| 2026-06-10 | Property listing/tenancy register, tenancy/contract renewal reminders, invoicing tied to TRN, maintenance-request-to-invoice | **PRICED** | §06 work packages: `property_unit_register`, `tenancies_contracts_reminders`, `invoicing_trn`, `maintenance_invoice_from_request` |
| 2026-06-10 | Agent performance visibility (who's actually closing) | **PRICED** — folded into `crm_leads` + `reports_dashboard` work packages | §06 |
| 2026-06-10 | Portal sync to Property Finder, Bayut, and Dubizzle | **DEFERRED** — Phase 2, priced separately, each with the portal dependency checklist | §07, `phase2-catalogue.yaml: portal_sync_property_finder`, `portal_sync_bayut_dubizzle` |
| 2026-06-10 | Website "contact us" lead capture | **DEFERRED** — Phase 2, priced separately | §07, `phase2-catalogue.yaml: website_lead_capture` |
| 2026-06-10 | Mobile access | **PRICED, but scoped honestly** — mobile-optimised browser access, included on Community edition; **NOT** a dedicated iOS/Android app (`clause-library/edition-and-upgrades.md`) | §06 edition disclosure |

No promise was made regarding a specific discount depth, a guaranteed
go-live date beyond the milestone plan in §08, or any scope beyond what's
listed above.
