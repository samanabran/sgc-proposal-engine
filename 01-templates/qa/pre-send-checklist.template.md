# Pre-Send QA Checklist (v2) — copy to 02-clients/{client}/04-review/qa-checklist.md

## Calc integrity

- [ ] `00-intake/client-brief.yaml`, `02-calc/risk-assessment.yaml`, `02-calc/pricing-worksheet.yaml` all fully completed
- [ ] `02-calc/gate-report.md` exists and all 41 gates (G1–G41) plus `market_test`/`budget_test` show `pass: true`
- [ ] `manifest.yaml: gates_passed` is `true`, `knowledge_version_used` pinned
- [ ] Every number in the draft matches the worksheet exactly

## Scope, edition, and exposure integrity

- [ ] Every capability described in §06 has corresponding hours in `number_2_build.delivery_hours`
- [ ] `phase2_deferred` items appear in §07, not §06 — never sold both ways at once (`known-defects.md` #6)
- [ ] Edition (`community`/`enterprise`) declared and matches `client-brief.yaml`; if `community`, upgrade policy and capability exclusions are stated in §06, in writing (G36–G38)
- [ ] All three exposures computed and recorded (G21); walk-away deal card was produced before this draft existed (G22)

## Commitments

- [ ] `verbal_promises_logged: true`, every entry classified PRICED / DEFERRED / EXCLUDED and reflected accordingly in the draft
- [ ] Adoption clause included (G-series, `clause-library/adoption.md`)
- [ ] Clawback present on any deferred structure (G4, G16)
- [ ] Referral, if offered, is capped per `clause-library/referral-capped.md` — never uncapped

## Legal / tax

- [ ] VAT clause is `clause-library/vat-uae.md` verbatim — states SGC is **not** VAT-registered, charges **no** VAT
- [ ] `vat-gross-up.md` present
- [ ] No clause used outside the library; every clause flagged `requires_counsel_review: true` carries the flag and header, and is not treated as final text
- [ ] No named individual consultant promised as a guarantee (G27)

## Cover letter and cross-references

- [ ] Cover letter states what the client **asked for**, not what was "agreed" — these can differ, especially after a concession or scope change
- [ ] Cross-references point to the correct section numbers
- [ ] Every performance claim is sourced, client-consented, or removed — no unsourced figures (`known-defects.md` #20)

## Cadence and review

- [ ] Payment cadence stated explicitly, meets or exceeds `payment-plans.yaml: min_cadence_current` (quarterly in advance) unless an approved exception is logged
- [ ] If subscription < AED 2,500/mo: review cadence stated as quarterly, not monthly

## Forbidden phrases — confirm NONE of these appear anywhere in the draft

`bargain` · `not on our public list` · `will not be extended to any other brokerage`
· `no VAT applies` · `VAT-registered` · `Odoo Enterprise` (if edition = community)
· `iOS / Android app` (if edition = community)

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Approved for issue   [ ] Changes required — see `reviewer-notes.md`
