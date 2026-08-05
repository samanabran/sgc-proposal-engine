# Gate Report — KP-2026-SUB-01_Rev1

Run against `pricing-worksheet.yaml` (this revision) per
`00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`
and `05-ops/validate.py`. **All 41 gates pass** (`RESULT: clean`, 14/14
automated checks, 2026-08-05). Cleared for internal review and Docuseal
routing. **NOT cleared for external/client issue** — see open items below.

## The three numbers

| | AED |
|---|---|
| Build Value (Implementation Value) | 121,716 |
| Mobilisation Fee (Kickoff, 40% — elevated risk band) | 48,686 |
| Recovery Component | 3,591 / month |
| Platform Component | 4,200 / month |
| **Subscription Fee (24mo preferred)** | **7,790 / month** |
| Quarterly billing | 23,370 |
| Payable at Kickoff (Mobilisation + Q1) | 72,056 |
| Year 1 | 142,166 |
| Full 24-month commitment | 235,646 |
| Alternative: 12-month term | 10,650 / month |
| VAT | None charged |

## Gate summary (all 41 v2.1 gates)

See `02-calc/pricing-worksheet.yaml: gates` for the full itemized block
with actuals and notes per gate — not reproduced in full here to avoid
drift between two copies of the same data. Summary: all PASS. Notable
ones:

- **G8/G23/G31 (margin)**: 53.6% — well above target. This is a
  *consequence*, not a design goal — see "Open items" below.
- **G15 (security sized to risk)**: elevated band, all three required
  instruments present (mobilisation_40pct, deposit_2_months, pdc_set).
- **G4/G7/G16/G25/G26/G28 (clawback, financing disclosure, liability
  cap, IP/data ownership, guarantee exclusions)**: all present in
  `03-draft/KP-2026-SUB-01_Rev1/09-partnership-terms.md` and
  `11-support-sla.md`. Four of these (deposit, PDC, liability cap, IP)
  carry explicit "pending counsel review" flags per the clause-library —
  correctly retained, not stripped, since this is an internal draft, not
  an issued document.
- **G37/G38 (edition/upgrade disclosure)**: satisfied via the MSA
  v2026.08 attachment, not proposal prose — matches VGE's own precedent
  and the 2026-08-04 user decision that proposal text stays silent on
  edition unless asked.

## Notes — read before treating this as ready for anything beyond internal review

1. **This is not a client-ready document.** CRM Lead 164's own "Pipeline
   Gate Review: incomplete" flag (BANT Q1-Q4) has not been closed. This
   proposal was built as an internal disarm-hesitation exercise per
   explicit user instruction, alongside that open gate, not in place of
   closing it.
2. **Risk band is placeholder-driven.** Two of eight `risk-assessment.yaml`
   inputs (entity_age_years, vat_registered) are unconfirmed conservative
   placeholders. If both resolve favorably, the band likely drops from
   elevated to moderate/low, and the mobilisation/deposit/PDC structure
   would loosen materially. Re-run the risk assessment with real answers
   before this goes anywhere near a client.
3. **The price moved substantially during today's build**, and in the
   opposite direction from the original strategic intent. Three iterations:
   34h/AED 4,840-mo (failed hour-benchmark badly) → 58h/AED 5,290-mo
   (still failed) → 192h/AED 7,790-mo (passes cleanly, after adding a
   genuine per-user scaling factor to `policy.yaml` itself — v2.1,
   `rollout_hours_per_user`, see `CHANGELOG.md`). The final price is
   ~47% above where this exercise started and now exceeds the original
   PRJ proposal's effective Year-1 cost — the opposite of the
   disarm-hesitation goal that motivated this rebuild. User was informed
   of this directly and explicitly chose to proceed with AED 7,790/mo
   as-is (2026-08-05) — not an oversight, a confirmed decision, but
   worth restating here since a gate report showing "all pass, 53.6%
   margin" reads as good news out of context.
4. **This is a knowledge-layer change, not just a client-specific one.**
   `policy.yaml` moved 2.0 → 2.1. VGE's already-issued Rev1-Rev3 figures
   are unaffected (5 users, under the 10-user free threshold on the new
   overlay). Any *other* in-flight mid_market/large-user-count deal
   priced against v2.0 should be re-checked against v2.1 before issue.
5. **Two open non-pricing gaps, out of this document's scope to close**:
   WhatsApp Business API integration has no basis anywhere in this
   repo's pricing knowledge layer — escalate before ever quoting it
   (see `verbal-promises.md` #3). Portal sync's five preconditions
   (RERA/DLD licence, agency ID, portal-side verification, image
   compliance, client's own portal API subscription) are unconfirmed.

Reviewer: _______________  Date: _______________
