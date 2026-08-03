# Gate Report — VGE-2026-SUB-01_Rev3

Run against `pricing-worksheet.yaml` (this revision), per
`00-knowledge/commercial-rules/subscription-guardrails.md` and
`05-ops/validate.md`. All ten gates pass — cleared for draft/issue.

| Gate | Check | Actual | Required | Result |
|---|---|---|---|---|
| G1 — Platform floor | Subscription price ≥ platform floor | AED 7,176/mo | AED 2,900/mo | **PASS** |
| G2 — Term ≥ recovery | Recovery completes within term | Recovers exactly at month 24 | ≤ 24 months | **PASS** |
| G3 — Rate provenance | Every rate traces to `pricing/*.yaml` | All 8 work packages + rate_aed sourced | — | **PASS** |
| G4 — Documentation coverage | Documentation hours ≥ minimum | 10 hrs | 10 hrs (5% of 200 delivery hrs) | **PASS** (exact) |
| G5 — QA coverage | QA hours ≥ minimum | 16 hrs | 16 hrs (8% of 200 delivery hrs) | **PASS** (exact) |
| G6 — PM coverage | PM = segment pm_pct × subtotal | AED 13,628 (15.0%) | 15% (smb) | **PASS** |
| G7 — Segment rate integrity | Rate matches segment pin | AED 395/hr | AED 395/hr (smb) | **PASS** |
| G8 — Gross margin floor | (build value − internal cost) / build value | 68.4% | ≥ 30% (target 35%) | **PASS** — comfortably above target |
| G9 — Market test | Year-1 cost vs. incumbent × 1.30 | AED 113,367 vs. ceiling AED 148,200 (0.995× incumbent monthly-equivalent) | ≤ 1.30× | **PASS** |
| G10 — Budget test | Year-1 cost vs. previously rejected budget | AED 113,367 vs. AED 165,000 rejected | Must not exceed without justification | **PASS** — 31.3% under |

## Notes

- G4 and G5 land exactly on their computed minimums — not padded, not
  short. If scope grows even slightly on a future revision, re-verify
  these rather than assuming they still clear.
- G9's 0.995× reading is notable: extending the term from 18 to 24 months
  (Rev2 → Rev3) brought the effective annual cost *below* the client's
  cited competing quote on a pure monthly-equivalent basis, on top of
  clearing the 1.30× ceiling with room to spare. Worth highlighting in
  §01 Executive Summary.
- No gate failures on this or either prior revision. Revisions 1→2→3 were
  driven by client-requested scope and term changes, not by correcting a
  failed gate — see `manifest.yaml: escalations` for both.

Reviewer: _______________  Date: _______________
