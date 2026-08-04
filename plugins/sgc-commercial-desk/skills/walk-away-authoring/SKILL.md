---
name: walk-away-authoring
description: Desk-only skill. Authors the per-deal walk-away card and the desk-side cost-to-serve / margin arithmetic. Computes the figures the SDR plugin never sees.
version: 1.0.0
owner: Commercial Desk
position: desk-side; runs at step 7 of the proposal pipeline
---

# walk-away-authoring

The desk-side counterpart to `subscription-pricing`. The SDR enters the
deal; the desk computes the desk-only numbers (CTS, internal build
cost, margin floor, peak cash exposure, reservation pricing) and
returns them to the worksheet.

## When to use

- Trigger phrases: "compute the walk-away card", "fill the deal card", "compute CTS", "what's the margin floor", "what's the peak cash exposure", "what's the reservation price", "log the desk-only numbers", "compute the ceiling".

If the SDR has not produced an intake + risk assessment, refuse. If
the deal is below published floor, route to `published-floor-authoring`
first.

## Position in the workflow

Step 7 of the proposal pipeline (after pricing, exposure, walk-away).
Runs in the desk plugin. The desk's RBAC ensures only the approver
runs this; the SDR plugin never invokes it.

## Bundled knowledge files to read, in order

1. `knowledge/policy.yaml` (full, desk-only) — segments, overlays, gates, cost_to_serve, financing_uplift
2. `knowledge/hosting.yaml` (full) — list prices, AWS pass-through, cost-basis note
3. `knowledge/payment-plans.yaml` (full) — cadence table, hard_caps, withdrawn structures
4. `knowledge/phase2-catalogue.yaml` (full) — phase-2 items with marginal costs
5. `knowledge/concession-ladder.yaml` (full) — concession and compensator value_formulas
6. `knowledge/risk-security-matrix.yaml` (full) — bands and instruments
7. `knowledge/07-protection/walkaway/deal-card.template.md` — the per-deal template
8. `knowledge/07-protection/walkaway/reservation-pricing.md` — floor formula
9. `knowledge/07-protection/exposure/exposure-model.md` — three-exposure formulas
10. `knowledge/07-protection/exposure/portfolio-limits.yaml` — absolute caps, runway
11. `knowledge/04-governance/approval-matrix.md` — sign-off levels
12. `knowledge/04-governance/escalation-triggers.md` — when to abort vs. escalate
13. The client's `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/pricing-worksheet.yaml` (the SDR-completed worksheet)

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/deal-card.md` — completed walk-away card with desk-only figures filled
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/exposure-calculator.yaml` — completed three-exposure calculation
- `<workspace>/sgc-proposals/<CLIENT-CODE>/02-calc/gate-report.md` — G1–G53 results, with desk-only pass/fail reasons
- `<workspace>/sgc-proposals/<CLIENT-CODE>/manifest.yaml: escalations` — every concession and compensator with AED values

The SDR plugin never reads these completed files; the desk returns
the published figures (the gated view) to the worksheet.

## What it refuses

- **Missing intake** — refuses if the SDR has not produced the three intake files. Cite `step-gate.md` step 1.
- **Missing risk assessment** — refuses if `02-calc/risk-assessment.yaml` is not produced. Cite `step-gate.md` step 3.
- **Pricing worksheet incomplete** — refuses if any worksheet section is blank or `RESOLVE:` on a figure field. Cite `step-gate.md` step 4.
- **Below published floor** — refuses to author a deal card for a deal below the corresponding cell in the SDR plugin's `published-floor-table.yaml` unless the desk's `published-floor-authoring` skill lowers the floor and re-issues the file. Cite G42.
- **Above any absolute floor breach** — refuses to author a deal card that breaches G8, G16, G18, G23, G35, G36, G38, G40. Per `PRECEDENCE.md`, no authority level overrides these. Cite the absolute floor.
- **Concession without a compensator** — refuses to log a concession whose compensator sum is below the concession value. Cite G14.
- **Reserve-triggered withdrawal** — refuses to author a deal card when the structure would be the withdrawn `option_b_zero_mobilisation`. Cite `payment-plans.yaml: withdrawn.option_b_zero_mobilisation.status: suspended`.

## Margin-floor enforcement (desk-only)

The desk computes:

- `target_gross_margin` = 35% (G8 / G31 / G23)
- `min_gross_margin` = 30% (G8)
- `absolute_margin_floor` = 25% (G23) — no authority level overrides this
- `max_total_give` = `0.10 × contract_value` (G13, hard cap)
- `combined_give_plus_guarantee` = `0.12 × contract_value` (G31, hard cap)

The desk refuses to author a deal card where the worst-case margin
(concessions + maximum guarantee-credit exposure, applied together)
is below 25%. (Source: G31.)

## Reservation pricing

`revenue_floor(margin) = (build_cost + CTS × term) / (1 − margin)`. Run twice — at 0.35 target and at 0.25 absolute floor. Both values appear on the deal card under "three numbers" (List / Target / Absolute). The deal card is a one-page document; full template at `07-protection/walkaway/deal-card.template.md`.

## Walk-away abort criteria

Per `07-protection/abort/abort-criteria.md`, the deal is aborted if any of:

- Risk score ≥ 76 (refuse band)
- Absolute margin floor fails (worst-case below 25%)
- Portfolio limits breached (per `07-protection/exposure/portfolio-limits.yaml`)
- Zero mobilisation in a deal that doesn't have a documented withdrawal pattern
- Cash exposure below quarterly collected amount
- A VAT-registered claim (G35)
- Enterprise edition without mobilisation covering full annual licence (G40)

A walk-away on a triggered abort criterion is the correct outcome
(G30). The desk does not negotiate around these.

## Escalation path

- **Absolute floor breach** — refuse and route to the approver. The approver may not override; the only remediation is scope or structure change.
- **Concession that breaches a hard cap** — refuse and route to the approver with the computed AED balance; the approver may ratify the change (logged to `manifest.yaml: escalations`) or reject the concession.
- **Portfolio cap breach** — refuse; new deferred-payment structures pause per `07-protection/monitoring/graduated-response.md`.
- **Refuse risk band (76+)** — abort per G30, or escalate to founder + Commercial Desk jointly for an exception. Per `approval-matrix.md`, an exception requires joint sign-off.
- **Reserve rebuild trigger** — the desk may lower `months_24` financing uplift from 0.18 to 0.12 only when liquid reserves reach 3 months opex, per `policy.yaml: financing_uplift.review_trigger`. Document the change in `manifest.yaml: escalations`.

## What this skill does NOT do

- It does not write the proposal §01–§13 prose. The SDR's `proposal-drafting` does that.
- It does not approve a deal. The approver does that, via `approval-gate` (step 12, the SDR-side skill that the approver is the only one who can sign off on).
- It does not change the canonical MSA. The deal card is a per-deal artefact; the MSA template is updated via the desk's `redacted-derivative-release` skill (which authorises a new `contracts/msa-sla.html` version).
- It does not write a covering email or call Zoho Sign. The `signature-dispatch` skill does that, after the approval record exists.

## Acceptance check (self-test)

Before allowing `proposal-drafting` (SDR-side) to render the proposal, this skill must be able to answer YES to each:

1. `02-calc/deal-card.md` is dated strictly before the first pricing conversation with the client (G22)?
2. Three reservation-pricing numbers (35% / 30% / 25%) are on the card?
3. `02-calc/exposure-calculator.yaml` covers all three exposures (G21)?
4. `02-calc/gate-report.md` covers all 53 gates, with desk-only pass/fail reasons for the internal-cost/margin-floor gates?
5. `manifest.yaml: escalations` is current, with AED values for every concession and compensator pair (G14)?
6. The deal does not breach any absolute floor (G8, G16, G18, G23, G35, G36, G38, G40)?
7. The deal does not breach any portfolio cap (`07-protection/exposure/portfolio-limits.yaml`)?
8. The deal does not require a reserve-rebuild trigger that hasn't been satisfied?
