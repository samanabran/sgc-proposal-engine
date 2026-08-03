# Subscription Proposal Runbook (v2)

The operating procedure for a subscription-model (`SUB`) Odoo proposal,
end to end. Read `AGENTS.md` first for the load order and absolute rules.

## 1. Intake

- Copy `02-clients/_SCAFFOLD` to `02-clients/{PREFIX}-{slug}/` — never
  copy a peer's folder.
- Fill `00-intake/client-brief.yaml`, including `edition_trigger` fields
  (does the client trip any `editions.yaml: enterprise.trigger_conditions`?)
  and `01-templates/calc/risk-assessment.template.yaml` inputs.
- Log every verbal commitment in `00-intake/verbal-promises.md` the same
  day, each marked PRICED / DEFERRED / EXCLUDED.
- Determine `segment` from user count against `policy.yaml: segments`.
  Determine `edition` — **Community by default**; only move to Enterprise
  if the brief explicitly trips a trigger condition.

## 2. Risk assessment

Score the client against `pricing/risk-security-matrix.yaml` before any
pricing conversation. The resulting band determines the required security
instrument(s) — this feeds both the walk-away card (step 4) and the
worksheet's mobilisation/cadence inputs.

## 3. Calc — the three-number model

**Number 1 — Cost to Serve (CTS), monthly, recurs forever**

```
CTS = licences + hosting_allocation + tooling + support_labour + account_mgmt
hosting_allocation = 360 × (users ÷ 20)
support_labour = ceil(users / 5) × 280
platform_floor = CTS × 1.25
```

`licences` is 0 for Community edition. Worked reference (5 users):
Community CTS = 0 + 90 + 50 + 280 + 100 = **520** → floor **650**;
Enterprise CTS = 360 + 90 + 50 + 280 + 100 = **880** → floor **1,100**.

Below AED 2,500/mo subscription: quarterly reviews only, not monthly —
monthly business-review calls cost roughly AED 10,800/yr in senior time
against a subscription that doesn't support it (see
`failure-modes/known-defects.md` #19).

**Number 2 — Build Value, one-time**

```
delivery_hours = sum of hour-lookup.yaml work packages (simple or standard band)
                 + documentation + qa + training overlays
build_value = (total_hours × segment_rate) × (1 + pm_pct) × (1 + contingency_pct)
internal_build_cost = total_hours × 150
```

`segment_rate` must exist on `rate-card.yaml: roles.*`. Reject
`forbidden_rates` (690) outright — see G9.

**Number 3 — Financing uplift on deferred value**

```
deferred = build_value − mobilisation
recovery_total = deferred × (1 + uplift)
recovery_monthly = recovery_total ÷ recovery_months
```

Disclose in one line to the client (`clause-library/financing-disclosure.md`).

**Assembly**

```
mobilisation = build_value × 0.33          # policy.yaml gates.default_mobilisation_pct
platform_portion = max(CTS × 1.25, market_defensible_floor)
subscription = platform_portion + recovery_monthly     # round to nearest 50
```

**Prepayment asymmetry (G11)**: discounts apply to `platform_portion`
only. On the recovery portion, the only available concession is reducing
or removing the financing uplift — recovery principal is never
discounted, because it is work already performed.

**Ceiling calculation (G12)**:

```
max_give_aed = revenue_baseline − (build_cost + CTS × term) / (1 − min_margin)
applied_give = min(cadence_table_ceiling, max_give_aed)
```

Always apply the lower of the two.

**Term selection**: build value ≤ AED 8,000 with mobilisation paid → 12
months. Build value AED 8,000–20,000 (typical boutique brokerage) →
**24 months**. Build value > AED 20,000 → 24–36 months, mobilisation
mandatory (never waived at this scale).

**Option structure**: **two options, never three.** Option A =
mobilisation paid, lower recurring cost. Option B = zero upfront — **this
is currently WITHDRAWN** (`payment-plans.yaml: withdrawn.option_b_zero_mobilisation`).
Do not offer it; do not construct a third tier.

## 4. Exposure and walk-away card

Before any pricing conversation with the client: compute all three
exposures (`07-protection/exposure/exposure-model.md`) and complete the
one-page walk-away deal card
(`07-protection/walkaway/deal-card.template.md`) — G21, G22.

## 5. Gate check

Run all 41 gates (`commercial-rules/subscription-guardrails.md`,
`payment-plan-guardrails.md`, `protection-guardrails.md`) against the
completed worksheet and write `02-calc/gate-report.md`. See
`05-ops/validate.md` for the automated check. **If any gate fails, stop.**
Reduce scope or run the concession ladder properly
(`pricing/concession-ladder.yaml`) — never discount around a failed gate.

## 6. Draft

Once `gates_passed: true`: render each proposal section (§01–§13, see
`01-templates/proposal/_section-map.md`) into
`03-draft/{PROPOSAL-REF}_RevN/`. Pull tax/legal/edition wording verbatim
from `clause-library/` — never paraphrase.

## 7. QA checklist and brand QA

Complete `04-review/qa-checklist.md` and `04-review/brand-qa-checklist.md`.
Confirm every entry in `verbal-promises.md` is reflected, every clause
requiring counsel review carries its flag, no forbidden phrase appears
anywhere in the draft, and brand tokens are used only from
`06-brand/registry.yaml`.

## 8. Human review

A human reviewer reads `02-calc/gate-report.md` and the draft, and either
approves for issue or returns `04-review/reviewer-notes.md` with required
changes.

## 9. Issue

Move the approved draft to `05-issued/{PROPOSAL-REF}_RevN/`. Update
`manifest.yaml`. **`05-issued/` is immutable from this point** — a
correction is a new revision, never an in-place edit.
