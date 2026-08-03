# Clause: VAT Gross-Up

**Purpose**: protect SGC against the cost of a future mandatory VAT
registration by disclosing upfront that VAT will be added if and when
registration happens, rather than absorbing it silently.
Registration triggers: `pricing/policy.yaml: vat.mandatory_threshold_aed`
(AED 375,000 taxable supplies, rolling 12 months) or voluntary
registration above `vat.voluntary_threshold_aed` (AED 187,500). Late
registration carries a penalty of `vat.late_registration_penalty_aed`
(AED 10,000) plus retroactive liability from the date registration became
mandatory.

**requires_counsel_review**: false.

**When mandatory**: every proposal, always — this is not optional or
deal-specific. Pairs with `vat-uae.md`.

**When it must NOT be used**: never omit it while `vat.registered: false`.

---

## Approved verbatim text

> Should SGC TECH AI become VAT-registered during the term, VAT at the
> prevailing rate will be added to invoices issued from the effective date
> of registration in accordance with UAE law.
