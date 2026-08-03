# Subscription Guardrails — G1–G10

These are the ten gates a completed `02-calc/pricing-worksheet.yaml` must
clear before a subscription (`SUB`) proposal may move from calc to draft.
Each gate mechanizes one or more of the `12-commercial-rules.md`. Run them in
order, in `02-calc/gate-report.md` (see `05-ops/validate.md` for the exact
procedure). **If any gate fails, stop and escalate — do not discount.**

| Gate | Check | Source | Enforces rule |
|---|---|---|---|
| **G1** — Platform floor | The recurring subscription price (`assembly.option_a.subscription_aed`) must be `≥ platform_floor_aed`, where `platform_floor_aed = cts_total_aed × policy.gates.platform_floor_multiplier (1.25)` | `pricing/policy.yaml: gates.platform_floor_multiplier`, `02-calc` `number_1_cost_to_serve.platform_floor_aed` | The recurring fee alone — before any one-time build margin — covers monthly cost-to-serve with headroom |
| **G2** — Term ≥ recovery | Subscription `term_months` must be long enough that `mobilisation_aed + recovery_total_aed` is fully recovered within the term | `02-calc` `number_3_financing` | Prevents a subscription that never pays back its build cost |
| **G3** — Rate provenance | Every rate, hour figure, and percentage in the worksheet traces to a key in `pricing/*.yaml` | Rule 3 | Auditability — no invented numbers |
| **G4** — Documentation coverage | `documentation_hours ≥ max(overlays.documentation_hours_min, 5% of dev hours)` | Rule 4, `policy.yaml: overlays` | No custom feature ships undocumented |
| **G5** — QA coverage | `qa_hours ≥ max(overlays.qa_hours_min, 8% of delivery hours)` | Rule 5, `policy.yaml: overlays` | QA is never waived |
| **G6** — PM coverage | PM line = segment `pm_pct` × subtotal (15% standard, 10% startup) | Rule 6 | Every implementation includes PM |
| **G7** — Segment rate integrity | `blended_rate_aed` used matches the segment's pinned rate in `policy.yaml: segments` (280 / 395 / 525) | Rule 7 | No off-card rate slips into a worksheet |
| **G8** — Gross margin floor | `(build_value_aed − internal_build_cost_aed) / build_value_aed ≥ policy.gates.min_gross_margin (0.30)`, target 0.35 | `pricing/policy.yaml: gates`, `02-calc` `number_2_build` | Floor below which the one-time build is not viable regardless of win probability |
| **G9** — Market test | `year1_client_cost_aed ≤ incumbent_benchmark_aed_mo × 12 × policy.gates.max_multiple_of_incumbent (1.30)` | `pricing/policy.yaml: gates.max_multiple_of_incumbent` | Keeps SGC in the "specialist boutique, 15–20% under mid-tier" position, not into Big-4 territory (see `market-data/benchmarks.yaml`) |
| **G10** — Budget test | If the client previously rejected a budget (`budget_rejected_aed`), `year1_client_cost_aed` must not exceed it without an explicit scope or value justification logged in `manifest.yaml: escalations` | Client brief `budget_rejected_aed` | Prevents re-quoting a number the client has already said no to |

In `02-calc/pricing-worksheet.yaml`, G1, G2, and G8 are recorded directly
under `gates:`; G9 and G10 are recorded under `market_test` and
`budget_test`. G3–G7 are enforced by construction if the worksheet was built
by following `runbook/subscription-proposal-runbook.md` §2 in order — record
a pass/fail for each explicitly in `gate-report.md` regardless.

## On a failed gate

Reduce scope, not price:

- **G1/G8 fail** → the deal is undersized for its cost base. Cut a hosting
  tier, drop a module, or raise the segment (more users than the
  `startup_boutique` rate should support). Do not manually lower the rate.
- **G2 fail** → extend the term or raise mobilisation. Do not shorten the
  recovery assumption to force a pass.
- **G9 fail** → the price has drifted toward Big-4 territory. Re-check for
  double-counted overlays before cutting scope.
- **G10 fail** → escalate to the Commercial Desk with the value justification
  before re-quoting near the rejected number.

Every failure and its resolution gets one line in `manifest.yaml:
escalations`, even if the deal ultimately clears on a re-run.
