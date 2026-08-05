# Pre-Send QA Checklist — MRD-2026-SUB-01_Rev3

## Calc integrity

- [x] `client-brief.yaml`, `risk-assessment.yaml`, `pricing-worksheet.yaml` complete
- [x] `gate-report.md` shows all 41 gates + market_test/budget_test pass
- [x] `manifest.yaml: gates_passed` true, `knowledge_version_used` pinned
- [x] Every number in the draft matches the worksheet exactly

## Scope, edition, exposure

- [x] Every §06 capability has hours in `number_2_build.delivery_hours`
- [x] `phase2_deferred` (portal syncs, website capture) appear in §07, not §06
- [x] Edition (Community) declared in §06 with exclusions disclosed in writing
- [x] All three exposures computed; walk-away card dated 2026-06-10, before the first pricing conversation

## Commitments

- [x] All six items in `verbal-promises.md` classified and reflected
- [x] Adoption clause present (§09), tied directly to the client's stated deal-breaker
- [x] Clawback present (§09)
- [x] No referral offered on this deal — not applicable

## Legal / tax

- [x] VAT clause states SGC holds no registration, charges no VAT — corrected from both prior revisions' errors
- [x] `vat-gross-up.md` present
- [x] Every counsel-review clause carries its flag; none presented as final
- [x] No named individual consultant promised (§09 key-person clause present instead)

## Cover letter and cross-references

- [ ] Not yet drafted — pending human review sign-off before transmittal letter is finalized
- [x] Cross-references point to correct section numbers
- [x] No unsourced performance claims anywhere in this draft (contrast with Rev1/Rev2 — see `known-defects.md` #20)

## Cadence and review

- [x] Quarterly-in-advance cadence stated, meets G33 minimum
- [x] Subscription (AED 1,700/mo) is below the AED 2,500 threshold — review cadence stated as quarterly, not monthly

## Forbidden phrases — confirmed NONE present

Checked against: `bargain`, `not on our public list`, `will not be
extended to any other brokerage`, `no VAT applies`, `VAT-registered`,
`Odoo Enterprise`, `iOS / Android app`. **All clear** — contrast directly
with Rev1/Rev2, which contained several of these.

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Approved for issue   [ ] Changes required — see `reviewer-notes.md`

**Blocker before issue (not a QA failure, a known open item)**: entity
fields in `06-brand/entity/legal-identity.yaml` remain unresolved — see
`reviewer-notes.md`.
