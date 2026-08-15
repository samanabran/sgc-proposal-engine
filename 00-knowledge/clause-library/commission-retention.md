# Clause: Commission Retention (Clawback Reserve)

**Purpose**: protect SGC against paying out commission on cash that is
later reversed — refund, chargeback, non-delivery termination, or a
financed structure that never completes collection. Mirrors the build
principal protection in [[clawback]] (`clause-library/clawback.md`), but
on the internal commission line rather than the client-facing recurring
fee.

**Provenance note (RULE V / RULE 1):** the 14% combined commission rate
(`commission_sales_pct` 7 + `commission_delivery_pct` 7) is documented at
`00-knowledge/pricing/business-cost-basis.yaml:27-29`. The 5% retention
figure is NOT independently documented elsewhere in this repo as of this
pass — it is introduced here per explicit instruction in the correction-pass
brief ("5% retention held for clawback... confirmed"). Flagged rather than
silently treated as pre-existing policy: if a different retention figure
is authoritative elsewhere (verbal agreement, individual contractor
agreement, etc.), that source overrides this document and this file needs
updating to match, not the reverse.

**requires_counsel_review**: **true** — specifically the netting mechanism
below. See "UAE wage-deduction law" note at the end; do not treat this
clause as enforceable as drafted until Legal confirms the netting language
survives review.

**This clause exists because of a defect pattern, not hypothetically.**
The correction-pass brief that produced this file states: *"A clause
referenced but not reproduced is the exact defect found in two
client-issued documents (§ VGE/MRD); do not repeat it internally."*
Searched this repo for the specific catalogued instance of that defect
under that description and could not locate one — NOT FOUND as a discrete
entry in `00-knowledge/failure-modes/known-defects.md`'s 20-item list, nor
under an obvious filename in `02-clients/VGE-*` or `02-clients/MRD-*`. The
closest analog on record is defect #8 in that list ("No clawback... Caught
by G4/G16") and the general convention in `clawback.md` of reproducing
approved verbatim text rather than referencing it. This file follows that
convention: full operative text below, not a pointer to another document.

---

## When mandatory

Any commission paid on a deal where cash is collected over time rather
than 100% upfront — i.e. every milestone-based and every subscription-based
deal. There is no discretionary case for omitting retention on a deferred
structure; see `commission_released()` in `05-ops/pricing_engine.py` for
the enforced invariant (commission released can never exceed rate x
cash-in, at any point).

## Approved verbatim text

> Commission is earned on cash actually collected, not on contract value.
> Of the commission amount earned on each payment received, 5% (the
> "Retention") is withheld and held in reserve rather than paid out
> immediately, for the reasons and under the terms below.
>
> **1. Trigger events.** The Retention becomes payable to SGC (i.e. is
> released from reserve back to the company, not to the commissioned
> individual) upon any of the following: (a) the client terminates the
> engagement before the committed term for any reason other to SGC's
> material breach; (b) a payment already collected and commissioned upon
> is subsequently refunded, charged back, or reversed; (c) delivery of
> the committed scope does not occur and the client is entitled to a
> refund of amounts collected; (d) a commissioned deal is found, on audit,
> to have been commissioned on a payment that was never actually received
> by SGC (see `known-defects.md` item on unsourced/unverified figures —
> the same provenance discipline applies to commission triggers as to
> client-facing money figures).
>
> **2. Calculation method.** Retention is calculated per payment, not per
> deal: 5% of the commission amount earned on that specific payment is
> withheld at the time the payment is recorded, before any commission is
> released to the individual. This is a running per-payment reserve, not
> a lump sum computed once at deal close.
>
> **3. Recovery mechanism.** If a trigger event under §1 occurs, SGC's
> right to recover extends first to the Retention reserve held against
> that deal. If the Retention reserve is insufficient to cover the
> reversed amount, SGC's recovery right extends to netting against the
> individual's future commission earnings (see §5) — recovery is not
> sought as a direct deduction from base salary or wages.
>
> **4. Time limit.** The Retention on a given payment is held for 12
> months from the date that payment was collected, or until the end of
> the client's committed term, whichever is shorter. If no trigger event
> under §1 has occurred by that date, the Retention on that payment is
> released to the individual in full.
>
> **5. Right to net against future commission.** Where §3 recovery exceeds
> the Retention reserve, SGC reserves the right to net the shortfall
> against the individual's future commission earnings on other, unrelated
> deals, rather than seeking direct repayment. This right is limited to
> netting against commission (a variable, discretionary-timing payment),
> not against fixed wages.

---

## Flag for legal review — do not treat as adjudicated

UAE labour law restricts deduction from wages. This clause is drafted so
that recovery under §3/§5 operates against **commission** (netting against
future commission earnings), not as a deduction from base salary/wages —
because netting-against-future-commission is understood to be the
practical enforcement mechanism available, not post-exit recovery via
wage deduction, which the law constrains. **This is a flag, not a legal
conclusion.** The verbatim text above has NOT been reviewed by counsel.
Named reviewer role: **Legal**, escalated via **Commercial Desk** (the
convention used elsewhere in this repo, e.g. `subscription-guardrails.md`
gate ownership column) — do not issue this clause to any individual's
commission agreement until that review is complete.
