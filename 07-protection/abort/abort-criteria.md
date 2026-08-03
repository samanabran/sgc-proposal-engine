# Abort Criteria

**These are absolute (G30). An SDR who walks away from a deal on any of
these triggers acted correctly and is not penalised for the lost deal —
pushing a deal through past one of these is the failure, not walking
away.**

A deal must be aborted (or returned to intake/risk-assessment for
re-scoping — not silently pushed through) when:

- The client's risk score lands in the `refuse` band (76+,
  `pricing/risk-security-matrix.yaml`) and no re-scoping brings it down —
  e.g. an expired trade licence, or a default on the `payment_history_sgc`
  weight.
- The deal cannot clear `absolute_margin_floor` (25%) at any defensible
  scope — see `walkaway/reservation-pricing.md` absolute floor.
- Portfolio limits would be breached — `07-protection/exposure/portfolio-limits.yaml`
  `max_peak_cash_exposure_single_deal_aed`, `max_aggregate_peak_cash_exposure_aed`,
  or `max_concurrent_deferred_builds` — and no available compensator
  (`concession-ladder.yaml`) brings the deal back inside them.
- The client requires a zero-mobilisation structure and will not accept
  any alternative — Option B is withdrawn (`payment-plans.yaml: withdrawn`)
  and there is currently no substitute that clears the cash-exposure caps.
- The client insists on cash-below-quarterly cadence
  (`payment-plans.yaml: min_cadence_current`) without the security
  instruments the risk band requires.
- The client requires SGC to state a VAT-registered status, charge VAT,
  or claim a free-zone VAT exemption — none of which are legally
  available to SGC currently (G35).
- The client requires Enterprise-edition capability commitments while
  refusing to fund the Enterprise mobilisation floor (G40).

## What "abort" means in practice

Not necessarily "never work with this client" — often it means returning
to intake with a smaller, differently-structured, or deferred-start deal
that does clear the criteria above. Log the abort and its reason in
`manifest.yaml: escalations` regardless of outcome, so the pattern is
visible in the monthly portfolio review.
