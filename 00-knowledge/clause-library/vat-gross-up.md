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

**When mandatory**: in the MSA (§C.6), always — this is not optional or
deal-specific, and is never omitted there regardless of what the sales
proposal says. Pairs with `vat-uae.md`.

**In the sales proposal specifically** (per user decision 2026-08-04):
omitted by default, same as `vat-uae.md` — include only if the client or
SDR explicitly asks about tax treatment, and always paired with
`vat-uae.md`, never alone.

**When it must NOT be used**: never omit it from the MSA while
`vat.registered: false`. The gross-up right this clause protects (adding
VAT to invoices from the date SGC registers, without needing to
renegotiate price) must exist in the binding contract regardless of
proposal-level silence.

---

## Approved verbatim text

> Should SGC TECH AI become VAT-registered during the term, VAT at the
> prevailing rate will be added to invoices issued from the effective date
> of registration in accordance with UAE law.
