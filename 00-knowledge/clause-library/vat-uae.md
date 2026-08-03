# Clause: VAT (UAE) — v2, corrected

**Purpose**: state SGC's actual VAT registration status accurately. SGC
TECH AI (Scholarix Global Consultants FZE) is **not** currently registered
for UAE VAT and holds no TRN as of this version — see
`pricing/policy.yaml: vat.registered: false`. Charging VAT while
unregistered is illegal; claiming free-zone exemption is factually wrong
(Designated Zone treatment applies to goods, not services — see
`market-data/vertical-notes/uae-tax-vat.md`).

**requires_counsel_review**: false (fact-stating clause, not a legal
construction — but re-verify against `policy.yaml: vat.registered`
immediately before every issue, since this is the one fact in the repo
most likely to change without the clause library being updated in step).

**When mandatory**: every proposal, always, while `vat.registered: false`.

**When it must NOT be used**: the moment SGC obtains a TRN. At that point
this clause is replaced by a VAT-registered version (not yet drafted —
`RESOLVE` once registration happens) and every proposal must charge VAT
from the effective registration date.

---

## Approved verbatim text

> All fees are quoted in AED. SGC TECH AI is not currently registered for
> UAE VAT, and no VAT is charged on this proposal.

---

## FORBIDDEN WORDING

Never write, and never say aloud on a call:

- **"No VAT applies — we operate from a free zone."** Factually wrong.
  Free zone status does not exempt services from VAT; only specific
  Designated Zone goods transactions get special treatment. See
  `market-data/vertical-notes/uae-tax-vat.md`.
- **"SGC TECH AI is VAT-registered."** Currently false. Do not say this
  even if a client assumes it, even to sound more established.

Every proposal using this clause must also carry `vat-gross-up.md` — the
two are a pair, not alternatives.
