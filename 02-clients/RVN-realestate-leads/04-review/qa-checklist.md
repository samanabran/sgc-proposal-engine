# Pre-Send QA Checklist — RVN-2026-SUB-01_Rev1

## Calc integrity

- [x] `00-intake/client-brief.yaml`, `02-calc/risk-assessment.yaml`, `02-calc/pricing-worksheet.yaml` all fully completed
- [x] `02-calc/gate-report.md` exists and all 41 gates (G1-G41) plus `market_test`/`budget_test` show `pass: true` (both test gates N/A per client's own statements, recorded as such)
- [x] `manifest.yaml: gates_passed` is `true`, `knowledge_version_used` pinned (pricing v3.1)
- [x] Every number in the draft (§01, §06, §10, §13) matches `pricing-worksheet.yaml` exactly

## Scope, edition, and exposure integrity

- [x] Every capability described in §06 has corresponding hours in `number_2_build.delivery_hours` — cross-checked line by line
- [x] `phase2_deferred` items (telephony/call-analyzer, sensor/attendance integration) appear in §05 and §07, NOT §06 as included — verified
- [x] Edition (community) declared internally, matches `client-brief.yaml` (G36); §06 does not name "Community" or imply Enterprise — silent by default, per policy
- [x] All three exposures computed and recorded (G21); walk-away deal card (`02-calc/deal-card.md`) predates this draft (G22)

## Commitments

- [x] `verbal_promises_logged: true` in `client-brief.yaml: notes`; every entry in `verbal-promises.md` classified PRICED / DEFERRED / EXCLUDED and reflected in the draft — cross-checked against §05/§06/§07/§13
- [x] Adoption clause included (§09, `clause-library/adoption.md` verbatim)
- [x] Clawback present (§09, `clause-library/clawback.md` verbatim) — deferred structure exists (mobilisation < build value)
- [x] No referral clause offered on this deal — N/A

## Legal / tax

- [x] §10 is silent on VAT by default — confirmed, no VAT line appears
- [x] No clause used outside the library; §09 clauses flagged `[DRAFT — pending counsel review]` carry the flag
- [x] No named individual consultant promised (G27) — §09 key-person clause generic

## Cover letter and cross-references

- [ ] Cover letter / transmittal letter — NOT YET DRAFTED for this revision (see `04-review/reviewer-notes.md`); template exists at `01-templates/comms/transmittal-letter.md`
- [x] Cross-references point to correct section numbers (§05↔§07 Phase 2 items, §06↔pricing-worksheet)
- [x] Every performance claim is sourced from the transcript/summary or the worksheet — no unsourced figures

## Cadence and review

- [x] Payment cadence stated explicitly (quarterly in advance), meets `min_cadence_current`
- [x] Subscription (AED 1,680/mo) is above the AED 2,500/mo quarterly-review threshold... **correction: AED 1,680 < AED 2,500 — quarterly reviews apply, not monthly.** §11/§13 do not promise monthly business reviews; consistent.

## Forbidden phrases — confirmed NONE appear anywhere in the draft

`bargain` · `not on our public list` · `will not be extended to any other brokerage`
· `no VAT applies` · `VAT-registered` · `Odoo Enterprise` · `iOS / Android app`

Grep-checked across `03-draft/RVN-2026-SUB-01_Rev1/` — none present.

## RVN-specific check: uncatalogued-feature honesty

- [x] §05, §06, §07, §12 all explicitly distinguish what IS priced (manual CRM call logging, native activity tracking) from what is NOT priced (automated telephony/call-analyzer, sensor-based attendance) — no ambiguity that could read as "included."
- [x] No invented hours, rate, or Phase 2 catalogue price attached to either uncatalogued item — both explicitly state "scoped separately, pending information from the client."

## Sign-off

Reviewer: _pending human review_  Date: _______________
Result: [ ] Approved for issue   [x] Pending — see `04-review/reviewer-notes.md` for the one open item (transmittal letter not yet drafted)
