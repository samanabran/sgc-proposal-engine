# Subscription Proposal Runbook (sanitized for SDR plugin)
# Original: 00-knowledge/runbook/subscription-proposal-runbook.md (desk-only file)
# Redacted by: plugins/sgc-commercial-desk/skills/redacted-derivative-release
# Verified by: plugins/sgc-proposal-engine/ci/diff-redacted-derivatives.py
#
# This derivative carries the stage structure, term selection, option
# structure, gate check, QA, and draft steps. The CTS formula,
# `internal_build_cost = total_hours × 150`, the mobilisation / platform
# portion arithmetic, the `max_give_aed` formula, and the AED 10,800/yr
# note are desk-only and live in the desk plugin.

The operating procedure for a subscription-model (`SUB`) Odoo proposal,
end to end. Read `AGENTS.md` first for the load order and absolute rules.

## 1. Intake

- Run `init-workspace.sh` to create `<cwd>/sgc-proposals/{PREFIX}-{slug}/`
  from `workspace-bootstrap/`. Never copy a peer's folder.
- Fill `00-intake/client-brief.yaml`, including `edition_trigger` fields
  (does the client trip any `editions.yaml: enterprise.trigger_conditions`?)
  and the risk-assessment inputs.
- Log every verbal commitment in `00-intake/verbal-promises.md` the same
  day, each marked PRICED / DEFERRED / EXCLUDED.
- Determine `segment` from user count against `policy.yaml: segments`.
  Determine `edition` — **Community by default**; only move to Enterprise
  if the brief explicitly trips a trigger condition.

## 2. Risk assessment

Score the client against `risk-security-matrix.yaml` before any pricing
conversation. The resulting band determines the required security
instrument(s) — this feeds both the walk-away card (step 4) and the
worksheet's mobilisation/cadence inputs.

## 3. Calc — the three-number model

The full Cost-to-Serve (CTS) and build-value formulas are desk-only.
The SDR enters the deal into the worksheet using the published segment
rates and the published-floor table. The desk computes the actual CTS
and reports it back. The SDR does not derive a margin floor or compute
internal build cost — both are desk-only.

**Disclosure to the client** (one line, from
`clause-library/financing-disclosure.md`): "Deferring the build carries a
[uplift_pct]% financing component."

**Prepayment asymmetry (G11)**: discounts apply to `platform_portion`
only. On the recovery portion, the only available concession is reducing
or removing the financing uplift — recovery principal is never
discounted, because it is work already performed.

**Ceiling calculation (G12)**: applied by the desk. The SDR sees the
binding value of `min(cadence_table_ceiling, max_give_aed)` reported in
the worksheet; they don't compute it.

**Term selection**: build value ≤ AED 8,000 with mobilisation paid → 12
months. Build value AED 8,000–20,000 (typical boutique brokerage) →
**24 months**. Build value > AED 20,000 → 24–36 months, mobilisation
mandatory (never waived at this scale).

**Option structure**: **two options, never three.** Option A =
mobilisation paid, lower recurring cost. Option B = zero upfront — **this
is currently WITHDRAWN** (do not offer it; do not construct a third
tier). The desk plugin has the full withdrawal reason and the
reserve-rebuild trigger.

## 4. Exposure and walk-away card

Before any pricing conversation with the client: the desk computes all
three exposures (`07-protection/exposure/exposure-model.md`) and
completes the one-page walk-away deal card
(`07-protection/walkaway/deal-card.template.md`) — G21, G22. The SDR
sees the resulting published figures in the worksheet.

## 5. Gate check

Run all 53 gates (G1–G41 commercial, G42–G45 plugin-conversion, G46–G52
signature, G53 approval-record) against the completed worksheet and
write `02-calc/gate-report.md`. **If any gate fails, stop.** Reduce scope
or run the concession ladder properly (`concession-ladder.yaml`) — never
discount around a failed gate.

## 6. Draft

Once `gates_passed: true`: render each proposal section (§01–§13, see
`templates/proposal/_section-map.md`) into
`03-draft/{PROPOSAL-REF}_RevN/`. Pull tax/legal/edition wording verbatim
from `clause-library/` — never paraphrase.

## 7. QA checklist and brand QA

Complete `04-review/qa-checklist.md` and `04-review/brand-qa-checklist.md`.
Confirm every entry in `verbal-promises.md` is reflected, every clause
requiring counsel review carries its flag, no forbidden phrase appears
anywhere in the draft, and brand tokens are used only from
`brand/tokens/`.

## 8. Human review

The approval-gate skill runs at the end of step 8 (see Part 1 of
`skills/approval-gate/SKILL.md`). The named approver produces
`05-approval/approval-record.yaml` with a SHA-256 binding to the frozen
PDF. No proposal is sent without that record.

## 9. Issue

The signature-dispatch skill (step 9) calls Zoho Sign using the approval
record. Move the approved draft to `04-issued/{PROPOSAL-REF}_RevN/`
immutable once the envelope is sent. A correction is a new revision,
never an in-place edit.
