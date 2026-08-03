<!--
Section 10 — Commercial Terms
Source: 02-calc/pricing-worksheet.yaml (assembly), clause-library/{vat-uae, financing-disclosure}.md
This is the section a client will scrutinize hardest. Every figure here
must match the worksheet exactly — no rounding beyond what the worksheet
itself rounds to.
-->

# Commercial Terms

## Pricing summary

| | Option A (mobilisation) | Option B (zero mobilisation) |
|---|---|---|
| Mobilisation | AED [option_a.mobilisation_aed] | AED 0 |
| Recurring subscription | AED [option_a.subscription_aed]/mo | AED [option_b.subscription_aed]/mo |
| Year 1 total | AED [option_a.year1_client_cost_aed] | AED [option_b.year1_client_cost_aed] |

All figures exclusive of VAT — see below.

## Payment schedule

[Milestone-based schedule for mobilisation, per runbook §5 model-specific
notes — e.g. 40/40/20 default for fixed-fee delivery once discovery is
complete; monthly in advance for the recurring subscription line.]

## VAT

<!-- clause-library/vat-uae.md, verbatim -->

## Financing disclosure

<!-- Include only if Option A/B involves a financing uplift.
clause-library/financing-disclosure.md, verbatim -->

## Knowledge version

This proposal was priced against knowledge layer version
[knowledge_version_used, from manifest.yaml] — see repository `CHANGELOG.md`.
