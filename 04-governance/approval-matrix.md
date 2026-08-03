# Approval Matrix

**This structure is a reasonable invention, not a sourced fact.** Nothing
in `00-knowledge/` specifies who signs off at what threshold — only the
gate mechanics (`commercial-rules/subscription-guardrails.md`) and the
escalation instruction in `AGENTS.md: On uncertainty`. The thresholds below
are anchored to real `policy.yaml` numbers where one exists and reasoned
about where it doesn't; treat the whole table as a starting operating
policy for Sales leadership to formally adopt or revise, not as something
already ratified.

## Sign-off levels

| Level | Who | Scope |
|---|---|---|
| L0 — SDR | The drafting SDR | Standard-terms proposals, no gate failures, no off-card items |
| L1 — Sales Lead | Sales Lead | Elevated monthly value, discount depth within a bounded range, non-standard payment terms |
| L2 — Commercial Desk | Commercial Desk | Any gate failure, any off-card rate/module, any pricing at or below the platform floor |
| L3 — Sales Leadership | Sales Leadership / Partner | Exceptions Commercial Desk itself can't clear — e.g. a one-off floor exception, or a deal above a large total-value threshold |

## Thresholds

| Condition | Approval required | Basis |
|---|---|---|
| All 10 gates pass, standard segment terms, no discount off card rate | **L0 (SDR)** — no additional sign-off, proceed to QA checklist and human review per the normal runbook sequence | Standard case; the gate report itself is the control |
| Monthly subscription value > AED 2,500/mo | **L1 (Sales Lead)** | Anchored to `policy.yaml: gates.review_cadence_monthly_threshold_aed` (2,500) — invented as an approval trigger; the source key only labels a review-cadence threshold, not an approval rule, so this is an inference, not a restated fact |
| Any manual discount off list/card rate, up to 10% | **L1 (Sales Lead)** — gates must still pass after the discount | Invented threshold; no source caps discount depth explicitly, only G8/G9 cap the outcome |
| Discount off list/card rate greater than 10% | **L2 (Commercial Desk)** | Invented threshold |
| Total contract value (mobilisation + full term) > AED 150,000 | **L1 (Sales Lead)** | Invented threshold, loosely anchored to the top of `benchmarks.yaml: market_positioning.erp_rollout_bundle_c_plus_y1_aed` SGC band (70,000–150,000) as a "this is now a large deal for SGC's band" marker |
| Total contract value > AED 500,000 | **L2 (Commercial Desk)** + **L3 (Sales Leadership)** | Invented threshold — pushes into territory `benchmarks.yaml` associates with Big-4/large-enterprise scope, outside SGC's stated specialist-boutique positioning |
| Any G1–G10 gate failure | **L2 (Commercial Desk)**, mandatory, per `AGENTS.md: On uncertainty` — reduce scope, never price around it | `commercial-rules/subscription-guardrails.md`; see `escalation-triggers.md` for the full per-gate list |
| Rate, module, or work package not on the card (i.e., not a key in `pricing/*.yaml`) | **L2 (Commercial Desk)** | `AGENTS.md` absolute rule; `known-defects.md #15` |
| Client budget below `platform_floor_aed` for the deal | **L2 (Commercial Desk)** | G1 (`subscription-guardrails.md`) |
| Quoting at or near a client's previously rejected budget (G10 trigger) | **L2 (Commercial Desk)**, with a logged value justification in `manifest.yaml: escalations` before requoting | G10; `known-defects.md #10` |
| Any legal/VAT clause requiring paraphrase (verbatim clause doesn't fit) | **L2 (Commercial Desk)** + legal review, before draft goes to client | `AGENTS.md`; `known-defects.md #6` |
| Correction to an already-issued proposal (`05-issued/`) | **L1 (Sales Lead)** to authorize the new revision or correction notice; **L2** if the correction involves pricing, not just a clerical fix | `AGENTS.md`; `05-ops/naming-conventions.md` revision numbering; `known-defects.md #5` |
| One-off exception below the G8 margin floor | **L3 (Sales Leadership)** only, with written rationale logged in `manifest.yaml: escalations` — this is the rare exception, not a routine escalation outcome | Not sourced; margin-floor exceptions should be exceptional almost by definition |

## Notes

- A gate failure is never resolved by an SDR alone, regardless of deal
  size — see `AGENTS.md: On uncertainty`: "reduce scope, never price."
  L0 authority never extends to overriding a gate.
- Approval levels stack: a deal that's both above AED 500,000 **and** has a
  gate failure needs both L2 and L3 sign-off, not just the higher of the
  two.
- This table should be revisited once real deal volume exists to validate
  whether AED 2,500/mo and AED 150,000/500,000 are the right lines — they
  are starting assumptions, not calibrated thresholds.
