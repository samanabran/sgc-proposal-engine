# Gate Report — VGE-2026-SUB-01_Rev3

Run against `pricing-worksheet.yaml` (this revision) per
`00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`.
**All 41 gates pass.** Cleared for draft and review. Issue is separately
blocked on the proposal's `RESOLVE:` fields (noted in the build-time
panel of the proposal HTML).

## The three numbers

| | AED |
|---|---|
| Implementation Value (disclosed, brief §3) | 14,800 |
| Mobilisation Fee (Kickoff) | 4,900 |
| Recovery Component | 487 / month |
| Platform Component | 1,163 / month |
| **Subscription Fee** | **1,650 / month** |
| Quarterly billing | 4,950 |
| Payable at Kickoff (Mobilisation + Q1) | 9,850 |
| Year 1 | 24,700 |
| Full 24-month commitment | 44,500 |
| VAT | None charged |

## Gate summary (all 41 v2 gates)

| Gate | Result |
|---|---|
| G1 Platform floor | PASS — 1,650 >> 988 |
| G2 Term >= recovery | PASS — recovery completes exactly at month 24 |
| G3 Mobilisation >= 33% | PASS — 33.1% (4,900 / 14,800) |
| G4 Clawback present | PASS |
| G5 No post-recovery drop | PASS |
| G6 Term at kickoff | PASS |
| G7 Financing disclosed | PASS — 18% uplift stated |
| G8 Margin >= 30% | PASS — 47.3% |
| G9 Rate provenance | PASS — 280 AED/hr, startup_consultant pin |
| G10 Concessions capped | PASS — no concessions |
| G11-G20 (payment-plan) | PASS — see worksheet |
| G21 All exposures computed | PASS — contractual 9,900, cash 0, economic 0 |
| G22 Walk-away card produced | PASS — 2026-08-03, before pricing conversation |
| G23 Absolute margin floor | PASS — 47.3% >= 25% |
| G24 Portfolio limits | PASS — peak cash exposure AED 0 |
| G25-G30 (protection) | PASS — see worksheet |
| G31 Worst-case margin | PASS — 42% with full guarantee-credit exposure |
| G32 Cash-positive within 30 days | PASS — day 1 |
| G33 Min cadence quarterly | PASS |
| G34 Mobilisation covers 3rd-party cost | PASS — no trigger |
| G35 No false VAT claim | PASS |
| G36-G41 (edition) | PASS — Community declared, exclusions disclosed, demo matches edition |
| market_test | N/A — client did not state incumbent monthly figure |
| budget_test | PASS — 29.4% under the AED 40,000 upper rejected anchor |

## Notes

- All §3 brief figures are pinned verbatim in `pricing-worksheet.yaml`
  under `number_3_financing` and `assembly` — the proposal does not
  recompute anything from memory.
- Cash exposure is AED 0 throughout the build — mobilisation (4,900) +
  Q1 (4,950) = 9,850 collected at Kickoff fully covers the delivery
  cost curve for the 6-week build window.
- The risk assessment was originally written with a moderate band
  reflecting the abandoned-systems signal from the transcript; on
  review, that signal is properly addressed through the adoption clause
  (§09), not as a financial security instrument, and the brief §3
  specifies Mobilisation at 33% only. Risk band corrected to low; the
  deal card and the proposal reflect this.
- The rejected-budget figure is recorded as a range (AED 30,000–40,000
  anchors, both probed not committed) per the transcript, not as a
  single midpoint. The midpoint (AED 35,000) is used only inside the
  worksheet's `budget_test` calculation; the proposal prose uses the
  range language throughout.
- The earlier v1 figures of AED 3,700 mobilisation and AED 43,300 total
  are superseded; this worksheet and the resulting proposal must not
  reproduce them. Drift warning: see §3 of the brief.

Reviewer: Renbran Madelo (CEO)  Date: 2026-08-04
