# Exposure Model

Compute all three for every option in the worksheet (G21), before the
walk-away card is produced.

## Contractual exposure

```
contractual_exposure(t) = build_value_aed - cumulative_recovered(t)
```

Protected by the clawback clause — if the client terminates, the
unrecovered balance becomes due immediately (`clause-library/clawback.md`).
This number only matters if the clawback is actually enforceable and
collected; it is not a substitute for cash exposure below.

## Cash exposure

```
cash_exposure(t) = max over t of [cumulative_cost(t) - cumulative_collected(t)]
```

This is the number that actually threatens SGC's runway. **Build labour
must follow the actual delivery curve, not a straight line** — roughly
two-thirds of implementation effort lands in the first three weeks of a
typical boutique brokerage build (discovery, configuration, migration
front-load the calendar; QA, training, and hypercare are lighter and
later). Straight-lining cost across the term understates the peak —
compute cost against the real week-by-week delivery curve, then find the
maximum gap against what's been collected by that same week.

Protected by mobilisation (paid before cost accrues) and payment cadence
(collections arriving frequently enough that the gap never grows
unchecked). This is the exposure `07-protection/exposure/portfolio-limits.yaml`
caps in absolute AED terms.

## Economic exposure

```
economic_exposure(t) = internal_build_cost_to_date(t) - value_delivered_and_invoiced(t)
```

Protected by staged delivery: don't release configuration for a later
phase until the invoices covering the earlier phase have actually
cleared (`risk-security-matrix.yaml: instrument_types.self_help:
staged_configuration_release`).

## Reporting

Record all three, for both Option A and (where still relevant) Option B,
in the worksheet's exposure block. `walkaway/deal-card.template.md` shows
only the cash exposure peak on the one-page card — that's the number a
walk-away decision hinges on in practice — but all three are logged in
`02-calc/pricing-worksheet.yaml` for the gate report.
