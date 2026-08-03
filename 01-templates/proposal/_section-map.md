# Proposal Section Map

The required contents of each proposal section, §01–§13. Every drafted
proposal in a client's `03-draft/` or `05-issued/` folder must contain all
thirteen, in this order, each rendered from the matching template in this
directory. This map is the checklist a reviewer uses at `04-review` stage —
a section present but thin on required content is a review-log finding, not
a pass.

Adapted from the pricing playbook's Appendix A (Best-Practice Proposal
Template) and Appendix B (SOW Template), split into SGC's 13-section format.

| § | File | Required contents | Primary source |
|---|---|---|---|
| 01 | `01-executive-summary.md` | Business outcome, one-paragraph scope snapshot, headline commercial figure, timeline | `02-calc/pricing-worksheet.yaml: assembly`, client brief |
| 02 | `02-about.md` | SGC TECH AI positioning statement, relevant credentials | `market-data/benchmarks.yaml: strategic_position` |
| 03 | `03-understanding-business.md` | Client context, vertical, decision maker, stated goals | `00-intake/client-brief.yaml`, `00-intake/call-transcript-*.md` |
| 04 | `04-as-is.md` | Current-state observations, incumbent system(s), pain points | Client brief, `market-data/vertical-notes/` |
| 05 | `05-to-be.md` | Target-state narrative, phased approach | Client brief, runbook |
| 06 | `06-solution-phase1.md` | Modules, work packages, and deliverables in Phase 1 scope | `pricing-worksheet.yaml: number_2_build`, `pricing/hour-lookup.yaml`, `pricing/saas-modules.yaml` |
| 07 | `07-options-inclusions.md` | Phase 2 / deferred options, assumptions, standard exclusions | `pricing/phase2-catalogue.yaml`, `clause-library/exclusions-standard.md` |
| 08 | `08-implementation-recovery.md` | Timeline, milestones, incumbent decommission/cutover terms | `clause-library/exclusivity-replacement.md`, SOW-style milestone structure |
| 09 | `09-partnership-terms.md` | Term, commencement, adoption, clawback, referral, continuation clauses as applicable | `clause-library/term-commencement.md`, `adoption.md`, `clawback.md`, `referral-capped.md`, `post-recovery-continuation.md` |
| 10 | `10-commercial-terms.md` | Full pricing table, VAT, financing disclosure, payment schedule | `pricing-worksheet.yaml: assembly`, `clause-library/vat-uae.md`, `financing-disclosure.md` |
| 11 | `11-support-sla.md` | Support tier, response times, training included | `pricing/support-training.yaml` |
| 12 | `12-why-sgc.md` | Differentiators, delivery model, relevant proof points | `03-library/worked-examples/`, `market-data/benchmarks.yaml` |
| 13 | `13-next-steps.md` | Approval mechanism, signature block, validity period | Governance sign-off requirements, `04-governance/approval-matrix.md` |

Every commercial figure appearing in any section must trace back to the
client's `02-calc/pricing-worksheet.yaml` — no section template introduces
a number the worksheet doesn't already contain.
