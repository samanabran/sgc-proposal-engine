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
| Build value (one-time) | 15,999 |
| Internal build cost | 7,562 |
| Mobilisation (33%) | 5,280 |
| Recovery monthly (24mo, 18% uplift) | 527 |
| **Subscription (platform 1,150 + recovery 527, rounded)** | **1,700/mo** |
| Year 1 client cost | 25,680 |

## Gate summary

| Gate | Result |
|---|---|
| G1 Platform floor | PASS — 1,700 >> 650 |
| G2 Term >= recovery | PASS — recovers exactly at month 24 |
| G3 Mobilisation >= 33% | PASS — exactly 33.0% |
| G4 Clawback present | PASS |
| G5 No post-recovery drop | PASS |
| G6 Term at kickoff | PASS |
| G7 Financing disclosed | PASS — 18% uplift stated |
| G8 Margin >= 30% | PASS — 52.7% |
| G9 Rate provenance | PASS — 280 AED/hr, `rate-card.yaml: roles.startup_consultant` |
| G10 Concessions capped | PASS — no concessions on this deal |
| G11-G20 (payment-plan) | PASS — see worksheet `gates` block |
| G21 All exposures computed | PASS |
| G22 Walk-away card produced | PASS — dated 2026-06-10, before first pricing conversation |
| G23 Absolute margin floor | PASS — 52.7% >= 25% |
| G24 Portfolio limits | PASS — peak cash exposure AED 0 |
| G25-G30 (protection) | PASS — see worksheet `gates` block |
| G31 Worst-case margin | PASS — 48% even with full guarantee-credit exposure |
| G32 Cash-positive within 30 days | PASS — cash-positive at kickoff |
| G33 Min cadence quarterly | PASS |
| G34 Mobilisation covers 3rd-party cost | PASS — N/A, no trigger |
| G35 No false VAT claim | PASS |
| G36-G41 (edition) | PASS — Community declared, exclusions disclosed, no abandoned modules, demo matches edition |
| market_test | PASS — 1.216x incumbent (PropSpace upper range) |
| budget_test | PASS — 14.4% under the AED 30,000 previously-rejected quote |

## Notes

- This deal has **zero cash exposure at any point in the build** — see
  `exposure-calculator.yaml`. Mobilisation plus the first quarterly
  payment together exceed cumulative internal cost throughout the 6-week
  delivery window.
- G29 (evidence file) passes for everything obtainable at draft/issue
  stage; signature and counsel review on flagged clauses are re-verified
  before go-live specifically, per G29's own scope — this is not a
  deferred failure, it is the correct sequencing.
- Arithmetic note (historical, 2026-08-03, kept for the record): this
  worksheet's `build_value_aed` was then 14,812, derived directly from
  `subtotal + pm + contingency`, differing by AED 12 from the
  illustrative figure originally quoted for this deal type (14,800) due
  to rounding in the original illustration. **This note turned out to be
  the direct, pre-existing confirmation that VGE's brief-pinned 14,800
  and MRD's own 14,812 shared one origin** — both are the same
  pre-Class-B, pre-hypercare additive calculation for identical scope/
  segment/N, one frozen as an external constant, one left live. See
  CHANGELOG.md pricing v3.0 addendum, 2026-08-05.
- Updated 2026-08-05: `build_value_aed` is now 15,999 (Class A-D engine
  migration — Class B and hypercare, never priced before, now included).
  See CHANGELOG.md for the full derivation and the resulting Subscription
  Fee change (1,650→1,700/mo).

Reviewer: _______________  Date: _______________
