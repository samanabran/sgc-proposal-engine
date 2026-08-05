# Financing Amortisation — F1–F4

Source: `.omc/plans/pricing-engine-cost-class-model.md` Rev.2 §H (K-3 —
verified correct, unchanged since Rev.1). Filed here as a governed
reference so a future reader doesn't have to re-derive it from a client
worksheet by hand. Worked against Kallat's real figures
(`02-clients/KP-kallat-properties/02-calc/pricing-worksheet.yaml:70-76`):
`financed_remainder_aed: 73,030`, `uplift_pct: 0.18`,
`recovery_total_aed: 86,175`, `recovery_monthly_aed: 3,591`.

## F2 — flat vs. annualised, tested against real figures

Flat-on-principal test: `73,030 × 1.18 = 86,175` — **exact match** to the
worksheet. **Confirmed: the current model is flat-on-principal**, a
one-time markup on the financed remainder, divided evenly over the term
— not a compounding amortisation. Residual = 0; no ambiguity.

## F1 — proper amortisation comparison

Solving `73,030 = 3,591 × [1 − (1+i)^−24] / i` for the monthly rate `i`
implied by the actual cash flows: **i ≈ 1.37%/month**, i.e. **≈16.4%
nominal annual / ≈17.8% effective APR** — modestly *below* the headline
18%.

Cross-check: a truly amortising 18%-APR loan (1.5%/mo) over the same
24-month term would require monthly payment = `73,030 / 20.03` = **AED
3,646** (total finance charge AED 14,474) — **more** than Kallat is
actually being charged (AED 13,145 total, at AED 3,591/mo).

**Finding**: the flat-on-principal method is **client-favourable**
relative to a true 18%-APR amortisation for this term length. Reported
as such, not softened — "uncited" (the 18%/6% uplifts appear in no xlsx
sheet nor any of the 12 Commercial Rules, only in `policy.yaml:
financing_uplift`, a repo-native gate-policy decision from the "v2
hardening pass") is not the same as "too high."

## F3 — derived rate = cost_of_capital + risk_premium(band)

**Cannot be computed.** No sourced cost-of-capital figure exists
anywhere in this repo — checked `00-knowledge/`, `_source-documents/`,
and both source PDFs for "cost of capital," "WACC," "overdraft rate":
zero matches. Per P5 (no unsourced benchmarks), this is not substituted
with an invented figure. **Open**, tracked in
`pricing-engine-cost-class-model.md` §L. Collapse trigger: SGC's actual
bank overdraft/credit-line quote.

## F4 — counsel flag

A deferred-payment structure carrying a flat interest-equivalent
component may constitute a credit arrangement under UAE consumer/
commercial finance rules. **This flag persists through internal
sign-off**, unresolved, per P10 — distinct from (not satisfied by)
`clause-library/financing-disclosure.md`'s existing client-facing
disclosure requirement. Client disclosure of the uplift is not the same
as counsel confirming the structure's legal character.

## Commission-impact coefficient — also open, no source exists

No commission/sales-comp-plan document exists anywhere in this repo. Per
P5, no coefficient is invented. See
`pricing-engine-cost-class-model.md` §G/§L.
