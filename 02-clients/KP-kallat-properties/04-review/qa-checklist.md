# Pre-Send QA Checklist — KP-2026-SUB-01_Rev1

**This document governs an INTERNAL-ONLY artifact** (Docuseal, SDR
signature). Several checklist items below that would normally gate an
external send are marked N/A for that reason, not skipped — re-run this
checklist in full if this ever moves toward an actual client send.

## Calc integrity

- [x] `00-intake/client-brief.yaml`, `02-calc/risk-assessment.yaml`, `02-calc/pricing-worksheet.yaml`, `02-calc/deal-card.md`, `02-calc/gate-report.md` all complete
- [x] All 41 v2.1 gates recorded in `pricing-worksheet.yaml: gates` — all pass (`validate.py`: `RESULT: clean`)
- [x] `manifest.yaml: gates_passed: true`, `knowledge_version_used: pricing v2.1 (2026-08-05)` pinned
- [x] Every figure in `04-draft/KP-2026-SUB-01_Rev1_Internal.html` traces to `pricing-worksheet.yaml`

## Scope, edition, and exposure integrity

- [x] Every §06 capability has corresponding hours in `number_2_build.delivery_hours` (worksheet)
- [x] `phase2_deferred` items (portal sync, AI scoring, additional users) appear in §07, never in §04/§06
- [x] Edition (Community) NOT named in proposal prose (per 2026-08-04 user decision) — satisfied instead by MSA attachment (G37/G38)
- [x] All three exposures computed (G21) and recorded in `exposure:` block
- [x] Walk-away deal card produced before any pricing conversation (G22) — **N/A caveat**: no pricing conversation has occurred at all; card exists purely as an internal artifact

## Commitments

- [x] All 8 verbal-promise items in `00-intake/verbal-promises.md` classified PRICED / DEFERRED / EXCLUDED / NOT APPLIED, reflected in the draft
- [x] Adoption clause included (§09)
- [x] Clawback present (§09) on the deferred value (73,030)
- [x] No referral credit offered as a firm commitment — flagged as a plausible compensator in `deal-card.md` only, not promised in the draft

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
- [x] Subscription AED 7,790/mo is above the AED 2,500/mo review threshold — monthly business-review cadence would be the applicable default per `policy.yaml`, not stated explicitly in this internal draft (add if this ever moves toward external issue)

## Forbidden phrases — confirmed NONE present

Checklist: `bargain`, `not on our public list`, `will not be extended to any other brokerage`, `VAT-registered`, `Odoo Enterprise`, `iOS / Android app` (affirmative), `AED 690`, `AED 550`, `TRN` (as a literal value), `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `Odoo Studio` (as included). Confirmed via `05-ops/validate.py` check 18 (clean) plus manual review of all 13 sections.

## Internal-document-specific items

- [x] "INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION" banner present on the rendered PDF cover
- [x] §13 explicitly states this is not ready for external send and lists the three open items (BANT gate, risk placeholders, price-vs-strategy tension)
- [x] No client-facing branding/watermark system applied — deliberate scoping decision given internal-only status, documented in `04-draft/assemble_and_render.py`'s docstring

## Automated validation

`python 05-ops/validate.py 02-clients/KP-kallat-properties/` run
2026-08-05 (final pass, after all 13 sections drafted): **exit code 0,
RESULT: clean**. All 14 checks pass.

## Open items (not blockers for internal Docuseal routing, blockers for anything beyond)

1. CRM Lead 164's "Pipeline Gate Review: incomplete" (BANT Q1-Q4) — unresolved.
2. Risk-assessment placeholders (entity_age_years, vat_registered) — unconfirmed.
3. Price tension vs. original disarm-hesitation goal — user informed and confirmed proceeding 2026-08-05, documented in `gate-report.md`.

## Sign-off

Reviewer: _______________  Date: _______________
Result: [ ] Cleared for Docuseal internal routing   [ ] Changes required
