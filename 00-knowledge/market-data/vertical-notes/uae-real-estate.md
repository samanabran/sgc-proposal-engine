# UAE Real Estate — Vertical Note

Read before pricing a real estate brokerage, agency, or developer deal
(the VGE-vongeyern-realestate live example is this vertical — see
`02-clients/VGE-vongeyern-realestate/`).

## Market band

`market-data/benchmarks.yaml: industry_pricing_bands_aed.real_estate_developer`
— MARKET BENCHMARK, pricing playbook Part 7: 10–20 weeks, AED 180,000–520,000
implementation, AED 950,000+ as a premium-tier reference ceiling. This is a
**developer**-scale band (leads, units, finance, service). A boutique
brokerage is smaller — size against `pricing/policy.yaml: segments` by user
count, not against this developer band; use the band only as an upper
sanity-check, not a floor.

Distinguishing note from the source table: "installments, property-specific
reporting" is the recurring differentiator that drives scope beyond a
generic Sales/CRM/Accounting build — see below.

## Regulatory and portal context

- **RERA (Real Estate Regulatory Agency)** and, in Dubai specifically,
  **DLD (Dubai Land Department)** are the relevant regulators for brokerage
  licensing, listing compliance, and trust account handling. A client
  operating under RERA/DLD rules may require:
  - Broker/agent license number tracking against listings and deals.
  - Trust account (escrow) segregation for client funds — this is an
    **accounting configuration** requirement (chart-of-accounts and
    approval-rule scope), not a CRM feature. Scope it under
    `hour-lookup.yaml: finance_setup`, not `sales_crm_configuration`.
  - Commission calculation and clawback logic tied to deal stage, not
    invoice date — see `clause-library/clawback.md` for the standard
    contractual treatment.
- **Portal API gating**: property portals (e.g. Bayut, Property Finder, and
  DLD's own listing feeds) typically require the listing brokerage to be
  independently verified/licensed before granting API/feed access.
  Integration scope in a proposal must note this as a **client-side
  dependency and assumption**, not something SGC can guarantee timing on —
  this belongs in §04 As-Is and §07 Options & Inclusions with an explicit
  assumption, per Commercial Rule 9.
- **TRN (Tax Registration Number)**: real estate transactions (sale,
  lease) have their own VAT treatment nuances (e.g. bare land vs. commercial
  vs. residential supply can differ) distinct from the general services VAT
  handling in `uae-tax-vat.md`. Flag any transaction-type-specific VAT
  question for legal review — do not resolve it inside the proposal.

## What this means for a proposal

- Expect `finance_setup` hours to run toward the high end of the
  `hour-lookup.yaml` range (trust accounting, commission-linked journals)
  even for a small user count.
- Installments and property-specific reporting are real scope, not a
  "nice to have" — if the client brief mentions payment plans to end
  buyers, this is a distinct requirement from the subscription financing
  terms SGC itself offers the client (`policy.yaml: financing_uplift`).
  Do not conflate the two in the calc worksheet or the draft.
- License/portal dependencies are assumptions to state explicitly, not
  risks to price around silently.

This note is operating guidance, not legal or regulatory advice. RERA/DLD
rules and portal policies change; escalate rather than guess on anything
license- or compliance-specific.
