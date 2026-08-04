---
name: subscription-pricing
description: Steps 3–8 of the SDR pipeline. Computes the pricing worksheet, payment-plan worksheet, risk assessment, exposure, walk-away card, and gate check for a deal whose intake is complete.
version: 1.0.0
owner: SDR
position: 3-8
---

# subscription-pricing

The pricing, exposure, walk-away, and gate-check stages. Runs after intake and risk assessment, before drafting.

## When to use

- Trigger phrases: "price this", "build the worksheet", "run the numbers", "what does this cost", "compute the exposure", "do the gate check", "make the deal card", "build the cash exposure".

If intake is incomplete, this skill will refuse (see below). If a draft is requested, route to `proposal-drafting`.

## Position in step gate

Steps 3 through 8. The fixed sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** unless the previous skill (`proposal-intake`) has produced:

- `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/client-brief.yaml`
- `<workspace>/sgc_proposal_engine/sgc-proposals/<CLIENT-CODE>/00-intake/verbal-promises.md`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/session-log.md`

With all Tier 0 fields answered or escalated per `sufficiency-rules.yaml: tier_0`.

This skill **does not produce the draft** — that is `proposal-drafting` (step 9+). The pricing work has to be complete and the gate report clean before drafting can start.

## Bundled knowledge files to read, in order

1. `knowledge/policy.yaml` (sanitized derivative) — segments, overlays, gates, VAT
2. `knowledge/rate-card.yaml` (verbatim) — role rates, forbidden_rates
3. `knowledge/editions.yaml` (verbatim) — Community vs Enterprise, exclusions
4. `knowledge/hosting.yaml` (sanitized derivative) — published tier list prices
5. `knowledge/payment-plans.yaml` (sanitized derivative) — cadence table, hard caps
6. `knowledge/phase2-catalogue.yaml` (sanitized derivative) — phase-2 items
7. `knowledge/concession-ladder.yaml` (sanitized derivative) — concession/compensator names
8. `knowledge/hour-lookup.yaml` (verbatim) — work-package hours
9. `knowledge/risk-security-matrix.yaml` (verbatim) — risk bands and instruments
10. `knowledge/published-floor-table.yaml` (new) — minimum quotable subscription per cell
11. `knowledge/commercial-rules/subscription-guardrails.md`, `payment-plan-guardrails.md`, `protection-guardrails.md` — G1–G41 statements
12. `knowledge/guardrails-g42-g53.yaml` (mirror) — G42–G45, G53

The internal cost-to-serve (CTS) formula, the absolute margin floor, the
internal AED/h, and the cash-exposure caps live in the desk plugin.
The SDR enters the deal, the desk computes and returns the
desk-side values for the worksheet.

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/pricing-worksheet.yaml`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/payment-plan-worksheet.yaml`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/risk-assessment.yaml`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/exposure-calculator.yaml`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/deal-card.md`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/gate-report.md`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/manifest.yaml` (updates)

## What it refuses

- **Incomplete intake** — refuses if any Tier 0 field is missing or unresolved. Cite `sufficiency-rules.yaml: tier_0.on_incomplete`.
- **Out-of-order invocation** — refuses if `proposal-intake` has not produced its three files. Cite `step-gate.md` step 1.
- **Rates not on the card** — refuses to accept any rate that is not on `rate-card.yaml`. Forbidden rates (AED 690, AED 550) fail immediately. Cite G9 and `fabrication-rules.md`.
- **Below published floor** — refuses to write a subscription below the corresponding cell in `published-floor-table.yaml` (G42). Emits `RESOLVE:` and routes to desk rather than proceeding.
- **Discount on the recovery portion** — refuses any discount applied to the recovery portion of a subscription (G11). Cite `clause-library/post-recovery-continuation.md` and the G11 row of `payment-plans.yaml`.
- **Insufficient mobilisation** — refuses any deal whose mobilisation is below 33% of build value without a logged concession (G3, G34). The desk may approve a logged concession via the deal card.
- **VAT charge or claim** — refuses to write "VAT inclusive", "VAT exempt", "free zone exempt", or any TRN field (G35, G45). The MSA §C.6 carries the gross-up clause.
- **Community misdescribed** — refuses to call Community "Enterprise" anywhere in the proposal (G36, G44).
- **Any gate failure left unresolved** — refuses to mark `gates_passed: true` while any of G1–G53 is failing. Cite `step-gate.md` step 8.

## Escalation path

- **Below published floor** — `RESOLVE: <cell> = <proposed_aed>, floor = <floor_aed>`. The desk-side `published-floor-authoring` skill may lower the floor (or refuse) and reply.
- **Tier 1 still `RESOLVE:`** — carry forward into the proposal as a `RESOLVE:` placeholder, per `sufficiency-rules.yaml: tier_1`. The skill flags each open Tier 1 in the gate report and the approval request.
- **Rate not on the card** — escalate to `walk-away-authoring` skill (desk). Cite AGENTS.md absolute rule.
- **Any absolute floor breached** (G8, G16, G18, G23, G35, G36, G38, G40) — stop, log to `manifest.yaml: escalations`, and route to the desk. Per `PRECEDENCE.md`, no authority level overrides these.
- **Concession** — name the concession and the compensators in `manifest.yaml: escalations`; the desk computes the AED balance and the desk signs the change.
- **A vague request** ("proposal for a Dubai brokerage, 8 users") — refuse to price. Route back to `proposal-intake`. The single most common refusal of this skill is "I cannot price without the Tier 0 batch answered. Intake is step 1; pricing is steps 3–8; out-of-order is refused."

## Concession behaviour

A concession is named by the SDR; the desk computes and signs the AED
balance. The SDR never writes a `value_formula` field into a deal card
or worksheet. The `concession-ladder.yaml` derivative the SDR reads
carries names, effect descriptions, the forbidden list, and the
procedure — not the formula values. (Source: `concession-ladder.yaml`
in this plugin's `knowledge/`.)

## Acceptance check (self-test)

Before allowing `proposal-drafting` to run, this skill must be able to answer YES to each:

1. `manifest.yaml: gates_passed: true`?
2. `manifest.yaml: walkaway_card_produced: true` with a date strictly before the first pricing conversation?
3. `02-calc/gate-report.md` covers all 53 gates with pass/fail and one-line reason?
4. Every figure on the worksheet traces to `rate-card.yaml` or a published list price (G43)?
5. Mobilisation ≥ 33% (G3) and covers any third-party upfront cost (G34)?
6. Cadence ≥ quarterly in advance (G33)?
7. No forbidden phrase in any of the six files (G35, G44, G45)?
8. No RESOLVE open in any figure field that the deal card requires?
