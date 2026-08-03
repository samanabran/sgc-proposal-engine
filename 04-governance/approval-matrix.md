# Approval Matrix (v2)

**This structure is a reasonable operating policy, not a sourced fact** —
same caveat as v1: anchored to real `policy.yaml`/`payment-plans.yaml`
numbers where one exists, reasoned about where it doesn't.

## Sign-off levels

| Level | Who | Scope |
|---|---|---|
| L0 — SDR | The drafting SDR | Standard-terms deals: all 41 gates pass on first run, no concession, risk band low/moderate (`risk-security-matrix.yaml`) |
| L1 — Commercial Desk | Commercial Desk | Concessions run through `concession-ladder.yaml` with logged compensators (G14); elevated risk band security instruments; deferred-start cadence, max 3 months |
| L2 — Finance | Finance | Cadence-ceiling calculations (G12); portfolio-limit exceptions within `07-protection/exposure/portfolio-limits.yaml`; worst-case gate (G31) sign-off |
| L3 — Sales leadership | Sales leadership | Non-standard structures (`milestone_or_usage` cadence, G20); high risk band deals |
| **Founder + Commercial Desk jointly** | — | Any deal approaching aggregate portfolio caps; any entity-fact resolution in `06-brand/entity/legal-identity.yaml` |

## Absolute floors — no authority level overrides these

- Margin below `absolute_margin_floor` (25%, **G23**)
- Waiving a clawback on any deferred structure (**G16**)
- Any VAT registration misstatement (**G35**) or edition misdescription
  (**G36**) — these are not discretionary, they're factual accuracy
- Withholding client data as security (**G18**)

## Thresholds

| Condition | Approval required | Basis |
|---|---|---|
| All 41 gates pass, standard terms, low/moderate risk band | **L0 (SDR)** | Standard case — the gate report is the control |
| Any concession (`concession-ladder.yaml`) | **L1 (Commercial Desk)**, with compensators logged and gates re-run (G14) | `payment-plan-guardrails.md` |
| Elevated or high risk band | **L1 (Commercial Desk)** for elevated; **L1 + L3** for high | `risk-security-matrix.yaml` bands |
| Refuse risk band (76+) | Abort per `07-protection/abort/abort-criteria.md`, or **Founder + Commercial Desk jointly** for an exception | G30 |
| Deferred-start cadence | **L1 (Commercial Desk)**, max 3 months | `payment-plans.yaml: cadences.deferred_start` |
| Milestone/usage-based cadence | **L3 (Sales leadership)** | `payment-plans.yaml: cadences.milestone_or_usage` |
| Subscription < AED 2,500/mo | **L0 (SDR)** — quarterly review cadence applies automatically, no escalation needed | `policy.yaml: gates.review_cadence_monthly_threshold_aed` |
| Enterprise edition triggered | **L0 (SDR)** to identify the trigger condition; **L2 (Finance)** to confirm mobilisation covers full annual licence prepayment (G40) | `editions.yaml` |
| Rate, work package, or module not on any `pricing/*.yaml` file | **L1 (Commercial Desk)** | `AGENTS.md` absolute rule |
| Correction to an already-issued proposal | **L1 (Commercial Desk)** to authorize the new revision or correction notice | `05-ops/naming-conventions.md`, `known-defects.md` #9/#5 (v1 numbering — an already-issued document is never edited in place regardless of the defect being corrected) |

## Notes

- A gate failure is never resolved by an SDR alone, regardless of deal
  size. L0 authority never extends to overriding a gate.
- Approval levels stack — a high-risk-band deal with a requested
  concession needs both the risk-band sign-off and the concession
  sign-off, not just the higher of the two.
- Revisit these thresholds once real deal volume exists to calibrate
  against `07-protection/doctrine.md`'s reserve constraint — they are
  starting assumptions.
