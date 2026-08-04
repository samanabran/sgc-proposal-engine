<!--
Section 10 — Commercial Terms (v2)
Source: pricing-worksheet.yaml (assembly), clause-library/{vat-uae,
vat-gross-up, financing-disclosure, payment-cadence}.md
Every figure MUST match the worksheet exactly. TWO options only — never
three, and Option B (zero mobilisation) is currently withdrawn.

VAT disclosure is OMITTED from this section by default (per user
decision 2026-08-04) — no "exclusive of VAT" line, no vat-uae.md /
vat-gross-up.md text, unless the client or SDR explicitly asks about tax
treatment. When asked, use both clauses verbatim (they are a pair, never
one without the other) and record the origin per fabrication-rules.md.
The MSA (§C.6) and Order Form always carry the accurate, binding VAT
position and the gross-up right regardless of what this section says —
this section's silence never overrides or waives that.
-->

# Commercial Terms

## Pricing summary

| | Option A — mobilisation paid |
|---|---|
| Mobilisation (33% of build value) | AED [assembly.option_a.mobilisation_aed] |
| Recurring subscription | AED [assembly.option_a.subscription_aed]/mo |
| Year 1 total | AED [assembly.option_a.year1_client_cost_aed] |

## Payment cadence

<!-- clause-library/payment-cadence.md, filled with the selected cadence -->

## Financing disclosure

<!-- Include only if deferred_aed > 0. clause-library/financing-disclosure.md, verbatim -->

## Knowledge version

Priced against knowledge layer version [knowledge_version_used, from
manifest.yaml] — see repository `CHANGELOG.md`.
