---
name: deal-card-review
description: Desk-only review skill. The approver reads the deal card, exposure calculation, and gate report together. Ratifies or returns reviewer notes.
version: 1.0.0
owner: approver (Ali Asghar Teli Muhammad Iqbal Teli)
position: desk-side; runs after walk-away-authoring
---

# deal-card-review

The approver's review skill. Reads the desk-completed deal card and
ratifies or returns reviewer notes. The SDR plugin never invokes this.

## When to use

- Trigger phrases: "review the deal card", "ratify the deal", "return reviewer notes", "approve the deal card", "open the gate report", "is the deal ready".

This skill is the only place the approver can act on a deal before
the approval record. The approver's name (literal: `Ali Asghar Teli
Muhammad Iqbal Teli`) is enforced.

## Bundled knowledge files to read, in order

1. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/deal-card.md`
2. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/exposure-calculator.yaml`
3. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/gate-report.md`
4. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/pricing-worksheet.yaml`
5. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/payment-plan-worksheet.yaml`
6. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/session-log.md` (confirmed fact ledger)
7. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/verbal-promises.md`
8. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/manifest.yaml`
9. `knowledge/04-governance/approval-matrix.md` — sign-off levels
10. `knowledge/04-governance/escalation-triggers.md` — when to abort vs. escalate
11. `knowledge/07-protection/abort/abort-criteria.md` — 7 triggers

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/04-review/reviewer-notes.md` — if returning for changes
- `manifest.yaml: review_log` — append every review action (date, decision, reason)

This skill **does not write the approval record**. That is the
approver's own action on `approval-gate` (step 12, the SDR-side skill
that produces the approval packet and waits for the approver's
decision). The decision lands in `05-approval/approval-record.yaml`.

## What it refuses

- **Missing walk-away card** — refuses to review a deal whose `deal-card.md` is missing or undated. Cite G22.
- **Missing exposure calculation** — refuses to review a deal whose `exposure-calculator.yaml` is missing or covers fewer than three exposures. Cite G21.
- **Missing gate report** — refuses to review a deal whose `gate-report.md` is missing or covers fewer than 53 gates.
- **Open `RESOLVE:` on an entity field that the contract requires** — refuses to review a deal with any open `RESOLVE:` on `client.legal_name`, `client.jurisdiction`, `client.trade_licence_number`, `client.registered_address`, or any field in `06-brand/entity/legal-identity.yaml`. Cite `escalation-triggers.md:35-44`.
- **Any absolute floor breach** — refuses to ratify a deal that breaches G8, G16, G18, G23, G35, G36, G38, G40. Per `PRECEDENCE.md`, no authority level overrides these. Cite the absolute floor.
- **Refuse risk band without a joint-sign-off exception** — refuses to ratify a deal in the refuse risk band (76+) unless founder + Commercial Desk have jointly signed the exception per `approval-matrix.md`. Cite G30.
- **Concession without logged compensators** — refuses to ratify a deal whose `manifest.yaml: escalations` does not have a matched AED value for every concession and compensator. Cite G14.
- **An approval record already exists for a different artifact** — refuses to ratify a new deal while an existing approval for the same client is in flight. The existing approval must be voided (per G53 re-approval triggers) before a new one is produced.

## What it checks (the approver's checklist)

1. **Three numbers on the deal card** — List at 35% target, Target floor at 30%, Absolute floor at 25%. The numbers must match the reservation pricing calculation in `07-protection/walkaway/reservation-pricing.md`.
2. **Top three compensators** — named, with the AED values the desk computed.
3. **Risk band and required instruments** — match the score in `risk-assessment.yaml` and the band table in `risk-security-matrix.yaml`.
4. **Abort criteria** — none of the 7 triggers in `07-protection/abort/abort-criteria.md` are tripped.
5. **Gate report** — every gate G1–G53 has a status (pass/fail) and a one-line reason. The internal-cost / margin-floor / cash-exposure gates have desk-only reasons. The plugin-conversion gates (G42–G45) and the signature gates (G46–G52) and the approval gate (G53) have their reasons.
6. **Fact ledger** — every client-attributed statement in the worksheet and the deal card has an origin tag.
7. **Verbal promises** — every row in `verbal-promises.md` is reflected in the deal card or the worksheet with classification (PRICED / DEFERRED / EXCLUDED).
8. **Portfolio cap** — peak cash exposure does not push aggregate above `07-protection/exposure/portfolio-limits.yaml: max_aggregate_peak_cash_exposure_aed`.
9. **Edition and upgrade policy** — matches `editions.yaml: community.upgrade_policy` (Community) or carries the Enterprise exclusion list verbatim.
10. **VAT position** — gross-up clause from `clause-library/vat-gross-up.md` is verbatim in the MSA §C.6. No "VAT inclusive", "VAT exempt", "free zone exempt", or TRN field.

## What it produces

- `04-review/reviewer-notes.md` (if returning for changes) — bullet list of required changes, each citing a specific file:line and the gate or guardrail that demands the change.
- `manifest.yaml: review_log` (if ratifying) — `[{ date, reviewer: "Ali Asghar Teli Muhammad Iqbal Teli", decision: "ratify" | "return_for_changes", reason: "..." }]`

## Escalation path

- **Absolute floor breach** — refuse to ratify; the SDR's `subscription-pricing` must re-run with reduced scope or a different structure. The approver may not override.
- **Refuse risk band** — refuse to ratify without founder + Commercial Desk joint sign-off. The deal is aborted per G30; an exception requires both signatures.
- **Reserve rebuild trigger** — the desk's `walk-away-authoring` may lower the `months_24` financing uplift from 0.18 to 0.12 only when reserves reach 3 months opex. The approver ratifies that change after the trigger is satisfied.
- **Open Tier 1 RESOLVE:** — refuse to ratify until the SDR returns to intake and closes the field.

## Sole approver

`Ali Asghar Teli Muhammad Iqbal Teli` — Company Manager, Scholarix
Global Consultants FZCO / SGC TECH AI. No delegation, no alternate, no
"approved by agent on behalf of." This is enforced at
`approval-gate` and again at `signature-dispatch`. This skill's
reviewer's decision lands in `manifest.yaml: review_log`; the formal
approval record is the approver's own action.

## What this skill does NOT do

- It does not write the approval record. The approval record is the approver's own decision, written after this review.
- It does not send the proposal. `signature-dispatch` does, after the approval record exists.
- It does not change the canonical MSA template. The desk's `redacted-derivative-release` does, via the appropriate plugin.
