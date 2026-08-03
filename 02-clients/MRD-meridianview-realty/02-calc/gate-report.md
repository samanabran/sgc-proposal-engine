# Gate Report — MRD-2026-SUB-01_Rev3

Run against `pricing-worksheet.yaml` (this revision) per
`00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`.
**All 41 gates pass, plus market_test and budget_test.** Cleared for
draft/review/issue.

## The three numbers

| | AED |
|---|---|
| Cost to Serve (monthly) | 520 |
| Platform floor (CTS x 1.25) | 650 |
| Build value (one-time) | 14,812 |
| Internal build cost | 6,900 |
| Mobilisation (33%) | 4,888 |
| Recovery monthly (24mo, 18% uplift) | 488 |
| **Subscription (platform 1,150 + recovery 488, rounded)** | **1,650/mo** |
| Year 1 client cost | 24,688 |

## Gate summary

| Gate | Result |
|---|---|
| G1 Platform floor | PASS — 1,650 >> 650 |
| G2 Term >= recovery | PASS — recovers exactly at month 24 |
| G3 Mobilisation >= 33% | PASS — exactly 33.0% |
| G4 Clawback present | PASS |
| G5 No post-recovery drop | PASS |
| G6 Term at kickoff | PASS |
| G7 Financing disclosed | PASS — 18% uplift stated |
| G8 Margin >= 30% | PASS — 53.4% |
| G9 Rate provenance | PASS — 280 AED/hr, `rate-card.yaml: roles.startup_consultant` |
| G10 Concessions capped | PASS — no concessions on this deal |
| G11-G20 (payment-plan) | PASS — see worksheet `gates` block |
| G21 All exposures computed | PASS |
| G22 Walk-away card produced | PASS — dated 2026-06-10, before first pricing conversation |
| G23 Absolute margin floor | PASS — 53.4% >= 25% |
| G24 Portfolio limits | PASS — peak cash exposure AED 0 |
| G25-G30 (protection) | PASS — see worksheet `gates` block |
| G31 Worst-case margin | PASS — 48% even with full guarantee-credit exposure |
| G32 Cash-positive within 30 days | PASS — cash-positive at kickoff |
| G33 Min cadence quarterly | PASS |
| G34 Mobilisation covers 3rd-party cost | PASS — N/A, no trigger |
| G35 No false VAT claim | PASS |
| G36-G41 (edition) | PASS — Community declared, exclusions disclosed, no abandoned modules, demo matches edition |
| market_test | PASS — 1.169x incumbent (PropSpace upper range) |
| budget_test | PASS — 17.7% under the AED 30,000 previously-rejected quote |

## Notes

- This deal has **zero cash exposure at any point in the build** — see
  `exposure-calculator.yaml`. Mobilisation plus the first quarterly
  payment together exceed cumulative internal cost throughout the 6-week
  delivery window.
- G29 (evidence file) passes for everything obtainable at draft/issue
  stage; signature and counsel review on flagged clauses are re-verified
  before go-live specifically, per G29's own scope — this is not a
  deferred failure, it is the correct sequencing.
- Arithmetic note: this worksheet's `build_value_aed` (14,812) is derived
  directly from `subtotal + pm + contingency` and is fully reproducible
  from the inputs above. It differs by AED 12 from the illustrative
  figure originally quoted for this deal type (14,800) due to rounding in
  the original illustration — the number here is the one that actually
  reconciles, which is the entire point of keeping the calculation in a
  worksheet rather than a headline figure.

Reviewer: _______________  Date: _______________
