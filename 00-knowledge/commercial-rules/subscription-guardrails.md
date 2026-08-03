# Subscription Guardrails — G1–G10

Core deal-shape gates. Every completed `02-calc/pricing-worksheet.yaml`
clears these before draft. **If any gate fails, stop and escalate — do not
discount.** See `00-knowledge/PRECEDENCE.md` for how these rank against
`payment-plan-guardrails.md` (G11–G20) and `protection-guardrails.md`
(G21–G41) when they interact.

| Gate | Rule | Test | Owner |
|---|---|---|---|
| **G1** | Recurring platform price ≥ cost-to-serve floor | `platform_portion_aed ≥ CTS × policy.gates.platform_floor_multiplier (1.25)` | Commercial Desk |
| **G2** | Term ≥ recovery period | `mobilisation_aed + recovery_total_aed` fully recovered within `term_months` | Commercial Desk |
| **G3** | Mobilisation ≥ 33% default | `mobilisation_aed ≥ build_value_aed × policy.gates.default_mobilisation_pct (0.33)`; waiving mobilisation is a priced concession (`concession-ladder.yaml: waive_mobilisation`), never a silent default | SDR + Commercial Desk |
| **G4** | Clawback present | Any deferred-value structure carries `clause-library/clawback.md` verbatim | Commercial Desk |
| **G5** | No post-recovery price drop | Subscription rate after full recovery stays flat (`clause-library/post-recovery-continuation.md`), never silently reduced | Commercial Desk |
| **G6** | Term starts at kickoff | `term_commencement.md`: term and first invoice both anchor to kickoff, not go-live | SDR |
| **G7** | Financing priced and disclosed | Uplift % shown to client in one line (`clause-library/financing-disclosure.md`) whenever `deferred_aed > 0` | SDR |
| **G8** | Gross margin ≥ 30% over full term | `(revenue_over_term − cost_over_term) / revenue_over_term ≥ policy.gates.min_gross_margin (0.30)` | Finance |
| **G9** | Every rate exists on rate card | Every AED/hr figure traces to `rate-card.yaml: roles.*`; reject `forbidden_rates` (690) outright | SDR + validate script |
| **G10** | Concessions capped, no exclusivity granted | Any concession runs through `concession-ladder.yaml`; no proposal grants pricing exclusivity to a client (`clause-library/exclusivity-replacement.md`) | Commercial Desk |

## On a failed gate

Reduce scope, not price. G1/G8 failing means the deal is undersized for
its cost base — cut scope or raise the segment, don't manually lower the
rate. G2 failing means extend the term or raise mobilisation. G3 failing
(mobilisation short of 33%) requires running the concession ladder, not a
silent exception. Every resolution gets one line in
`manifest.yaml: escalations`.
