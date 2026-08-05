# Changelog — Knowledge Layer

Every change to `00-knowledge/` or `01-templates/` is logged here, in semver.
Client worksheets pin the version active when they were built
(`manifest.yaml: knowledge_version_used`); a later bump never silently
revalues an existing proposal.

## pricing v1.0 — 2026-08-03

Initial seed of the knowledge layer from `commercial-pricing-revised-v2.xlsx`
(v1→v2 revision, 22 Jul 2026) and the SGCTECH.AI Odoo Implementation Pricing
Strategy playbook (v1.0, 18 Jul 2026).

- Added `pricing/rate-card.yaml` — 13 roles, revised UAE specialist-boutique
  band (280–800 AED/hr).
- Added `pricing/saas-modules.yaml` — 18 Odoo modules + 4 Microsoft SKUs.
- Added `pricing/hosting.yaml` — 3 managed-hosting tiers (Contabo/Hetzner) +
  AWS pass-through reference rates.
- Added `pricing/support-training.yaml` — 3 support SLA tiers, 3 training
  formats, 3 cybersecurity services.
- Added `pricing/hour-lookup.yaml` — work-package → hour range, sourced from
  the pricing playbook's Excel-ready service catalog (Part 6).
- Added `pricing/phase2-catalogue.yaml` — deferred-scope items not costed in
  Phase 1 (AI Solutions catalog, advanced integrations).
- Added `pricing/policy.yaml` — segments, overlays, cost-to-serve
  coefficients, financing uplift, and the G-series commercial gates.
- Added `commercial-rules/12-commercial-rules.md` — verbatim from the xlsx
  Commercial Rules sheet (unchanged since v1).
- Added `commercial-rules/subscription-guardrails.md` — G1–G10, derived from
  `policy.yaml` gates plus the playbook's payment-structure guidance (Part 10).
- Added `market-data/benchmarks.yaml` + `sources.md` — UAE/GCC partner
  density, regional rate comparison, and industry pricing bands from the
  pricing playbook (Parts 2, 6, 7, 9).
- Added `market-data/vertical-notes/uae-real-estate.md` and
  `uae-tax-vat.md`.
- Added `failure-modes/known-defects.md` — seeded with the defect classes the
  gate structure exists to prevent (see file for the full list).
- Ported **VGE-vongeyern-realestate** in as the live worked example, Rev1 and
  Rev2 in `05-issued/`, Rev3 in `03-draft/`.

All figures in this release are sourced from the two documents above, now
archived in `_source-documents/`. Where the source used a range, `policy.yaml`
records the specific operating value SGCTECH commits to — see inline comments
for the rationale.

## pricing v2.1 — 2026-08-05

Note: `policy.yaml`/`rate-card.yaml` were already at `version: 2.0` (the
"v2 hardening pass" referenced throughout the knowledge layer — mobilisation
25%→33%, 24-month uplift 12%→18%, VAT flipped off) before this entry, but
that jump was never logged here — a pre-existing gap in this file, not
backfilled retroactively; see `policy.yaml`'s own inline "v2 changes from
v1" comment for what changed in that pass.

This entry documents the actual v2.1 change:

- Added `pricing/policy.yaml: overlays.rollout_hours_per_user` (4h) and
  `overlays.rollout_hours_free_users` (10). `hour-lookup.yaml`'s work
  packages are flat regardless of company size — there was no mechanism for
  build hours to scale with headcount at all. Discovered building
  **KP-2026-SUB-01** (Kallat Properties, 40 users): using every single
  package in `hour-lookup.yaml` at standard band only reached ~52-60h total,
  against `05-ops/validate.py`'s hour-benchmark gate expecting ~9.2h/user
  (~368h for 40 users, fail floor at 50% = 184h). The new overlay adds
  genuine per-user rollout effort (role/permission setup, individual
  training coordination, data-validation touch points, hypercare support
  fanned across more people) beyond the flat per-package hours, scaling
  only above the first 10 users so small deals are unaffected —
  **VGE-vongeyern-realestate's already-issued Rev1-Rev3 figures are
  unchanged** (5 users < 10-user free threshold, contributes 0 additional
  hours).

## pricing v2.2 — 2026-08-05 (REVERTED same day)

An attempt was made this same day to replace `05-ops/validate.py`'s
uncited `9.2 * users` benchmark with `4.8 * users` (xlsx Packages Growth +
Scale convergence). The change was reverted before end-of-day for the
following reasons — recording them here so the *next* attempt doesn't
re-derive the same trap:

1. **Lowering a floor can only convert fails to passes, never the reverse**
   — the four-client "all clean" run was tautological, not evidence.
   `--selftest` covers regex carve-outs unrelated to the constant.
   Real coverage would require fixtures at 95/100/105% of the floor
   asserting the pass/fail flip lands as intended.

2. **Kallat's actual defect is over-scoping, not under-scoping** —
   lowering the under-scoping floor widens the gap between the existing
   gate and the failure mode that's live. The control that would have
   caught Rev1 (a ceiling against the 22,000–55,000 implementation band
   from `market-positioning.yaml`) does not exist yet.

3. **Two agreeing points aren't convergence** — Starter is 1.6h/user;
   Growth 4.8; Scale 4.8. The curve is flattening, not constant.
   Kallat at 40 users is double the largest observation, so 4.8 is an
   extrapolation, not a benchmark. Residuals confirm: 9.2 puts small
   deals at 100–113% of benchmark and big at 52–53%; 4.8 puts big at
   100–102% and small at 192–217%. No single constant fits because
   rollout effort per user likely declines with scale. Fix shape:
   band-based, or drop the per-user proxy in favour of hour-lookup.yaml
   scope sums. Constant swap relocates the error, doesn't fix it.

4. **192h vs 192h reference is the shape of failure G6 catches** —
   when a choice is available, don't pick the one that flatters the
   deal under review. Constant swap happened to place the problem deal
   at exactly 100% of benchmark.

5. **`rollout_hours_per_user` overlay loses its stated justification**
   — under v2.2 the floor drops to 96h for 40 users; the v2.1 4h/user
   overlay was load-bearing to clear 184h, not to model real per-user
   effort. With that justification gone, the overlay either needs
   independent evidence or comes out. Status quo (revert to v2.1) keeps
   the rule-of-thumb without claiming the citation that wasn't earned.

6. **Precedence blocker got worse, not better** — two knowledge-layer
   versions stamped 2026-08-05, with v2.2 sourced from a workbook
   stamped v2, 22 Jul 2026. The repo ingested a number from one
   lineage without ever establishing which lineage is authoritative.
   That was a halt condition; it was stepped over rather than closed.

**State at end-of-day**: `05-ops/validate.py` literal restored to `9.2 *
users` (back to v2.1 semantics on check 4). No call/derived figures in
any client worksheet changed. Kallat Rev2 remains blocked, unchanged,
pending: (a) precedence resolution between the xlsx and playbook lineages,
(b) boundary fixtures for any future benchmark change, (c) the missing
over-scope ceiling gate.

**The restored 9.2 constant is recorded here as KNOWN DEBT, not as the
validated state.** Reading "reverted, clean" and concluding the prior
benchmark was correct is the exact failure mode G6 catches. Specifically,
under 9.2h/user the corpus misfits:

| Client | users | total_h | benchmark | h/user delivered | % of benchmark |
|---|---|---|---|---|---|
| VGE      |  5 |  52 |  46 | 10.4 | 113% |
| MRD      |  5 |  46 |  46 |  9.2 | 100% |
| Kallat   | 40 | 192 | 368 |  4.8 |  52% |
| Prosper  | 31 | 152 | 285 |  4.9 |  53% |

The small deals land at 100–113% of benchmark and the large ones at
52–53%. Under 9.2 the gate is satisfied only by the under-scope-floor
direction; the over-scope direction is unenforced. No per-user constant
fits all four cleanly. Reverting to 9.2 was correct for *stability* (no
silent revaluing of live client worksheets — every active deal still
clears the floor it was built against). It is **not** correct as a
sustained position. Before any future benchmark change ships, the
fixtures, precedence, and ceiling gate work below must land.

## pricing v3.0 — 2026-08-05

Replaces `overlays.rollout_hours_per_user` / `rollout_hours_free_users`
(v2.1, 2026-08-05 — the mechanism this same file's v2.2-revert entry
above flagged as load-bearing rather than evidence-based) with a
four-class cost model — Class A (scope-driven, user-invariant), Class B
(per-user, one-time, bottom-up, Wright's-law learning curve), Class C
(banded recurring), Class D (true per-user vendor licence, structurally
zero under Community). Full derivation:
`.omc/plans/pricing-engine-cost-class-model.md` (Rev.2).

**Deletion, not retuning, per P11** — the overlay's own function was
closing a `hour-lookup.yaml` Class A scope gap (bulk-import engineering,
training-content design, hypercare support capacity), mislabeled as a
per-user multiplier, and it billed that work at the mid_market blended
rate (525 AED/hr) — a real, demonstrated rate-mix-ceiling violation
(`validate.py: check_v2_rate_mix_ceiling`) on work that is structurally
Class B. **The corrected bottom-up Class B figure for Kallat (N=40) is
10.73h against the deleted overlay's 120h — a ~109h GAP, not a saving:
the Class A/C lines added below absorb only part of the difference, and
their own O/M/P estimates are themselves new and Grade D (no delivered
actual exists yet for any of them). This recompute is a DISCOVERY of what
the deal should cost once per-user provisioning is billed at its own role
rate, not a fix or a discount** (K-6, carried forward verbatim as
required).

Added, in this order (D-9 — new Class A/C scope landed *before* the
overlay was deleted, so no commit priced the corpus with neither
mechanism):
- `hour-lookup.yaml` v2.1: `migration_record_validation_signoff`,
  `bulk_user_import_csv`, `training_content_design_multiagent` (Class A,
  Grade D).
- `support-training.yaml` v2.1: `hypercare.hypercare_golive_support`
  (one-time, pod-scaled, priced at `support_rate_aed`).
- `class-b-task-inventory.yaml` (new) + `cost-classes.md` (new): the
  governed Class B task inventory (`time_basis` explicit per task, D-3;
  per-task `role`, D-5) and the A–D taxonomy documentation.
- `05-ops/pricing_engine.py` (new): single code path for `B_hours(N)` and
  the marginal-user onboarding fee — read by both `validate.py` and
  `05-ops/test_pricing_engine.py` (P14).
- `05-ops/test_pricing_engine.py` (new): T1–T7 harness. Notable findings
  from actually running it against the full N=1..400 range (not the 8
  sample points used in the pre-approval planning pass): **B_hours(N)/N
  is non-increasing everywhere EXCEPT at exactly 5 points (N=20, 33, 46,
  59, 72) — every one of them a `role_count(N)` step boundary, fully
  explained by `role_permission_design` being itself a flat-per-role step
  function.** The planning-stage claim that this finding "disappeared
  entirely" was based on too coarse a sweep and is corrected here, not
  quietly fixed — reported per P12.
- `05-ops/validate.py`: V1 (effort reconciliation, 40% tolerance derived
  from `hour-lookup.yaml`'s own simple/standard variance, not chosen to
  pass anything), V2 (rate-mix ceiling, per-task-role), V3 (band check,
  annotation-only), V4 (positioning-claim check, computed), plus R1–R12
  (the 12 Commercial Rules as executable checks — several reuse existing
  checks 1–18 where they already hold). `check_4`'s literal `9.2 *
  users` benchmark is **untouched** (K-5).
- `rate-card.yaml` v2.1: header documentation defect fixed (contents
  authoritative over the false "180-300" header claim); new governed
  `passthrough_band` field (60–120 AED/hr) — a real xlsx figure (`Market
  Positioning` sheet, row 7) never transcribed into `benchmarks.yaml`
  during the v1.0 ingestion, now closed.
- `financing-amortization.md` (new): files the F1–F4 derivation (flat
  18% uplift confirmed exact against Kallat's real figures, and
  client-favourable versus a true 18%-APR amortisation) as a governed
  reference.
- `phase2-catalogue.yaml` v2.1: `additional_user` (AED 250/mo, marginal
  cost 102, non-discountable) replaced by `onboarding_fee_per_marginal_user`
  (one-time, script-derived, ≈AED 9 at the Kallat N=40→41 baseline — lower
  than either of two earlier hand-estimates, for a stated reason: the
  marginal user falls in the bulk-provisioning regime, not a re-tuned
  constant) + `platform_capacity_fee` (banded, negotiable AED 76–250/user/
  month). The pre-existing AED 102 figure has **no derivation shown
  anywhere in this repo** — neither confirmed nor contradicted by the
  bottom-up AED 58–180 range computed here, not described as
  corroboration (D-8).

**Cross-client impact**: VGE and MRD (both 5 users, both under the
10-user threshold that made the deleted overlay contribute 0 hours to
either deal anyway) are **unaffected in figures**. Kallat and Prosper
(both unissued, internal-only per each `manifest.yaml`) were recomputed
in place — see each client's `manifest.yaml` 2026-08-05 escalation entry:
Kallat `build_value_aed` 121,716 → 56,072 (Subscription Fee 7,790 →
5,850/mo, 24mo option), Prosper 96,359 → 55,006 (6,490 → 5,270/mo). Gross
margin drops correspondingly (Kallat 53.6%→40.8%, Prosper 52.2%→42.6%)
but stays comfortably above the 30% minimum and 25% absolute floor on
both.

**New finding surfaced by the recompute, not hidden**: both recomputed
worksheets now **fail** `validate.py check_4` (the legacy, uncited
9.2h/user benchmark this same file's v2.2-revert entry already flagged
as "known debt") — Kallat 100.7h vs a 368h/184h-floor reference, Prosper
92.1h vs 285.2h/142.6h. This is not a regression to paper over: a
properly-classed recompute failing an unvalidated legacy floor is
evidence the floor itself was never well-founded (the deleted overlay
was originally added in v2.1 specifically to clear this exact check),
not evidence the recompute is wrong (P7). `check_4`'s literal remains
untouched per K-5; this is logged as an open item, same status as the
9.2-vs-4.8 question above.

**Still open, unresolved by this recompute**: the "15–20% below
mid-tier" positioning claim is still present in both Kallat's and
Prosper's draft prose (`03-draft/.../02-about.md`) and now fails
`validate.py check_v4_positioning_claim` at the 525 AED/hr blended rate
(525 > the 382.5 threshold) — this is a draft-text edit, not a worksheet
recompute, and remains for a follow-up pass. R11 (standalone quotation
PDF) and R12 (one-page commercial summary) remain missing for all four
corpus clients — a confirmed, repo-wide, pre-existing gap
(`kallat-recost-rev2.md` D5), not created or closed by this build.

**V5 corpus prediction, written before running, corrected once**:
predicted Prosper's V2 would PASS ("no rollout_hours legacy field billed
at 525") — **wrong**, Prosper's worksheet had the identical defect shape
at a smaller scale (84h). Corrected in `validate.py:
run_v5_corpus_prediction()` with the error left visible, not quietly
rewritten, per V5's own discipline.

**UNVALIDATED, carried forward** (Grade D, each with a named collapse
trigger in `pricing-engine-cost-class-model.md` Rev.2 §L): learning-curve
exponent (b=0.15), `role_count(N)` divisor (13, single-anchor), time-basis
reference cohort (N_ref=5), support-minutes/user, N_bulk=25, all four new
`hour-lookup.yaml`/`support-training.yaml` entries' own O/M/P (no
delivered actual exists for any of them yet), cost-of-capital (F3, no
source exists anywhere in this repo), commission-impact-per-discount (no
source exists), WhatsApp Business API hours (Grade D, see
`pricing-engine-cost-class-model.md` Rev.2 §N). None of these block
pricing — each has a PERT range and a named collapse trigger — but none
should be presented client-facing as dirham-exact.
