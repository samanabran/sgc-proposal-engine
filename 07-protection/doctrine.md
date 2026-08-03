# Protection Doctrine

SGC TECH AI currently operates with liquid reserves of AED 7,000–14,000
against monthly opex of AED 6,000–7,000 — 1 to 2 months' runway. This is
not a footnote; it is the binding constraint behind every gate in
`00-knowledge/commercial-rules/protection-guardrails.md`. A single
mispriced deal can consume a meaningful fraction of the company's entire
cash buffer.

## The three exposures

Every deal carries three distinct, separately-protected exposures:

- **Contractual exposure** — the unrecovered build principal if a client
  terminates early. Protected by the clawback clause (G4, G16).
- **Cash exposure** — the peak point, over the life of the deal, where
  SGC has spent more delivering than it has collected. Protected by
  mobilisation and payment cadence (G3, G33, G34). This is the exposure
  that actually threatens the company's runway — a deal can be
  contractually fully protected by a clawback and still bankrupt the
  business if the cash timing is wrong.
- **Economic exposure** — the unrecovered internal delivery cost (labour
  at internal rate, not billed rate) at any point in the build. Protected
  by staged delivery — not releasing later-phase configuration until
  earlier invoices clear (`risk-security-matrix.yaml: instrument_types.self_help`).

See `exposure/exposure-model.md` for the computation, and
`walkaway/deal-card.template.md` for how this becomes a one-page
pre-conversation artifact.

## Why cash exposure, specifically, is the priority

Margin percentage is a health metric measured at the end of a deal. Cash
exposure is a solvency metric measured at every point *during* one. A
72%-margin deal can still fail the company if its cash trough exceeds
reserves before the margin is ever realized. `exposure/portfolio-limits.yaml`
sets absolute AED ceilings, not percentages, precisely because a
percentage of a shrinking number gives false comfort.

## The abort principle

`abort/abort-criteria.md` lists conditions under which walking away from
a deal is the *correct* outcome, not a failure of salesmanship. G30
states this explicitly: an SDR who aborts on a triggered criterion is not
penalised for the lost deal. The alternative — pushing a deal through
that trips an abort criterion — risks the company's actual survival, not
just one quarter's numbers.
