# Pre-Send QA Checklist — VGE-2026-SUB-01_Rev3

## Calc integrity

- [x] `02-calc/pricing-worksheet.yaml` fully completed, no blank fields
- [x] `02-calc/gate-report.md` exists and all ten gates (G1–G10) show `pass: true`
- [x] `manifest.yaml: gates_passed` is `true`
- [x] `manifest.yaml: knowledge_version_used` is pinned ("pricing v1.0 (2026-08-03)")
- [x] Every number in the draft matches the worksheet exactly — spot-checked §10 against `assembly`

## Scope integrity

- [x] Every module/work package in §06 also appears in `number_2_build.delivery_hours`
- [x] No module or work package appears in the draft that isn't in the worksheet
- [x] `phase2_deferred` items (AI Lead Scorer Lite, AI Chatbot Lite) appear in §07, not §06
- [x] `exclusions_confirmed: true` in the worksheet, and standard exclusions text is present verbatim in §07

## Commitments

- [x] `verbal_promises_logged: true` in `manifest.yaml`, and every logged promise appears in the draft (training commitment: §09, §11; accounting scope: §06)
- [x] `adoption_clause_included` matches — §09 contains the adoption clause
- [x] `clawback_included` matches — §09 contains the clawback clause

## Legal / tax

- [x] VAT clause in §10 is `clause-library/vat-uae.md` verbatim, unedited (plus a factual note on TRN/mainland status, added below the clause, not altering the clause itself)
- [x] Financing disclosure, term-commencement, adoption, clawback, and post-recovery-continuation clauses used verbatim
- [x] No vertical-specific compliance question required escalation this revision — scope unchanged from Rev2, which already cleared legal review

## Format

- [x] All 13 sections present, in order, matching `01-templates/proposal/_section-map.md`
- [x] Proposal ref `VGE-2026-SUB-01_Rev3` follows `05-ops/naming-conventions.md` exactly

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Approved for issue   [ ] Changes required — see `reviewer-notes.md`
