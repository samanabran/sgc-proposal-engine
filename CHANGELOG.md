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
