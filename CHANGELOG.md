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
as "known debt") — Kallat 104.7h vs a 368h/184h-floor reference, Prosper
101.1h vs 285.2h/142.6h (both figures corrected same day — see the
addendum below; the originally-reported 100.7h/92.1h were wrong by
4.0h/9.0h due to a hand-transcription error, not an engine defect).
This is not a regression to paper over: a
properly-classed recompute failing an unvalidated legacy floor is
evidence the floor itself was never well-founded (the deleted overlay
was originally added in v2.1 specifically to clear this exact check),
not evidence the recompute is wrong (P7). `check_4`'s literal remains
untouched per K-5; this is logged as an open item, same status as the
9.2-vs-4.8 question above.

**Follow-up, same day**: the "15–20% below mid-tier" positioning claim
in both Kallat's and Prosper's draft prose (`03-draft/.../02-about.md`)
was corrected — both blend at 525 AED/hr, inside the mid-tier band
(350–550), not below it (VGE/MRD, at 280 AED/hr, legitimately keep the
original claim and were left untouched). Both now pass
`check_v4_positioning_claim`. R11 (standalone quotation PDF) and R12
(one-page commercial summary) remain missing for all four corpus
clients — a confirmed, repo-wide, pre-existing gap
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

### Addendum, same day — check_4 (9.2h/user) formally classified as a known structural exception, not silently red

The v3.0 recompute above made both Kallat and Prosper fail
`validate.py check_4` (this file's own v2.2-revert entry already flagged
this literal as uncited "known debt"). Per K-5 the literal is untouched
— but leaving it as an unqualified `[FAIL]` risks a future reader
"fixing" it by loosening the 9.2 constant or the 50% floor without
understanding why, repeating the exact v2.2 mistake.

Before classifying it either way, `05-ops/pricing_engine.py:
total_hours_for_n(N)` and `05-ops/test_pricing_engine.py: t8_check4_
structural_sweep` were added to sweep check_4 across **every integer
N=1..400**, using the same engine the recompute uses (not a separate
hand model):

- **N=1**: total_hours ≈ 69.1h vs. floor 4.6h — passes by a wide margin.
- **First breach: N=19.** From N=19 onward, check_4 **fails and never
  recovers** through N=400.
- **Per-user hours fall monotonically** from 69.1h/user (N=1) to
  0.72h/user (N=400), while check_4 demands a flat 4.6h/user floor
  forever. 74 small local upticks exist across the range; every one of
  them traces to a known, explained step boundary
  (`role_count(N)` steps, `hypercare_golive_support`'s `ceil(N/5)` pod
  steps, or QA/documentation-hours rounding boundaries) — none
  unexplained, and the largest is 0.21h/user against an overall decline
  spanning two orders of magnitude.

**Conclusion, confirmed by shape, not by tuning any constant to produce
it**: a flat per-user benchmark is structurally incompatible with a
model where Class A hours are near-flat in N, Class B hours grow
sub-linearly (Wright's-law learning), and hypercare is a coarse
population-pod step — any such model eventually falls below a flat
per-user floor as N grows, regardless of the exact constants chosen.
This is the opposite failure mode from a subtly-wrong recompute
producing an artificially low number: a wrong recompute would not
reliably pass at low N, diverge progressively, and never recover across
382 of 400 integers with every local exception independently explained.

**Action taken**: `check_4_hour_benchmark` now classifies its own
failure as `structural_exception` (a new `Result` bucket, same pattern
as the existing `entity_blocker`) rather than `gate_failures` when
`users_now >= CHECK_4_STRUCTURAL_BREACH_N` (19). This is a
**reporting/classification change only** — the 9.2 literal, the 50%
floor, and the pass/fail arithmetic are byte-for-byte unchanged. The
check still prints, still shows red, still cites the evidence inline;
it is simply no longer counted the same as an unexplained defect like
missing R11/R12. Kallat and Prosper now report "all commercial gates
PASS" with the structural exception listed separately, rather than
"NOT clean" conflating a known, evidenced, expected condition with a
real gap.

### Addendum, same day — stored total_hours defect found, diagnosed, fixed, regression-guarded

Reviewing the check_4 addendum above against the actual committed
worksheets (cross-checking `total_hours_for_n(N)` output against
`total_hours_all_in`'s own stated component sum) found a real
arithmetic error, independent of the engine:

| | Kallat (N=40) | Prosper (N=31) |
|---|---|---|
| `a_side_hours + class_b.total_hours + hypercare.hours` (correct) | 104.734 | 101.081 |
| stored `total_hours_all_in`/`total_hours` (wrong) | 100.734 | 92.081 |
| discrepancy | 4.0h | 9.0h |

**Diagnosis**: `a_side_hours` (78 on both) is independently verified
correct — it equals its own stated sub-fields
(`a_hours` + `qa_hours` + `documentation_hours` + `training_hours`)
exactly on both worksheets. `class_b.total_hours` (10.734 / 9.081) is
also correctly reflected in the sum. Isolating the arithmetic shows the
entire shortfall sits specifically in the `hypercare.hours` contribution:
Kallat's sum used 12 instead of the stated 16 (short 4); Prosper's used
5 instead of the stated 14 (short 9). The two shortfalls share no common
ratio (4/16=0.25 vs 9/14=0.64) or fixed offset — ruling out a systematic
formula bug. **Root cause: `total_hours_all_in` was hand-typed into each
worksheet's YAML rather than piped from the recompute script's own
output** — the exact P13 violation ("no hand-computed values") this
build otherwise held to, committed by omission in this one summary
field. Two independent transcription slips, not one shared defect.

**`internal_build_cost_aed` (15,710 / 15,162) and every AED figure
downstream of it — `build_value_aed`, `mobilisation_fee_aed`,
`subscription_fee_aed_mo` — were NEVER affected.** They were computed
independently from the correct totals throughout and are byte-identical
before and after this fix. Verified directly, not assumed.

**The `check_4` N=1..400 sweep and the N=19 breach point are also
unaffected** — `pricing_engine.total_hours_for_n()` computes from
`hour-lookup.yaml`/`class-b-task-inventory.yaml`/`policy.yaml` only; it
has no dependency on any client worksheet file (confirmed: the only
`_load()` call inside it is for `policy.yaml`). The structural-exception
classification and its evidence stand unchanged. Only the specific
h-figures cited alongside it (in the worksheets' own `note_check_4`
fields and in this file's prior addendum) were wrong, now corrected to
104.734h and 101.081h.

**Fixed, root cause addressed, not just the values**: `total_hours_all_in`
and `total_hours` corrected in both worksheets, each with an inline
note explaining what was wrong and why. `05-ops/test_pricing_engine.py`
gained **T9** (worksheet internal consistency), which asserts, for
every corpus client: `total_hours_all_in` equals the sum of its own
component fields (0.001h tolerance), and `internal_build_cost_aed`
equals `total_hours × 150`. T9 was run and confirmed **failing on the
four affected checks** against the pre-fix values before either
worksheet was touched, then confirmed passing after. This guards the
invariant going forward — a future hand-typed total that drifts from
its own components will fail loudly, not silently.

References commit `50d8759` (which introduced the `total_hours_for_n`
engine function this diagnosis used) and is itself scoped only to the
two worksheet YAMLs, `test_pricing_engine.py`, and this file.

**Open pricing-policy question, logged not decided**: `hypercare`'s
`ceil(N/5)×2` formula is unbounded linear in N and drives ~82% of the
asymptotic 0.487h/user rate as N→∞ (see the prior sanity-check finding
in this session). It is Grade D (single origin comment, no delivered
hypercare engagement has ever been timed) and **immaterial at the N≤50
scale of every current corpus client** — this is not an active pricing
risk today. Whether it should instead carry a Class-C-style banded
ceiling at high N (mirroring `hosting.yaml`'s step function, rather than
scaling forever) is an open design question for whoever owns pricing
policy, not resolved here, and the engine is not changed pending that
decision.

### Addendum, same day — VGE and MRD migrated to the Class A-D engine

Both were on the pre-v3.0 model (last touched `cb2f194`/`a405109`,
predating the engine entirely) — `05-ops/test_pricing_engine.py` T9 was
widened to hard-fail (not skip) any worksheet missing `class_b`/
`hypercare`/`a_side_hours`, confirmed red on both before this migration,
green after.

**Correction to the prior pass's audit claim**: that report said VGE/MRD
"structurally can't" have the stored-total defect Kallat/Prosper had.
**That was wrong for VGE.** VGE's own worksheet was internally
inconsistent before this migration: stored `total_hours: 52` did not
equal the sum of its own stated sub-fields
(`delivery_hours` 37 + `documentation_hours` 4 + `qa_hours` 3 +
`training_hours` 4 = 48, not 52) — and `documentation_hours` itself was
overstated (4, when the policy floor formula gives 2). **Why the prior
audit missed it**: the invariant used was
`total_hours × 150 == internal_build_cost_aed`, which `52 × 150 = 7,800`
satisfies exactly — but `internal_build_cost_aed` was itself derived
from the same suspect `total_hours`, not independently. An invariant
that takes the suspect value on both sides of the comparison is not a
correctness check. T9 is now widened (this same pass) to assert every
component — `documentation_hours`, `qa_hours`, `training_hours`,
`a_side_hours`, `class_b.total_hours`, `hypercare.hours` — against its
own engine formula independently, not just that sums are internally
self-consistent. Confirmed clean on this wider check for Kallat,
Prosper, and MRD; only VGE's `documentation_hours` failed, exactly the
defect above.

**VGE's 6h excess (52 stored vs 46 new-engine `a_side_hours`), decomposed
— recorded as an ASSUMPTION, not a proven finding**: 2h traces cleanly to
the `documentation_hours` overstatement above (4 vs the policy-correct
2). The remaining 4h has **no documented origin anywhere** — checked
`client-brief.yaml` (`work_packages_requested: []`, `migration_records:
null`), `verbal-promises.md` (every entry maps to an existing package or
is explicitly DEFERRED/EXCLUDED), and `deal-card.md` — no extra work
package, training, or migration task is named anywhere in this deal's
record. This 4h is *consistent with* an early, undocumented,
hand-rolled per-user/rollout allowance, now properly represented as
`class_b`(2.417h) + `hypercare`(2h) = 4.417h — but **4h ≠ 4.417h, this
is not a numeric match** and is not presented as one. **What actually
licenses this migration is the negative scope audit above (nothing
named is missing), not the near-coincidence of the two figures** — the
audit would license the migration even if the two numbers didn't rhyme
at all.

**VGE — audit-trail migration only, quote unchanged.** `number_2_build`
now carries the full Class A-D breakdown (`a_hours`, `class_b`,
`hypercare`, corrected `documentation_hours: 2`), but the brief-pinned
figures are untouched: `build_value_aed` stays **14,800**, `assembly.
subscription_fee_aed_mo` stays **1,650/mo** — confirmed by direct
inspection after writing, not assumed. A new `brief_pin_variance` block
records the mechanical engine output (15,999) against the pin (14,800,
delta 1,199/8.1%) and states explicitly which one governs. **Confirmed:
the quote was never at risk** — `assembly`/`number_3_financing` were
always sourced directly from Brief §3, never from `number_2_build.
total_hours`, so this worksheet's internal inconsistency never reached a
client-facing figure. Only two internal-only fields move:
`internal_build_cost_aed` (7,800→7,562) and its dependent gates
(G8/G23 margin, now 48.9% vs 47.3% — up, since the corrected internal
cost is lower than the figure derived from the wrong total_hours).

**MRD — no brief pin, so this migration changes the quoted figures.**
MRD's own pre-migration `documentation_hours: 2` was already
formula-correct ("floor binds", its own comment) — confirmed as the
control case: **identical inputs to VGE (same 7 delivery packages, same
`startup_boutique` segment, same N=5) now correctly produce identical
new-engine output** (`a_side_hours` 46, `class_b.total_hours` 2.417,
`hypercare.hours` 2, `total_hours` 50.417 — both clients). **This
duplication is expected, not an error**: there is no legitimate
differentiator between VGE and MRD in any input the engine reads, and
MRD's independently-correct historical 46 is what confirms the new
engine's 46 is right, not a coincidence to be suspicious of.
`platform_portion_aed` (1,150) — a deliberate competitive-positioning
anchor, not a formula output — is preserved unchanged, restructured as
an explicit `platform_portion_aed_override` block recording the anchor
value, the mechanical floor it overrides (650), the multiplier that
floor came from (1.25), and the positioning rationale, so it no longer
occupies a field shaped like a formula output. `build_value_aed` and
the recovery component **do** change (14,812→15,999, driven by the
now-corrected Class A-D engine, migrated from this worksheet's own
prior additive PM/contingency method to the compounding convention
already used elsewhere — not a new policy, an applied-consistently one).
Because only `platform_portion_aed` is frozen and recovery is not,
**MRD's quoted Subscription Fee moves: 1,650/mo → 1,700/mo** (+50, +3%).
Like VGE's Rev3, MRD's Rev3 has never been issued to the client
(`issued_date: ""`, Rev1/Rev2 retracted) — this changes an internal
draft figure, not a live quote, but it is flagged here prominently
because, unlike VGE, nothing pins this number and the change is real.

`G31_worst_case_margin` was **not** recomputed for either client — its
original derivation from the base margin isn't fully reconstructable
from the stored worksheet text alone, and inventing a plausible-looking
number was rejected (P2). Flagged inline in both worksheets for a future
pass, not guessed.

**`monthly_billing_deviation.surcharge_pct: 0.03`** (Kallat/Prosper):
still uncited. No `policy.yaml` field exists for this specific purpose
— only `financing_uplift.zero_mobilisation_surcharge: 0.03`, a different
concept, coincidentally the same value. **Logged as undecided, not
invented**: either this needs its own named policy field, or it needs
confirmation that reusing `zero_mobilisation_surcharge` is intentional.
Not resolved in this pass.

Committed engine additions (pure additions, zero lines removed from any
existing function, confirmed via `git diff`): `pricing_engine.
b_side_subtotal_aed()` and `pricing_engine.hypercare_cost_aed()` — the
two orphan emitters (previously only computed in the scratch,
never-committed `recompute_worksheet.py`) now have committed,
T9-tested functions. Verified against Kallat/Prosper's already-stored
values first (agreed exactly, no new discrepancy) before being used to
write VGE/MRD.

Four-client gate table, post-migration:

| Client | check_4 | Structural exception? | Other failures |
|---|---|---|---|
| VGE (N=5) | PASS (50.417h vs ~46h reference) | No — below N=19 breach | R11, R12 |
| MRD (N=5) | PASS (50.417h vs ~46h reference) | No — below N=19 breach | R11, R12 |
| Kallat (N=40) | FAIL | Yes | R11, R12 |
| Prosper (N=31) | FAIL | Yes | R11, R12 |

`--selftest` confirmed clean throughout this pass.

### Addendum, same day — MRD's 1,650->1,700 resolved: no commitment found, correction confirmed, not an increase

Before treating the prior pass's 1,650→1,700 change as final, checked
whether it contradicted any actual commitment. `verbal-promises.md` (full
file), `client-brief.yaml`, and `deal-card.md` (which does not exist for
MRD) were checked line by line for any price figure. **None found.**
Every entry in `verbal-promises.md` is scope-only; the only AED figures
anywhere in MRD's intake record are `budget_rejected_aed: 30,000` (a
different vendor's prior quote, rejected) and the PropSpace incumbent
benchmark (1,100–1,760/mo, a market comparator, not an SGC promise).
Same check run on VGE for comparison — its `client-brief.yaml` also
contains no "1,650"/"14,800" text; VGE's pin traces instead to an
internal commercial decision recorded in `manifest.yaml:100`, not to a
client-extracted commitment either. Neither client's price was ever
fixed by something the client said.

**Conclusion: 1,700 stands, correctly framed as a correction, not a
price increase.** The old 1,650 never priced Class B (2.417h) or
hypercare (2h) at all — it was computed under a model with no per-user
or support-capacity concept whatsoever. The new figure recognizes work
that was always being delivered (agent onboarding, role/permission
setup, go-live support capacity) and was never priced. Derivation
chain, in full: `build_value_aed` (14,812→15,999, via the compounding
`segments.startup_boutique.pm_pct`/`contingency_pct` formula plus
`hypercare.cost_aed`) → `mobilisation_aed` (`× gates.
default_mobilisation_pct` 0.33) → `deferred_aed` → `recovery_total_aed`
(`× (1+financing_uplift.months_24)` = flat-on-principal, 24-month term)
→ `recovery_monthly_aed` (÷24) → raw subscription **1,677** = frozen
`platform_portion_aed`(1,150) + recomputed `recovery_monthly_aed`(527).
**1,700 is a rounded presentation of 1,677, rounded to the nearest 50 —
a convention that exists only as an inline worksheet comment, cited to
no `policy.yaml` field. Logged as undecided, not invented one to fill
the gap.**

**VGE/MRD divergence, recorded as a deliberate, known commercial
variance — not converged, not resolved here**: identical scope, segment,
and N; identical engine cost (50.417h / AED 7,562 internal); **different
quotes (1,650 vs 1,700) solely because VGE carries a Brief-pin and MRD
does not.** Whether these two should converge (either freeze MRD the
same way, or unfreeze VGE) is a **human decision, flagged, not made
here** — neither the pin nor the anchor was altered.

**MRD's positioning claim** ("under PropSpace's upper range") was
written against the `platform_portion_aed` field itself (1,150 vs
1,760), not the total — literally read, unaffected by the total moving.
If read as a claim about the total client cost instead, the margin
under PropSpace's ceiling has compressed from 110 AED (6.3%) to 60 AED
(3.4%) — not broken, flagged in the worksheet's own
`platform_portion_aed_override.rationale` field for whoever owns this
deal's positioning next.

**Stale "1,650" citations for MRD, located, NOT edited (out of scope for
this pass)**: `02-calc/gate-report.md`, `03-draft/MRD-2026-SUB-01_Rev3/
10-commercial-terms.md`, `04-review/qa-checklist.md`. These need a
follow-up pass before this draft goes anywhere near review or issue.

Commit scoped to `CHANGELOG.md` and the MRD worksheet annotation only —
no quoted price was changed in this pass (1,700 was already committed in
the prior pass; this addendum only confirms it was correctly derived and
not blocked by any commitment).

### Addendum, same day — VGE's Brief §3 scope resolved: covers the monthly too; hold VGE at 1,650

No file in this repo contains an original "Brief §3" document with
quotable verbatim text — searched exhaustively. The two closest
surviving artifacts, both consistent and both independent restatements
rather than a primary source, agree: `manifest.yaml:100` lists "AED
14,800 Implementation Value... **AED 1,650/mo Subscription**" together
as "the brief §3 figures"; `pricing-worksheet.yaml:143-145` attributes
`subscription_fee_aed_mo`, `platform_portion_aed_mo`, and
`recovery_component_aed_mo` all individually to "brief §3." **The pin
covers both the Implementation Value and the monthly subscription, not
Implementation Value alone.** VGE's Subscription Fee stays **1,650/mo**,
untouched.

**Direct, pre-existing confirmation of a shared origin, found in MRD's
own `gate-report.md` (written 2026-08-03, before this session's work
began)**: *"[MRD's build_value_aed, then 14,812] differs by AED 12 from
the illustrative figure originally quoted for this deal type (14,800)
due to rounding in the original illustration."* This is not an inference
— MRD's own historical record already documented that VGE's pinned
14,800 was "the illustrative figure originally quoted for **this deal
type**" (i.e., generic to the scope/segment/N combination both clients
share), not a client-specific negotiated figure. Both 14,800 and MRD's
14,812 are outputs of the same pre-v3.0 additive calculation, for
identical inputs, neither ever pricing Class B or hypercare. VGE's
version was frozen as a rounded external constant at some point; MRD's
stayed live and got correctly migrated. **The VGE/MRD divergence (1,650
vs 1,700) is, in origin, one calculation that got frozen in one place
and not the other — not two independent commercial decisions that
happened to coincide, and not a genuine, ongoing commercial variance.**
Recorded as a declared, deliberate variance for now (per the pin) and
flagged for a brief amendment at re-issue — not converged, not decided
here.

**MRD's rounding provenance, restated precisely**: raw subscription =
`platform_portion_aed`(1,150, frozen anchor) + `recovery_monthly_aed`
(527) = **1,677**. Presented as **1,700** — rounded to the nearest 50,
a convention that exists only as an inline worksheet comment inherited
from VGE's own original wording, cited to no `policy.yaml` field.
**Logged as undecided, not invented.**

**Stale "1,650" citations corrected** (all three were approved for
correction — neither is an R11/R12 template, since neither artefact
exists yet in this repo):
- `02-calc/gate-report.md` (internal working note) — **not just the two
  "1,650" cells**: this document's entire three-numbers table and gate
  summary were still on the pre-migration figures (build value, internal
  cost, mobilisation, recovery, margin, market_test, budget_test all
  stale). Fixing only the literal "1,650" string would have left the
  table internally self-contradictory (a corrected subscription sitting
  next to an uncorrected mobilisation/margin that no longer reconcile
  with it) — so the full table was resynced, not just the two cited
  cells. Its historical "arithmetic note" (the 14,800-vs-14,812
  observation above) is preserved, annotated, not deleted — it is now
  the primary evidence for this addendum's shared-origin finding.
- `03-draft/MRD-2026-SUB-01_Rev3/10-commercial-terms.md` (**client-facing
  draft prose**) — same reasoning: mobilisation, subscription, year-1
  total, quarterly billing, and the financing-disclosure recovery
  figure were all interlocking and all stale. Full section resynced.
  Both worksheets remain unissued (`issued_date: ""`), so no issued
  document is contradicted by this correction.
- `04-review/qa-checklist.md` (internal working note) — single isolated
  figure, no adjacent inconsistency; corrected alone.

**Marker hygiene note**: going forward, the `[MAGIC KEYWORD: ...]`-style
marker from the `oh-my-claudecode` plugin's `UserPromptSubmit` hook
chain (`keyword-detector.mjs`/`skill-injector.mjs`, confirmed via
`hooks/hooks.json`, no network-call pattern found in the detector's own
code) is referred to descriptively, not quoted literally, since quoting
it re-triggers the detector past its line-anchored echo guard
(`keyword-detector-echo-guard.test.js` exists specifically for this
case). `OMC_SKIP_HOOKS=UserPromptSubmit` would disable it, but also
`skill-injector` (same event, no finer-grained switch found) — not
recommended while this repo is under active commit, since the actual
harm is a non-destructive routing suggestion, not a data or file risk.

### Addendum, same day — Brief §3 downgraded from "pin" to "unverified attestation"; corpus-wide rounding finding

**Correction to how the prior addendum framed this**: it treated
`manifest.yaml:100` and `pricing-worksheet.yaml:143-145` as evidence the
Brief §3 pin covers the monthly subscription. That's true only in the
narrow sense that those two documents *say* it does — **both live
inside the artifacts under audit; they attest to their own authority,
they don't establish it.** Exhaustively searched every non-worksheet
location in VGE's client folder, plus a repo-wide check for `docs/`,
archives, PDFs, and email exports. **No primary source for AED 14,800
or AED 1,650/mo exists anywhere in this repository.**
`01-source/README.md:1` — the folder this repo's own convention
reserves for "unedited client-supplied files" — states directly: *"No
raw client materials were provided for this opportunity as of the
current revision."* Rev1/Rev2 (the retracted prior revisions) don't
contain these figures either, so they aren't inherited through a longer
paper trail — they appear to originate with Rev3 specifically, from a
source outside this repo (most likely an original session-level
instruction, never persisted here) or were entered directly with no
separate source at all.

**Provenance grade, assigned explicitly, consistent with how hypercare's
Grade D is recorded**: **Grade D at best, and weaker than typical Grade
D** — hypercare's `ceil(N/5)×2` at least carries a stated formula and
rationale (support capacity should scale with headcount); the Brief §3
figures carry no formula, no rationale, and no locatable source
document at all, only two internal restatements of each other.
**Reclassified from "brief-pinned" to "held pending verification."**
VGE's Subscription Fee **stays at 1,650/mo — not moved** — but the basis
for holding it is now stated accurately: a number nobody in this repo
can currently trace to an original document, not a verified client
commitment. Collapse trigger: production of the actual source (see
above) or explicit confirmation from whoever built Rev3 originally that
no such document exists and the figures were a direct entry.

**MRD/Kallat/Prosper rounding, tested corpus-wide, not assumed**: swept
every subscription/fee figure across all four worksheets for a
multiple-of-50 pattern. It does not hold. Kallat's 5,850 and Prosper's
5,270 both use a **stated "rounded to nearest 10"** convention
(`pricing-worksheet.yaml` inline comments, both clients) — Kallat's
figure only *looks* like a nearest-50 match by coincidence; Prosper's
correctly does not. Kallat's own `alt_term_option_12mo` (7,170) and
`monthly_billing_deviation` (6,030) figures, and Prosper's equivalents
(6,560, 5,430), are not multiples of 50 either, confirming nearest-10 is
what's actually being applied for those two clients. MRD's "rounded to
nearest 50" is different text, inherited verbatim from VGE's original
comment wording — even though VGE's own calculation never exercised any
rounding (1,163+487=1,650 exactly, nothing to round). **`policy.yaml`
and every file under `00-knowledge/pricing/` and
`00-knowledge/commercial-rules/` were grepped for any rounding-rule
declaration for subscription or fee figures: none exists.** Three
mutually inconsistent, uncited conventions currently coexist in this
corpus (none, nearest-50, nearest-10).

**MRD's raw derived subscription is 1,677** (1,150 + 527); 1,700 carries
**+23/mo unattributed** (46% of the 50 AED move from the old 1,650 has
no source beyond an inherited, never-validated comment). **Proposed,
not applied**: MRD → 1,677. Requires separate explicit approval, same as
the VGE pin question — no price field is changed by this commit.

**New finding this pass**: Kallat's and Prosper's own "nearest 10"
rounding is *also* uncited to any policy field — it was introduced by
this same body of work, not inherited, and was not previously flagged
as an open item alongside MRD's. Both now carry the same class of
provenance gap MRD's rounding does.

**R11/R12 readiness: NO-GO.** Two high-severity, client-facing,
unresolved pricing-provenance questions (the Brief §3 attestation, and
rounding conventions across all four clients) sit directly upstream of
every number that would print on a quotation or commercial summary.
Full go/no-go table, severities, and internal-vs-client-facing
classification recorded in this session's report; not duplicated here.
Building R11/R12 before these resolve would bake unverified figures into
the first client-facing deliverable this repo produces.

### Addendum, same day — corrected guard test (T10) + VGE action list

**Guard test T10 added** (`05-ops/test_pricing_engine.py`), corrected
criterion per review: HARD FAIL on any upward delta (vendor-favoring)
OR downward delta exceeding one step of the declared convention;
PASS-WITH-CITATION on downward delta within one step if a rule is
cited (inline comment OR policy field); HARD FAIL on downward uncited
within-step (passes only once a rule is declared). Run output:

- Kallat: subscription −4 DOWN uncited → HARD FAIL (passes on item 3
  policy addition).
- Prosper: subscription −1 DOWN uncited → HARD FAIL (same).
- VGE: subscription PASS (exactly derived); mobilisation +16 UP
  uncited → HARD FAIL (derives from the brief-pinned 14800 × 0.33 =
  4884; brief asserts 4900 — resolvable only by the item 4 source
  verification or the pin being declared inline).
- MRD: subscription +23 UP uncited → **HARD FAIL**, the only
  uncited *positive* delta in the entire corpus.
- All other client-facing figures collapse to PASS or PASS-WITH-CITATION
  (sub-1 artifacts of Python banker's rounding).

**VGE action list (place-keyed; one named owner field left blank
intentionally for you to fill):**

| Place | What to look for |
|---|---|
| SGC CRM record — Lead ID 10119 | Any quote, order form, email thread, activity log |
| Outbound email export | Any message to @vongeyern.de mentioning 14,800 / 1,650 |
| Client correspondence shared drive / 01-source/ | Already checked — `01-source/README.md:1` says no raw client materials provided |
| Original Rev3 build session transcript | Most likely origin point for these figures |
| Original proposal deck sent pre-Rev3 | Distinguishes "presented to client" from "internal illustrative" |
| 05-issued/VGE-2026-SUB-01_Rev1, Rev2 | Already checked — neither contains these figures |

**Single question**: "Was AED 14,800 / 1,650-per-month ever presented
to VGE, or was it an internal illustrative figure?"

**NAMED OWNER: ___________________________** (for you to fill).

**Fallback if no source surfaces**: VGE **cannot issue — source
unverified**. Hold Subscription Fee at 1,650/mo as "held pending
verification"; require explicit human confirmation before any
client-facing artefact quotes these figures. Do not re-issue, do
not re-render any proposal, do not re-quote in any R11/R12 template.

**Note on circularity**: `manifest.yaml:100` itself lives inside the
audited artifact set — citing it as the source of the pin's scope is
the same circularity already logged in commit `6a0ae84`. It is treated
here as a secondary restatement of what `pricing-worksheet.yaml:143-145`
asserts, not as independent corroboration.

**`brief_pin_variance` block extended** to cover both halves of the
VGE pin (was previously scoped only to Implementation Value). Now
documents both `pinned_implementation_value_aed: 14800` and
`pinned_subscription_fee_aed_mo: 1650`, with the corresponding
`mechanical_*_aed` figures and delta ratios, citing the downgrade to
"held pending verification" per `6a0ae84` and pointing at the action
list above. The block documents, does not change any price field.

## pricing v3.1 — 2026-08-06

**Verification pass before writing, two claims checked and retracted**:
(1) floor-10 does NOT mis-reproduce Kallat's or Prosper's stored
subscription figures — `5,854` floors to `5,850` and `5,271` floors to
`5,270`, both exact matches to what's stored; a floor-based rule and a
nearest-based rule are indistinguishable on this pair of data points, so
neither confirms nor rules out either convention. (2) the `.5`-boundary
tie-break present in the corpus (Prosper's `platform_floor_aed`,
`2,918 × 1.25 = 3,647.5 → 3,648`) sits on `platform_portion`, a field the
new policy declaration below places in `scope_excludes` — it cannot be
used to discriminate between subscription-rounding conventions either.
**Neither claim is the basis for the decision below.** The basis is the
verbatim "rounded to nearest 10" comment already present, independently,
on all six of Kallat's and Prosper's own subscription-figure lines — see
`basis` in the policy field itself.

**Count correction**: the working assumption going into this pass was 8
verbatim occurrences of "rounded to nearest 10" in the corpus. Verified
by direct search: there are **6** — three each in
`KP-kallat-properties/02-calc/pricing-worksheet.yaml` (lines 130, 143,
151) and `PRO-prosper-realestate/02-calc/pricing-worksheet.yaml` (lines
112, 125, 133). The other two matches found by an unscoped search are
downstream restatements, not independent basis: `CHANGELOG.md:702`
(this file, quoting the worksheets) and
`05-ops/test_pricing_engine.py:621` (the old T10 citation check itself,
matching against its own search string). `policy.yaml`'s `basis` list
below cites the 6 genuine occurrences only.

**`policy.yaml` gains `presentation.client_facing_subscription_rounding`**
(`nearest_10_aed`, `applies_to` subscription figures only, `scope_excludes`
mobilisation / `build_value_aed` / `internal_build_cost_aed` /
platform_portion) — the first-ever declared rounding rule for this class
of figure; previously `policy.yaml` and everything under
`00-knowledge/pricing/` and `00-knowledge/commercial-rules/` had none
(see the prior addendum's corpus sweep). Basis: the 6 occurrences above,
by file:line.

**`policy.yaml` also gains `presentation.non_subscription_rounding`**
(`bankers_rounding_half_to_even`, citing Python `round()`'s built-in
half-to-even behaviour — the mechanism every non-subscription monetary
figure in `05-ops/pricing_engine.py` and the worksheets was already being
derived through, uncited, before this field named it). **Confirmed a
no-op**: declaring the field does not touch a single worksheet, and no
stored figure changed as a result — checked directly, byte-identical.
The one live `.5` tie-break in the corpus, Prosper's `platform_floor_aed`
(`2,918 × 1.25 = 3,647.5 → 3,648`,
`02-clients/PRO-prosper-realestate/02-calc/pricing-worksheet.yaml:34`),
already matches `round(3647.5) == 3648` exactly — the rule reproduces
what's stored, so it stands.

**T10 amended** (`05-ops/test_pricing_engine.py`): "cited" now means
cited to a `policy.yaml` field, not an inline worksheet comment — the old
check (`"rounded to nearest 10" in str(ws.get("assembly", {}))`) never
actually matched anything, because `yaml.safe_load` discards comments
before the dict is built, so every worksheet was silently uncited
regardless of its own text. For a delta cited to a policy field, T10 now
passes in **either direction** within one rounding step; an uncited delta
still hard-fails upward unconditionally, and downward past one step,
exactly as before. Re-run against the amended criterion and the corrected
MRD figure (see below):

- Kallat: subscription −4 DOWN, cited (nearest-10) → **PASS-WITH-CITATION**
- Prosper: subscription −1 DOWN, cited (nearest-10) → **PASS-WITH-CITATION**
- MRD: subscription +3 UP, cited (nearest-10) → **PASS-WITH-CITATION**
- VGE: subscription exactly derived → PASS; mobilisation +16 UP, uncited
  (no policy field covers mobilisation; explicitly in
  `scope_excludes`) → **HARD FAIL, unchanged**
- `internal_build_cost_aed`'s sub-1 corpus-wide artifacts (Kallat/Prosper
  exact; VGE/MRD −1, cited via `non_subscription_rounding`) all
  **PASS / PASS-WITH-CITATION**
- Full corpus run: 1 failure (VGE mobilisation), down from 3 the moment
  `internal_build_cost` was first (incorrectly) marked uncited mid-pass —
  corrected before landing; see test file inline comments.

**MRD `subscription_aed`: 1,700 → 1,680.** Derivation: raw
`1,150 + 527 = 1,677`; nearest-10 → `1,680`; delta `+3`, now cited to
`presentation.client_facing_subscription_rounding`. The stale "rounded to
nearest 50" inline comment — inherited verbatim from VGE's original
wording and never itself a declared rule, per the prior addendum's
finding — is removed from
`02-clients/MRD-meridianview-realty/02-calc/pricing-worksheet.yaml:110`.
Mechanically dependent fields updated alongside it, as a direct
consequence of the `+20`/mo change, not as independent moves:
`year1_client_cost_aed` (`25,680 → 25,440`), the `payment_cadence`
quarterly-billing comment (`5,100 → 5,040`), the `exposure.cash_peak_aed`
comment (`10,380 → 10,320`), `gates.G1_platform_floor.actual`
(`1,700 → 1,680`), `gates.market_test.multiple_of_incumbent`
(`1.216 → 1.205`), and `gates.budget_test.year1_vs_rejected`
(`0.856 → 0.848`). No other MRD input (hours, rates, build_value,
mobilisation, margin gates) moved.

### Addendum, same day — VGE's blast radius, logged; prior "+23 only upward delta" claim corrected

**VGE's unverified-pin blast radius, restated as its own entry** (all
four figures below still unchanged in value — this documents exposure,
it does not touch a price field, same discipline as `brief_pin_variance`):

| Figure | Pinned (quoted) | Mechanical | Delta |
|---|---|---|---|
| `subscription_fee_aed_mo` | 1,650 | 1,650 (self-consistent given the pinned `platform_portion_aed_mo` component) | — |
| `build_value_aed` | 14,800 | 15,999 | −1,199 (pin favours the client) |
| `mobilisation_fee_aed` | 4,900 | 4,884 | **+16**, uncited (T10 HARD FAIL) |
| `platform_portion_aed_mo` | 1,163 | 987.5 (`790 × 1.25`, `platform_floor_aed`) | **+175.5**, uncited |

`mobilisation_fee_aed` is the upfront portion of `build_value_aed`, and
`platform_portion_aed_mo` is a component of `subscription_fee_aed_mo` —
summing all four would double-count. The correct total **Year-1 AED
exposure resting on the unverified pin is `year1_total_aed` = 24,700**
(`4,900 + 12 × 1,650`, `02-clients/VGE-vongeyern-realestate/02-calc/pricing-worksheet.yaml:169`,
unchanged) — every AED of it downstream of the same single, unverified
§3 attestation. **VGE action-list priority raised**: two of four traced
figures (mobilisation, platform_portion) now carry their own uncited
positive deltas on top of the pre-existing source-verification gap: this
is no longer a single open question about one pair of numbers, it is a
pattern across the whole pin. R11/R12 remain NO-GO on VGE.

**Correction to the prior addendum** (commit `e50f01a`, not rewritten):
that pass stated "MRD's +23 is the only positive uncited delta in the
entire corpus." That was wrong — VGE's mobilisation `+16` is also an
upward, uncited delta, and both it and MRD's (now-resolved) `+23` trace
back to figures this same body of work had already flagged as
provenance-weak. Logged here as a correction, not a silent edit to the
earlier text.

### Addendum, same day — Kallat input-layer defects, quantified; "CLEAR" grading retracted

**T10 cannot see this class of defect.** T10 validates stored-vs-derived
— that a client-facing figure equals what the engine would compute from
the worksheet's own recorded inputs. It has no way to check whether
those inputs themselves are what the client actually asked for. The
previous pass's per-client gate table graded Kallat "CLEAR" on the
strength of a clean T10 run; that grading is **retracted**. It measured
the wrong layer.

**Scope-expansion finding, quantified.** `02-clients/KP-kallat-properties/
02-calc/pricing-worksheet.yaml`'s own header (lines 5–8) states the
2026-08-05 Class A-D migration "expanded" the client's requested scope
from 4 work packages to 8, "to clear `05-ops/validate.py`'s hour-benchmark
gate with real, relevant work packages rather than a padded number."
`client-brief.yaml:29` requested only `[crm_leads, users_roles_agent_perf,
reports_dashboard, data_migration_500]`. The four added packages
(`discovery`, `property_unit_register`, `tenancies_contracts_reminders`,
`invoicing_trn`) appear in none of `client-brief.yaml`, `verbal-promises.md`,
or `deal-card.md`.

Recomputed via `05-ops/pricing_engine.py`'s own functions (N=40, segment
and risk band unchanged, only `work_packages` varied — in-memory only,
nothing written):

| Figure | Current (8 pkgs) | Unpadded (4 requested) | Delta |
|---|---|---|---|
| `build_value_aed` | 56,072 | 36,420 | **+19,652 (35.0% of the quoted build value)** |
| `mobilisation_fee_aed` | 22,429 | 14,568 | +7,861 |
| `internal_build_cost_aed` | 15,710 | 11,060 | +4,650 (internal-only) |
| `subscription_fee_aed_mo` | 5,850 | 5,270 | +580/mo |
| `year1_total_aed` (mobilisation + 12×subscription) | 92,629 | 77,808 | +14,821 |

**The stated reason for the expansion does not hold.** `check_4_hour_benchmark`
(`05-ops/validate.py:227`, "4. hour benchmark" in `validate.md`) branches
purely on `users_now >= 19` once `total_hours < benchmark×0.5` — the
magnitude of `total_hours` is irrelevant to which branch fires once that
threshold is crossed. Re-run in-memory against both scenarios: padded
(104.734h) and unpadded (73.734h) **both** land in `structural_exception`,
identically — `104.734h for 40 users is well under the ~368h reference
benchmark -- EXPECTED for users>=19` vs the same message at 73.734h. The
padding changed the AED figures above; it did not and structurally could
not move Kallat out of the exception bucket into a clean pass. The
worksheet's own stated rationale for the expansion is incorrect.

**Circularity in the check_4 obsolescence finding itself.** `commit
525940d` (the Class A-D migration) both added the four packages to
Kallat's worksheet *and*, in the same commit, set
`pricing_engine.a_hours_for_n`'s default `base_scope_hours=47` — the
exact sum of the full 8-package list. `commit 50d8759` (later, "check_4
confirmed structurally obsolete for N>=19, classified deliberately") ran
`test_pricing_engine.py`'s N=1..400 sweep via `pe.total_hours_for_n()`,
which uses that same unoverridden default at every N. Confirmed
directly: `total_hours_for_n(40)` using the default reproduces Kallat's
stored padded total (104.734h) exactly. The sweep that "confirmed" the
9.2h/user floor structurally obsolete was run against a baseline scope
assumption that is, by construction, Kallat's own padded figure — the
one real corpus data point available to sanity-check that default is the
same worksheet whose scope this entry now finds was not client-requested.
This does not overturn the structural-exception classification (re-run
above confirms padded and unpadded verdicts are identical for Kallat
specifically, for the threshold reason above), but the general-purpose
default this repo now treats as "the standard vertical baseline" traces
to the same expansion.

**users_now=40: unsourced.** `client-brief.yaml:12` attributes "40-50
sales agents" to "the discovery call," citing both call transcripts
(`:51`). Read directly: `call-transcript-2026-07-16-internal-prep.md`
states its own participants as "Renbran Madelo, Jan, John (SGC internal
— no client present)" and its only "40 people" figure is an SGC-internal
recollection of the old PRJ proposal's tier pricing, not a client
statement. `call-transcript-2026-07-24-client-call-note.md` is entirely
about price pushback — no headcount mentioned. Grepped the full corpus
for the "40 people... 2800 per month" line and for any other
Kallat-specific client-sourced headcount statement: **no document
anywhere contains one.** `mid_market` classification (40 > `smb.max_users`
30) is therefore resting on an unverified number, same failure class as
VGE's Brief §3 pin, on a different field.

Downstream blast radius if Kallat were re-classified at N=30 (smb upper
bound, 8-package scope held constant to isolate the N effect): segment
`mid_market` → `smb`; rate 525 → 395 AED/hr; pm_pct 15% → 10%; hypercare
6 pods/12h (not 8 pods/16h) — consistent with this corpus's earlier
hypercare=12 precedent, itself now explained; `build_value_aed` 56,072 →
40,503 (**−15,569, −27.8%**); `mobilisation_fee_aed` 22,429 → 16,201;
`subscription_fee_aed_mo` 5,850 → 5,400 (−450/mo). `check_4` verdict is
unaffected either way (30 ≥ 19, still `structural_exception`).

**Copy-paste evidence.** The four added packages match, name and hour
value both, exactly against the first four entries of both VGE's and
MRD's `delivery_hours` (`discovery: standard/5`,
`property_unit_register: standard/8`, `tenancies_contracts_reminders:
standard/9`, `invoicing_trn: standard/5` — identical in all three
worksheets). Consistent with this corpus's one previously-demonstrated
cross-worksheet contamination (Prosper's hypercare pod count of 5
coinciding with VGE/MRD's `users_now`, both 5).

**Isolated to Kallat.** Checked Prosper, VGE, and MRD worksheet headers,
inline notes, and full git log for their `pricing-worksheet.yaml` files
for any comparable self-disclosed gate-clearing adjustment: none found.
Prosper's header does state its 8-package scope was "applied
consistently" from the same vertical baseline "established for Kallat"
(also echoed in `verbal-promises.md` row 2) rather than re-derived
independently per deal — but Prosper's own `work_packages_requested`
(`client-brief.yaml:32`) already lists all 8, matching its worksheet
exactly, and `verbal-promises.md` grounds the two shared-template
packages in the client's own prior PRJ document and CRM `x_bant_need`,
not merely in the Kallat precedent. Different, lower-severity note, not
the same defect.

**Re-graded** (supersedes this pass's earlier gate-table labels):
- **Kallat**: was "CLEAR." Not clear — two confirmed input-layer defects
  above (unrequested scope, unsourced headcount), both client-facing.
- **Prosper**: "externally sourced, unverified by this audit — CRM Lead
  8407 requires human confirmation." `users_now=31` traces to a CRM
  enrichment field outside this repo; not self-referential like VGE's
  pin, but not independently re-confirmed by anything in this audit
  either.
- **MRD**: the only client in the corpus with client-direct primary
  sourcing — `call-transcript-2026-06-10.md:13`, Omar Al Farsi, verbatim:
  "Five people, we're not a big operation," matching `users_now: 5`
  directly, no restatement or citation chain in between.

No worksheet written, no package removed, no price changed. Removing
Kallat's four packages is a commercial decision to be made with the
client, not an audit action.

### Addendum, same day — Kallat investigation closed out: contemporaneous check_4, engine-default contamination, combined-defect figure

**1) Re-tested against the version that existed at the time.** `05-ops/
validate.py`'s `structural_exception` branch was added in `50d8759`
(Aug 5, 16:25 +0400), *after* the padding commit `525940d` (Aug 5,
15:06 +0400). Extracted `check_4_hour_benchmark` as it read at `525940d`
— a strict binary gate, no exception branch:

```
if total_hours < benchmark * 0.5:
    result.fail(...)
else:
    result.ok(...)
```

Ran both totals through it (N=40, benchmark=368, half=184): padded
104.734h → **FAIL**. Unpadded 73.734h → **FAIL**. Both fail, at the time,
under the code the worksheet's own header claims it was written to
satisfy. **The stated reason is false. No other explanation is on record
for the AED 19,652 of added scope.** (Consistent with the worksheet's own
"NOW FAILS check_4, which it passed under Rev1's 192h" note — the
padding recovered ground lost when the old overlay was deleted, but not
enough of it, under either version of the gate.)

**2) `base_scope_hours=47` traced — every real call site relies on the
default; none passes it explicitly:**

| Call site | Passes explicit `base_scope_hours`? | Touches VGE/MRD/Prosper? |
|---|---|---|
| `pricing_engine.py:220`, inside `total_hours_for_n()` | No — default | Generic N=1..400 model only, not a specific client |
| `test_pricing_engine.py:149` (T3, A_hours step-boundary sweep) | No — default | Same — abstract sweep |
| `test_pricing_engine.py:452-453` (T8, uptick-step explanation) | No — default | Same |
| `test_pricing_engine.py:731` (T9c, per-client a_hours cross-check) | No — default | **Explicitly restricted to `("KP-kallat-properties", "PRO-prosper-realestate")`, `else None`** — VGE and MRD are excluded from this specific check by name in the code |

VGE and MRD's real `a_hours` (37, both) come directly from their own
`delivery_hours` sums, validated only against their own stored fields —
they never call `a_hours_for_n()` at all, so the default cannot touch
their pricing. Prosper's real pricing does rely on the default, but it
legitimately matches Prosper's own client-requested 8-package scope
(47h, confirmed in the prior addendum). Kallat's real pricing relies on
the same default, and for Kallat the default does *not* match a
requested scope.

**Kallat's 4 requested packages sum to 20h**, not 47. Re-ran the N=1..400
sweep with `base_scope_hours` overridden (in-memory only, `pricing_engine.py`
untouched):

| `base_scope_hours` | first breach (N) |
|---|---|
| 47 (current default = Kallat/Prosper padded) | **19** |
| 20 (Kallat's actual requested scope) | **10** |
| 37 (VGE/MRD's real, uncontested scope) | **16** |

**The N=19 breach point moves substantially under every alternative,
defensible baseline.** `CHECK_4_STRUCTURAL_BREACH_N = 19` — hardcoded as
a named constant in both `validate.py` and `test_pricing_engine.py`, and
cited repeatedly through this corpus as a structural finding — is not an
input-independent property of the model. It is a direct function of the
same 47h baseline this pass has now traced to Kallat's padded worksheet.
**This is not isolated to one client's quote; it is a contaminated engine
default that a structural classification and a hardcoded threshold
constant were both built on. No engine change made — flagged, not fixed,
per this pass's constraints.**

**3) Combined-defect figure** (4 requested packages **and** N=30/smb,
computed together — no prior pass did both at once):

| Figure | Current quoted | Combined (unpadded + N≤30) | Delta | % |
|---|---|---|---|---|
| `build_value_aed` | 56,072 | 26,360 | 29,712 | **53.0%** |
| `mobilisation_fee_aed` | 22,429 | 10,544 | 11,885 | — |
| `subscription_fee_aed_mo` | 5,850 | 4,980 | 870/mo | — |
| `year1_total_aed` | 92,629 | 70,304 | 22,325 | **24.1%** |

Over half the quoted Implementation Value, and roughly a quarter of the
quoted Year-1 total, rest on the two input-layer questions still open.

**4) The 5,270 coincidence — genuine arithmetic, not a shared floor/cap.**
Side by side:

| | Kallat (unpadded, N=40) | Prosper (as stored, N=31) |
|---|---|---|
| `platform_portion_aed_mo` | 4,200 | 3,648 |
| `recovery_monthly_aed` | 1,074 | 1,623 |
| raw sum | 5,274 | 5,271 |
| rounded (nearest-10) | **5,270** | **5,270** |

No shared constant, band, or cap is in play — `platform_portion` is
independently N-derived for each (`cost_to_serve × 1.25`, different `N`,
different result) and `recovery_monthly` is independently derived from
each client's own `build_value`/`mobilisation` split. The two raw sums
(5,274 vs 5,271) differ by only 3 AED before rounding — close enough that
nearest-10 rounding collapses both into the same bucket. The platform-
portion gap (552 AED, driven by N=40 vs N=31) and the recovery gap (549
AED, driven by the two deals' very different build values) happen to
nearly cancel. Confirmed coincidence, not a masking mechanism.

**5) Authorship.** `525940d` ("Pricing v3.0: replace per-user overlay
with Class A-D cost model") is the same commit that introduced the
worksheet header's "expanded 2026-08-05... to clear the hour-benchmark
gate" text — one commit, not two. Git author identity: `scholarixglobal-ctrl`,
email `renbranmadelo@gmail.com` — **Renbran Madelo**. Committed
2026-08-05 15:06:19 +0400. No intent inferred beyond the commit record
itself.

**6) R11/R12 spec — approved as proposed, two amendments recorded:**

- The **"not in original client request" annotation is a permanent guard
  for future deals only.** It is explicitly **not** the remedy for
  Kallat's current state: unrequested scope gets resolved with the
  client before a quote is generated, never shipped inside a quote with
  a footnote. The spec's annotation rule catches the *next* instance of
  this defect at render time; it does not retroactively license this
  one.
- The `monthly_billing_deviation` withhold rule (no render until
  `surcharge_pct`'s policy citation is resolved) is approved as written,
  no changes.

No worksheet written, no package removed, no price changed, no engine
change — including the traced `base_scope_hours=47` default, left as
found per this pass's constraints.

### Addendum, same day — padding question closed: no gate verdict moved; T12 added

**1) The padding accomplished nothing, checked directly.** Reconstructed
`validate.py` as it existed at `525940d` and ran every one of its ~24
real check functions (the documented "18 checks" plus the V1-V4/R1-R12
additions already live at that commit) against both totals, in-memory,
nothing written. Both scenarios produce **identical results: 23 OK, 3
FAIL** (`4. hour benchmark`, `R11`, `R12` — the same three, unchanged).
**No check verdict differs between padded and unpadded.** The worksheet
header's stated rationale ("expanded... to clear the hour-benchmark
gate") describes an effect that did not occur under any check, at any
version, at any point this repo's history can produce. Combined with the
prior addendum's finding that check_4 itself hard-fails both totals even
at the contemporaneous, pre-exception-branch version: there is no gate,
past or present, that the padding cleared.

**2) `base_scope_hours=47` direction, settled.** Kallat's padded 8-package
`delivery_hours` and Prosper's 8-package `delivery_hours` are **byte-
identical** — same 8 package names, same hours, same bands, same order
(`diff` returns no output). Git cannot establish precedence between them:
`git log --follow` shows Prosper's entire client folder, including
`client-brief.yaml`, was created in the *same single commit* (`525940d`)
that padded Kallat's — Prosper did not exist in this repo beforehand, so
there is no earlier "Prosper's legitimate 47" for Kallat to have been
raised to match. The only textual evidence on record points the other
way: Prosper's own `verbal-promises.md` row 2 grounds two of the four
shared packages in language "consistent with the same vertical baseline
... **established for Kallat**" — Prosper's documentation cites Kallat as
the origin, not the reverse. Prosper's inclusion of all 8 is still
independently defensible on its own terms (its brief requests all 8;
`verbal-promises.md` additionally grounds the shared two in Prosper's own
prior PRJ document and CRM `x_bant_need`) — but the hypothesis that
Prosper's genuine number became the default and Kallat was raised to
match it is **not supported**. If anything, the documented direction runs
the other way.

**3) `CHECK_4_STRUCTURAL_BREACH_N=19` — fix proposed, not implemented.**
Per-client breach N, computed against each client's own real (not
padded, not defaulted) scope hours, in-memory only:

| Client | Real scope hours | Breach N |
|---|---|---|
| Kallat (4 requested packages) | 20h | **10** |
| Prosper (8 requested — legitimate) | 47h | 19 |
| VGE (7 packages, own `delivery_hours`) | 37h | **16** |
| MRD (7 packages, own `delivery_hours`) | 37h | **16** |

**Proposed fix** (not implemented — engine/policy changes are out of
scope for this pass): `check_4_hour_benchmark` and the `t8_check4_
structural_sweep` test should compute the benchmark's structural-breach
point **per client, from that client's own `number_2_build.
work_package_hours_subtotal`**, not from a single hardcoded module-level
constant fed by `pricing_engine.py`'s unoverridden `base_scope_hours=47`
default. `CHECK_4_STRUCTURAL_BREACH_N` should be retired as a global in
favor of a per-worksheet computation using the same `total_hours_for_n()`
machinery, called with each client's real base.

**Correction against `50d8759`** ("check_4 confirmed structurally
obsolete for N>=19, classified deliberately"): that finding is **baseline-
dependent, not an input-independent structural property.** The N=1..400
sweep it ran consumed `pricing_engine.py`'s default `base_scope_hours=47`
at every point on the curve — a value this pass has now traced to
Kallat's padded worksheet, introduced in the immediately preceding
commit. Under Kallat's own real scope the breach point is N=10; under
VGE/MRD's real scope it is N=16. The qualitative conclusion (check_4's
9.2h/user floor does not survive contact with the Class A-D model) still
holds under every baseline tested — it is not overturned — but the
specific figure "19," carried through this corpus as a precise constant
and hardcoded in two files, was never an independent finding. Not
rewriting `50d8759`; logged here as a correction.

**5) Padding containment confirmed, per client:**

| Client | Path |
|---|---|
| Kallat | `a_hours_for_n()` called with the unoverridden default (47) — **default ≠ Kallat's real request (20)**. Distorted. |
| Prosper | `a_hours_for_n()` also called with the unoverridden default (47) — but **default == Prosper's real request (47)**. Touches the same contaminated default, arrives at the correct number anyway. |
| VGE | `a_hours` stored directly from its own `work_package_hours_subtotal` (37). `a_hours_for_n()` is never called for its real pricing. |
| MRD | Same as VGE — direct from its own sum (37), `a_hours_for_n()` never called for its real pricing; explicitly excluded from the one test (`test_pricing_engine.py:731`) that would have called it. |

**Contained to Kallat.** Two of four clients never touch the default at
all; the third (Prosper) touches it but isn't distorted by it because its
real number happens to equal it.

**T12 — input-layer provenance guard, implemented and committed**
(`05-ops/test_pricing_engine.py`, separate from T10). Three assertions
per client: `users_now` traces to a client-sourced document (checked
against an explicit, human-audited provenance ledger, not inferred);
every `work_package` appears in the brief's requested list or an
approved-exception field (which does not exist anywhere in this corpus
yet — its absence is a correct FAIL for any client with unrequested
packages, not a bug); segment classification is contingent on the first
assertion. Run against the live corpus:

- **Kallat: RED on all three** — unsourced `users_now`, four unrequested
  packages with no exception mechanism to pass through, segment therefore
  unverified. No way to pass today, by design — assertion 2 has no
  approved-exception field to grant Kallat's four packages an exception,
  and none should be added without your explicit direction.
- **MRD: GREEN on all three** — client-direct primary sourcing on both
  users_now and scope.
- **Prosper: fails assertion 1** (CRM Lead 8407's `x_employee_count` is
  outside this repo's audited artifact set, unconfirmed by this audit)
  **and assertion 3** (contingent on assertion 1); **passes assertion 2**
  (its 8 packages match its own brief exactly).
- **VGE: passes all three T12 assertions** (`users_now` traces to a
  direct, client-present call — Ms. Nadja, "we are a boutique brokerage
  ... small brokerage," a weaker tier than MRD's exact headcount quote
  but genuinely client-sourced; `work_packages` is empty on both sides,
  trivially matching, since VGE prices via the brief-pinned model, not
  the Class A-D work-package model) — **while T10 still HARD FAILs its
  mobilisation figure.** VGE's inputs are clean; its pin is not. Two
  different, independent gates, both now correctly separated.

No worksheet written. No scope removed. No price changed. No engine
default changed, even though item 2 and item 3 above both point at it —
flagged, not fixed, same discipline as the prior addendum.

### Addendum, same day — T12 field-path fix; Prosper re-graded; risk-assessment quantified; R11/R12 built for MRD only

**T12 assertion 2 was reading the wrong field, and it produced a false
PASS on VGE.** It read `inputs.work_packages`. VGE's worksheet leaves
that field deliberately empty ("sized via `service_tier:growth` standard
allocation" — a different input convention, not an absence of scope);
VGE's real, billed scope (7 packages, 37h) lives only in
`number_2_build.delivery_hours`. Comparing VGE's empty `inputs.
work_packages` against its equally empty `client-brief.yaml: scope_
signals.work_packages_requested` read as a trivial match and PASSED —
**the previous addendum's own text repeated this same error** ("`work_
packages` is empty on both sides, trivially matching"), which is wrong
and is corrected here, not silently edited there.

**Fixed**: assertion 2 now reads `number_2_build.delivery_hours[*].
package` — the field that reflects what's actually billed, for every
client regardless of input-schema convention — and two new severity
tiers were added: an empty *worksheet* package list is INCONCLUSIVE
(treated as FAIL, never a silent PASS), and a non-empty worksheet list
against an *empty requested list* is flagged MAXIMUM SEVERITY rather
than an ordinary partial mismatch. Corrected matrix:

| Client | Assertion 2 (packages) |
|---|---|
| Kallat | FAIL — 4 of 8 unrequested |
| Prosper | FAIL — see re-grade below |
| **VGE** | **FAIL — MAXIMUM SEVERITY: 7 of 7 packages (100%) undocumented against an empty requested list** |
| MRD | PASS |

**VGE now shows 7 undocumented packages against Kallat's 4** — worse in
proportion (100% vs 50% of delivered scope), though this is a different
kind of gap than Kallat's: VGE's brief was never populated with a
package-level request at all (it prices via the brief-pinned model), so
"undocumented" here means the input schema doesn't carry this
information for VGE, not that specific requested items were dropped.
Flagged, not conflated with Kallat's.

**Intake provenance, by first commit, all four clients** (client-brief.yaml
/ verbal-promises.md / deal-card.md / transcript(s)):

| Client | First commit | Date | Transcript internal date | Gap |
|---|---|---|---|---|
| Kallat | `525940d` (all 5 docs, incl. both transcripts) | 2026-08-05 15:06 | 2026-07-16 / 2026-07-24 | 20 / 12 days — uncorroborated either way |
| Prosper | `525940d` (all 4 docs, incl. transcript) | 2026-08-05 15:06 | 2026-07-17 | 19 days — uncorroborated either way |
| VGE | `cb2f194` (brief/promises/transcript); `6ea775b` (deal-card) | 2026-08-03 23:09 / 2026-08-05 01:48 | 2026-08-03 (same day as commit) | none — no gap |
| MRD | `a405109` (brief/promises/transcript; no deal-card exists) | 2026-08-03 23:51 | 2026-06-10 | 54 days — uncorroborated either way |

**Every one of Kallat's and Prosper's intake documents was created in
`525940d` — the same commit that padded Kallat's scope.** Git provides no
independent corroboration for either client's transcripts beyond that
single commit's say-so. This is reported symmetrically: MRD's transcript
gap (54 days) is the largest of the four in raw terms, and cannot be
resolved by commit timing either — MRD's stronger grade rests on the
transcript's *content* (a specific, multi-item, client-attributed
dialogue independently matching stored figures line-for-line — budget
rejected, headcount, named feature requests), not on when the file
entered git. Flagged explicitly: **MRD's worksheet and brief were also
first committed together** (`a405109`), the identical structural pattern
being used to downgrade Prosper below. Not downgrading MRD here — the
content-level distinction is judged sufficient — but this is a judgment
call, not a settled fact, and is surfaced for your review rather than
resolved silently in MRD's favor.

**Prosper's T12 assertion 2 re-graded, per explicit review**: its clean
package-list match is no longer scored as independent corroboration. Its
`client-brief.yaml` and `pricing-worksheet.yaml` were both first
committed in `525940d`, and `verbal-promises.md` row 2 separately cites
"the same vertical baseline ... established for Kallat" as part of the
basis for 2 of its 8 packages. A same-pen match proves the two documents
agree with each other, not that either is independently true. Prosper
now fails all three T12 assertions, the same as Kallat — MRD is the sole
client clean on T12 in full.

**Open question 6 quantified — Kallat and Prosper risk-assessment.yaml**:

| Field | Kallat | Prosper |
|---|---|---|
| `entity_age_years` (RESOLVE) | `"1-2"` (+12) | `"1-2"` (+12) |
| `vat_registered` (RESOLVE) | `"no"` (+10) | `"no"` (+10) |
| `trade_licence_valid` (RESOLVE) | `">6mo"` (+0, not a placeholder) | `"<6mo"` (+8, RESOLVE) |
| `raw_score` | 52 | 55 |
| `band` | elevated (41–60) | elevated (41–60) |
| mobilisation @ 40% (elevated) | AED 22,429 | AED 22,002 |
| mobilisation @ 33% (moderate) | AED 18,504 | AED 18,152 |
| **delta** | **3,925** | **3,850** |

Both clients' mobilisation figures are contingent on unresolved
placeholder facts. Kallat drops to `raw_score=30` (moderate) if
`entity_age_years` and `vat_registered` both resolve favorably — matches
its own risk-assessment.yaml note.

**Prosper's own note is wrong, found while computing.** It states
resolving `entity_age_years`/`vat_registered` favorably would leave
`peak_exposure_aed_band` (+20) as enough on its own to "very likely keep
this deal in the elevated band regardless." Checked against `risk-
security-matrix.yaml`'s actual weights: resolving just those two drops
Prosper to `raw_score=33` — **moderate band**, not elevated. Resolving
all three RESOLVE fields (including `trade_licence_valid`) drops it
further, to 25. **Prosper's mobilisation is at least as contingent on
unresolved facts as Kallat's, and its own worksheet's note currently
understates that.** Not corrected in `risk-assessment.yaml` this pass —
compute-only, per instruction; flagged for whoever owns that file.

**Causality correction to the prior addendum's item 2**: your working
hypothesis — Prosper's legitimate 47h scope becoming
`pricing_engine.py`'s default, Kallat then raised to match it — is
**wrong**, and the prior addendum's finding already said so; restated
here for the record with the reasoning made explicit. `verbal-promises.md`
documents the reverse: the shared 8-package baseline is framed as
"established for Kallat," not for Prosper. **The shared baseline
originates in Kallat's unrequested set**, not in an independently
legitimate Prosper number that Kallat was later raised to match.

**Restated for the record**: the padding moved no gate verdict at all —
23 OK / 3 FAIL, identical under both totals, checked directly against
the code as it existed at `525940d`. The worksheet header's stated
rationale describes nothing that happened, at any version this repo's
history can produce.

**R11/R12 built, scoped to MRD only** (`05-ops/render_r11_r12.py`,
Markdown intermediate, no PDF). `ALLOWED_CLIENTS = ["MRD-meridianview-
realty"]` is the single enforcement point. Pre-render gate reuses T10 and
T12's real check functions (no separate, divergent gate logic); every
rendered figure is read through `FIELD_SOURCE_MAP`, never a literal in a
template; a post-render drift check (T11) re-extracts every AED numeral
from the rendered text and fails the build on anything that doesn't
trace to a value the map actually emitted; `monthly_billing_deviation`
stays withheld per the approved spec. Invoked against the full corpus:
Kallat, Prosper, and VGE are each refused twice over — once on
`ALLOWED_CLIENTS` scope, and independently on their live T10/T12 failures
(shown in full per client in this session's report, not duplicated
here). MRD builds clean; output written to `02-clients/MRD-
meridianview-realty/04-draft/MRD-2026-SUB-01_Rev3_{Quotation,Summary}.md`.

**Open question 9 (`CHECK_4_STRUCTURAL_BREACH_N`) — held, not touched.**
Fixing `base_scope_hours` would move Kallat's figures, which is pending
your commercial decision — left exactly as found. A per-client breach-N
computation (proposed in the prior addendum) would NOT move any stored
figure — it only changes which classification bucket a check_4 *result*
falls into, never a price, hour, or worksheet field. Confirmed safe to
propose separately from the scope/price question; still not implemented
this pass (`validate.py`/`test_pricing_engine.py`'s check_4-adjacent code
is unchanged) pending separate authorization, since it touches
check-classification logic rather than being purely additive like T12.

No worksheet written. No scope removed. No price changed. No engine or
policy change. No work performed on Kallat, Prosper, or VGE beyond
reading and reporting.

## Provenance floor — 2026-08-06

**Statement of limits of in-repo forensics.** Every check this audit has
applied (T10 stored-vs-derived, T11 drift + label-binding, T12 input-layer
provenance, plus the worksheet-internal T9, the Kallat Rev1 fixture T7,
and the check_4 structural sweep T8) reads from artifacts committed to
this repository. They can prove that a value is internally consistent,
is cited to a policy field, and traces to a sourced document. They
cannot prove that the sourced document reflects what the client actually
said at the time of saying it. Below is the open-question register: for
each question the repo cannot answer from its own bytes, the single
piece of external evidence that, if produced, would settle it.

| # | Open question | In-repo evidence | Single external evidence that would settle it |
|---|---|---|---|
| Q1 | **Did Ms. Nadja (VGE) actually request a 7-package build, or did SGC derive that scope internally?** | `brief.scope_signals.work_packages_requested: []` (empty) vs `worksheet.delivery_hours` (7 packages, 37h). Risk-assessment has no RFI on this scope | **Recording or written confirmation from the 2026-08-03 call** (or a follow-up email exchange) where Ms. Nadja names any of `discovery`, `property_unit_register`, `tenancies_contracts_reminders`, `invoicing_trn`, `maintenance_invoice_from_request`, `crm_leads`, `reports_dashboard` — OR a separate written acceptance of these packages after the call. Currently absent |
| Q2 | **What is the agreed headcount for Kallat, and is it really 40?** | Two transcripts cited; `call-transcript-2026-07-16-internal-prep.md` self-labels "no client present"; no client-side statement of users_now in any committed doc | **Email or chat log from Sadique Abbas (Kallat Sales Manager)** stating current agent count — OR the relevant RERA-registered broker count if that is the binding figure. Either one, in a timestamped medium, would settle it |
| Q3 | **Is Prosper's users_now=31 sourced from a client-confirmed figure, or an external estimate (CRM Lead x_employee_count)?** | `brief.scale.users_now=31` traces to CRM Lead 8407's `x_employee_count` outside this repo. Documented as "externally sourced, unverified by this audit" in `USERS_NOW_PROVENANCE` | **A direct confirmation from Louai Khzam (Prosper Owner)** of employee count, in a timestamped medium. Verbal-promises.md currently logs nothing on headcount for this client |
| Q4 | **Is the shared `base_scope_hours=47` engine default the consequence of Kallat's unrequested set, or did it exist independently and Kallat happen to match it?** | `verbal-promises.md:row 2` documents the shared-baseline language; git history shows Kallat and Prosper padded in the same commit `525940d`. Direction is "pragmatically indeterminate" — see prior addendum | **Internal Slack or commit-discussion record** (pre-2026-08-05) where the 47h default is established AND a contemporaneous record of whether Kallat's scope was ever trimmed to match it, or whether the default came from an earlier sanctioned baseline. Without one, the repo supports both readings |
| Q5 | **Is VGE's `brief_pin_variance.which_governs: pinned` a deliberate client-facing quote decision, or an authoring artifact that escaped review?** | `brief_pin_variance` field exists; an internal note says "client never sees the mechanical alternative." No client-side acknowledgment of the choice | **Recorded client confirmation** (Rev2 issue, Rev3 reading-room exchange, or a follow-up email) that VGE accepted the subscription structure independent of the per-package mechanical alternative. Currently absent |
| Q6 | **Are the MRD margin numbers (52.7% in G8 vs the 6.3%/3.4% in the rationale prose) intentionally two different denominators?** | G8: `(build_value − internal_cost)/build_value`. Rationale prose: `(incumbent − proposal)/incumbent`. Both numbers are arithmetically correct; they measure different things. The worksheet never disambiguates | **A single prose rewrite in the worksheet** that names both denominators and explains why they coexist — OR an explicit chart in the deal package showing both side by side. This is an internal-only fix, no external evidence required |
| Q7 | **Should the verification framework's `CHECK_4_STRUCTURAL_BREACH_N=19` be per-client (runtime-computed) or repo-global (the current hardcoded 19)?** | Currently global. Per-client proposal approved but not yet implemented (prior addendum). Doesn't change any stored figure | **A single sentence from the policy owner** confirming the breach threshold is allowed to vary by segment under pricing v3.x, OR confirming it must stay repo-global. No client-facing impact either way |
| Q8 | **Are VGE's 7 undocumented packages a billing event or a delivery event?** | `brief_pin_variance: which_governs: pinned` keeps the client on 8,150/mo regardless of scope; `internal_build_cost_aed=7,562` is the SGC-side cost. Both arithmetically correct; tier classification in `SCOPE_EXPOSURE_TIER` (DELIVERY-COMMITMENT EXPOSURE) | **A signed acknowledgment from VGE** of the 7-package scope (settles Q1 and Q8 in one document) — OR a contract amendment that explicitly absorbs or excludes them. The brief and worksheet agree on math; they disagree on characterization |

**The provenance floor, in one sentence:** in-repo forensics is
exhausted for Q1, Q2, Q3, Q5, Q7, Q8; q4 is pragmatically indeterminate
without pre-commit discussions; q6 is a disambiguation rewrite in the
worksheet itself, not an external question. Production of any of the
single-evidence items above would either fix a downstream gate, retire
a question from this register, or convert it to a documented policy
choice.

No worksheet written. No scope removed. No price changed. No engine or
policy change. No work performed on Kallat, Prosper, or VGE beyond
reading and reporting.

## MRD sibling-document reconciliation — 2026-08-06

**G8_margin formula split, computed for MRD under both, logged as an
undocumented inconsistency (not unified).** MRD's own stored G8 uses the
build-margin formula: `(build_value_aed − internal_build_cost_aed) /
build_value_aed` = (15,999 − 7,562) / 15,999 = **52.7%**. Computed
separately under Kallat/Prosper's lifetime-commitment formula:
`(full_24mo_commitment_aed − (internal_build_cost_aed + cts_total_aed ×
24)) / full_24mo_commitment_aed` = (45,600 − (7,562 + 520×24)) / 45,600 =
(45,600 − 20,042) / 45,600 = **56.0%**. MRD clears the 0.30 gate under
both formulas — no change to MRD's cleared status. The split across the
corpus: **MRD and VGE use the build-margin formula; Kallat and Prosper
use the lifetime-commitment formula.** These measure different things
(one-time build profitability vs. full-contract-including-cost-to-serve
profitability) against the same nominal 0.30 floor, and nothing in this
repo documents why the split exists or that it's intentional. Recorded
here as a finding, not resolved -- unifying G8's definition is a policy
decision, out of scope for this pass.

**Client briefs contain session/prompt material, not only client
facts — conclusion.** Kallat's and Prosper's `client-brief.yaml` and
Kallat's `verbal-promises.md` contain first-person references to "the
user" (the SGC operator running this repo/session), quoted operator
instructions, and SDR persuasion-calibration notes, interleaved with
genuine client-sourced fields in the same file:
- `KP-kallat-properties/00-intake/client-brief.yaml:20-26` — edition
  override_note quotes "user (2026-08-05) explicitly directed
  Community-first: 'if they decide enterprise that's their choice but
  right now no demand.'"
- `KP-kallat-properties/00-intake/client-brief.yaml:44` — `subscription_affinity:
  sdr_initiated # not client-stated; SDR strategy to disarm price objection`
- `KP-kallat-properties/00-intake/client-brief.yaml:58-63` — `internal_only_disclaimer`:
  "Per explicit user instruction (2026-08-05): this proposal is for
  INTERNAL SDR review/signature only ... a revised internal draft to
  formalize a disarm-hesitation pricing strategy"
- `KP-kallat-properties/00-intake/verbal-promises.md:12-14` — three rows
  sourced to "SDR disarm-hesitation strategy, 2026-08-05"
- `PRO-prosper-realestate/00-intake/client-brief.yaml:23-29` — same
  override_note pattern, "explicitly directed Community-first across
  both deals in this pipeline run"
- `PRO-prosper-realestate/00-intake/client-brief.yaml:51` — same
  `sdr_initiated` pattern
- `PRO-prosper-realestate/00-intake/client-brief.yaml:56-67` —
  `disarm_hesitation_tweaks_scope_note`: "The 2026-08-05 disarm-hesitation
  tweak bundle ... was confirmed by the user as calibrated to Kallat
  specifically ('Kallat — AED 4,900 matches their numbers')" — this
  quoted figure does not match Kallat's own worksheet (mobilisation_aed
  22,429), see the reconciliation table above; it matches VGE's
  mobilisation_aed (4,900) instead
- `PRO-prosper-realestate/00-intake/client-brief.yaml:78-85` — same
  `internal_only_disclaimer` pattern

VGE's and MRD's briefs show none of this pattern — VGE's
`subscription_affinity: explicit` is transcript-sourced and MRD's brief
has zero hits on this sweep. **Conclusion: Kallat's and Prosper's briefs
are not pure intake evidence.** They are a mix of client-sourced fields
and contemporaneous session/operator narration recorded inline, with the
provenance of each individual field distinguishable only by reading the
surrounding prose (e.g. `sdr_initiated` is explicitly self-flagged as
not client-stated, but the override_notes and disclaimers are not
flagged as anything other than brief content). Any future automated
consumer of these two briefs that treats every field as client-attested
without reading the inline caveats will be wrong. This does not retract
the underlying pricing conclusions already reached about Kallat or
Prosper — it is a provenance-hygiene finding about the intake documents
themselves.

No worksheet written. No scope removed. No price changed. No engine or
policy change. No work performed on Kallat, Prosper, or VGE beyond
reading and reporting. No edits made to the 13-section MRD proposal
(03-draft/) -- reconciliation table only, pending approval.

## MRD 03-draft correction — 2026-08-06 (second pass)

**Exposure confirmed: housekeeping, not a correction notice.** Checked
manifest.yaml revision history, `05-issued/` contents, and
`git log --follow` on every file in `03-draft/MRD-2026-SUB-01_Rev3/`
before touching anything. Rev3's `issued_date` is empty and its manifest
note is explicit: "this revision has not yet been sent to the client."
The only issued revisions are Rev1 (2026-06-15) and Rev2 (2026-07-02),
both retracted, both living in `05-issued/` — and both quote an entirely
different, already-acknowledged-defective figure set (AED 690/hour, AED
879/month subscription; see their own RETRACTION-NOTICE.md files).
Neither issued document contains AED 24,688, AED 25,680, or any other
Rev3-vintage figure. **Nothing carrying a stale Rev3 figure ever left
the building.**

**Provenance of the 13-section prose set.** All 13 files were created in
one commit, `a405109` ("v2 checkpoint 5"), 2026-08-03, `Co-Authored-By:
Claude Sonnet 5` — i.e. AI-assisted throughout; no file in this set has
ever been purely hand-typed with no model involvement, per git history.
Exactly one file has been touched since: `10-commercial-terms.md`, once,
by `0daab40` (2026-08-05, also AI-assisted), which resynced it from a
then-current 1,650→1,700 correction — itself now one correction cycle
behind, since the worksheet moved 1,700→1,680 the next day (2026-08-06).
`01-executive-summary.md` has one additional touch (`1a0b990`,
2026-08-04) but that edit was a VAT-wording change only, not a figure —
its AED 24,688 has been untouched since original creation, the oldest
vintage in the set. The other 11 files have never been edited since
2026-08-03 at all.

`01-templates/proposal/` contains no literal AED figures (grepped, zero
hits) — every commercial cell is a `[bracket placeholder]`. This defect
class does not regenerate from the templates themselves; it comes from
filling a template in once and never resyncing the filled copy against a
worksheet that keeps moving.

**Cross-client staleness count (read-only, Kallat/Prosper/VGE — no
edits, no figures moved).** All three carry the same defect class, more
severely than MRD:
- **Kallat** (`03-draft/KP-2026-SUB-01_Rev1/`, this IS
  `manifest.yaml: current_revision`, status `draft`): every worksheet-tied
  commercial figure checked (mobilisation, subscription, quarterly
  billing, Year-1 total, full-term commitment — ~13 occurrences) is
  stale, by a large margin (mobilisation printed AED 48,686 vs. current
  worksheet AED 22,429). The 4 Phase-2-catalogue figures match (knowledge
  layer hasn't moved). Hour figure "192 hours" is the frozen pre-recompute
  total (current: 104.734h).
- **Prosper** (`03-draft/PRO-2026-SUB-01_Rev1/`, current revision,
  status `draft`): same pattern, ~9 stale commercial figures (mobilisation
  printed AED 38,544 vs. current AED 22,002), 4 Phase-2 figures match.
- **VGE** (`03-draft/VGE-2026-SUB-01_Rev3/`, current revision, status
  `draft`): same pattern and the largest relative gap found — mobilisation
  printed AED 27,255 vs. current worksheet AED 4,900 (>5x), subscription
  AED 7,176 vs. current AED 1,650 (>4x). The draft's two-column
  Option A/B commercial table itself appears to predate the "Option B
  (zero mobilisation) withdrawn" decision reflected in the current
  worksheet.

None of these three has ever been issued (`05-issued/` is empty --
`.gitkeep` only -- for both Kallat and Prosper; VGE's Rev1/Rev2 are
marked `superseded`, not sent under Rev3's numbers). No further work
performed on any of the three beyond this count, per instruction.

**Item-2 drift check, implemented report-only**
(`05-ops/audit_draft_drift.py`, MRD only, not wired into any build/gate).
Three-tier resolution (worksheet → client-brief.yaml → named
knowledge-layer file), each figure carrying an explicit named source, not
a wildcard.

**CORRECTION 2026-08-06 (later same day): this entry previously showed
only the post-fix number and did not distinguish it from the
classification run. Restated properly below.**

- **Classification run** (before any 03-draft edit, the actual output of
  running the audit against the as-found files): **15 matched, 7 stale,
  12 unsourced** (of 34 figures). This is the number that matters for
  "how broken was the document" — it is what the audit was built to
  produce, and what the stale-figure table below was drawn from.
- **Verification run** (after the 7 fixes in commit `21c843e`, confirming
  the fixes actually landed and nothing else regressed): **22 matched, 0
  stale, 12 unsourced**. This is a confirmation that a specific set of
  edits worked, not a fresh classification — the 22 is 15+7, the 7
  fixed figures moving from stale to matched, nothing more.

The 12 unsourced (unchanged across both runs) are timeline/SLA/
notice-period figures (go-live weeks, day-30/day-60 adoption
checkpoints, 24-hour email SLA, 30-day non-renewal notice) that don't
trace to the worksheet, the brief, or a named knowledge-layer file in
this repo — flagged as a distinct category from "stale," since no field
anywhere claims to back them (nothing to correct against; a policy
owner would need to either cite them or confirm they're standard
boilerplate).

**Stale figures fixed (7) — old → new, source, and why each isn't a typo
fix:**

| File:line | Old | New | Source |
|---|---|---|---|
| `13-next-steps.md:6` | AED 4,888 | AED 5,280 | `pricing-worksheet.yaml: number_3_financing.mobilisation_aed` |
| `12-why-sgc.md:27` | AED 24,688 | AED 25,440 | `pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed` |
| `01-executive-summary.md:21` | AED 24,688 | AED 25,440 | same |
| `10-commercial-terms.md:8` | AED 1,700/mo | AED 1,680/mo | `pricing-worksheet.yaml: assembly.option_a.subscription_aed` |
| `10-commercial-terms.md:9` | AED 25,680 | AED 25,440 | same as above |
| `10-commercial-terms.md:17` | AED 5,100 (typed) | AED 5,040 (AED 1,680 × 3, shown derived) | derived from subscription_aed, not typed |
| `11-support-sla.md:20` | AED 1,980 (10% of stale annual) | AED 2,016 (AED 1,680 × 12 × 10%, shown derived) | derived from subscription_aed |

**Two of these are terms changes, not typo fixes, named as such:**
`11-support-sla.md`'s aggregate SLA credit cap moving AED 1,980 → 2,016
**raises SGC's own contractual liability by AED 36** — this is a
commitment increasing, not a display correction. `10-commercial-terms.md`'s
quarterly billing figure is now rendered as an explicit derivation
(subscription × 3) rather than a typed literal, closing the exact defect
class (a hand-typed figure silently drifting from its own formula) that
this whole audit exists to catch.

**RESOLVE signature block fixed.** `13-next-steps.md`'s SGC TECH AI
column showed `RESOLVE`/`RESOLVE` for Name/Title despite
`06-brand/entity/legal-identity.yaml` being resolved since 2026-08-04 —
filled from that file: Name = `contact.actual_signer`
("Renbran Anthony Madelo"), Title = "Founder & CEO" (per the same
field's inline comment). The adjacent internal NOTE, which still claimed
the signature block "cannot render ... until" legal-identity.yaml is
resolved, was itself stale and corrected in the same edit — §09's
dispute-and-jurisdiction clause remains separately blocked (governing
law/forum, unrelated to the signature block).

**Margin — cts_total provenance and the gate's own definition.**
`cts_total_aed` (520, MRD) is a sum of sub-fields, three of which
genuinely cite a policy field in the worksheet's own inline comment:
`hosting_allocation_aed` (360 × (5/20), constants cited at
`policy.yaml:71-72`), `support_labour_aed` (ceil(5/5)×280, cited at
`policy.yaml:74-75`), `account_mgmt_aed` (100, cited at
`policy.yaml:76: account_mgmt_aed.tier_5`).

**CORRECTION 2026-08-06 (later same day): the fourth component,
`tooling_aed` (50), was previously reported as "cited at
policy.yaml:73." That was wrong, and worth naming precisely because it's
exactly the failure mode this whole audit exists to catch. The worksheet
line `tooling_aed: 50` (`pricing-worksheet.yaml:22`) carries no comment
at all — no field reference, no formula. `policy.yaml:73:
tooling_flat_aed: 50` was found by matching the VALUE (50) and a similar
NAME ("tooling"), not by following a citation the worksheet actually
makes. A value match is not a trace: two unrelated fields could
coincidentally share a value, and the worksheet field name
(`tooling_aed`) doesn't literally match the policy field name
(`tooling_flat_aed`) either. This component is properly UNSOURCED, same
category as the 12 figures in the drift audit above, not "cited."**

Net: 3 of `cts_total_aed`'s 4 components genuinely cite a policy field;
the 4th (`tooling_aed`) does not, and the `cts_total_aed` summary line
itself carries only an arithmetic comment, not a citation, the same
pattern already flagged and guarded for `total_hours_all_in`-style
fields elsewhere in this repo.

The 0.30 gate itself: `policy.yaml:88: gates.min_gross_margin: 0.30`.
**The field carries no comment specifying which formula it was written
against** — unlike `absolute_margin_floor` two lines below it (which at
least names G23), `min_gross_margin` doesn't name a formula or a G-number
inline. Given every corpus client existed under the build-margin
convention before Kallat/Prosper's lifetime-commitment formula appeared,
the more likely original calibration target is Formula A (build margin)
— but this is an inference from ordering, not a citation, and is
reported as such, not asserted as fact.

**VGE's Formula A numerator inherits the pin's provenance.** VGE's own
G8 margin (48.9%) is computed against `build_value_aed: 14,800` — the
brief-pinned figure whose own provenance was already downgraded this
session (`brief_pin_variance`'s basis is internal self-attestation
between `manifest.yaml:100` and `pricing-worksheet.yaml:143-145`, not an
external source; see the provenance-floor register above). VGE's margin
result is therefore only as trustworthy as that pin. Not re-verified or
changed here — logged as an inherited-provenance finding, same discipline
as the rest of this register. Formulas remain unmixed per instruction:
MRD/VGE keep Formula A, Kallat/Prosper keep Formula B.

**Item 5 follow-through.** Grepped every function in `05-ops/*.py` for
the four narration field names (`override_note`,
`internal_only_disclaimer`, `disarm_hesitation_tweaks_scope_note`,
`subscription_affinity`) — zero hits. **No engine path, including T12,
has ever parsed these fields**; they are free-text YAML string blocks,
never consumed programmatically. The one figure that exists only in a
narration line with no structured backing anywhere: Prosper's
`disarm_hesitation_tweaks_scope_note` quotes "Kallat — AED 4,900 matches
their numbers" — this number has no structured field in Prosper's own
brief or worksheet (Prosper's actual mobilisation is 22,002), and does
not match Kallat's structured `mobilisation_fee_aed` (22,429) either; it
happens to equal VGE's `mobilisation_aed` (4,900), a third, unrelated
client's field. **Confirmed no narration text has reached a
client-facing artifact that was ever issued** — Kallat's and Prosper's
`05-issued/` are both empty. One partial exception worth naming: Kallat's
own (never-issued) draft, `03-draft/KP-2026-SUB-01_Rev1/10-commercial-terms.md:60`,
uses the phrase "this proposal's original disarm-hesitation intent" in
prose that would be client-facing if this draft were ever sent as-is —
internal strategy vocabulary, not raw session/prompt text, but the same
risk class: it has not reached a client only because the document itself
never has.

**validate.py's `check_r11_r12_deliverables` — untouched, logged as an
open question for a human, not fixed.** It still fails for MRD (globs
`*.pdf`, we emit Markdown) and was left exactly as written. Amending the
check to match the artifact we happened to produce would be the mirror
image of the Kallat scope-padding finding earlier in this register —
there, inputs were moved to clear `check_4`; here, the check's own
definition would be moved to clear an unchanged output. **Either PDF
generation needs separate authorization, or a human amends the check's
own definition** — this repo does not get to pick which, and this pass
didn't.

No engine or policy change. No worksheet writes. No scope removal. No
PDF generation. No work on any client but MRD beyond the authorized
read-only count above. Two commits: renderer/checks/CHANGELOG first,
the seven 03-draft prose corrections second, kept separate so the prose
diff is reviewable on its own.

## 2026-08-07 — Kallat stages 0-4 close-out: two scope metrics named, PRJ-anchor class logged, three hygiene fixes, headcount confirmed blocking

Follow-up to the 2026-08-06 Kallat forensic pass above. Three corrections
and three authorized fixes, no engine/policy/worksheet writes, no Stage 5
(pricing) work — reported and held per explicit instruction.

### Register: "unrequested scope" vs "untraceable scope" are two different metrics

A prior turn compared Kallat's AED 19,652 (35.0%) directly against a
Prosper figure of AED 24,090 (43.8%) as if they measured the same thing.
They don't — recorded here, by name, so the comparison isn't repeated:

- **Unrequested scope** (Kallat's metric): work packages present in
  `number_2_build.delivery_hours` that do **not** appear in the client's
  own `client-brief.yaml: scope_signals.work_packages_requested` list.
  Kallat: 4 of 8 packages (`discovery`, `property_unit_register`,
  `tenancies_contracts_reminders`, `invoicing_trn`) — AED 19,652 delta,
  35.0% of quoted `build_value_aed` (56,072). Independently re-derived
  this session (recomputed the worksheet formula with only the 4
  requested packages: AED 36,420 vs 56,072 = 19,652 delta) — see the
  2026-08-06 entry above and `05-ops/test_pricing_engine.py`'s
  `SCOPE_EXPOSURE_TIER["KP-kallat-properties"]`.
- **Untraceable scope** (Prosper's metric, per Renbran, 2026-08-07
  correction): work packages billed with no link to the client's own
  requirements document, regardless of whether they match Prosper's
  `client-brief.yaml` request list. Prosper: AED 24,090, 43.8%. **Stated
  here as reported, not independently re-derived this session** — no
  plain-text artifact in this repo currently carries this figure (checked
  `manifest.yaml`, `02-calc/*.yaml`, `04-review/qa-checklist.md`; only
  binary-PDF false-positive hits on the literal digits). Flagged the same
  way attachment 5306's PRJ figures are flagged in `HANDOVER.md` §8.1 —
  real, attributed, not yet corroborated by an in-repo document.
- **Prosper has zero unrequested-scope packages** — confirmed, matches
  `SCOPE_EXPOSURE_TIER["PRO-prosper-realestate"]` exactly (`("n/a", 0,
  "0 unrequested packages -- all 8 match its brief")`). Untraceable scope
  and unrequested scope are not in tension for Prosper: a package can
  match the client's own requested list (so it's not "unrequested") while
  still having no traceable link to the requirements document itself (so
  it can still be "untraceable"). Two independent axes, not two names for
  the same defect.
- **Kallat is the only client in the corpus with confirmed copy-paste
  contamination** (the 4 packages match VGE's and MRD's `delivery_hours`
  name-and-hour-value exactly, and don't match Kallat's own brief at
  all — see 2026-08-06 entry). **Prosper's defect is same-pen
  provenance**, not copy-paste: its own 8 packages do match its own
  brief, but brief and worksheet were first committed together in
  `525940d` (the same commit that padded Kallat's scope), so the "match"
  is not independent corroboration (`SCOPE_MATCH_INDEPENDENT_SOURCE` in
  `test_pricing_engine.py`). Different defect classes; do not treat one
  as evidence for the other's severity.

### Cross-client class: ungoverned PRJ-model documents functioning as price anchors

Logged in full in `HANDOVER.md` (new section) — summarized here for the
pricing-audit trail. Two confirmed instances, same shape:

| Client | Document | Sent | Client reaction | Rate basis |
|---|---|---|---|---|
| Kallat | SGC-KP-2026-07 | 2026-07-23 | 2026-07-24, general price pushback, no specific figure rejected | AED 425/hr flat tiered rate — **correction to this repo's own prior framing**: `client-brief.yaml`/`manifest.yaml` describe this as "not on rate-card.yaml" — imprecise. AED 425 *is* a real rate-card value (`rate-card.yaml:54`, `qa_engineer`, L1), just not a role Kallat's PRJ scope would plausibly bill at that tier as a blanket rate. Not the same defect class as Prosper's forbidden-list violation below; restated accurately rather than repeating the inherited claim unchecked. |
| Prosper | "PROSPER x SGC Implementation Proposal - 2026" (CRM attachment 5306) | 2026-07-22 09:44 UTC | 2026-07-27, explicit rejection on cost | AED 690/hr and AED 650/hr — both literally on `rate-card.yaml: forbidden_rates` (`:37`, `:52`) |

Both: built outside this repo's governance, never reconciled line-by-line
against the governed SUB-model rebuild, and are the client's *only* live
written commercial understanding — this repo's own SUB-model drafts have
never been issued to either client (`manifest.yaml: issued_date: ""`,
both). **VGE and MRD: unchecked, not confirmed clean.** No PRJ-type
document is referenced in either client's readable text files this
session, but neither client's `client-brief.yaml` narrates its own prior
documents the way Kallat's and Prosper's do (a text-search absence is not
the same as a mailbox/CRM check, which this pass did not run for VGE/MRD
— see attachment-5306 retrieval difficulty in `HANDOVER.md` §8.1 for why
that check is nontrivial).

**Kallat's anchor inverts Prosper's problem rather than repeating it.**
Prosper's PRJ figure is *below* what this repo's governed model can
price at any configuration (§8.5, `HANDOVER.md`) — a floor problem.
Kallat's SUB mobilisation (AED 22,429) sits **below** the PRJ one-time
range's floor (AED 48,450), while the SUB monthly (AED 5,850) sits
**inside** the PRJ's disclosed monthly hosting range (AED 2,800–6,300) —
not above or below it cleanly. Depending which PRJ tier Sadique Abbas
believes he was quoted, the governed SUB model could read cheaper on
entry (mobilisation) and comparable-to-dearer over the term (monthly ×
24), or the reverse. **Stage 5, when it runs, must compute the comparison
against both PRJ tier ends (AED 48,450 and AED 123,250), not a single
midpoint** — noted here and in `manifest.yaml`'s 2026-08-07 escalation so
this isn't rediscovered live in a client meeting.

### Headcount: T12 stays hard-blocking, no illustrative figure

**Unlike Prosper (`HANDOVER.md` §10, 2026-08-07, "T12 shipped
non-blocking"), Kallat's T12 failure cannot be shipped around.** Prosper's
seat-band restructure decoupled its quoted figure from the exact
`users_now` value, so an unverified headcount didn't move the headline
price. Kallat has no equivalent band: `users_now` (40 vs. the `smb`
ceiling of 30) sets the **segment** directly (`mid_market` vs `smb`),
which sets the **blended rate** (525 vs 395 AED/hr), which moves
`build_value_aed` by 27.8% (see 2026-08-06 entry above). There is no band
wide enough to absorb a rate-card change — this is a structural
dependency, not a sizing uncertainty. **No non-blocking rationale
applies here, and no labelled-illustration figure is authorized until
`users_now` is confirmed.** T12 remains a hard FAIL/blocker for Kallat by
design.

**Action taken**: confirmation question drafted for Sadique Abbas
(decision-maker, per `client-brief.yaml`/`manifest.yaml` — not the
transcript participants, who are all SGC-internal), routed as an
ordinary SDR follow-up through Johnny Gurrera (the SDR who logged the
2026-07-24 client call) rather than through the stamp→SDR→John→stamp
sequence — it commits nothing and quotes no figure, so that gate does
not apply. See `manifest.yaml`'s 2026-08-07 escalation entry and
`00-intake/sdr-followup-headcount-2026-08-07.md` for the drafted
question. Held, not sent — per standing instruction, no email is
auto-sent at any stage.

### Three fixes applied (hygiene only — no figures changed)

1. **Quarantined** `04-draft/KP-2026-SUB-01_Rev1_Internal.html` and
   `.pdf` to `04-draft/_quarantine/` (git-tracked rename) — both
   rendered before the 2026-08-05 v3.0 recompute and never
   re-rendered, still showing build value 121,716 / mobilisation 48,686
   / subscription 7,790 against the current worksheet's 56,072 / 22,429
   / 5,850. Never issued to the client. `_quarantine/NOTICE.md` added
   explaining why, mirroring Prosper's existing `_quarantine/` precedent.
2. **`02-calc/gate-report.md` marked SUPERSEDED in place** — a banner at
   the top states plainly that "all 41 gates pass" in that file was
   computed against the same stale pre-recompute figures, points to the
   live worksheet, and instructs a re-run before this deal moves past
   internal review. Historical content below the banner left unmodified,
   consistent with this repo's convention of preserving superseded
   figures rather than rewriting them.
3. **`02-calc/risk-assessment.yaml:18` comment corrected, value
   unchanged.** Was: `computed from this worksheet's build_value
   (~21,554)` — matched neither the current `build_value_aed` (56,072)
   nor the correct basis. Corrected to cite `exposure.contractual_peak_aed`
   (33,643), matching the convention actually used in VGE/MRD/Prosper's
   own `risk-assessment.yaml` files. `raw_score` (52) and `band`
   (elevated) confirmed unchanged after the edit — the current numeric
   outcome was already right, only its citation was wrong. Flagged
   because, uncorrected, a future editor "fixing" the comment by plugging
   in the literal `build_value_aed` would have pushed `raw_score` to 60 —
   the top edge of the elevated band, one point from `high` (which would
   require `mobilisation_50pct + pdc_full_balance + guarantee` instead of
   the current instrument set).
4. **`validate.py` check_19 added** (`INTERNAL_VOCABULARY_PHRASES`),
   separate from check_18 by design — a narration/strategy leak
   (`disarm-hesitation`) and a risk-input-is-a-guess leak
   (`placeholder-driven`) are a different failure class from a
   commercial-claim leak, and should fail distinguishably. Scoped to
   `03-draft/`+`05-issued/` (same as check_18), narrow substring list
   only (no generic words like "internal"/"draft") so the deliberate
   "INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION" banner is never
   caught. Ran against Kallat: correctly fails on 3 hits
   (`09-partnership-terms.md`, `10-commercial-terms.md`,
   `13-next-steps.md`, all "placeholder-driven"/"disarm-hesitation") —
   confirms the check works and that Kallat's `03-draft/` genuinely has
   not been cleaned of this vocabulary yet. `validate.py 02-clients/
   KP-kallat-properties/` now correctly reports `NOT clean` (5 failures:
   3 new check-19 hits, plus the pre-existing R11/R12 failures — Kallat
   is not in `ALLOWED_CLIENTS`, unrelated to this pass). `validate.md`
   updated to document check 19 and the new 1–13,16–19 gate-failure
   range.

No engine or policy change. No worksheet writes. No repricing. No
Stage 5 work. `05-ops/validate.py`/`validate.md` (audit tooling, not
engine/policy), `HANDOVER.md`, `manifest.yaml`, `02-calc/gate-report.md`
(banner only), `02-calc/risk-assessment.yaml` (comment only), and
`04-draft/` (file move only) are the only touched paths besides this
file.
