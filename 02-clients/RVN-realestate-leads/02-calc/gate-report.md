# Gate Report — RVN-2026-SUB-01_Rev1

Run against `pricing-worksheet.yaml` (this revision) per
`00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`.
**All 41 gates pass.** Cleared for draft and review. Issue remains
separately blocked on check-14 entity-facts resolution (administrative,
not a gate failure — see `manifest.yaml: escalations`) and on the two
uncatalogued feature requests requiring Commercial Desk scoping before
they can be priced (see below).

## The three numbers

| | AED |
|---|---|
| Build Value (one-time) | 15,327 |
| Mobilisation Fee (Kickoff) | 5,058 |
| Security Deposit, 1 month (refundable, moderate risk band) | 1,680 |
| Recovery Component | 505 / month |
| Platform Component | 1,170 / month |
| **Subscription Fee** | **1,680 / month** |
| Quarterly billing | 5,040 |
| Payable at Kickoff (Mobilisation + Deposit + Q1) | 11,778 |
| Year 1 (Mobilisation + 12 months) | 25,218 |
| Full 24-month commitment | 45,378 |
| VAT | None charged |

## Gate summary (all 41 v2 gates)

| Gate | Result |
|---|---|
| G1 Platform floor | PASS — 1,170 = CTS floor exactly (936 x 1.25) |
| G2 Term >= recovery | PASS — recovery completes exactly at month 24 |
| G3 Mobilisation >= 33% | PASS — 33.0% (5,058 / 15,327) |
| G4 Clawback present | PASS |
| G5 No post-recovery drop | PASS |
| G6 Term at kickoff | PASS |
| G7 Financing disclosed | PASS — 18% uplift stated |
| G8 Margin >= 30% | PASS — 34.3% |
| G9 Rate provenance | PASS — 280 AED/hr startup_consultant (a-side); 90/450 AED/hr Class B per-task rates, both traced to rate-card.yaml; no forbidden_rates present |
| G10 Concessions capped | PASS — no concessions |
| G11-G20 (payment-plan) | PASS — see worksheet |
| G15 Security sized to risk | PASS — moderate band, mobilisation_33pct + deposit_1_month both present |
| G21 All exposures computed | PASS — contractual 10,269, cash 0, economic 0 |
| G22 Walk-away card produced | PASS — `02-calc/deal-card.md`, before pricing conversation |
| G23 Absolute margin floor | PASS — 34.3% >= 25% |
| G24 Portfolio limits | PASS — peak cash exposure AED 0 |
| G25-G30 (protection) | PASS — see worksheet |
| G31 Worst-case margin | PASS — 28.7% with full 10%-of-ACV guarantee-credit exposure applied; combined give(0%)+guarantee(10%) = 10%, within the 12% combined cap |
| G32 Cash-positive within 30 days | PASS — day 1 |
| G33 Min cadence quarterly | PASS |
| G34 Mobilisation covers 3rd-party cost | PASS — no trigger (Community edition, no Enterprise licence prepay) |
| G35 No false VAT claim | PASS |
| G36-G41 (edition) | PASS — Community declared, exclusions live in MSA/Order Form §A.9 (not the sales proposal, per G37/G38), demo environment matches edition (G41) |
| market_test | N/A — client did not state an incumbent CRM cost |
| budget_test | N/A — client explicitly stated no fixed CRM budget |

## Notes

- Users sized at 7 (transcript: "1234677, people" = 7; separately
  confirmed "six or seven max" for CRM seats). The two owners/bosses and
  the marketing team are explicitly excluded from CRM licensing — this
  is a scope decision from the client, not a cost-avoidance assumption
  by SGC.
- Risk band is **moderate**, not low — 4 of 8 risk-matrix inputs are
  ASSUMPTIONS because the call transcript did not cover entity age, VAT
  registration, trade licence status, or exact jurisdiction. Scored
  toward the higher-risk side per the protective-default convention (see
  `risk-assessment.yaml: notes`). This is why the deal card requires a
  security deposit in addition to mobilisation, where a `low`-band deal
  (like VGE) would not.
- G1 is a boundary pass, not a comfortable margin above the floor —
  `platform_portion_aed_mo` equals the CTS floor exactly (1,170 = 1,170)
  because no `market_defensible_floor` is documented above the CTS floor
  for this segment/vertical. If a future revision needs headroom here
  (e.g. a concession request against the platform portion), re-derive
  from a higher anchor before conceding — there is currently zero margin
  above G1's own floor to give away.
  **RESOLVED (2026-08-15):** `policy.gates.platform_floor_multiplier`
  (1.25) IS the floor value itself — `936 × 1.25 = 1,170` flows directly
  into `platform_portion_aed_mo` (`pricing-worksheet.yaml`), it is not a
  margin uplift applied before a separate floor check. So the "zero
  headroom" language above describes the fee's own margin, not a
  multiplier's spare capacity — the stronger and correct reading. G23
  sensitivity figures recorded elsewhere (Option A +18.52%, Option B
  +14.14% breach) describe cost breach against this same floor, not
  against multiplier headroom.
- **Two client-requested capabilities are explicitly NOT priced in this
  worksheet and NOT included in the Phase 1 solution**: (1) automated
  call-analyzer/telephony integration for auto-captured call volume and
  pickup-rate metrics, and (2) attendance/break-time tracking via RVN's
  existing physical sensor/badge system. Neither has a catalogue entry
  in `hour-lookup.yaml`, `saas-modules.yaml`, or `phase2-catalogue.yaml`
  — per SKILL.md §7, these are escalated rather than priced by analogy.
  Native Odoo Community CRM activity logging (manual call outcome,
  notes, follow-up flag) IS included in Phase 1 under `crm_leads` and
  satisfies the client's stated need for logged call detail; it does
  NOT auto-capture call events from a phone system. This distinction
  must be made explicitly and honestly at the Monday demo — see
  `00-intake/monday-meeting-flow.md`.
- No VAT charged, no VAT-registration claim anywhere in the draft.

Reviewer: _pending human review — see manifest.yaml: stage_
