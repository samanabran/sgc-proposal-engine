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

| 11 | Multi-source lead capture (portals, direct, referral) into one CRM, framed against the recurring cost of per-lead portal charges — client is frustrated that paid leads scatter across sources with nothing forcing a controlled pipeline | User-supplied context, 2026-08-06, plus `document:Talha's Meeting Notes_otter_ai_transcript.txt` (a recorded, two-speaker walkthrough — CRM lead-stage restrictions, agent performance dashboard, e-learning, commission/KYC-AML workflow, multi-company/Lebanon, AI assistant) | PRICED (partial) — the underlying centralized-CRM-with-stage-gating capability is already base scope (`crm_leads`, `users_roles_agent_perf`, priced in the passed Rev1 worksheet). Automated portal-side lead capture (Property Finder / Bayut sync) is DEFERRED — Phase 2, `phase2-catalogue.yaml` (`portal_sync_property_finder` AED 3,900, `portal_sync_bayut_dubizzle` AED 3,400 one-time), conditional on the 5 client-side preconditions in `portal_dependency_note` |
| 12 | Agent performance dashboard/leaderboard, e-learning/onboarding LMS, commission calculation + clawback engine, KYC/AML automated workflow gating commission release, multi-company/multi-branch (incl. Lebanon), Outlook/Gmail sync, conversational AI assistant ("SGC AI Brain") | `document:Talha's Meeting Notes_otter_ai_transcript.txt` (full transcript, same identity caveat as #11 below) | **NOT APPLIED, omitted entirely from Rev2 by explicit user instruction (2026-08-06)** — "no need to scope all in the proposal, only the priorities." Commission engine and KYC/AML automation additionally have **no priceable basis anywhere in this repo's knowledge layer** — `financing-amortization.md` confirms no commission/sales-comp-plan document exists in this repo at all (same open item already flagged in `phase2-catalogue.yaml`'s `commission_impact` note). Not to be silently reintroduced into a future revision without a real scoping/pricing exercise first |

| 13 | Migration timeline verbally quoted: "24 hours if organized... three days, four days" if data is messy | `document:Talha's Meeting Notes_otter_ai_transcript.txt:299` (organized, ~24h) and `:305` (messy, 3-4 days) | **Logged as unpriced verbal exposure, 2026-08-07 — distinct from and in addition to the documentary scope exclusion.** Migration (`data_migration_500`) is excluded from the quoted scope (config ii) because the client's own written requirements document never asks for it — that exclusion basis stands independently. This entry exists because a verbal timeline commitment was separately made on the call regardless of what's priced; if migration is ever added back into scope, this timeline was already floated to the client and should be reconciled against, not silently superseded |
| 14 | AI capability demonstrated live: "AI brain" sales-performance/financial-summary generation, API-key-based AI configuration, and a Telegram bot creating CRM leads from natural-language messages | `document:Talha's Meeting Notes_otter_ai_transcript.txt:353` (API keys), `:359` (AI brain demo), `:365` (Telegram lead-creation demo, timestamp 27:05) | **NOT APPLIED — AI capability and AI usage credits excluded explicitly from the Rev3 offer, 2026-08-07.** No equivalent priceable item exists for this specific demonstrated capability (closest catalogue analog remains `ai_lead_scorer_lite`/`standard`, already noted in row 6 as a different capability). Logged as demo exposure per the same discipline as row 12/Commission Tracking — a live demonstration is not an implied inclusion, and the offer states this directly rather than leaving it to be discovered later |

## Portal Sync correction, 2026-08-06 — logged as previously scoped

**Finding (established in the 2026-08-06 scope-reconciliation pass, not
repeated here in full — see `manifest.yaml`'s Rev2 entry and item 5 of
that pass)**: the client's own requirements document lists "Portal
Tracking" as **Nice to Have** (§6), describing passive visibility of
where a listing was posted (Property Finder, Bayut, Dubizzle, website,
social media) — a tracking field. Rev2
(`03-draft/PRO-2026-SUB-01_Rev2/`) led with the catalogued **Portal
Sync** add-on (AED 3,900 + 3,400, an active bi-directional feed/API
integration per `phase2-catalogue.yaml`'s own `portal_dependency_note`)
as the headline priority. That overstates what was actually asked for —
a materially larger, differently-scoped capability positioned as the
answer to a Nice to Have tracking request.

**Correction, logged formally**: Portal Sync must not lead any future
revision of this proposal. If offered at all, it stays a disclosed,
Phase 2, opt-in add-on — not the headline. Rev2's existing draft file is
NOT edited in this pass (no client-facing draft work authorized this
pass beyond the answered question form, see manifest.yaml) — this entry
exists so the correction is on record before Rev2 is ever touched again,
not as a substitute for actually fixing the draft.

## Identity correction, 2026-08-06 — "Talha's Meeting Notes" transcript

**Corrected**: `00-intake/_source-documents/email-2026-07-27_rejection_fwd-2026-07-28.eml`
proves **Talha Sheraz is SGC's own Business Development Executive** (both
client replies open "Dear Talha," his own signature confirms the title) —
**not a Prosper contact**. `risk-assessment.yaml`'s "assigned to Talha
2026-07-01" note was always correctly read as CRM-lead-ownership (an SGC
rep assigned to the deal), and rows #11/#12 above never asserted Talha
was client-side — but "assigned to Talha" is now a **confirmed** basis
for treating a transcript titled "Talha's Meeting Notes" as plausibly his
own recording of a Prosper meeting (he owns this account), not merely a
phonetic-name coincidence. Tightened above accordingly.

**Not corrected, because the evidence doesn't support it either way**:
whether "Speaker 1" *within* that transcript (the second, non-Talha
voice — asking about Lebanon expansion, "our CEO's goal," accounts/KYC,
Outlook integration, "we are commission based") is Dian Sajulga or
another SGC colleague. The rejection email establishes who Talha is; it
says nothing about who Speaker 1 is in a separate document. Speaker 1's
content (idiosyncratic operational specifics: a named expansion market,
an internal headcount band, a compensation structure) reads more like
genuine client disclosure than an internal rehearsal script — unlike the
*other*, already-logged 2026-07-17 transcript, which self-declares in
its own header "internal rehearsal... not present: any Prosper
representative." That distinction is a real basis for treating this
transcript as more likely genuinely client-present, not less — but it
remains an inference, not a confirmed fact, and is left exactly that
hedged rather than flipped to "internal notes" on the strength of a
finding (who Talha is) that doesn't bear on the question (who Speaker 1
is).

**What rested on this**: only `manifest.yaml`'s Rev2 revision entry and
rows #11/#12 above — checked, neither the Rev2 draft prose
(`03-draft/PRO-2026-SUB-01_Rev2/`) nor its rendered HTML names "Talha"
anywhere, so nothing client-facing was built on the identity question
either way. `deal-card.md` and `HANDOVER.md` do not mention "Talha" at
all (checked 2026-08-06) — nothing to correct in either file.

## Cross-reference note

Item #9's underlying use case (agents updating leads and logging visits
from mobile) is genuinely covered by this proposal via responsive browser
access — the earlier document's specific technical framing ("native app")
is not literally true under Community edition, but the capability the
client actually needs is delivered. Worth a quick, low-drama mention if
the client ever specifically asks whether it's an installable app, per
`deal-card.md`.
