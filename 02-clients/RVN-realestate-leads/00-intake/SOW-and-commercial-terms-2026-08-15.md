# RVN — SOW & Commercial Terms (internal/reviewable draft)

**Rule 0 — Provenance**: `02-clients/RVN-realestate-leads/` (the folder name in this repo — no folder named exactly `RVN` exists) is **untracked in git** as of this session's start (`git status --short` showed `??`); it was created earlier this session by copying `_SCAFFOLD` and running the pipeline, then committed later in this session at `e2d6a1f` and further modified in `a143c85`. It is not one of the four pre-existing draft clients (KP, MRD, PRO, VGE). I can verify this from the repo directly — not inferred.

**Rule 1 note**: this repo has no `sgc.pricing.activity`, `sgc.pricing.unpriced.request`, or `sgc.pricing.retainer` model — confirmed multiple times this session (`git cat-file` on every cited commit hash fails; no such object anywhere in this checkout; see `PROPOSAL_PRICING_CODE_INVENTORY.md`, committed `a143c85`). The real catalogue is `00-knowledge/pricing/*.yaml` (`hour-lookup.yaml`, `rate-card.yaml`, `policy.yaml`, `payment-plans.yaml`, `phase2-catalogue.yaml`) plus `02-calc/pricing-worksheet.yaml` for this deal. Every figure below is traced to those files. Anything with no catalogue row is marked **[UNPRICED — Commercial Desk]**, not a number.

---

## G23 report

Margin floor is 25% (absolute), 30% target. Checked against `02-calc/pricing-worksheet.yaml`:

- **Option A** (12mo, revenue AED 29,367 vs cost AED 18,583 = internal_build_cost 7,351 + CTS 936×12): **36.7% — PASS**, cushion 18.52% before breach.
- **Option B** (24mo, revenue AED 45,378 vs cost AED 29,815): **34.3% — PASS**, cushion 14.14% before breach.

**No row breaches the floor at the current (unvalidated) cost basis.** Both cushions were verified and reported to the user earlier this session (`00-intake/audit-2026-08-15-part3.md`, section C) — the passing result assumes salary is the entire cost of employment and 96% utilisation, which does not hold for a UAE FZCO with visas, medical cover, gratuity and leave. No burden figure is invented here; flagged as a real open question, not resolved.

---

## Unpriced-item routing list

| Item | Requirement | Reason unpriced | Routing |
|---|---|---|---|
| Automated call-analyzer / telephony integration | R7/R8 (automated capture) | No catalogue row in `hour-lookup.yaml`/`saas-modules.yaml`; blocked on C1 (device/PBX decision) | **[UNPRICED — Commercial Desk]** |
| Sensor/badge attendance API integration | R9 | No catalogue row; vendor/API unknown (C2) | **[UNPRICED — Commercial Desk]** |
| WhatsApp Business API (BSP) | C3 | Third-party pass-through cost (per-conversation + template pre-approval + Meta business verification); no BSP entry anywhere in the knowledge base | **[UNPRICED — Commercial Desk]**, third-party, not SGC margin |
| Push-notification-with-latency-SLA | R2 disclosure | No catalogue entry for a guaranteed-latency push capability | **[UNPRICED — Commercial Desk]** (not required for R2's baseline — see below) |
| Staged/multi-installment milestone billing | Option A payment structure | `payment-plans.yaml: milestone_or_usage`, `treatment: escalate, approval: sales_leadership` | **Not routed** — no ticketing/desk mechanism exists in this repo to route it to. Presenting **single-payment-at-kickoff** instead (see Option A below), stated plainly on the document face. |

---

## Requirements register (verified against transcript, corrections noted)

| Ref | Requirement | Timestamp | Disposition | Notes |
|---|---|---|---|---|
| R1 | Meta + Google Ads lead capture (currently → Google Sheets) | 01:24 | IN-SCOPE-V1 | |
| R2 | WhatsApp instant-lead notification today; CRM's day-one replacement is in-app, on-refresh — **not** a push alert with a stated latency | 02:11 | IN-SCOPE-V1 (disclosure register) | Same "state the limitation in the client's favour" pattern as C1/C2/C3 — see §06 below |
| R3 | Automatic lead distribution + one-click manual reassignment | 15:17, 15:55 | IN-SCOPE-V1 | |
| R4 | Per-lead status, remarks, follow-up state | 03:29–04:26 | IN-SCOPE-V1 | |
| R5 | Volume — **see C-A below, resolved to 500–600/month** | 04:34 | IN-SCOPE-V1 (sizing input only) | |
| R6 | 6–7 sales users (telesales + brokers), marketing/owners excluded | 04:46–06:04 | IN-SCOPE-V1 | |
| R7 | Call logging: dialled/day, answered/not, time, disposition, notes | 07:00–10:34, 18:04 | IN-SCOPE-V1, **manual entry only (C1)** — see Judgement Call below | |
| R8 | 250 calls/day/agent target *enforcement* | 07:22, 12:12 | **Reclassified (C1) — see Judgement Call.** Manual self-entry delivers *self-reporting*, not *enforcement*. | |
| R9 | Attendance sensor integration | 10:44–11:45 | DISCOVERY — no catalogue row for the fallback either (C2) | |
| R10 | Daily reporting, replacing the WhatsApp group format | 08:21 | IN-SCOPE-V1 | |

---

## Mandatory judgement call (stated here, in the document body, not only internally)

**If C1 resolves to mixed iOS/Android handsets with no company devices issued, R7 and R8 cannot be delivered as the client currently imagines them.** iOS does not expose call logs to any third-party app — this is an Apple platform restriction, not an SGC build decision, and no amount of scope or budget changes it without a company-device or cloud-PBX decision RVN hasn't made yet.

On manual self-entry (what's actually priced in Phase 1):
- **R7 is delivered**: an agent can log an outcome, time, and notes for a call they made. This is real and testable.
- **R8 is NOT delivered as "enforcement."** A manually self-entered call log tells you what an agent *chose to record*, not what actually happened. Whether they hit 250 calls/day becomes **self-reported**, not independently verified. Treating manually-entered numbers as an enforcement mechanism is not a credible data-quality assumption at this volume (up to 250 entries/agent/day) — the reporting dashboard in §06 shows logged-call counts, and that is explicitly a self-reported figure, not a verified one, stated identically in both the "what done looks like" section and the exclusions section below so the two don't contradict each other.

This reconciliation replaces any earlier wording that implied the dashboard "enforces" the 250-call target — it reports what agents logged, in the client's favour, said plainly rather than left implicit.

---

## SOW

### Objective
Replace RVN's manual Google-Sheet/WhatsApp lead-and-call workflow with an Odoo CRM configured for RVN's sales/telesales team (6–7 seats), covering lead capture, distribution, call-outcome logging (self-reported, per the judgement call above), and daily reporting — scoped exactly to what R1–R10 above resolve to, nothing implied beyond it.

### In-scope deliverables

| Ref | Deliverable | Acceptance criterion (testable) |
|---|---|---|
| R1 | Meta/Google Ads leads land in CRM | A lead created via the existing ad-to-Sheet pipeline appears in the CRM lead list within one sync cycle, with source tagged Meta or Google |
| R2 | In-app new-lead notification | Assigned agent sees the lead in-app on next refresh/login — **not** a guaranteed push within N seconds (no catalogue SLA exists for that) |
| R3 | Auto-distribution + manual override | A new lead is auto-assigned per the configured rule; Ms Dia can reassign any lead to a different agent in one click, confirmed by a UI walkthrough |
| R4 | Per-lead status/remarks | Every lead record has a status field (new/contacted/follow-up/converted/lost) and a free-text remarks/notes field, editable by the assigned agent |
| R6 | 6–7 seats, role-scoped | Exactly the sales/telesales/broker roles have CRM logins; marketing and ownership accounts are not provisioned unless explicitly requested |
| R7 | Manual call logging | Agent can record outcome (answered/not answered/follow-up), a timestamp, and free-text notes against a lead, in under 3 clicks |
| R8 (as reclassified) | Self-reported call-count dashboard | Dashboard shows logged-call count per agent per day against the 250/day reference figure, **labelled as self-reported, not verified** |
| R9 | **DISCOVERY only** — no priced deliverable in Phase 1 | N/A — see Exclusions |
| R10 | Daily reporting dashboard | Management can view, without asking any agent directly, the day's logged call activity per agent, replacing the WhatsApp group format |
| — | Data migration | Existing Google Sheets lead history migrated, sized to the R5-resolved 500–600/month band (see C-A) |

### Explicit exclusions

**OUT-OF-SCOPE:**
- Automated/system-verified call detection or recording (R7/R8 as originally imagined) — blocked on C1, no company-device/PBX decision made
- Attendance/break-time tracking via the client's physical sensor (R9) — no catalogue row exists even for the CRM-native manual fallback; genuinely unpriced, not a refusal
- WhatsApp integration of any kind with a *personal* WhatsApp number — not technically possible, full stop
- Billing/invoicing functionality — explicitly excluded per the client's own statement on the call
- Property-portal (Bayut/Property Finder/Dubizzle) feed integration — **[PRV] this is an assumption pending confirmation, NOT a statement of what the client said.** The portals were mentioned only as ad-spend context (09:04), never as a requirement. Corrects an earlier draft that incorrectly asserted "none were requested on this call" as fact — that phrasing overclaimed certainty the transcript doesn't support. Real status: open question, see below (C-F).

**PHASE-2 (named, not silently dropped):**
- Automated call-analyzer/telephony integration, contingent on RVN's device/PBX decision (C1)
- Sensor/badge attendance integration, contingent on vendor/API identification (C2)
- WhatsApp Business API via a BSP, contingent on RVN wanting it and a BSP quote (C3) — third-party cost, not SGC margin
- Property-portal feed integration, contingent on RVN confirming it's actually wanted (C-F)

### Client-side dependencies

| Dependency | Owner | Due date |
|---|---|---|
| Meta Business Manager admin access | RVN (Mr Nazim or delegate) | Before kickoff |
| Google Ads admin access | RVN | Before kickoff |
| Confirmed device/PBX decision (C1) | Mr Nazim | Monday meeting or within 5 business days |
| Sensor vendor/model/API confirmation (C2) | Ms Dia | Monday meeting |
| WhatsApp intent confirmation — personal-only vs. BSP interest (C3) | Mr Nazim | Monday meeting |
| Exact historical Google Sheets row count | Ms Dia | Before kickoff |
| Property-portal feed scope decision (C-F) | Mr Nazim | Monday meeting |
| Hosting/data-residency preference | Mr Nazim | Before kickoff — see Hosting below |
| Arabic UI requirement (yes/no) | Mr Nazim / Ms Dia | Monday meeting |

### Assumptions register (all flagged [PRV] unless confirmed)

- **[PRV]** Lead volume is 500–600/month (resolved per C-A below, not the "400–600" figure that appeared in an earlier draft)
- **[PRV]** Property-portal feeds are out of scope (C-F — genuinely unconfirmed either way)
- **[PRV]** Standard Odoo Community hosting (SGC-managed) is acceptable — no data-residency requirement stated by the client (see Hosting below)
- **[PRV]** No Arabic UI requirement — not stated either way on the call
- **[OPEN]** Support SLA/hours preference — not discussed
- **[OPEN]** User count at 12 and 24 months — client stated "we don't want to lag" on timeline but gave no headcount growth figure

### Third-party costs (borne by RVN, not SGC)

| Item | Status |
|---|---|
| Odoo Community licence | **None** — Community edition has zero per-user licence cost (confirmed: `number_1_cost_to_serve.licences_aed: 0` in the worksheet) |
| WhatsApp Business API (BSP) | **[UNPRICED — Commercial Desk]** — per-conversation cost, template pre-approval, Meta business verification, all third-party. No SGC margin on this line if/when it's scoped. |
| SMS/telephony (if C1 resolves to cloud PBX) | **[UNPRICED — Commercial Desk]** — contingent on C1 |

### Hosting & data residency

**Not silently excluded — stated here as an open dependency.** Standard SGC-managed Odoo Community hosting is the default assumption **[PRV]**; no data-residency requirement was raised by the client on the call. If RVN requires UAE-resident hosting specifically or on-premise infrastructure, that changes scope and must be confirmed before kickoff — it cannot sit silently in "exclusions" while also being undiscussed.

### Change control

**As a standalone clause, not buried in exclusions**: any scope addition beyond the deliverables listed above (including anything in the Phase-2 list becoming Phase-1) requires a written change request, re-costed against the same catalogue and gate process as this document, and signed off before work begins. No verbal scope change is binding.

### Go-live definition

Go-live is achieved when: (1) all R1–R4, R6, R7, R10 deliverables above pass their acceptance criteria in a live walkthrough with Ms Dia; (2) historical lead data is migrated and spot-checked; (3) the sales/telesales team has completed both training sessions. Per §06 above, R8 is delivered as self-reported reporting, not enforcement — go-live does not require independent call verification, because nothing priced here provides it.

### Lead time per deliverable

**[OPEN]** — `hour-lookup.yaml` has no `lead_time_days` field anywhere in this catalogue; confirmed by direct inspection. No lead-time figure is stated per deliverable because none exists to cite. The week-by-week timeline below is the only schedule commitment this document makes.

---

## Commercial terms

### Effort reconciliation (correcting the prompt's own premise)

The build is **not** 49 hours × a flat AED 280/hr = AED 13,720 with an unexplained ~AED 1,607 "Class B balance." That figure doesn't match this worksheet. The real breakdown, fully traced, nothing unlabelled:

| Component | Hours | Rate | AED |
|---|---|---|---|
| A-side (25 work-package hours + 8h named Class-A addition [migration record validation/sign-off] + 3 QA + 2 documentation + 4 training) | 42 | 280 (blended, startup_consultant) | 11,760 |
| B-side (Class B, 6 named tasks, per-task role rates) | 3.005 | 90/450 blend, per task | 540.43 |
| **Subtotal** | 45.005 | | **12,300.43** |
| + PM (10%, startup_boutique) | | | 1,230.04 |
| + Contingency (5%) | | | 615.02 |
| **Build value core** | | | **14,207.00** |
| + Hypercare (4h, 2 pods × 2h, added after core, no PM/contingency markup) | 4 | 280 | 1,120 |
| **Build value total** | **49.005** | | **15,327** |

Every hour traces to `hour-lookup.yaml` (work packages) or `rate-card.yaml` (Class B per-task rates) — confirmed via `validate.py` checks V1/R3, both pass. The "16 unlabelled hours" claim in the prompt does not hold against this worksheet: every hour is accounted for in one of the five labelled buckets above.

### C-A — Lead volume, resolved

The client's own words on the call: *"minimum of 500, 600"* (04:34) — the real transcript quote does not contain a "400." An earlier draft's §06 stated "400–600/month 'confirmed on the discovery call'" — that lower bound is unsourced and is corrected here. **Resolved band: 500–600/month.** The `data_migration_500` work package (sized to 500 historical records) is checked against this and remains appropriately sized — it targets the low end of the confirmed band, not below it.

### C-B — Financing arithmetic, resolved (blocking item, now closed)

Verified: `platform_portion_aed_mo` (1,170) + `recovery_component_aed_mo` (505) = **1,675**, not 1,680. The worksheet already documents this exactly (`subscription_fee_aed_mo_raw: 1675`) and separately documents the reason the *billed* figure is 1,680: `policy.yaml`'s `presentation.client_facing_subscription_rounding` field (added pricing v3.1, 2026-08-06) rounds the client-facing monthly figure to the nearest AED 10. This is a real, cited policy rule — not an arbitrary choice made to close this ticket.

**Resolution: (ii)** — the monthly figure **stays AED 1,680** (policy-correct, already used consistently in every other total in this and prior drafts), and the **financing-premium disclosure is corrected**, not the monthly fee:

- Recurring revenue over 24 months at the billed rate: 1,680 × 24 = AED 40,320
- Platform-only cost portion over the same 24 months: 1,170 × 24 = AED 28,080
- Financing-attributable revenue: 40,320 − 28,080 = **AED 12,240**
- Financed remainder: AED 10,269
- **True financing premium: 12,240 − 10,269 = AED 1,971 = 19.2% of the deferred amount**

The previously-disclosed "AED 1,848 / 18%" figure was computed on the pre-rounding AED 1,675 monthly rate and never corrected once the client-facing figure rounded up to AED 1,680. That's a real disclosure error in earlier drafts, corrected here. The AED 123 gap (1,971 − 1,848) traces to the AED 5/month rounding delta compounded over 24 months plus the recovery-schedule rounding already present in `recovery_monthly_aed` (505, itself rounded from 504.875).

**Crossover, re-derived**: because the *billed* monthly figures (1,170 vs 1,680) were already correct in every total published earlier — only the premium *disclosure wording* was wrong — the crossover arithmetic is unchanged: extra upfront under Option A (15,327 − 5,058 = 10,269) ÷ monthly saving (1,680 − 1,170 = 510) = **20.135 months**, gap AED 69 at that point. Confirmed, not re-derived to a different number, since the inputs to that specific calculation were never the ones that were wrong.

### C-C — Cross-horizon comparison, fixed

No more presenting "29,367 (12mo)" beside "45,378 (24mo)" as if directly comparable. Below, every total is labelled with its own horizon; where horizons differ, it is captioned "not comparable — different horizons," never presented side-by-side without that caption.

### C-D — Deposit relabelled

AED 1,680 is **exactly one month of Option B's subscription (1,680/mo)**, and **1.44 months of Option A's subscription (1,170/mo)**. Relabelled below as "Refundable security deposit — AED 1,680 (= 1 month at Option B's rate; 1.44 months at Option A's rate)," not a flat "1 month" label that only holds for one of the two options.

### C-E — Deposit inclusion/exclusion, stated per row

Marked explicitly on every total row below.

### Two options, normalised, non-comparable horizons captioned

| | Option A — Milestone Payment | Option B — Subscription |
|---|---|---|
| Structure | Full build value paid as a single milestone at kickoff — see routing note below on staged billing | 33% mobilisation at kickoff; remainder financed at 18% uplift |
| Kickoff milestone/mobilisation | AED 15,327 | AED 5,058 |
| Monthly subscription | AED 1,170 (platform only, no financing) | AED 1,680 (platform 1,170 + financing-inclusive 510, billed-rate; pre-rounding raw = 1,675) |
| Refundable security deposit | AED 1,680 (**= 1.44 months at this option's rate**) | AED 1,680 (**= 1 month at this option's rate**) |
| Billed quarterly in advance | AED 3,510 | AED 5,040 |
| **Kickoff payable, deposit INCLUDED** | AED 20,517 (15,327 + 1,680 + 3,510) | AED 11,778 (5,058 + 1,680 + 5,040) |
| Minimum term | 12 months | 24 months |
| **12-month total (deposit EXCLUDED, refundable)** | AED 29,367 | *not applicable — below minimum term* |
| **24-month total (deposit EXCLUDED, refundable)** | AED 43,407 | AED 45,378 |
| **36-month total (deposit EXCLUDED, refundable)** | AED 57,447 | AED 65,538 |

**Caption, required**: the 12-month and 24-month rows above are **not comparable to each other** — they represent different commitment horizons. Compare Option A to Option B only at matching horizons (24mo vs 24mo, 36mo vs 36mo); Option A's 12-month figure has no Option B equivalent because Option B's minimum term is 24 months.

**Financing premium**: AED 1,971 = **19.2%** of the AED 10,269 deferred amount (corrected per C-B above).

**Crossover**: the two options cost effectively the same at roughly 20 months (AED 69 apart at month 20.135 exactly) — below that, Option B is cheaper; beyond it, Option A is. Not a hard decision point at any single month.

### Fee structure at 7/10/15 seats — flat vs per-user, with the known defect flagged

Both options above are priced for **7 seats as a flat platform fee** — the CTS-based platform portion (AED 1,170/mo) does not scale linearly per-seat within this worksheet's Class A/B model; it is a function of the whole-team cost-to-serve, not a per-seat multiplication. **Refusing to publish 7/10/15-seat growth figures**, per the same reasoning applied earlier this session: the only per-user marginal rate that exists in the catalogue is AED 250/user/month (`phase2-catalogue.yaml`, current v2.1, applies only to *additional* users beyond the initially quoted seat count, not a re-derivation of the base fee at a different headcount) — and a documented, known-defect scale curve exists elsewhere in this repo's history (an 11× user increase historically producing only a 9% cost increase, a structurally implausible result) that this worksheet was never re-verified against for N=10 or N=15. Publishing speculative per-seat figures here would repeat that exact defect. **Additional-user rate beyond 7: AED 250/user/month** (v2.1, current, verified) is the only real, catalogue-backed number available.

### Included in the monthly fee vs. chargeable extra

| Included | Chargeable extra |
|---|---|
| Hosting (SGC-managed, standard tier) | Custom hosting/data-residency requirement, if raised (Open dependency above) |
| Backups | Any Phase-2 item above (call-analyzer, sensor integration, WhatsApp BSP) |
| Platform updates | Additional users beyond 7, at AED 250/user/month |
| Baseline support (hours/SLA: **[OPEN]** — not discussed on the call) | Overage support beyond baseline (rate: **[UNPRICED — Commercial Desk]** — no `sgc.pricing.retainer`-style overage rate exists in this repo's catalogue; `saas-modules.yaml`/`policy.yaml` checked, neither has one) |

**Option B / retainer note**: the prompt asks for "included support hours + overage rate" per an `sgc.pricing.retainer` model. That model doesn't exist in this repo (see Rule 1 note above). This worksheet's support line (`hypercare` block) covers a fixed 4-hour post-launch hypercare window, not an ongoing monthly support-hours allocation — there is no catalogued monthly support-hours-included figure to report. **[OPEN]**, not invented.

### Milestone-billing routing (Option A structure note)

Per `payment-plans.yaml`, staged/multi-installment billing (`milestone_or_usage`) is gated `treatment: escalate, approval: sales_leadership`. **Not routed anywhere** — no ticketing/Commercial Desk mechanism exists in this repo to route it to; stating that plainly rather than pretending an action happened, same as reported earlier this session. Option A above is presented as **single-payment-at-kickoff**, which needs no escalation. If RVN wants a true staged (kickoff/mid-build/go-live) structure, that requires an actual human Commercial Desk decision before it can be quoted.

### VAT

SGC TECH AI is **not currently VAT-registered**; **no VAT is charged**, so the question of inclusive-vs-exclusive doesn't arise on this quote (`clause-library/vat-uae.md`). Should SGC TECH AI become VAT-registered during either option's term, VAT at the prevailing rate (5%) would be added to invoices from that point forward, per `clause-library/vat-gross-up.md` — **a tax-treatment question for RVN's own accountant/counsel before signing a multi-year commitment**, not resolved definitively here.

### Quotation validity

30 days from issue. **Sourcing**: template convention — no `policy.yaml` value sets this figure (confirmed by direct check). Recorded as a decision made **2026-08-15**, source = template convention. **Deciding human: _______________ [BLOCKS ISSUE until filled]** — per the governance requirement, this document cannot issue while this line is blank.

---

## Open questions for Monday (standalone section)

1. **C1 — Call capture**: what handset OS mix does the sales team actually use (iOS/Android split)? Will RVN issue company devices, or is a cloud PBX/click-to-call number pool acceptable instead? Until answered, automated call tracking stays unpriced.
2. **C2 — Attendance hardware**: sensor system vendor/model, and does it expose an API or data export? Until answered, attendance integration stays unpriced (and note: even the manual fallback has no catalogue row today).
3. **C3 — WhatsApp**: is personal-WhatsApp-only acceptable long-term, or is RVN interested in WhatsApp Business API via a BSP (real, separate, third-party cost)?
4. **R2 — notification method**: is in-app, on-refresh notification acceptable as the day-one replacement for today's instant WhatsApp alerting, or does RVN consider that a regression? Listed here as its own item, not only buried inside a scope bullet, because it's a stated requirement with a real gap against current behaviour.
5. Meta Business Manager admin access — who grants it, when?
6. Google Ads admin access — who grants it, when?
7. Exact historical Google Sheets row count to migrate.
8. Property-portal feed scope (Bayut/Property Finder/Dubizzle) — genuinely open, not assumed either way (C-F).
9. Hosting and data residency preference — any requirement, or is SGC-managed standard hosting acceptable?
10. Arabic UI requirement — yes/no?
11. Support SLA and hours preference — not discussed at all yet.
12. User count expected at 12 and 24 months — needed for headcount-growth planning beyond the initial 7 seats.

---

## Timeline (identical across both options)

| Week | Milestone |
|---|---|
| 1 | Kickoff |
| 1–2 | Discovery confirmation + Google Sheets data-quality sign-off |
| 3–4 | CRM configuration + migration |
| 5 | Training (two sessions) |
| 5–6 | Go-live |
| 8 | Hypercare close |

This timeline is identical for Option A and Option B — the payment structure does not change the delivery schedule.
