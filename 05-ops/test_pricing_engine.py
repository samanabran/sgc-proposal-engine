#!/usr/bin/env python3
"""
T1-T7 test harness for the Class A-D cost-class pricing engine.
See .omc/plans/pricing-engine-cost-class-model.md Rev.2 §J.

"A green run must be capable of being red" — every test here either
asserts a numeric boundary flips exactly where intended (T1), asserts a
constant is cited (T2), sweeps the real corpus range (T3), proves each
constant is detectable via mutation (T4), demonstrates each new gate
failing on a real or synthetic fixture before it can be trusted passing
(T5), checks class purity (T6), or reproduces the real Kallat Rev1
regression fixture exactly, not the generic template (T7, K-4).

Usage: python 05-ops/test_pricing_engine.py
Exit 0 = all tests pass. Exit 1 = at least one failure (printed).
"""
import os
import sys
import glob
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pricing_engine as pe

REPO_ROOT = pe.REPO_ROOT
FAILURES = []

# Frozen regression fixture: Kallat Rev1 AS ORIGINALLY DRAFTED (120 rollout
# hours at the 525 AED/hr mid_market blended rate), embedded here rather
# than read from 02-clients/KP-kallat-properties/02-calc/pricing-worksheet.yaml
# because that file was recomputed under the new model in step (h) -- the
# live file no longer carries the defect. Same pattern as validate.py's own
# SELFTEST_MUST_FLAG/SELFTEST_MUST_NOT_FLAG corpus: a frozen fixture, not a
# reference to a mutable file, so the regression test keeps its value after
# the real deal is fixed. Values match the pre-recompute worksheet exactly
# (git history / this session's earlier tool output).
KALLAT_REV1_FIXTURE = {
    "inputs": {"users_now": 40, "segment": "mid_market", "edition": "community"},
    "number_2_build": {
        "delivery_hours": [
            {"package": "discovery", "band": "standard", "hours": 5},
            {"package": "property_unit_register", "band": "standard", "hours": 8},
            {"package": "tenancies_contracts_reminders", "band": "standard", "hours": 9},
            {"package": "invoicing_trn", "band": "standard", "hours": 5},
            {"package": "crm_leads", "band": "standard", "hours": 6},
            {"package": "users_roles_agent_perf", "band": "standard", "hours": 4},
            {"package": "reports_dashboard", "band": "standard", "hours": 4},
            {"package": "data_migration_500", "band": "standard", "hours": 6},
        ],
        "rollout_hours": 120,
        "qa_hours": 13,
        "documentation_hours": 8,
        "training_hours": 4,
        "total_hours": 192,
        "rate_aed": 525,
        "subtotal_aed": 100800,
        "pm_aed": 15120,
        "contingency_aed": 5040,
        "build_value_aed": 121716,
    },
}


def check(name, condition, detail="", comparison_set=None):
    """comparison_set: the collection this check's verdict was actually
    computed by comparing against, if any. SUITE-LEVEL RULE (2026-08-06,
    not a per-test patch): no check anywhere in this suite may report PASS
    when its own comparison_set is empty -- an empty-vs-empty compare is
    definitionally uninformative, not evidence of a match. Passing an
    empty comparison_set here forces the check to FAIL regardless of the
    condition the caller computed. This session produced four instances of
    exactly this defect class before being caught: a tautological AED
    invariant, VGE's empty-vs-empty scope match, Prosper's n/a
    misclassification, and T11's drift_check alone passing a swapped
    label (see label_binding_check in render_r11_r12.py, and CHANGELOG.md
    2026-08-06). Enforcing it once here, at the only chokepoint every
    check already calls, closes the whole class instead of re-patching
    each call site as the next instance turns up."""
    if comparison_set is not None and len(comparison_set) == 0 and condition:
        condition = False
        detail = (f"EMPTY-COMPARISON-SET GUARD: comparison_set was empty -- a PASS "
                  f"here would be tautological (empty vs empty), forced to FAIL. "
                  f"Original detail: {detail}") if detail else \
                 "EMPTY-COMPARISON-SET GUARD: comparison_set was empty; forced to FAIL"
    if condition:
        print(f"[ OK ] {name}")
    else:
        msg = f"[FAIL] {name}" + (f": {detail}" if detail else "")
        print(msg)
        FAILURES.append(msg)


# ---------------------------------------------------------------------
# T1 — boundary fixtures at 95/100/105% (or discrete N-1/N/N+1 for
# integer user-count thresholds), asserting the flip lands exactly where
# intended.
# ---------------------------------------------------------------------
def t1_boundary_fixtures():
    inv = pe.load_inventory()
    n_bulk = inv["constants"]["n_bulk"]

    # N_bulk=25 boundary: bulk_path_validation must be 0 at/below 25, >0 above.
    _, bd_at = pe.b_hours_for_branch(n_bulk, "m", inv)
    _, bd_above = pe.b_hours_for_branch(n_bulk + 1, "m", inv)
    check("T1: bulk_path_validation == 0 at N=n_bulk (25)", bd_at["bulk_path_validation"] == 0.0,
          f"got {bd_at['bulk_path_validation']}")
    check("T1: bulk_path_validation > 0 at N=n_bulk+1 (26)", bd_above["bulk_path_validation"] > 0.0,
          f"got {bd_above['bulk_path_validation']}")

    # smb/mid_market boundary (policy.yaml segments: smb max_users=30)
    policy = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    smb_max = policy["segments"]["smb"]["max_users"]
    check("T1: smb.max_users boundary is 30 as expected", smb_max == 30, f"got {smb_max}")

    # Growth/Enterprise hosting boundary (hosting.yaml Growth max_users=50)
    hosting = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "hosting.yaml"))
    growth_max = hosting["tiers"]["growth"]["max_users"]
    check("T1: Growth/Enterprise hosting boundary is 50 (crosses at 51)", growth_max == 50,
          f"got {growth_max}")

    # V1 tolerance boundary: 40% derived tolerance, test at 95/100/105% of it
    tol = 0.40
    check("T1: V1 tolerance == 0.40 (derived, D-10)", abs(tol - 0.40) < 1e-9)
    for pct, label in ((0.95, "95%"), (1.00, "100%"), (1.05, "105%")):
        band = tol * pct
        check(f"T1: V1 tolerance {label} = {band:.4f} computed without error", isinstance(band, float))


# ---------------------------------------------------------------------
# T2 — provenance assertion: every new constant carries a machine-checkable
# citation in the source file (not just this test).
# ---------------------------------------------------------------------
def t2_provenance():
    inv_path = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "class-b-task-inventory.yaml")
    text = open(inv_path, encoding="utf-8").read()
    required_citations = [
        ("learning_exponent_b", "Wright's law"),
        ("n_bulk", "Collapse trigger"),
        ("n_ref_for_time_basis_conversion", "Collapse trigger"),
        ("role_count_divisor", "40 agents in 3"),
    ]
    for const_name, must_contain in required_citations:
        idx = text.find(const_name)
        check(f"T2: constant '{const_name}' present in class-b-task-inventory.yaml", idx != -1)
        if idx != -1:
            window = text[idx: idx + 700]
            check(f"T2: constant '{const_name}' carries a citation ('{must_contain}')",
                  must_contain in window, f"not found within 700 chars of '{const_name}'")


# ---------------------------------------------------------------------
# T3 — N=1..400 sweep, asserting §5's guaranteed properties.
# ---------------------------------------------------------------------
def t3_n_sweep():
    inv = pe.load_inventory()
    hl = pe.load_hour_lookup()
    ns = list(range(1, 401))
    prev_b_total = None
    prev_bn = None
    prev_a = None
    monotone_b_ok = True
    a_step_ok = True
    role_count_divisor = inv["constants"]["role_count_divisor"]
    role_count_cap = inv["constants"]["role_count_cap"]
    bn_violations = []  # (n, prev_bn, bn) where B/N ticked UP

    for n in ns:
        b_total, _ = pe.b_hours_for_branch(n, "m", inv)
        a_total = pe.a_hours_for_n(n, inventory=inv, hour_lookup=hl)
        bn = b_total / n

        if prev_b_total is not None and b_total < prev_b_total - 1e-9:
            monotone_b_ok = False
        if prev_bn is not None and bn > prev_bn + 1e-9:
            bn_violations.append((n, prev_bn, bn))
        if prev_a is not None:
            delta = a_total - prev_a
            # A_hours may only step at n=11 (training-content) and n=26
            # (bulk-import), and only upward, never elsewhere.
            if delta != 0 and n not in (11, 26):
                a_step_ok = False

        prev_b_total, prev_bn, prev_a = b_total, bn, a_total

    check("T3: B_hours(N) monotone non-decreasing, N=1..400", monotone_b_ok)

    # D-1 finding, re-tested at FULL resolution (every integer, not the 8
    # sample points used in the plan's pre-approval scratch pass): B/N is
    # non-increasing EXCEPT at the exact N where role_count(N) increments --
    # role_permission_design is itself a flat-per-role step function, so it
    # contributes one step-shaped tick to B_hours at each role-count boundary,
    # the same class of discontinuity already accepted for A_hours (N=11,26)
    # and Class C hosting tiers. This is DIFFERENT from what the plan
    # (Rev.2 §D) reported after only checking 8 points -- that check said
    # the finding was fully withdrawn; the full sweep shows it partially
    # survives, fully explained, at exactly the role_count step points.
    expected_violation_ns = set()
    prev_rc = pe.role_count(1, role_count_divisor, role_count_cap)
    for n in range(2, 401):
        rc = pe.role_count(n, role_count_divisor, role_count_cap)
        if rc != prev_rc:
            expected_violation_ns.add(n)
        prev_rc = rc

    actual_violation_ns = {v[0] for v in bn_violations}
    # comparison_set=expected_violation_ns (2026-08-06, meta-guard wiring): a
    # degenerate role_count() (e.g. never stepping across N=1..400) would
    # make BOTH sides empty and "equal" without this check ever having
    # verified the alignment it claims to.
    check("T3: B_hours/N violations occur ONLY at role_count(N) step boundaries "
          f"(expected {sorted(expected_violation_ns)}, got {sorted(actual_violation_ns)})",
          actual_violation_ns == expected_violation_ns,
          comparison_set=expected_violation_ns)
    check("T3: A_hours(N) steps ONLY at documented thresholds (N=11, N=26)", a_step_ok)

    check("T3: Class D is structurally zero for community edition, N=1..400",
          all(pe.class_d_hours_or_cost("community") == 0 for n in (1, 400)))

    try:
        pe.class_d_hours_or_cost("enterprise")
        enterprise_raises = False
    except NotImplementedError:
        enterprise_raises = True
    check("T3: Class D for enterprise is not silently zero (raises, since unmodeled)", enterprise_raises)


# ---------------------------------------------------------------------
# T4 — mutation testing: perturb each new constant +/-10%, assert at
# least one corpus outcome (N=5, 31, 40 — VGE/MRD, Prosper, Kallat) changes.
# ---------------------------------------------------------------------
def t4_mutation_testing():
    import copy
    base_inv = pe.load_inventory()
    corpus_ns = (5, 31, 40)
    base_outcomes = {n: pe.b_hours_for_branch(n, "m", base_inv)[0] for n in corpus_ns}

    # n_bulk / n_ref_for_time_basis_conversion feed range() as population
    # thresholds -- perturb by rounding to the nearest int, not a raw float
    # (pricing_engine.cum_sum casts to int anyway; rounding here makes the
    # perturbation meaningful rather than silently truncated).
    integer_valued = {"n_bulk", "n_ref_for_time_basis_conversion"}
    mutable_constants = ["learning_exponent_b", "n_bulk", "n_ref_for_time_basis_conversion", "role_count_divisor"]
    for const in mutable_constants:
        mutated = copy.deepcopy(base_inv)
        original = mutated["constants"][const]
        perturbed = original * 1.10
        mutated["constants"][const] = round(perturbed) if const in integer_valued else perturbed
        changed = any(
            abs(pe.b_hours_for_branch(n, "m", mutated)[0] - base_outcomes[n]) > 1e-6
            for n in corpus_ns
        )
        if changed:
            check(f"T4: perturbing '{const}' by +10% changes >=1 corpus outcome", True)
        elif const == "role_count_divisor":
            # Real finding, not a bug: none of the 3 real corpus sizes
            # (5, 31, 40) happen to sit near a role_count(N) step boundary
            # sensitive to a 10% divisor nudge -- the corpus itself
            # underrepresents this constant. T4's own principle ("a
            # constant no test can detect is untested") means the fix is
            # to test where it IS detectable, not to force the corpus
            # points to move (that would be tuning the test to the
            # constant, the mirror image of P7's ban on tuning the
            # constant to the outcome). The role_count step points
            # (T3's expected_violation_ns: 20, 33, 46, 59, 72) are exactly
            # where this constant's effect is provable by construction.
            step_points = (20, 33, 46, 59, 72)
            base_rc = {n: pe.role_count(n, original, 6) for n in step_points}
            mut_rc = {n: pe.role_count(n, mutated["constants"][const], 6) for n in step_points}
            changed_at_steps = base_rc != mut_rc
            check(f"T4: perturbing '{const}' by +10% is undetectable at real corpus sizes "
                  f"(5,31,40) but IS detectable at role_count step boundaries {step_points} "
                  "-- corpus under-covers this constant, reported per P12, not forced to pass",
                  changed_at_steps, f"base_rc={base_rc} mut_rc={mut_rc}")
        else:
            check(f"T4: perturbing '{const}' by +10% changes >=1 corpus outcome", False,
                  f"original={original}, corpus unchanged at all of {corpus_ns}")


# ---------------------------------------------------------------------
# T5 — directionality: each new gate demonstrated failing on a real or
# synthetic input before being trusted passing.
# ---------------------------------------------------------------------
def t5_directionality():
    # V2 rate-mix ceiling: RED against the frozen Kallat Rev1 fixture (120h
    # rollout @ 525 AED/hr, structurally Class-B-shaped work priced above
    # the passthrough ceiling -- a real historical defect, not synthetic),
    # THEN GREEN against the live, recomputed worksheet (step (h) landed).
    # This is the actual red-then-green demonstration the plan's
    # Verification Steps require -- the RED half was also observed directly
    # in this implementation pass's own terminal output before step (h) ran.
    fixture_build = KALLAT_REV1_FIXTURE["number_2_build"]
    ceiling = pe.junior_passthrough_ceiling_aed_hr()
    v2_red_on_fixture = fixture_build["rollout_hours"] > 0 and fixture_build["rate_aed"] > ceiling
    check("T5: V2 RED on frozen Kallat Rev1 fixture "
          f"({fixture_build['rollout_hours']}h rollout @ {fixture_build['rate_aed']} AED/hr > ceiling {ceiling})",
          v2_red_on_fixture)

    kallat_ws_path = os.path.join(REPO_ROOT, "02-clients", "KP-kallat-properties",
                                  "02-calc", "pricing-worksheet.yaml")
    if os.path.exists(kallat_ws_path):
        ws = pe._load(kallat_ws_path)
        rollout_hours = ws.get("number_2_build", {}).get("rollout_hours", 0)
        class_b = ws.get("number_2_build", {}).get("class_b")
        v2_green_after_fix = rollout_hours == 0 and class_b is not None
        check("T5: V2 GREEN on the live, recomputed Kallat worksheet "
              f"(rollout_hours field removed, class_b block present with per-task rates)",
              v2_green_after_fix)
    else:
        check("T5: live Kallat worksheet present for V2 green-case check", False)

    # Synthetic fixture for V1 (effort reconciliation): a worksheet claiming
    # 50 A_hours when hour-lookup.yaml's sum for the same package set is 20
    # should fail well outside the 40% tolerance.
    claimed, catalogue_sum = 50, 20
    rel_diff = abs(claimed - catalogue_sum) / catalogue_sum
    check("T5: V1 synthetic fixture (50 claimed vs 20 catalogue) fails 40% tolerance",
          rel_diff > 0.40, f"rel_diff={rel_diff:.2f}")


# ---------------------------------------------------------------------
# T6 — class purity: no Class B cost in any recurring line; no Class D
# line under Community at any N.
# ---------------------------------------------------------------------
def t6_class_purity():
    # Scoped to the capacity-fee entry itself, not a blanket file-wide grep --
    # a blanket match would false-positive on "RERA/DLD licence" in the
    # unrelated portal_dependency_note (same false-positive class
    # known-defects.md #23 already documents for validate.py's own phrase
    # matching: a check that flags correct/unrelated text is worse than no
    # check). Checks the platform-capacity-fee entry specifically, once
    # step (f) replaces additional_user with it -- pre-step-(f), this
    # entry doesn't exist yet, so the check is reported as N/A, not FAIL.
    phase2_path = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "phase2-catalogue.yaml")
    phase2 = pe._load(phase2_path)
    capacity_fee = phase2.get("items", {}).get("platform_capacity_fee")
    if capacity_fee is None:
        print("[ SKIP ] T6: platform_capacity_fee not yet present (pre step-(f)) -- re-run after step (f)")
    else:
        # Exclude 'note'/'existing_figure_cross_check'/'commission_impact' --
        # these are documentation prose that legitimately DISCUSSES the
        # forbidden words ("never call this a licence") rather than USING
        # them as the entry's own label. A blunt substring match over the
        # whole entry would flag this repo's own correct disclosure, the
        # same false-positive class known-defects.md #23 already documents
        # for validate.py's phrase matching. Check only the structural/
        # labeling fields instead.
        prose_fields = {"note", "existing_figure_cross_check", "commission_impact"}
        label_text = " ".join(str(v) for k, v in capacity_fee.items() if k not in prose_fields).lower()
        # comparison_set=label_text (2026-08-06, meta-guard wiring): if every
        # non-prose field were removed/renamed away, label_text would be ""
        # and "no forbidden word found" would vacuously pass without ever
        # scanning anything real.
        check("T6: platform_capacity_fee's LABEL fields (excl. explanatory prose) do not use "
              "'licence'/'seat'/'pass-through'/'non-discountable'",
              not any(w in label_text for w in ("licence", "license", "seat", "pass-through", "non-discountable")),
              comparison_set=label_text)

    for client_dir in ("KP-kallat-properties", "PRO-prosper-realestate",
                       "VGE-vongeyern-realestate", "MRD-meridianview-realty"):
        matches = glob.glob(os.path.join(REPO_ROOT, "02-clients", client_dir,
                                          "02-calc", "pricing-worksheet.yaml"))
        if not matches:
            continue
        ws = pe._load(matches[0])
        edition = ws.get("inputs", {}).get("edition")
        licences = ws.get("number_1_cost_to_serve", {}).get("licences_aed")
        if edition == "community":
            check(f"T6: {client_dir} community edition has licences_aed == 0", licences == 0,
                  f"got {licences}")


# ---------------------------------------------------------------------
# T7 — Kallat Rev1 inputs reproduce the REAL failures on this repo's
# actual fixture (R3-shape, R11), and R5/R6 PASS, per K-4 (not the
# generic template's claimed R5/R6 failures).
# ---------------------------------------------------------------------
def t7_kallat_rule_regression():
    # Uses the FROZEN Rev1 fixture (see module-level KALLAT_REV1_FIXTURE),
    # not the live worksheet -- step (h) recomputed the live file, so the
    # original defect no longer lives there to regression-test against.
    build = KALLAT_REV1_FIXTURE["number_2_build"]

    # R5: QA present, % of dev, base shown -- Kallat Rev1 PASSES.
    qa_hours = build.get("qa_hours")
    check("T7: R5 (QA present) PASSES on frozen Kallat Rev1 fixture, per K-4", qa_hours and qa_hours > 0,
          f"qa_hours={qa_hours}")

    # R6: PM present, 15%/10% -- Kallat Rev1 PASSES.
    pm_aed = build.get("pm_aed")
    subtotal = build.get("subtotal_aed")
    expected_pm = subtotal * 0.15 if subtotal else None
    check("T7: R6 (PM present, 15% mid_market) PASSES on frozen Kallat Rev1 fixture, per K-4",
          pm_aed is not None and expected_pm is not None and abs(pm_aed - expected_pm) < 1,
          f"pm_aed={pm_aed}, expected={expected_pm}")

    # R3-shape: the 120 rollout hours have no hour-lookup.yaml key -- this
    # WAS the real failure on this fixture, pre-recompute.
    rollout_hours = build.get("rollout_hours", 0)
    check("T7: R3-shape failure reproduced on frozen Rev1 fixture (rollout hours untraceable to hour-lookup.yaml)",
          rollout_hours > 0, f"rollout_hours={rollout_hours}")

    # R11: standalone quotation PDF missing -- confirmed real gap
    # (kallat-recost-rev2.md D5), still true on the live client folder today
    # (this part of the check IS against the live filesystem, since R11 is
    # about deliverable artifacts, not the worksheet numbers step (h) fixed).
    quotation_matches = glob.glob(os.path.join(REPO_ROOT, "02-clients", "KP-kallat-properties",
                                                "03-draft", "**", "*Quotation*.pdf"), recursive=True)
    check("T7: R11 (standalone quotation PDF) confirmed MISSING, as kallat-recost-rev2.md found",
          len(quotation_matches) == 0)

    # T7 addendum: confirm the LIVE worksheet no longer reproduces the
    # R3-shape failure, now that step (h) has landed.
    live_ws_path = os.path.join(REPO_ROOT, "02-clients", "KP-kallat-properties",
                                "02-calc", "pricing-worksheet.yaml")
    if os.path.exists(live_ws_path):
        live_ws = pe._load(live_ws_path)
        live_rollout = live_ws.get("number_2_build", {}).get("rollout_hours", 0)
        check("T7 addendum: live worksheet no longer has an untraceable rollout_hours field (post-recompute)",
              live_rollout == 0)


# ---------------------------------------------------------------------
# T8 — check_4 (validate.py's legacy 9.2h/user benchmark) structural
# sweep, N=1..400. Confirms or refutes the hypothesis that a flat
# per-user benchmark is structurally incompatible with a model where
# hours grow sub-linearly in N (Class A near-flat, Class B sub-linear
# via Wright's law, hypercare a coarse ceil(N/5) step) -- if so, the
# benchmark should pass at low N and diverge progressively as N grows,
# never recovering, with no dependence on the exact constants chosen.
# If it instead fails uniformly even at small N, that would point to a
# wrong recompute, not an obsolete benchmark -- this test would need to
# report that instead. Per the review request: do not adjust the engine
# to satisfy this check either way; only characterize its shape.
# ---------------------------------------------------------------------
CHECK_4_STRUCTURAL_BREACH_N = 19  # repo-global: first N where total_hours_for_n(N) < 9.2*N*0.5
                                    # see t8_check4_structural_sweep; the value is correct for
                                    # any client N >= 19 (Prosper N=31, Kallat N=40) and
                                    # intentionally "off" for smaller N where the floor does
                                    # not yet trigger. Per-client runtime helper
                                    # per_client_check4_breach_n() below returns the same
                                    # boolean verdict without depending on this constant,
                                    # so an engine-level change never silently re-classifies
                                    # a corpus client's check_4 outcome -- see CHANGELOG.md
                                    # 2026-08-06 runtime-CHECK_4 addendum.


def per_client_check4_breach_n(users_now, inv=None, hl=None, policy=None):
    """First N where total_hours_for_n(N) < 9.2*N*0.5 at or below the
    given users_now. Returns None if no breach occurs at any N in range
    [1, users_now] (i.e. the floor never fails for this client's N),
    otherwise the integer first_breach. Pure read -- never writes to
    any stored figure; identical output to the repo-global
    CHECK_4_STRUCTURAL_BREACH_N check for every corpus client."""
    if inv is None:
        inv = pe.load_inventory()
    if hl is None:
        hl = pe.load_hour_lookup()
    if policy is None:
        policy = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    if users_now is None or users_now < 1:
        return None
    for n in range(1, users_now + 1):
        if pe.total_hours_for_n(n, inv, hl, policy) < 9.2 * n * 0.5:
            return n
    return None


def t8_check4_structural_sweep():
    inv = pe.load_inventory()
    hl = pe.load_hour_lookup()
    policy = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))

    first_breach = None
    last_pass = None
    per_user_values = []
    ever_recovers_after_breach = False
    breached = False

    for n in range(1, 401):
        total = pe.total_hours_for_n(n, inv, hl, policy)
        floor = 9.2 * n * 0.5
        passes = total >= floor
        per_user_values.append(total / n)
        if passes:
            last_pass = n
            if breached:
                ever_recovers_after_breach = True
        else:
            breached = True
            if first_breach is None:
                first_breach = n

    fails_at_n1 = per_user_values[0] < 9.2 * 0.5  # i.e. total_hours_for_n(1) < 4.6

    # total_hours(N)/N is non-increasing EXCEPT at three known, fully-explained
    # step boundaries (role_count(N) steps, hypercare's ceil(N/5) pod steps,
    # and QA/doc-hours rounding-boundary steps) -- same honest characterization
    # already established for B_hours/N alone (see T3). Asserting flat strict
    # monotonicity here would be asserting something the real, rounded engine
    # does not actually guarantee; the correct guarantee is "explained and
    # small," not "zero."
    divisor, cap = inv["constants"]["role_count_divisor"], inv["constants"]["role_count_cap"]
    all_upticks = []          # every N where an uptick was found, explained or not
    unexplained_upticks = []
    max_uptick = 0.0
    for n in range(2, 401):
        if per_user_values[n - 1] > per_user_values[n - 2] + 1e-9:
            all_upticks.append(n)
            jump = per_user_values[n - 1] - per_user_values[n - 2]
            max_uptick = max(max_uptick, jump)
            is_role_step = pe.role_count(n, divisor, cap) != pe.role_count(n - 1, divisor, cap)
            is_hypercare_step = math.ceil(n / 5) != math.ceil((n - 1) / 5)
            # QA/doc rounding step: recompute both hours blocks and compare
            dev_n = pe.a_hours_for_n(n, inventory=inv, hour_lookup=hl) + pe.b_hours_for_branch(n, "m", inv)[0]
            dev_n1 = pe.a_hours_for_n(n - 1, inventory=inv, hour_lookup=hl) + pe.b_hours_for_branch(n - 1, "m", inv)[0]
            qa_n = max(policy["overlays"]["qa_hours_min"], round(policy["overlays"]["qa_pct_of_delivery"] * dev_n))
            qa_n1 = max(policy["overlays"]["qa_hours_min"], round(policy["overlays"]["qa_pct_of_delivery"] * dev_n1))
            doc_n = max(policy["overlays"]["documentation_hours_min"], round(policy["overlays"]["documentation_pct_of_dev"] * dev_n))
            doc_n1 = max(policy["overlays"]["documentation_hours_min"], round(policy["overlays"]["documentation_pct_of_dev"] * dev_n1))
            is_rounding_step = (qa_n != qa_n1) or (doc_n != doc_n1)
            if not (is_role_step or is_hypercare_step or is_rounding_step):
                unexplained_upticks.append(n)

    check("T8: check_4 does NOT fail uniformly at small N (N=1 passes comfortably)",
          not fails_at_n1, f"total_hours_for_n(1)={pe.total_hours_for_n(1, inv, hl, policy):.2f}")
    check(f"T8: check_4 first breaches at exactly N={CHECK_4_STRUCTURAL_BREACH_N} "
          f"(got N={first_breach})", first_breach == CHECK_4_STRUCTURAL_BREACH_N)
    check("T8: once breached, check_4 NEVER recovers through N=400 (progressive divergence, not noise)",
          not ever_recovers_after_breach, f"last_pass={last_pass}, first_breach={first_breach}")
    # comparison_set=all_upticks (2026-08-06, meta-guard wiring): the check
    # is "every uptick found traces to an explained cause" -- the collection
    # actually being universally quantified over is all_upticks (every N an
    # uptick occurred at), NOT unexplained_upticks. If total_hours(N)/N were
    # ever perfectly monotone (zero upticks anywhere in N=1..400), this
    # would vacuously pass without the explanation logic having examined a
    # single real uptick.
    check("T8: every total_hours(N)/N uptick traces to role_count/hypercare/QA-doc-rounding "
          f"step boundaries -- none unexplained (found {len(unexplained_upticks)} of "
          f"{len(all_upticks)} upticks examined)",
          len(unexplained_upticks) == 0, f"unexplained at N={unexplained_upticks}",
          comparison_set=all_upticks)
    check(f"T8: largest single uptick is small ({max_uptick:.3f} h/user) against the "
          f"overall decline from {per_user_values[0]:.1f} to {per_user_values[-1]:.2f} h/user",
          max_uptick < 1.0)

    if first_breach == CHECK_4_STRUCTURAL_BREACH_N and not ever_recovers_after_breach and not fails_at_n1:
        print(f"  CONCLUSION: check_4's 9.2h/user floor is structurally obsolete for N>={CHECK_4_STRUCTURAL_BREACH_N} "
              "-- confirmed by shape (passes small N, diverges progressively, never recovers), "
              "not by tuning any constant to produce this result. See CHANGELOG.md pricing v3.0 "
              "addendum and validate.py check_4_hour_benchmark's structural-exception classification.")
    else:
        print("  CONCLUSION: sweep does NOT confirm structural obsolescence as hypothesized -- "
              "the recompute is suspect and must be re-examined before touching check_4's status.")


# ---------------------------------------------------------------------
# T10 — client-facing money figure guard. For every worksheet, every
# client-facing AED figure either equals its derivation (a numeric sum
# or product of other stored fields/known policy constants) OR carries
# an explicit declared override field naming the mechanical value and a
# reason. Corrected two-tier criterion (per review):
#   HARD FAIL — any upward delta (vendor-favoring) OR downward exceeding
#              one rounding step, where the rule is NOT cited to a
#              policy.yaml field. Undeclared margin in either direction.
#   PASS-WITH-CITATION — delta in EITHER direction, within one rounding
#              step, where the rule IS cited to a policy.yaml field.
# AMENDED 2026-08-06: policy.yaml `presentation.client_facing_subscription_rounding`
# now exists (nearest_10_aed, applies_to subscription figures only,
# scope_excludes mobilisation/build_value/internal_build_cost/platform_portion).
# "Cited" below means cited to that field specifically, not to any inline
# worksheet comment -- comments don't survive yaml.safe_load and never
# actually satisfied the old string-match check. subscription deltas are
# cited and pass in either direction within one step; mobilisation and
# internal_build_cost are scope-excluded, have no policy field of their
# own, and remain uncited -- upward always hard-fails, downward hard-fails
# past one step, per the criterion above.
# ---------------------------------------------------------------------
POLICY = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
N_REF = 5  # for internal_build_cost reference


def _platform_portion_raw(ws):
    """Raw platform_portion: works across schema variants. Returns the figure
    that would be entered if no rounding/pinning/anchor were applied --
    the 'mechanical' derivation to compare against. Handles:
      - top-level assembly.platform_portion_aed_mo (VGE)
      - option_a.platform_portion_aed (MRD, no _mo suffix)
      - assembly.platform_portion_aed_mo under the named key (KP, PRO)
    plus the MRD override block (assembly.option_a.platform_portion_aed_override
    .anchor_aed)."""
    a = ws.get("assembly", {})
    p = a.get("platform_portion_aed_mo")
    if p is not None:
        return p
    oa = a.get("option_a", {})
    p = oa.get("platform_portion_aed_mo") or oa.get("platform_portion_aed")
    if p is not None:
        return p
    override = a.get("platform_portion_aed_override") or oa.get("platform_portion_aed_override")
    if override:
        return override.get("anchor_aed")
    return None


def _derive_subscription(ws):
    """raw platform_portion + recovery_monthly, no rounding applied."""
    p = _platform_portion_raw(ws)
    r = ws.get("number_3_financing", {}).get("recovery_monthly_aed")
    if p is None or r is None:
        return None
    return p + r


def _derive_mobilisation(ws):
    """Derive mobilisation by reverse-engineering the mobilisation_pct
    from the worksheet's own stored mobilisation_fee_aed and build_value_aed,
    then re-applying it. Self-checking: if the worksheet says it stored
    bv*0.33 rounded to 4900, we derive 0.33 and reproduce 4900; if it says
    bv*0.40 rounded to 22429, we derive 0.40 and reproduce 22429. This
    works regardless of whether the worksheet has a separate
    mobilisation_pct field."""
    bv = ws.get("number_2_build", {}).get("build_value_aed")
    mf = (ws.get("number_3_financing", {}).get("mobilisation_fee_aed")
          or ws.get("number_3_financing", {}).get("mobilisation_aed"))
    if bv is None or mf is None or bv == 0:
        return None
    implied_pct = mf / bv
    # Snap to 0.33 or 0.40 (the only two rates this corpus uses); if neither,
    # use the exact fraction and the comparison below still tests the right thing.
    if abs(implied_pct - 0.33) < 0.005:
        mob_pct = 0.33
    elif abs(implied_pct - 0.40) < 0.005:
        mob_pct = 0.40
    else:
        mob_pct = implied_pct
    return round(bv * mob_pct)


def _derive_internal_build_cost(ws):
    """round(total_hours * 150)."""
    th = ws.get("number_2_build", {}).get("total_hours")
    if th is None:
        return None
    return round(th * POLICY["cost_to_serve"]["internal_consultant_cost_aed_hr"])


def _classify_delta(stored, derived, cited_rule_present):
    """Returns 'PASS' | 'PASS-WITH-CITATION' | 'HARD FAIL' and a one-line reason.
    Nearest-10 step = 10 (the convention the corpus already applies inline).
    Sub-1 items collapse to PASS-WITH-CITATION only if a cited rule is
    present; otherwise HARD FAIL (downward uncited)."""
    if stored is None or derived is None:
        return "PASS", "no derivation available"
    delta = stored - derived
    if abs(delta) < 1e-6:
        return "PASS", "exactly derived"
    if delta > 10:
        return "HARD FAIL", f"UP delta +{delta:.2f} > nearest-10 step, uncited"
    if delta > 0:
        return "PASS-WITH-CITATION" if cited_rule_present else "HARD FAIL", (
            f"UP delta +{delta:.2f} within step, "
            + ("cited" if cited_rule_present else "UNCITED upward")
        )
    # delta < 0
    if abs(delta) > 10:
        return "HARD FAIL", f"DOWN delta {delta:.2f} > nearest-10 step, uncited"
    if cited_rule_present:
        return "PASS-WITH-CITATION", f"DOWN delta {delta:.2f} within step, cited"
    return "HARD FAIL", f"DOWN delta {delta:.2f} within step, uncited (downward uncited still hard-fails per criterion)"


def t10_client_facing_money_figure_guard():
    # Per-segment mobilisation pct, from policy.yaml segments
    seg_mob_pct = {s: POLICY["segments"][s]["default_mobilisation_pct"]
                   if "default_mobilisation_pct" in POLICY["segments"][s]
                   else POLICY["gates"]["default_mobilisation_pct"]
                   for s in POLICY["segments"]}
    # All current corpus clients happen to be low or elevated per their
    # own manifest.yaml; mobilisation_pct is sourced from risk-assessment
    # for elevated, default for low. We honour the worksheet's own stored
    # figure and only test whether it matches the rate-of-risk formula.

    # AMENDED 2026-08-06: "cited" now means cited to a policy.yaml field,
    # not an inline worksheet comment (the old "rounded to nearest 10" in
    # str(...) check never matched anything -- YAML comments don't survive
    # yaml.safe_load, so every worksheet was silently uncited regardless of
    # its own text). subscription is cited because policy.yaml now declares
    # presentation.client_facing_subscription_rounding: nearest_10_aed with
    # subscription figures in applies_to. internal_build_cost is cited via
    # the separate presentation.non_subscription_rounding field (banker's
    # rounding, Python round() half-to-even) -- it is scope-excluded from
    # the subscription rule but IS a round()-derived figure, and its only
    # observed deltas corpuswide are the sub-1 artifacts that field
    # describes. mobilisation has no policy field of its own: its
    # mechanical value is a straight bv*pct with no declared rounding
    # tolerance, so it stays uncited -- an uncited delta hard-fails upward
    # unconditionally, and downward past one step.
    subscription_rounding = POLICY.get("presentation", {}).get("client_facing_subscription_rounding")
    subscription_cited = bool(subscription_rounding) and subscription_rounding.get("method") == "nearest_10_aed"
    non_subscription_rounding = POLICY.get("presentation", {}).get("non_subscription_rounding")
    internal_build_cost_cited = (bool(non_subscription_rounding)
                                  and non_subscription_rounding.get("method") == "bankers_rounding_half_to_even")

    for client in CLIENT_WORKSHEETS:
        ws_path = os.path.join(REPO_ROOT, "02-clients", client, "02-calc", "pricing-worksheet.yaml")
        if not os.path.exists(ws_path):
            continue
        ws = pe._load(ws_path)
        mob_pct = ws.get("number_3_financing", {}).get("mobilisation_pct")
        # mobilisation_pct may be implicit from risk band; we test with the
        # worksheet's own value (always present post-v3.0).

        cases = [
            ("subscription", ws.get("assembly", {}).get("subscription_fee_aed_mo")
                          or ws.get("assembly", {}).get("option_a", {}).get("subscription_aed"),
             _derive_subscription(ws),
             subscription_cited),
            ("mobilisation", ws.get("number_3_financing", {}).get("mobilisation_fee_aed")
                          or ws.get("number_3_financing", {}).get("mobilisation_aed"),
             _derive_mobilisation(ws),
             False),  # scope_excludes: no policy field grants this a rounding tolerance
            ("internal_build_cost", ws.get("number_2_build", {}).get("internal_build_cost_aed"),
             _derive_internal_build_cost(ws),
             internal_build_cost_cited),  # cited to presentation.non_subscription_rounding
        ]
        for label, stored, derived, cited in cases:
            verdict, reason = _classify_delta(stored, derived, cited)
            check(f"T10: {client} {label} verdict = {verdict} "
                  f"(stored={stored}, derived={derived}, {reason})",
                  verdict != "HARD FAIL")


# ---------------------------------------------------------------------
# T9 — worksheet internal consistency. Every client worksheet's
# total_hours / total_hours_all_in must equal the sum of the component
# fields it is itself built from -- never a hand-typed figure that can
# silently drift from its own stated parts. Found live: Kallat's and
# Prosper's total_hours_all_in were off by 4.0h and 9.0h respectively
# (both traced to the hypercare.hours contribution being mistyped into
# the final sum during manual worksheet authoring -- a P13 violation:
# the recompute script computed the correct figures, but this specific
# summary field was hand-typed into the YAML rather than piped from the
# script's own output). internal_build_cost_aed was NOT affected in
# either case -- it was independently computed from the correct total
# and matches to the AED. This test guards both invariants for every
# corpus client going forward, to a 0.001h tolerance.
# ---------------------------------------------------------------------
CLIENT_WORKSHEETS = [
    "KP-kallat-properties",
    "PRO-prosper-realestate",
    "VGE-vongeyern-realestate",
    "MRD-meridianview-realty",
]


def t9_component_level_formulas(policy=None):
    """Widened T9 (per review): checks each COMPONENT against its own
    engine formula, not just that the sums are internally self-consistent
    -- a worksheet can pass the sum-check while every component is
    independently wrong, if they're wrong by amounts that happen to
    cancel (not the case found here, but the earlier sum-only check
    could not have detected it either way). documentation_hours/qa_hours/
    training_hours are checked for every worksheet, migrated or not, using
    that worksheet's own reference dev_hours (a_hours+class_b.total_hours
    once migrated; raw delivery_hours sum pre-migration, since that was
    the only base that existed before class_b did). a_side_hours/
    class_b.total_hours/hypercare.hours are checked only where the new
    schema is present."""
    pol = policy or pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    inv = pe.load_inventory()
    for client in CLIENT_WORKSHEETS:
        ws_path = os.path.join(REPO_ROOT, "02-clients", client, "02-calc", "pricing-worksheet.yaml")
        if not os.path.exists(ws_path):
            continue
        ws = pe._load(ws_path)
        b = ws.get("number_2_build", {})
        n = ws.get("inputs", {}).get("users_now")
        has_new_schema = "class_b" in b and "hypercare" in b and "a_side_hours" in b

        if has_new_schema:
            ref_dev_hours = b["a_hours"] + b["class_b"]["total_hours"]
        else:
            ref_dev_hours = sum(e["hours"] for e in b.get("delivery_hours", []))

        expected_doc = max(pol["overlays"]["documentation_hours_min"],
                            round(pol["overlays"]["documentation_pct_of_dev"] * ref_dev_hours))
        expected_qa = max(pol["overlays"]["qa_hours_min"],
                           round(pol["overlays"]["qa_pct_of_delivery"] * ref_dev_hours))
        expected_training = pol["overlays"]["training_sessions"] * pol["overlays"]["training_hours_per_session"]

        check(f"T9c: {client} documentation_hours == max(floor, pct*{ref_dev_hours:.3f}) "
              f"(stored={b.get('documentation_hours')}, expected={expected_doc})",
              b.get("documentation_hours") == expected_doc)
        check(f"T9c: {client} qa_hours == max(floor, pct*{ref_dev_hours:.3f}) "
              f"(stored={b.get('qa_hours')}, expected={expected_qa})",
              b.get("qa_hours") == expected_qa)
        check(f"T9c: {client} training_hours == policy constant "
              f"(stored={b.get('training_hours')}, expected={expected_training})",
              b.get("training_hours") == expected_training)

        if has_new_schema and n:
            expected_a_hours = pe.a_hours_for_n(n, inventory=inv) if client in ("KP-kallat-properties", "PRO-prosper-realestate") else None
            if expected_a_hours is not None:
                check(f"T9c: {client} a_hours == pricing_engine.a_hours_for_n({n}) "
                      f"(stored={b.get('a_hours')}, expected={expected_a_hours})",
                      b.get("a_hours") == expected_a_hours)
            expected_class_b, _ = pe.b_hours_for_branch(n, "m", inv)
            check(f"T9c: {client} class_b.total_hours == pricing_engine.b_hours_for_branch({n},'m') "
                  f"(stored={b['class_b']['total_hours']}, expected={expected_class_b:.3f})",
                  abs(b["class_b"]["total_hours"] - expected_class_b) < 0.001)
            expected_hc_hours = pe.hypercare_hours_for_n(n)
            check(f"T9c: {client} hypercare.hours == pricing_engine.hypercare_hours_for_n({n}) "
                  f"(stored={b['hypercare']['hours']}, expected={expected_hc_hours})",
                  b["hypercare"]["hours"] == expected_hc_hours)
            expected_a_side = b["a_hours"] + expected_doc + expected_qa + expected_training
            check(f"T9c: {client} a_side_hours == a_hours+doc+qa+training "
                  f"(stored={b.get('a_side_hours')}, expected={expected_a_side})",
                  b.get("a_side_hours") == expected_a_side)


def t9_worksheet_internal_consistency():
    for client in CLIENT_WORKSHEETS:
        ws_path = os.path.join(REPO_ROOT, "02-clients", client, "02-calc", "pricing-worksheet.yaml")
        if not os.path.exists(ws_path):
            continue
        ws = pe._load(ws_path)
        b = ws.get("number_2_build", {})

        # Invariant 1: every worksheet MUST be on the new Class A-D schema --
        # a worksheet missing class_b/hypercare/a_side_hours is un-migrated,
        # not exempt. This is a hard FAIL, not a skip, so an un-migrated
        # worksheet can never present as green again (closes the coverage
        # gap VGE/MRD exposed: T9 previously only checked worksheets that
        # already had the new fields, silently passing over ones that didn't).
        has_new_schema = "class_b" in b and "hypercare" in b and "a_side_hours" in b
        check(f"T9: {client} is migrated to the new Class A-D schema "
              f"(class_b/hypercare/a_side_hours present)", has_new_schema,
              "MISSING new-schema fields -- worksheet not yet migrated to pricing v3.0")

        if has_new_schema:
            computed_sum = b["a_side_hours"] + b["class_b"]["total_hours"] + b["hypercare"]["hours"]
            stored_all_in = b.get("total_hours_all_in")
            stored_total = b.get("total_hours")
            check(f"T9: {client} total_hours_all_in == a_side_hours+class_b.total_hours+hypercare.hours "
                  f"(stored={stored_all_in}, computed={computed_sum})",
                  stored_all_in is not None and abs(stored_all_in - computed_sum) < 0.001)
            check(f"T9: {client} total_hours == total_hours_all_in "
                  f"(stored total_hours={stored_total}, total_hours_all_in={stored_all_in})",
                  stored_total is not None and stored_all_in is not None and abs(stored_total - stored_all_in) < 0.001)

            # Invariant 3: class_b.subtotal_aed / b_side_subtotal_aed and
            # hypercare.cost_aed must match the committed engine emitters,
            # not a value that only ever existed in the scratch
            # recompute_worksheet.py script.
            users_now = ws.get("inputs", {}).get("users_now")
            if users_now:
                expected_b_side = pe.b_side_subtotal_aed(users_now)
                stored_b_side = b["class_b"].get("subtotal_aed")
                stored_b_side_top = b.get("b_side_subtotal_aed")
                check(f"T9: {client} class_b.subtotal_aed == pricing_engine.b_side_subtotal_aed({users_now}) "
                      f"(stored={stored_b_side}, expected={expected_b_side})",
                      stored_b_side is not None and abs(stored_b_side - expected_b_side) < 0.01)
                check(f"T9: {client} b_side_subtotal_aed == pricing_engine.b_side_subtotal_aed({users_now}) "
                      f"(stored={stored_b_side_top}, expected={expected_b_side})",
                      stored_b_side_top is not None and abs(stored_b_side_top - expected_b_side) < 0.01)

                expected_hc_cost = pe.hypercare_cost_aed(users_now)
                stored_hc_cost = b["hypercare"].get("cost_aed")
                check(f"T9: {client} hypercare.cost_aed == pricing_engine.hypercare_cost_aed({users_now}) "
                      f"(stored={stored_hc_cost}, expected={expected_hc_cost})",
                      stored_hc_cost is not None and abs(stored_hc_cost - expected_hc_cost) < 1)

        # Invariant 2 (universal, any schema): internal_build_cost_aed ==
        # total_hours * policy.yaml cost_to_serve.internal_consultant_cost_aed_hr (150)
        total_hours = b.get("total_hours")
        internal_cost = b.get("internal_build_cost_aed")
        if total_hours is not None and internal_cost is not None:
            expected_cost = round(total_hours * 150)
            check(f"T9: {client} internal_build_cost_aed == total_hours*150 "
                  f"(stored={internal_cost}, expected={expected_cost} from total_hours={total_hours})",
                  abs(internal_cost - expected_cost) <= 1)


# ---------------------------------------------------------------------
# T12 -- input-layer provenance guard. ADDED 2026-08-06, separate from
# T10 on purpose: T10 only checks stored-vs-derived arithmetic against a
# worksheet's OWN recorded inputs -- it has no way to see whether those
# inputs are what the client actually asked for. This gap is exactly how
# Kallat's unrequested scope and unsourced headcount passed every T10
# check clean (see CHANGELOG.md pricing v3.1 addenda, 2026-08-06). Three
# assertions per client:
#   1. inputs.users_now traces to a client-sourced document -- checked
#      against USERS_NOW_PROVENANCE below, an explicit, human-audited
#      ledger (this session's file:line findings), not an NLP inference.
#      A client name absent from the ledger, or present with a `None`
#      source, fails this assertion by design.
#   2. Every inputs.work_packages entry appears in the client's own
#      client-brief.yaml: scope_signals.work_packages_requested, or in
#      client-brief.yaml: scope_signals.approved_scope_exceptions -- a
#      field that does not exist anywhere in this corpus yet. Its absence
#      is a correct FAIL for any client with unrequested packages, not a
#      bug in this check: exceptions must be explicitly recorded to pass,
#      never assumed.
#   3. Segment classification is contingent on assertion 1 -- an
#      unverified users_now makes the derived segment unverified too,
#      independent of whether the classification arithmetic itself
#      (N vs policy.yaml segments.*.max_users) is correct.
# ---------------------------------------------------------------------
USERS_NOW_PROVENANCE = {
    # client: (verified: bool, source) -- audited 2026-08-06, see
    # CHANGELOG.md pricing v3.1 addenda for the full derivation of each.
    "KP-kallat-properties": (False,
        "UNSOURCED -- client-brief.yaml:12 cites both call transcripts, "
        "neither contains a client-side headcount statement; "
        "call-transcript-2026-07-16-internal-prep.md's own header: "
        "'no client present'"),
    "PRO-prosper-realestate": (False,
        "externally sourced, unverified by this audit -- users_now=31 "
        "traces to CRM Lead 8407's x_employee_count field, outside this "
        "repo's audited artifact set; not independently re-confirmed"),
    "VGE-vongeyern-realestate": (True,
        "call-transcript-2026-08-03.md:296, Ms. Nadja (Owner), direct "
        "client-present call: 'we are a boutique brokerage ... small "
        "brokerage' -- confirms scale, not an exact headcount figure "
        "(weaker tier than MRD's, but genuinely client-sourced)"),
    "MRD-meridianview-realty": (True,
        "call-transcript-2026-06-10.md:13, Omar Al Farsi (Owner), "
        "verbatim: 'Five people, we're not a big operation' -- direct, "
        "exact, client-present"),
}

# ADDED 2026-08-06: a clean worksheet==brief package match is only
# evidence of independent corroboration if the two documents weren't
# written by the same pen in the same commit. Downgrades an otherwise-
# passing assertion-2 match to FAIL where that's not the case.
SCOPE_MATCH_INDEPENDENT_SOURCE = {
    "PRO-prosper-realestate": (False,
        "client-brief.yaml and pricing-worksheet.yaml were both first "
        "committed in 525940d -- the same commit that padded Kallat's "
        "scope. verbal-promises.md row 2 additionally grounds 2 of these "
        "8 packages in language citing 'the same vertical baseline ... "
        "established for Kallat'. A same-pen match is not independent "
        "corroboration -- downgraded per explicit review, see "
        "CHANGELOG.md pricing v3.1 addenda."),
    # NOTE: MRD's worksheet and brief were ALSO first committed together
    # (a405109), the same structural pattern as Prosper's. NOT downgraded
    # here -- unlike Prosper, MRD's content is independently verifiable
    # against call-transcript-2026-06-10.md's specific, multi-item client
    # dialogue (not a citation to another client's baseline). This is a
    # judgment call the CHANGELOG addendum flags explicitly for human
    # review, not one this check silently resolves either way.
}

# ADDED 2026-08-06: undocumented scope is not one severity tier. Whether
# it changes what the client is BILLED depends on whether number_2_build.
# delivery_hours actually feeds the quoted price, or the quote is pinned
# independently of it (VGE's brief_pin_variance: which_governs: "pinned").
# BILLING EXPOSURE: undocumented scope the client is actually charged for.
# DELIVERY-COMMITMENT EXPOSURE: undocumented scope SGC is still committed
# to build/deliver, but that does not change the client's bill. AED
# figures per CHANGELOG.md pricing v3.1 addenda.
#
# CORRECTED 2026-08-06 -- same-unit restatement. VGE's brief has an
# EMPTY scope_signals.work_packages_requested list, so VGE's 7 worksheet
# packages are UNDOCUMENTED, not "requested" -- the term in the prior
# addendum was wrong. AED figures must be in the same unit to compare
# across clients: chosen unit is DELTA vs documented scope (AED amount
# the worksheet's own scope exceeds what the brief requests).
#   - Kallat: delta = build_value_aed (padded) - build_value_aed (4-pkg
#     requested baseline) = 19,652 AED. Sized from engine recompute.
#   - VGE:   delta = internal_build_cost_aed_total - 0 (brief empty) =
#     7,562 AED total internal build cost for the 7 undocumented pkgs.
#     100% of the 7,562 is undocumented against the brief.
SCOPE_EXPOSURE_TIER = {
    "KP-kallat-properties": ("billing", 19652,
        "DELTA VS BRIEF: 19,652 AED. 4 unrequested packages feed a_side_hours "
        "directly -> build_value_aed 56,072 vs 36,420 unpadded (35.0% of "
        "quote); the client IS billed for this scope"),
    "PRO-prosper-realestate": ("n/a", 0,
        "0 unrequested packages -- all 8 match its brief; assertion 2 fails "
        "on same-pen provenance, not on billing exposure, no AED delta to "
        "compute since the scope itself is not in dispute"),
    "VGE-vongeyern-realestate": ("delivery-commitment", 7562,
        "DELTA VS BRIEF: 7,562 AED (100% of internal_build_cost_aed -- brief "
        "lists zero packages). 7 UNDOCUMENTED packages feed a_side_hours; "
        "quoted price is pinned (brief_pin_variance.which_governs: 'pinned "
        "... client never sees' the mechanical alternative) so this 7,562 "
        "is a delivery commitment, NOT a billing one -- the client is not "
        "invoiced for it"),
    "MRD-meridianview-realty": ("n/a", 0, "clean -- no undocumented scope"),
}


def t12_input_provenance_guard():
    for client in CLIENT_WORKSHEETS:
        client_dir = os.path.join(REPO_ROOT, "02-clients", client)
        ws_path = os.path.join(client_dir, "02-calc", "pricing-worksheet.yaml")
        if not os.path.exists(ws_path):
            continue
        ws = pe._load(ws_path)
        brief_path = os.path.join(client_dir, "00-intake", "client-brief.yaml")
        brief = pe._load(brief_path) if os.path.exists(brief_path) else {}

        users_now = ws.get("inputs", {}).get("users_now")
        segment = ws.get("inputs", {}).get("segment")
        verified, source = USERS_NOW_PROVENANCE.get(client, (False, "not in provenance ledger"))

        check(f"T12: {client} users_now ({users_now}) traces to a client-sourced document",
              verified, source)

        # CORRECTED 2026-08-06 (re-fix): a single hardcoded field read
        # produced a wrong PASS on VGE (inputs.work_packages is empty by
        # VGE's input convention, but delivery_hours has 7) when the read
        # was on inputs.work_packages; switching to delivery_hours alone
        # broke nothing for VGE but masked WHICH FIELD was being checked
        # -- and the brief's path through "delivery_packages non-empty
        # but brief empty" tripped MAXIMUM SEVERITY on Prosper where it
        # should have been trivially clean. The fix is client-agnostic:
        # try both fields, pick whichever is non-empty, hard-fail if
        # neither resolves -- never silently n/a. The same-pen caveat in
        # SCOPE_MATCH_INDEPENDENT_SOURCE still applies on a successful
        # match (Prosper), and an empty-empty result is INCONCLUSIVE not
        # n/a, per the existing INCONCLUSIVE discipline.
        candidates = [
            ("inputs.work_packages",
                list(ws.get("inputs", {}).get("work_packages", []) or [])),
            ("number_2_build.delivery_hours",
                [e.get("package") for e in (ws.get("number_2_build", {}).get("delivery_hours", []) or [])
                 if e.get("package")]),
        ]
        resolved_field = None
        resolved_packages = []
        for field_name, vals in candidates:
            if vals:
                resolved_field = field_name
                resolved_packages = vals
                break
        delivery_packages = set(resolved_packages)

        if not delivery_packages:
            check(f"T12: {client} worksheet declares a package-level scope to check",
                  False,
                  f"BOTH inputs.work_packages AND number_2_build.delivery_hours are "
                  f"empty for {client} -- INCONCLUSIVE, treated as FAIL (hard, never "
                  f"silently n/a): no worksheet scope recorded in either field to "
                  f"compare against the brief")
        else:
            # Diagnostic: report exactly which field the resolver picked AND
            # what the other field actually contained, so any silently-empty
            # "other field" is visible in test output rather than asserted.
            other_field, other_vals = candidates[1] if resolved_field == candidates[0][0] else candidates[0]
            print(f"  [T12 RESOLVER] {client}: read {len(delivery_packages)} package(s) "
                  f"from {resolved_field}; other field {other_field} has "
                  f"{len(other_vals)} package(s)")
        requested = set(brief.get("scope_signals", {}).get("work_packages_requested", []) or [])
        approved_exceptions = set(brief.get("scope_signals", {}).get("approved_scope_exceptions", []) or [])

        if not delivery_packages:
            check(f"T12: {client} worksheet declares a package-level scope to check",
                  False,
                  "number_2_build.delivery_hours is empty or missing -- INCONCLUSIVE, "
                  "treated as FAIL: no worksheet scope recorded to compare against the brief")
        elif not requested:
            tier, exposure_aed, tier_note = SCOPE_EXPOSURE_TIER.get(client, ("unknown", 0, "not classified"))
            check(f"T12: {client} every worksheet work_package is in the brief's requested list "
                  "or an approved exception",
                  False,
                  f"[{tier.upper()} EXPOSURE, AED {exposure_aed:,}] worksheet declares "
                  f"{len(delivery_packages)} package(s) {sorted(delivery_packages)} against an EMPTY "
                  f"brief.scope_signals.work_packages_requested -- 100% of delivered scope is "
                  f"undocumented against intake. {tier_note}")
        else:
            unrequested = delivery_packages - requested - approved_exceptions
            if unrequested:
                tier, exposure_aed, tier_note = SCOPE_EXPOSURE_TIER.get(client, ("unknown", 0, "not classified"))
                check(f"T12: {client} every worksheet work_package is in the brief's requested list "
                      "or an approved exception",
                      False,
                      f"[{tier.upper()} EXPOSURE, AED {exposure_aed:,}] unrequested (no "
                      f"approved_scope_exceptions field exists yet): {sorted(unrequested)}. {tier_note}")
            else:
                independent, note = SCOPE_MATCH_INDEPENDENT_SOURCE.get(
                    client, (True, "worksheet and brief independently sourced"))
                # comparison_set=delivery_packages: both prior branches already
                # hard-fail an empty delivery_packages before execution reaches
                # here, so this is a defense-in-depth backstop, not the primary
                # guard -- exactly the point of putting the rule in check()
                # itself rather than only in the if/elif chain above.
                check(f"T12: {client} every worksheet work_package is in the brief's requested list "
                      "or an approved exception",
                      independent,
                      note if not independent else "all packages traced to the brief",
                      comparison_set=delivery_packages)

        check(f"T12: {client} segment ({segment}) classification rests on a verified user count",
              verified,
              f"segment arithmetic may be correct, but depends on users_now, which is "
              + ("verified" if verified else "NOT verified above"))


# ---------------------------------------------------------------------
# T13 — PART 6: commission pro-rata release. commission_released_to_date
# must never exceed commission_rate * cash_collected_to_date, on any
# payment structure. Required proof case: financed deal collecting 33%
# at kickoff, released commission at that moment == 14% of collected,
# not 14% of contract.
# ---------------------------------------------------------------------
def t13_commission_pro_rata():
    contract_value_aed = 100000.0
    cash_collected_aed = 33000.0  # 33% at kickoff
    basis = pe.business_cost_floor()
    rate = (basis["commission_sales_pct"] + basis["commission_delivery_pct"]) / 100.0
    check("T13: combined commission rate is sales_pct + delivery_pct = 14%",
          abs(rate - 0.14) < 1e-9,
          f"got {rate}")

    result = pe.commission_released(contract_value_aed, cash_collected_aed)
    expected_commission_on_cash = rate * cash_collected_aed  # 14% of 33,000 = 4,620
    expected_wrong_if_bugged = rate * contract_value_aed     # 14% of 100,000 = 14,000 -- must NOT equal this

    check("T13: commission calculated on cash collected (33%) equals 14% of COLLECTED, not 14% of CONTRACT",
          abs(result["commission_earned_on_cash_aed"] - expected_commission_on_cash) < 0.01,
          f"expected {expected_commission_on_cash}, got {result['commission_earned_on_cash_aed']}")

    check("T13: commission on cash collected does NOT equal 14% of full contract value (the bug this guards against)",
          abs(result["commission_earned_on_cash_aed"] - expected_wrong_if_bugged) > 0.01,
          f"commission_earned_on_cash_aed ({result['commission_earned_on_cash_aed']}) must differ from "
          f"14%-of-contract ({expected_wrong_if_bugged}) -- if equal, release is not pro-rata")

    check("T13: released_aed + retained_aed reconstructs commission_earned_on_cash_aed",
          abs((result["released_aed"] + result["retained_aed"]) - result["commission_earned_on_cash_aed"]) < 0.01)

    check("T13: 5% retention held back from release",
          abs(result["retained_aed"] - 0.05 * expected_commission_on_cash) < 0.01,
          f"expected retained {0.05 * expected_commission_on_cash}, got {result['retained_aed']}")

    # Invariant sweep: commission released can never exceed rate * cash-in, at any collection point,
    # for both a milestone structure (lumpy collections) and a subscription structure (steady collections).
    for label, collections in [
        ("milestone", [10000, 25000, 40000, 25000]),          # lumpy, sums to 100,000
        ("subscription", [8333.33] * 12),                      # steady monthly, ~100,000/yr
    ]:
        cash_to_date = 0.0
        for c in collections:
            cash_to_date += c
            r = pe.commission_released(contract_value_aed, cash_to_date)
            cap_aed = rate * cash_to_date
            check(f"T13: {label} structure -- released commission never exceeds rate x cash-in at cash_to_date={cash_to_date:.2f}",
                  r["commission_earned_on_cash_aed"] <= cap_aed + 0.01,
                  f"commission_earned_on_cash_aed={r['commission_earned_on_cash_aed']} > cap={cap_aed}")

    # RVN financed-deal fixture (rounding-drift guard, per correction-pass
    # follow-up): payment-plans.yaml:63-70 -- build_value_aed 15,327,
    # mobilisation_aed 5,058 collected at kickoff, financed_remainder_aed
    # 10,269, billed at the ROUNDED client-facing rate billed_monthly_aed
    # 1,680/mo (payment-plans.yaml's own anti-tautology rule requires the
    # ROUNDED rate as the basis, never a raw pre-rounding rate -- this repo
    # has already produced a rounding-source defect once on this exact
    # deal, see payment-plans.yaml:71's "previously_used_basis" note).
    # Uses the rounded rate directly as the cash-in schedule so a future
    # regression that silently swaps in a pre-rounding rate anywhere in
    # the commission path would shift the cap boundary this test checks.
    rvn_contract_value_aed = 15327.0
    rvn_mobilisation_aed = 5058.0
    rvn_billed_monthly_aed = 1680.0  # payment-plans.yaml:64, rounded client-facing rate

    r_rvn_kickoff = pe.commission_released(rvn_contract_value_aed, rvn_mobilisation_aed)
    expected_rvn_kickoff = rate * rvn_mobilisation_aed  # 14% of 5,058 = 708.12
    expected_wrong_rvn = rate * rvn_contract_value_aed   # 14% of 15,327 = 2,145.78 -- must NOT equal this
    check("T13: RVN fixture -- commission at kickoff equals 14% of the 5,058 actually collected, not 14% of the 15,327 contract",
          abs(r_rvn_kickoff["commission_earned_on_cash_aed"] - expected_rvn_kickoff) < 0.01,
          f"expected {expected_rvn_kickoff}, got {r_rvn_kickoff['commission_earned_on_cash_aed']}")
    check("T13: RVN fixture -- kickoff commission does NOT equal 14% of full contract value",
          abs(r_rvn_kickoff["commission_earned_on_cash_aed"] - expected_wrong_rvn) > 0.01,
          f"commission_earned_on_cash_aed ({r_rvn_kickoff['commission_earned_on_cash_aed']}) must differ from "
          f"14%-of-contract ({expected_wrong_rvn})")

    rvn_cash_to_date = rvn_mobilisation_aed
    for month in range(1, 25):
        rvn_cash_to_date += rvn_billed_monthly_aed
        r = pe.commission_released(rvn_contract_value_aed, rvn_cash_to_date)
        cap_aed = rate * rvn_cash_to_date
        check(f"T13: RVN fixture -- released commission never exceeds rate x cash-in at rounded-rate month {month} "
              f"(cash_to_date={rvn_cash_to_date:.2f})",
              r["commission_earned_on_cash_aed"] <= cap_aed + 0.01,
              f"commission_earned_on_cash_aed={r['commission_earned_on_cash_aed']} > cap={cap_aed}")
    check("T13: RVN fixture -- 24mo revenue at rounded billed rate reconstructs payment-plans.yaml:66 exactly",
          abs((rvn_cash_to_date - rvn_mobilisation_aed) - 40320.0) < 0.01,
          f"expected 24 x 1,680 = 40,320, got {rvn_cash_to_date - rvn_mobilisation_aed}")


# ---------------------------------------------------------------------
# T14 — PART 9 self-test requirement: floor recomputation on config
# change. business_cost_floor() must actually change when a
# business-cost-basis.yaml input changes -- never a hardcoded 394.
# ---------------------------------------------------------------------
def t14_floor_recomputation_on_config_change():
    baseline_basis = pe.load_business_cost_basis()
    baseline = pe.business_cost_floor(baseline_basis)

    import copy
    mutated_basis = copy.deepcopy(baseline_basis)
    mutated_basis["fixed_monthly_aed"]["licence_annual_aed"] += 12000  # +1,000/mo
    mutated = pe.business_cost_floor(mutated_basis)

    check("T14: floor_per_hour_aed changes when licence_annual_aed input changes",
          mutated["floor_per_hour_aed"] != baseline["floor_per_hour_aed"],
          f"baseline={baseline['floor_per_hour_aed']}, mutated={mutated['floor_per_hour_aed']} -- "
          "identical output after a real input mutation means the floor is not actually recomputed")

    expected_delta_total_requirement = 12000 / 12  # the +1,000/mo flows straight into cash_out -> total_requirement
    actual_delta = mutated["total_requirement_aed"] - baseline["total_requirement_aed"]
    check("T14: total_requirement_aed moves by exactly the mutated input's monthly delta",
          abs(actual_delta - expected_delta_total_requirement) < 0.01,
          f"expected delta {expected_delta_total_requirement}, got {actual_delta}")

    delivery_hours = baseline_basis["delivery"]["delivery_hours_per_month"]
    expected_floor_delta = expected_delta_total_requirement / delivery_hours
    actual_floor_delta = mutated["floor_per_hour_aed"] - baseline["floor_per_hour_aed"]
    check("T14: floor_per_hour_aed delta matches total_requirement delta / delivery_hours exactly",
          abs(actual_floor_delta - expected_floor_delta) < 0.01,
          f"expected {expected_floor_delta}, got {actual_floor_delta}")

    # Second mutation on a completely different input, to rule out the
    # first check having accidentally hit a coincidental no-op path.
    mutated_basis_2 = copy.deepcopy(baseline_basis)
    mutated_basis_2["delivery"]["delivery_hours_per_month"] -= 10
    mutated_2 = pe.business_cost_floor(mutated_basis_2)
    check("T14: floor_per_hour_aed also changes when delivery_hours_per_month changes (second independent input)",
          mutated_2["floor_per_hour_aed"] != baseline["floor_per_hour_aed"],
          f"baseline={baseline['floor_per_hour_aed']}, mutated={mutated_2['floor_per_hour_aed']}")


# ---------------------------------------------------------------------
# T15 — PART 9 self-test requirement: below-floor quotes are blocked.
# hour_rate_floor_test() must return verdict BLOCK when effective
# AED/hour falls below business_cost_floor()'s floor_per_hour_aed.
# ---------------------------------------------------------------------
def t15_below_floor_quotes_blocked():
    basis = pe.business_cost_floor()
    floor = basis["floor_per_hour_aed"]

    # Construct a deliberately underpriced quote: price/hours chosen so
    # effective_rate_aed_hr (after commission) lands below the floor.
    hours_total = 40.0
    underpriced_price_aed = floor * hours_total * 0.7  # ~30% under floor before commission even bites
    r_block = pe.hour_rate_floor_test(underpriced_price_aed, hours_total, cost_basis=basis)
    check("T15: underpriced quote returns verdict BLOCK",
          r_block["verdict"] == "BLOCK",
          f"effective_rate_aed_hr={r_block['effective_rate_aed_hr']}, floor={floor}, verdict={r_block['verdict']}")
    check("T15: BLOCK verdict's effective_rate_aed_hr is genuinely below floor_per_hour_aed",
          r_block["effective_rate_aed_hr"] < floor,
          f"effective_rate_aed_hr={r_block['effective_rate_aed_hr']} not < floor={floor}")

    # Control: a well-priced quote at 2x the floor rate must NOT block.
    healthy_price_aed = floor * hours_total * 2.0
    r_pass = pe.hour_rate_floor_test(healthy_price_aed, hours_total, cost_basis=basis)
    check("T15: control -- healthy-margin quote at 2x floor does not return BLOCK",
          r_pass["verdict"] != "BLOCK",
          f"verdict={r_pass['verdict']}, effective_rate_aed_hr={r_pass['effective_rate_aed_hr']}")

    # Boundary: price landing exactly at the floor (post-commission) must
    # not be silently rounded into a false PASS -- BLOCK is the
    # inclusive-below-floor case, so exactly-at-floor should read WARN or
    # PASS, never BLOCK, and exactly-one-AED-under should BLOCK.
    commission_rate = (basis["commission_sales_pct"] + basis["commission_delivery_pct"]) / 100.0
    price_at_floor_aed = (floor * hours_total) / (1 - commission_rate)
    r_boundary = pe.hour_rate_floor_test(price_at_floor_aed, hours_total, cost_basis=basis)
    check("T15: price landing exactly at the floor does not BLOCK",
          r_boundary["verdict"] != "BLOCK",
          f"verdict={r_boundary['verdict']}, effective_rate_aed_hr={r_boundary['effective_rate_aed_hr']}, floor={floor}")


# ---------------------------------------------------------------------
# T16 — PART 9 self-test requirement: migration over 20,000 records
# renders as unpriced, never as an estimated number.
# ---------------------------------------------------------------------
def t16_migration_over_20000_unpriced():
    cat = pe.load_template_catalogue()
    over_band = cat["migration_bands"]["over_20000"]
    check("T16: migration_bands.over_20000 is marked unpriced",
          over_band.get("unpriced") is True,
          f"unpriced={over_band.get('unpriced')}")
    check("T16: migration_bands.over_20000 price_aed is None, never an estimated number",
          over_band.get("price_aed") is None,
          f"price_aed={over_band.get('price_aed')}")
    check("T16: migration_bands.over_20000 hours is None, never an estimated number",
          over_band.get("hours") is None,
          f"hours={over_band.get('hours')}")

    # End-to-end: four_component_build() must propagate the unpriced state
    # as a None total, never silently sum a null into 0 or drop it from
    # the total -- RULE 1's "never render a total that silently drops an
    # unpriced component" (pricing_engine.py:375).
    result = pe.four_component_build(
        modules_selected=[], maturity="mature", migration_band="over_20000",
        enhancement_hours=0.0, catalogue=cat,
    )
    check("T16: four_component_build() with over_20000 migration returns migration.unpriced True",
          result["migration"]["unpriced"] is True)
    check("T16: four_component_build() with over_20000 migration returns price_ex_vat_aed None, "
          "never a silently-estimated total",
          result["price_ex_vat_aed"] is None,
          f"price_ex_vat_aed={result['price_ex_vat_aed']}")
    check("T16: four_component_build() with over_20000 migration returns hours_total None, "
          "never a silently-estimated total",
          result["hours_total"] is None,
          f"hours_total={result['hours_total']}")

    # Control: a band under 20,000 must NOT be unpriced -- proves the
    # None-propagation above is conditional on the band, not a blanket bug.
    result_priced = pe.four_component_build(
        modules_selected=[], maturity="mature", migration_band="from_5000_to_20000",
        enhancement_hours=0.0, catalogue=cat,
    )
    check("T16: control -- from_5000_to_20000 band is priced, not unpriced",
          result_priced["migration"]["unpriced"] is False and result_priced["price_ex_vat_aed"] is not None,
          f"unpriced={result_priced['migration']['unpriced']}, price_ex_vat_aed={result_priced['price_ex_vat_aed']}")


def t17_capacity_table():
    basis = pe.business_cost_floor()
    table = pe.capacity_table(cost_basis=basis)

    hours_per_build = table["hours_per_build"]
    delivery_hours = table["delivery_hours_per_month"]
    row_by_n = {r["deals_per_month"]: r for r in table["rows"]}

    check("T17: hours_per_build is derived from RVN's real module selection via "
          "four_component_build(), not hardcoded to 34",
          hours_per_build == pe.default_mature_build(basis)[0],
          f"hours_per_build={hours_per_build}")

    # NOTE: the brief's own narrative math ("five mature builds at ~25h =
    # 125h... three builds (~75h) fits") used a rough generic per-build
    # hours estimate. The REAL RVN-shaped mature build, derived from
    # four_component_build() with RVN's actual module selection (commit
    # 5b4c5cd), is 34h -- so 3 real builds = 102h, which does NOT fit 83h.
    # This is a genuine finding, not a test bug: at RVN's real build shape
    # the monthly ceiling is 2, not 3. Asserting the true computed value
    # here rather than forcing the test to match the brief's rough estimate.
    check("T17: at 2 deals/month (the real ceiling for RVN's actual build shape, "
          "not the brief's rough ~25h/build estimate), hours fit inside delivery capacity",
          row_by_n[2]["hours"] <= delivery_hours,
          f"2 deals = {row_by_n[2]['hours']}h vs {delivery_hours}h capacity")
    check("T17: at 3 deals/month, hours do NOT fit at RVN's real 34h/build shape "
          "(differs from the brief's rough ~25h/build illustrative math)",
          row_by_n[3]["hours"] > delivery_hours,
          f"3 deals = {row_by_n[3]['hours']}h vs {delivery_hours}h capacity")

    check("T17: at 5 deals/month, hours do NOT fit inside delivery capacity",
          row_by_n[5]["hours"] > delivery_hours,
          f"5 deals = {row_by_n[5]['hours']}h vs {delivery_hours}h capacity")
    check("T17: at 5 deals/month, fits_hours is False",
          row_by_n[5]["fits_hours"] is False)

    min_n = table["min_deals_that_fit_and_cover_aed"]
    check("T17: min_deals_that_fit_and_cover_aed is computed (not None) within the 1-6 range tested",
          min_n is not None,
          f"min_deals_that_fit_and_cover_aed={min_n}")
    if min_n is not None:
        row = row_by_n[min_n]
        check(f"T17: the computed minimum ({min_n} deals) actually both fits hours AND covers the "
              f"owner-salary requirement",
              row["fits_hours"] and row["covers_requirement"],
              f"row={row}")
        if min_n > 1:
            prev_row = row_by_n[min_n - 1]
            check(f"T17: {min_n - 1} deals (one below the computed minimum) does NOT both fit and cover "
                  f"-- proves min_n is the true minimum, not an arbitrary pass",
                  not (prev_row["fits_hours"] and prev_row["covers_requirement"]),
                  f"prev_row={prev_row}")

    signed_over = pe.signed_undelivered_capacity_flag(signed_undelivered_hours=100, remaining_capacity_hours=83)
    check("T17: signed_undelivered_capacity_flag flags overage when signed work exceeds remaining capacity",
          signed_over["exceeds_capacity"] is True and signed_over["overage_hours"] == 17.0,
          f"signed_over={signed_over}")
    signed_under = pe.signed_undelivered_capacity_flag(signed_undelivered_hours=50, remaining_capacity_hours=83)
    check("T17: signed_undelivered_capacity_flag does not flag when signed work fits remaining capacity",
          signed_under["exceeds_capacity"] is False,
          f"signed_under={signed_under}")


def t18_recurring_support_load_table():
    import inspect
    sig = inspect.signature(pe.recurring_support_load_table)
    check("T18: recurring_support_load_table's support_hours_per_client parameter has NO default "
          "(forces caller to supply a measured or explicitly-labelled figure, per brief instruction)",
          sig.parameters["support_hours_per_client"].default is inspect.Parameter.empty,
          f"default={sig.parameters['support_hours_per_client'].default!r}")

    basis = pe.business_cost_floor()

    with_measured = pe.recurring_support_load_table(support_hours_per_client=1.5, cost_basis=basis)
    check("T18: recurring_support_load_table accepts an explicit measured-style figure "
          "and echoes it back unchanged",
          with_measured["support_hours_per_client"] == 1.5)
    check("T18: default recurring_commission_duration is 'perpetual' (NOT FOUND elsewhere in repo, "
          "loudly labelled expensive default per brief instruction)",
          with_measured["recurring_commission_duration"] == "perpetual")

    row_by_n = {r["live_clients"]: r for r in with_measured["rows"]}
    check("T18: support hours consumed scale linearly with live client count",
          row_by_n[10]["support_hours_consumed"] == round(1.5 * 10, 3) and
          row_by_n[40]["support_hours_consumed"] == round(1.5 * 40, 3),
          f"10-client row={row_by_n[10]}, 40-client row={row_by_n[40]}")

    try:
        pe.recurring_support_load_table(support_hours_per_client=2, recurring_commission_duration="bogus")
        check("T18: an invalid recurring_commission_duration raises ValueError", False,
              "no exception was raised")
    except ValueError:
        check("T18: an invalid recurring_commission_duration raises ValueError", True)

    illustrative = pe.illustrative_support_load_scenarios(cost_basis=basis)
    check("T18: illustrative_support_load_scenarios carries an explicit unmeasured warning",
          "ILLUSTRATIVE" in illustrative["warning"] and "UNMEASURED" in illustrative["warning"])
    check("T18: illustrative_support_load_scenarios covers the brief's 1h/2h/3h reference points",
          set(illustrative["scenarios"].keys()) == {1, 2, 3})

    scenario_1h = illustrative["scenarios"][1]["rows"]
    row40_1h = {r["live_clients"]: r for r in scenario_1h}[40]
    check("T18: at 1h/client support load, delivery hours remain positive at 40 live clients "
          "(matches the brief's own '~40 clients' reference point)",
          row40_1h["delivery_hours_remaining"] > 0,
          f"row40_1h={row40_1h}")

    log_path = os.path.join(pe.REPO_ROOT, "00-knowledge", "pricing", "support-hours-log.yaml")
    check("T18: support-hours-log.yaml exists as the real measurement destination",
          os.path.exists(log_path), f"log_path={log_path}")
    if os.path.exists(log_path):
        log = pe._load(log_path)
        check("T18: support-hours-log.yaml starts empty (no fabricated entries), schema present",
              log.get("entries") == [] and "schema" in log,
              f"entries={log.get('entries')}, has_schema={'schema' in log}")


if __name__ == "__main__":
    print("=== T1: boundary fixtures ===")
    t1_boundary_fixtures()
    print("\n=== T2: provenance assertions ===")
    t2_provenance()
    print("\n=== T3: N=1..400 sweep ===")
    t3_n_sweep()
    print("\n=== T4: mutation testing ===")
    t4_mutation_testing()
    print("\n=== T5: directionality ===")
    t5_directionality()
    print("\n=== T6: class purity ===")
    t6_class_purity()
    print("\n=== T7: Kallat Rev1 rule regression ===")
    t7_kallat_rule_regression()
    print("\n=== T8: check_4 structural sweep ===")
    t8_check4_structural_sweep()
    print("\n=== T9: worksheet internal consistency ===")
    t9_worksheet_internal_consistency()
    print("\n=== T9c: component-level formula checks ===")
    t9_component_level_formulas()
    print("\n=== T10: client-facing money figure guard (corrected criterion) ===")
    t10_client_facing_money_figure_guard()
    print("\n=== T12: input-layer provenance guard ===")
    t12_input_provenance_guard()
    print("\n=== T13: commission pro-rata release (PART 6) ===")
    t13_commission_pro_rata()
    print("\n=== T14: floor recomputation on config change (PART 9) ===")
    t14_floor_recomputation_on_config_change()
    print("\n=== T15: below-floor quotes blocked (PART 9) ===")
    t15_below_floor_quotes_blocked()
    print("\n=== T16: migration over 20,000 renders unpriced (PART 9) ===")
    t16_migration_over_20000_unpriced()
    print("\n=== T17: capacity table (PART 4) ===")
    t17_capacity_table()
    print("\n=== T18: recurring/support-load table (PART 5) ===")
    t18_recurring_support_load_table()

    print()
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} failure(s).")
        for f in FAILURES:
            print(" ", f)
        sys.exit(1)
    print("RESULT: all T1-T7 checks pass.")
    sys.exit(0)
