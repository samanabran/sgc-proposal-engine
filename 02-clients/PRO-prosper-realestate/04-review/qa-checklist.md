# Pre-Send QA Checklist — PRO-2026-SUB-01_Rev1

**This document governs an INTERNAL-ONLY artifact** (Docuseal, SDR
signature). Several checklist items below that would normally gate an
external send are marked N/A for that reason, not skipped — re-run this
checklist in full if this ever moves toward an actual client send.

## Calc integrity

- [x] `00-intake/client-brief.yaml`, `02-calc/risk-assessment.yaml`, `02-calc/pricing-worksheet.yaml`, `02-calc/deal-card.md`, `02-calc/gate-report.md` all complete
- [x] All 41 v2.1 gates recorded in `pricing-worksheet.yaml: gates` — all pass (`validate.py`: `RESULT: clean`)
- [x] `manifest.yaml: gates_passed: true`, `knowledge_version_used: pricing v2.1 (2026-08-05)` pinned
- [x] Every figure in `04-draft/PRO-2026-SUB-01_Rev1_Internal.html` traces to `pricing-worksheet.yaml`

## Scope, edition, and exposure integrity

- [x] Every §06 capability has corresponding hours in `number_2_build.delivery_hours` (worksheet)
- [x] `phase2_deferred` items (portal sync, AI lead scoring, additional users) appear in §07, never in §04/§06
- [x] Items with no priceable basis at all (attendance, payroll/WPS) are explicitly flagged NOT APPLIED in §04/§05/§06/§07/§13, never silently omitted
- [x] Edition (Community) NOT named in proposal prose — satisfied instead by MSA attachment (G37/G38)
- [x] All three exposures computed (G21) and recorded in `exposure:` block
- [x] Walk-away deal card produced before any pricing conversation (G22) — **N/A caveat**: no pricing conversation has occurred at all; card exists purely as an internal artifact

## Commitments and prior-document conflicts

- [x] All 10 verbal-promise items in `00-intake/verbal-promises.md` classified PRICED / DEFERRED / EXCLUDED / NOT APPLIED, reflected in the draft
- [x] **Mobile access presented on its own terms** (§07) — responsive browser experience, not framed as a shortfall against the prior PRJ doc's native-app language, per 2026-08-05 user decision
- [x] Adoption clause included (§09)
- [x] Clawback present (§09) on the deferred value (57,815)
- [x] No referral credit or Kallat-specific disarm-hesitation concessions (free sandbox, refundable mobilisation) carried over without separate confirmation — documented in `client-brief.yaml`

## Legal / tax

- [x] No VAT line anywhere — proposal stays silent per omit-unless-asked convention; MSA carries the binding "not VAT-registered" position
- [x] Counsel-review clauses (security deposit, PDC, liability, IP, key-person, force majeure, dispute) all explicitly flagged "pending counsel review" in §09 — none presented as final
- [x] No named individual consultant promised (§09 — substitution right retained by SGC)
- [x] No TRN field printed as a literal value; §06/§07 reference "TRN-compliant invoicing" as a capability only

## Cross-references

- [x] Cross-references point to correct section numbers (§07 exclusions, §09 adoption/security, §10 commercial, §11 SLA, §13 next steps)
- [x] No unsourced performance claims anywhere

## Cadence and review

- [x] Quarterly-in-advance cadence stated in §10 (meets G33 minimum); monthly billing explicitly flagged as a disclosed deviation with surcharge
- [x] Subscription AED 6,490/mo is above the AED 2,500/mo review threshold — monthly business-review cadence would be the applicable default per `policy.yaml`, not stated explicitly in this internal draft (add if this ever moves toward external issue)

## Forbidden phrases — confirmed NONE present

Checklist: `bargain`, `not on our public list`, `will not be extended to any other brokerage`, `VAT-registered`, `Odoo Enterprise`, `iOS / Android app` (affirmative — checked specifically given the prior-doc conflict), `AED 690`, `AED 550`, `TRN` (as a literal value), `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `Odoo Studio` (as included). Confirmed via `05-ops/validate.py` check 18 (clean) plus manual review of all 13 sections.

## Internal-document-specific items

- [x] "INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION" banner present on the rendered PDF cover
- [x] §13 explicitly states this is not ready for external send and lists open items (BANT gate, remaining risk placeholders, unpriced attendance/payroll items)
- [x] No client-facing branding/watermark system applied — deliberate scoping decision given internal-only status, documented in `04-draft/assemble_and_render.py`'s docstring

## Automated validation

`python 05-ops/validate.py 02-clients/PRO-prosper-realestate/` run
2026-08-05 (after all 13 sections drafted): **exit code 0,
RESULT: clean**. All 14 checks pass, first pass — no iteration needed on
the hour-benchmark gate this time (152h vs. 142.6h floor, 31 users).

## Open items (not blockers for internal Docuseal routing, blockers for anything beyond)

1. CRM Lead 8407's "Pipeline Gate Review: incomplete" — unresolved, despite 94.61% stage probability.
2. Risk-assessment placeholders (entity_age_years, vat_registered, trade_licence_valid) — unconfirmed. (Decision-maker authority resolved 2026-08-05: Louai Khzam owner, Dian Sajulga trusted operational contact.)
3. Attendance tracking and payroll/salary/WPS — no priceable basis in this repo's knowledge layer at all; real scoping work needed if these remain important to the client. A ChatGPT-style assistant is partially addressable via the AI Lead Scorer add-on.

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Cleared for Docuseal internal routing   [ ] Changes required
