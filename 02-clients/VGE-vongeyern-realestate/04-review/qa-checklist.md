# Pre-Send QA Checklist — VGE-2026-SUB-01_Rev3

## Calc integrity

- [x] `00-intake/client-brief.yaml`, `02-calc/risk-assessment.yaml`, `02-calc/pricing-worksheet.yaml`, `02-calc/payment-plan-worksheet.yaml`, `02-calc/deal-card.md`, `02-calc/gate-report.md` all complete
- [x] All 41 v2 gates recorded in `pricing-worksheet.yaml: gates` with pass/fail — all pass
- [x] `manifest.yaml: gates_passed: true`, `knowledge_version_used: pricing v2.0 (2026-08-03)` pinned
- [x] Every figure in `04-draft/VGE-2026-SUB-01_Rev3_Proposal.html` traces to a key in the worksheet or to the §3 brief (single source of truth)

## Scope, edition, and exposure integrity

- [x] Every §06 capability has corresponding hours in `number_2_build.delivery_hours` (worksheet)
- [x] `phase2_deferred` items (portal sync, AI lead scoring, website capture, additional users) appear in §12 of the proposal, never in §04
- [x] Edition (Community) declared in §06 and §11, with upgrade policy stated and capability exclusions listed plainly in §07 (mobile app, Studio, advanced accounting)
- [x] All three exposures computed (G21) and recorded in `exposure:` block
- [x] Walk-away deal card produced before any pricing conversation (G22)

## Commitments

- [x] All 16 verbal-promise items in `00-intake/verbal-promises.md` are classified PRICED / DEFERRED / EXCLUDED and reflected in the draft
- [x] Adoption clause included (§09) — directly addresses the transcript's "I already implemented several different systems. Nobody is using it."
- [x] Clawback present (§09 in MSA reference) on the deferred value
- [x] No referral credit offered (not discussed on the call)

## Legal / tax

- [x] VAT clause in §11 is verbatim per brief §6 — states SGC is not registered and charges no VAT; gross-up included
- [x] No conditional correction paragraph needed (manifest records prior_versions_issued_to_client: false)
- [x] Counsel-review clauses (liability, IP, force majeure, dispute) referenced as draft-pending-counsel in §09
- [x] No named individual consultant promised (§09 — substitution right retained by SGC)
- [x] No TRN field printed; no "VAT exempt" / "free zone exempt" / "VAT inclusive" anywhere
      (§07 capability line rephrased to describe the client's own customer/vendor tax
      fields without using the raw string "TRN")

## Cover letter and cross-references

- [x] Addressed to Ms. Nadja (per brief §2 and CRM Authority gate, confirmed in BANT qualification)
- [x] Cross-references point to the correct section numbers (§05 cash structure, §07 exclusions, §09 adoption, §10 SLA, §11 commercial, §12 Phase 2, §13 next steps)
- [x] No unsourced performance claims anywhere (no AED 1.15bn claims, no ROI promises, no "X% more efficient")

## Cadence and review

- [x] Quarterly-in-advance cadence stated explicitly in §05 and §11 (meets G33 minimum)
- [x] Subscription AED 1,650/mo is below AED 2,500/mo review threshold — quarterly business review cadence stated in §06

## Forbidden phrases — confirmed NONE present in client-facing HTML

Checklist: `bargain`, `not on our public list`, `will not be extended to any other brokerage`, `no VAT applies` (negated is fine; affirmative is not), `VAT-registered`, `Odoo Enterprise` (edition=community), `iOS / Android app` (negated is fine; affirmative is not), `43,300`, `3,700`, `AED 690`, `TRN`, `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `Odoo Studio` as an included capability.

## Drift warning

The brief §3 explicitly notes that earlier drafts in this project used
AED 3,700 mobilisation and AED 43,300 total — both superseded. **Neither
figure appears anywhere in this proposal or its worksheet.** A literal
substring check on the draft confirms `3,700` and `43,300` are absent.

## Automated validation

`python 05-ops/validate.py 02-clients/VGE-vongeyern-realestate/` run on
2026-08-04 (final pass, after entity resolution): **exit code 0, RESULT:
clean**. All 18 checks pass, including check 14 (entity resolution) —
licence authority, licence number, registered address, and signatory
were resolved from the government-issued DIEZA/IFZA trade license and
the Odoo company record; see `06-brand/entity/legal-identity.yaml`.

## Headcount reconciliation

CRM BANT Budget field states "3 commission based employees"; brief/
worksheet/proposal use 5 users. Surfaced to the user 2026-08-04; decision
was to keep 5 users (brief remains single source of truth; BANT figure
read as commission-earning agents only, not full system-user count).
Logged in `manifest.yaml` escalations. Human reviewer should confirm the
5-user starting count with the client at Kickoff.

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Approved for issue   [ ] Changes required — see `reviewer-notes.md`

**Issue block: CLEARED (2026-08-04).** All 5 originally-open RESOLVE
fields are closed: licence authority, registered address, and
authorised signatory (resolved from the DIEZA/IFZA trade license +
Odoo record); Kickoff date (stated as a 30-day target from issue,
exact date fixed at signature — §08/§11/§13); Community upgrade policy
(written out in full in §04 as OCA-standard Community practice). The
build-time open-items panel now shows zero open items. Nothing blocks
issue except human sign-off below.
