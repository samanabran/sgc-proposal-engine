# Pre-Send QA Checklist — copy to 02-clients/{client}/04-review/qa-checklist.md

Complete before requesting human review. Every box must be checked before
`04-review/reviewer-notes.md` is opened; an unchecked box is a blocker, not
a note for later.

## Calc integrity

- [ ] `02-calc/pricing-worksheet.yaml` fully completed, no blank fields
- [ ] `02-calc/gate-report.md` exists and all ten gates (G1–G10) show `pass: true`
- [ ] `manifest.yaml: gates_passed` is `true`
- [ ] `manifest.yaml: knowledge_version_used` is pinned to a real `CHANGELOG.md` version
- [ ] Every number in the draft matches the worksheet exactly — spot-check §10 against `assembly`

## Scope integrity

- [ ] Every module/work package in §06 also appears in `number_2_build.delivery_hours`
- [ ] No module or work package appears in the draft that isn't in the worksheet
- [ ] `phase2_deferred` items appear in §07, not §06
- [ ] `exclusions_confirmed: true` in the worksheet, and `clause-library/exclusions-standard.md` is present verbatim in §07

## Commitments

- [ ] `verbal_promises_logged: true` in `manifest.yaml`, and every logged promise appears somewhere in the draft
- [ ] `adoption_clause_included` matches whether §09 contains the adoption clause
- [ ] `clawback_included` matches whether §09 contains the clawback clause

## Legal / tax

- [ ] VAT clause in §10 is `clause-library/vat-uae.md` verbatim, unedited
- [ ] Any other clause-library content used is verbatim, unedited
- [ ] Vertical-specific compliance notes (if any) flagged for human legal review, not resolved in the draft

## Format

- [ ] All 13 sections present, in order, matching `01-templates/proposal/_section-map.md`
- [ ] Cover page has client name, proposal ref, revision number, date, confidentiality marking
- [ ] Proposal ref follows `05-ops/naming-conventions.md` exactly

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Approved for issue   [ ] Changes required — see `reviewer-notes.md`
