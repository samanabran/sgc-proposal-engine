# Walk-Away Deal Card — PRO-2026-SUB-01_Rev1

**Produced before any pricing conversation with the client (G22).**
One page. Nothing beyond what's below.

## ⚠ Read this before the numbers

Unlike Kallat's build, this one passed the hour-benchmark gate cleanly on
the first pass (no scope-inflation drama). One thing still worth flagging:

1. **Roughly a third of what the client actually asked for has no
   priceable basis in this repo's knowledge layer**: attendance/check-in
   tracking and payroll/salary structure/WPS are named in CRM's
   `x_bant_need` and rehearsed in the internal demo-prep call, but neither
   exists in `hour-lookup.yaml` or `phase2-catalogue.yaml`. This proposal
   prices what it can and stays silent on the rest per governance rather
   than estimating by analogy — but that means this document, if ever
   shown externally, would visibly not answer those two items. See
   `verbal-promises.md` #4-#5.

The mobile-app question (prior doc promised a native app; this build
delivers responsive browser access instead) is resolved as of 2026-08-05
— presented on its own terms in §07 of the draft, not framed as a gap.
See `verbal-promises.md` #9.

## Three numbers (24-month option, preferred)

| | AED/mo |
|---|---|
| List (chosen Subscription Fee) | 6,490 |
| Target floor (30% margin) | 3,920 |
| **Absolute floor (25% margin — no approver may go below this)** | 3,551 |

(List = pricing-worksheet.yaml chosen 24mo Subscription Fee. Floors via
`07-protection/walkaway/reservation-pricing.md` against build_cost 22,800 +
CTS 2,918/mo × 24 months, less mobilisation 38,544.)

Actual computed margin on List: **~52.2%**. Passed the ≥30% target and
≥25% absolute floor comfortably without needing any post-hoc adjustment.

## Total give available

AED 2,570/mo to the target floor, AED 2,939/mo to the absolute floor
(24mo term). **Currently zero given.**

## Risk band and required security

Band: **elevated** (`pricing/risk-security-matrix.yaml`, raw_score 55 —
down from 60 after the decision-maker authority resolution below, still
near the top of the 41-60 range) — **placeholder-driven**, see
`02-calc/risk-assessment.yaml`. Three inputs (entity_age_years,
vat_registered, trade_licence_valid) remain unconfirmed conservative
placeholders. Decision-maker authority is now confirmed (2026-08-05):
**Louai Khzam is the owner** (final authority), **Dian Sajulga** is his
trusted, authorized operational contact — scored as `owner` (0) rather
than `manager` (5), matching the prior doc's own governance table.
Required instruments as currently scored: **Mobilisation at 40%** (AED
38,544 at Kickoff), **2-month deposit** (AED 12,980), **PDC set**. Unlike
Kallat, even a favorable resolution of the remaining unconfirmed inputs
likely keeps this in the elevated band — the >40k exposure component
(financed remainder AED 57,815) dominates the score on its own.

## Top 3 compensators for this deal

1. Annual-prepay billing cadence (removes Recovery Component in full).
2. Extended Initial Term beyond 24 months — not offered, same 24-month
   cap applied across both deals in this pipeline run.
3. Given the >AED 2,500 give-available band above, a straightforward
   price reduction is the more useful lever here if price sensitivity
   surfaces, same as Kallat's card noted.

(from `pricing/concession-ladder.yaml: compensators` — pre-selected before
the conversation, not improvised mid-negotiation.)

## Abort criteria

Reference `07-protection/abort/abort-criteria.md`. **None currently
triggered.** Flagged for attention: risk band is still placeholder-driven
on three inputs; underlying CRM "Pipeline Gate Review: incomplete"
(2026-08-02) has not been resolved despite the lead sitting at 94.61%
stage probability — that gap between CRM-recorded probability and actual
gate completeness is itself worth a second look.

## Incumbent benchmark

Prior unsigned PRJ-model proposal ("PROSPER x SGC Implementation Proposal
- 2026," CRM attachment, built outside this repo's governance, using
forbidden rates AED 690/650 per hr) quoted AED 45,000 fixed Phase 1 +
AED 1,450/mo mandatory Platform Care Plan, with its own illustrative
Year-1 scenarios of AED 60,950 (Phase 1 only) to AED 163,950 (Phase 1+2+
6mo retainer). This SUB-model revision's Year-1 total (24mo option) =
38,544 + (6,490 × 12) = **AED 116,424** — sits between the prior doc's
"Phase 1+2 activation" (97,950) and "Phase 1+2+retainer" (163,950)
scenarios, which is a reasonable position given this build already
includes listings/property register (the prior doc's own Phase 2 item) in
base scope. Not a strategic disarm-hesitation exercise like Kallat's —
this is simply the governed, compliant number for a broader base scope
than the prior doc's Phase 1 alone.
