# Gate Report — PRO-2026-SUB-01_Rev1

Run against `pricing-worksheet.yaml` (this revision) per
`00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`
and `05-ops/validate.py`. **All 41 gates pass** (`RESULT: clean`, 14/14
automated checks, 2026-08-05). Cleared for internal review and Docuseal
routing. **NOT cleared for external/client issue** — see open items below.

## The three numbers

| | AED |
|---|---|
| Build Value (Implementation Value) | 96,359 |
| Mobilisation Fee (Kickoff, 40% — elevated risk band) | 38,544 |
| Recovery Component | 2,843 / month |
| Platform Component | 3,648 / month |
| **Subscription Fee (24mo preferred)** | **6,490 / month** |
| Quarterly billing | 19,470 |
| Payable at Kickoff (Mobilisation + Q1) | 58,014 |
| Year 1 | 116,424 |
| Full 24-month commitment | 194,304 |
| Alternative: 12-month term | 8,760 / month |
| VAT | None charged |

## Gate summary (all 41 v2.1 gates)

See `02-calc/pricing-worksheet.yaml: gates` for the full itemized block
with actuals and notes — not reproduced in full here. Summary: all PASS.
Notable ones:

- **G8/G23/G31 (margin)**: 52.2% — comfortably above target on the first
  pass, using the same real-estate-brokerage-uae vertical baseline (8 work
  packages) established for Kallat directly, rather than under-scoping
  and re-expanding as happened there.
- **G15 (security sized to risk)**: elevated band (raw_score 55, down
  from 60 after the decision-maker authority resolution — see notes),
  all three required instruments present (mobilisation_40pct,
  deposit_2_months, pdc_set).
- **G37/G38 (edition/upgrade disclosure)**: satisfied via the MSA v2026.08
  attachment, not proposal prose — same basis as Kallat and VGE. Mobile
  access is presented as a responsive-browser capability on its own
  terms (§07), not framed as a shortfall against the prior PRJ doc — see
  `verbal-promises.md` #9.

## Notes — read before treating this as ready for anything beyond internal review

1. **This is not a client-ready document.** CRM Lead 8407's own "Pipeline
   Gate Review: incomplete" flag (2026-08-02) has not been closed, despite
   the lead sitting at 94.61% stage probability in CRM — that mismatch is
   itself worth flagging to whoever owns this pipeline. This proposal was
   built anyway per explicit user instruction, as the second of two
   individually-sequenced internal disarm-hesitation-adjacent rebuilds in
   this pipeline run.
2. **Risk band is placeholder-driven on three of eight inputs.**
   `risk-assessment.yaml`'s entity_age_years, vat_registered, and
   trade_licence_valid remain unconfirmed conservative placeholders.
   Decision-maker authority is now confirmed (2026-08-05): Louai Khzam is
   the owner, Dian Sajulga is his trusted, authorized operational
   contact — raw_score dropped from 60 to 55 accordingly, still elevated.
   A favorable resolution of the remaining three placeholders likely does
   not move this out of the elevated band — the financed-remainder
   exposure component (AED 57,815, >40k bucket) is the dominant driver of
   the score on its own. Re-run with real answers before this goes near a
   client.
3. **Two of the client's stated needs have no priceable basis in this
   repo's knowledge layer**: attendance/check-in tracking and payroll/
   salary structure/WPS. Both are named directly in CRM's `x_bant_need`
   and rehearsed in the internal demo-prep call, but neither exists in
   `hour-lookup.yaml` or `phase2-catalogue.yaml`. Escalate before ever
   quoting either — see `verbal-promises.md` #4-#5. A ChatGPT-style AI
   assistant is partially addressable via the AI Lead Scorer add-on
   (§07), a different capability, not a full substitute.
4. **This is built on the same knowledge-layer version as Kallat**
   (`policy.yaml` v2.1, `rollout_hours_per_user` overlay). No further
   knowledge-layer changes were made for this build.

Reviewer: _______________  Date: _______________
