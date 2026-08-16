#!/usr/bin/env python3
"""
SGC Proposal Engine — Class B / N-user cost-class pricing engine.

Single source of truth for B_hours(N) and the marginal-user onboarding
fee — called by validate.py (checks V1/V2) and test_pricing_engine.py
(T1-T7). P14 (single code path): §D, §F, and §G of
.omc/plans/pricing-engine-cost-class-model.md Rev.2 all read this module,
none hand-derives.

Reads 00-knowledge/pricing/class-b-task-inventory.yaml — no task minute
values or per-inventory constants are duplicated here beyond pure math
(Wright's law, PERT). See the plan document for the full derivation and
citations.
"""
import math
import os
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "class-b-task-inventory.yaml")
RATE_CARD_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "rate-card.yaml")
HOUR_LOOKUP_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "hour-lookup.yaml")
POLICY_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml")
TEMPLATE_CATALOGUE_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "template-catalogue.yaml")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_inventory():
    return _load(INVENTORY_PATH)


def load_rate_card():
    return _load(RATE_CARD_PATH)


def load_hour_lookup():
    return _load(HOUR_LOOKUP_PATH)


def load_policy():
    return _load(POLICY_PATH)


def load_template_catalogue():
    return _load(TEMPLATE_CATALOGUE_PATH)


def cum_sum(n, b):
    """Sigma_{i=1}^{n} i^-b, the Wright's-law cumulative-learning sum.
    n is cast to int -- T4 mutation-tests constants that feed this (n_bulk,
    n_ref) by perturbing them by a percentage, which produces a float;
    range() requires an int, and truncating is the correct behavior for a
    population-count threshold under perturbation."""
    return sum(i ** (-b) for i in range(1, int(n) + 1))


def to_first_unit(steady_state_value, n_ref, b):
    """D-3: convert an elicited steady-state-mean value to Wright's-law T1."""
    return steady_state_value * n_ref / cum_sum(n_ref, b)


def role_count(n, divisor, cap):
    """Distinct-role heuristic, Grade D — see class-b-task-inventory.yaml
    constants.role_count_divisor for citation."""
    return min(cap, max(1, round(n / divisor)))


def pert_mean(o, m, p):
    return (o + 4 * m + p) / 6.0


def junior_passthrough_ceiling_aed_hr(rate_card=None):
    """V2 clerical-task ceiling — rate-card.yaml: passthrough_band.high.
    Falls back to the sourced xlsx figure (120) with a warning if the
    governed field is not yet present (added in implementation step (g))."""
    rc = rate_card or load_rate_card()
    band = rc.get("passthrough_band")
    if band and "high" in band:
        return band["high"]
    return 120  # xlsx Market Positioning sheet row 7 — see D-6; governed field pending step (g)


def b_hours_for_branch(n, branch, inventory=None):
    """branch in {'o','m','p'}. Returns (total_hours, breakdown_dict_hours)."""
    inv = inventory or load_inventory()
    c = inv["constants"]
    b = c["learning_exponent_b"]
    n_bulk = c["n_bulk"]
    n_ref = c["n_ref_for_time_basis_conversion"]
    divisor = c["role_count_divisor"]
    cap = c["role_count_cap"]
    tasks = inv["tasks"]
    key = f"minutes_{branch}"

    breakdown = {}

    n_individual = min(n, n_bulk)
    cum_individual = cum_sum(n_individual, b) if n_individual > 0 else 0.0
    cum_full = cum_sum(n, b) if n > 0 else 0.0

    for name, spec in tasks.items():
        if spec.get("class") != "B":
            continue
        if name in ("role_permission_design", "exception_allowance", "bulk_path_validation"):
            continue  # handled separately below — not per-user-learning-curved in the generic sense

        ss_value = spec[key]
        if spec.get("time_basis") == "steady_state_mean":
            t1 = to_first_unit(ss_value, n_ref, b)
        else:
            t1 = ss_value

        if spec.get("bulk_replaced_above_n_bulk"):
            minutes = t1 * cum_individual
        else:
            minutes = t1 * cum_full
        breakdown[name] = minutes / 60.0

    # bulk-path validation — applies only to users beyond n_bulk
    bulk_spec = tasks.get("bulk_path_validation")
    n_bulk_users = max(0, n - n_bulk)
    if bulk_spec and n_bulk_users > 0:
        breakdown["bulk_path_validation"] = (bulk_spec[key] * n_bulk_users) / 60.0
    else:
        breakdown["bulk_path_validation"] = 0.0

    # exception allowance — flat 10% of N, no learning curve
    exc_spec = tasks["exception_allowance"]
    breakdown["exception_allowance"] = (exc_spec[key] * 0.10 * n) / 60.0

    # role/permission design — flat per distinct role, not per user
    rc_n = role_count(n, divisor, cap)
    design_spec = tasks["role_permission_design"]
    breakdown["role_permission_design"] = (design_spec[key] * rc_n) / 60.0

    total = sum(breakdown.values())
    return total, breakdown


def b_hours_pert(n, inventory=None):
    inv = inventory or load_inventory()
    o, _ = b_hours_for_branch(n, "o", inv)
    m, bd = b_hours_for_branch(n, "m", inv)
    p, _ = b_hours_for_branch(n, "p", inv)
    return {"o": o, "m": m, "p": p, "mean": pert_mean(o, m, p), "breakdown_m": bd}


def a_hours_for_n(n, base_scope_hours=47, inventory=None, hour_lookup=None):
    """A_hours(N): the fixed scope baseline plus the conditional Class A
    additions that trigger at documented N thresholds (D-9's new entries).
    Not a per-user scaling — a step function, same treatment as Class C."""
    hl = hour_lookup or load_hour_lookup()
    wp = hl["work_packages"]
    total = base_scope_hours
    if n > wp["migration_record_validation_signoff"].get("trigger_n", 0):
        total += wp["migration_record_validation_signoff"]["hours_standard"]
    if n > 25:
        total += wp["bulk_user_import_csv"]["hours_standard"]
    if n > 10:
        total += wp["training_content_design_multiagent"]["hours_standard"]
    return total


def marginal_user_fee(n_base, inventory=None):
    """D-2: marginal one-time onboarding fee for the (n_base+1)-th user —
    calls the SAME curve/rate logic as b_hours_for_branch, not a separately
    hand-derived T1 (P14)."""
    inv = inventory or load_inventory()
    c = inv["constants"]
    b = c["learning_exponent_b"]
    n_ref = c["n_ref_for_time_basis_conversion"]
    n_bulk = c["n_bulk"]
    divisor = c["role_count_divisor"]
    cap = c["role_count_cap"]
    tasks = inv["tasks"]

    n_next = n_base + 1
    bulk_regime = n_next > n_bulk
    minutes = {}

    for name in ("account_creation_credential", "individual_onboarding"):
        spec = tasks[name]
        if bulk_regime:
            minutes[name] = 0.0
        else:
            t1 = to_first_unit(spec["minutes_m"], n_ref, b)
            minutes[name] = t1 * (n_next ** -b)

    spec = tasks["per_agent_signoff"]
    t1 = to_first_unit(spec["minutes_m"], n_ref, b)
    minutes["per_agent_signoff"] = t1 * (n_next ** -b)

    minutes["bulk_path_validation"] = tasks["bulk_path_validation"]["minutes_m"] if bulk_regime else 0.0

    exc_spec = tasks["exception_allowance"]
    minutes["exception_allowance_marginal"] = exc_spec["minutes_m"] * 0.10

    delta_roles = role_count(n_next, divisor, cap) - role_count(n_base, divisor, cap)
    design_hours = 0.0
    design_fee_aed = 0.0
    if delta_roles > 0:
        design_spec = tasks["role_permission_design"]
        design_hours = (design_spec["minutes_m"] * delta_roles) / 60.0

    clerical_hours = sum(minutes.values()) / 60.0
    return {
        "clerical_hours": clerical_hours,
        "design_hours": design_hours,
        "delta_roles": delta_roles,
        "minute_breakdown": minutes,
        "bulk_regime": bulk_regime,
    }


def total_hours_for_n(n, inventory=None, hour_lookup=None, policy=None):
    """Reproduces exactly what a recomputed worksheet's number_2_build
    fields sum to at population N: a_hours(N) + qa + doc + training +
    class_b(N) + hypercare(N). Used by validate.py's check_4 structural
    analysis and by test_pricing_engine.py's sweep -- same engine, no
    separate hand model (P13/P14)."""
    inv = inventory or load_inventory()
    hl = hour_lookup or load_hour_lookup()
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))

    a_hours = a_hours_for_n(n, inventory=inv, hour_lookup=hl)
    b_total, _ = b_hours_for_branch(n, "m", inv)
    dev_hours = a_hours + b_total
    qa_hours = max(pol["overlays"]["qa_hours_min"], round(pol["overlays"]["qa_pct_of_delivery"] * dev_hours))
    doc_hours = max(pol["overlays"]["documentation_hours_min"], round(pol["overlays"]["documentation_pct_of_dev"] * dev_hours))
    training_hours = pol["overlays"]["training_sessions"] * pol["overlays"]["training_hours_per_session"]
    a_side_hours = a_hours + qa_hours + doc_hours + training_hours
    hypercare_hours = math.ceil(n / 5) * 2
    return a_side_hours + b_total + hypercare_hours


def b_side_subtotal_aed(n, inventory=None, rate_card=None):
    """Emits class_b.subtotal_aed / b_side_subtotal_aed: per-task hours x
    per-task-role rate, summed. This arithmetic previously lived ONLY in
    the scratch recompute_worksheet.py (never committed) -- the same class
    of risk (hand-computed, not engine-emitted) that caused the
    total_hours_all_in defect fixed in dd87dd2. No new formula: this wraps
    the exact per-task rate assignment already documented in
    class-b-task-inventory.yaml and cost-classes.md (junior_passthrough
    tasks at rate-card.yaml: passthrough_band midpoint, role_permission_design
    at rate-card.yaml roles.business_analyst)."""
    inv = inventory or load_inventory()
    rc = rate_card or load_rate_card()
    _, breakdown = b_hours_for_branch(n, "m", inv)
    junior_rate = junior_passthrough_ceiling_aed_hr(rc) - 30  # midpoint of the 60-120 band = 90
    ba_rate = rc["roles"]["business_analyst"]["rate_aed_hr"]
    total = 0.0
    for task_name, hours in breakdown.items():
        role = inv["tasks"][task_name]["role"]
        rate = junior_rate if role == "junior_passthrough" else ba_rate
        total += hours * rate
    return round(total, 2)


def hypercare_hours_for_n(n):
    """Hours only -- ceil(N/5) pods x 2h/pod (M-branch), the same formula
    already used inside total_hours_for_n(). Exposed standalone so
    hypercare_cost_aed() (and any future caller) doesn't have to
    re-derive it."""
    return math.ceil(n / 5) * 2


def hypercare_cost_aed(n, policy=None):
    """Emits hypercare.cost_aed: hypercare hours x support_rate_aed.
    Previously only computed in the scratch recompute_worksheet.py script,
    same orphan-emitter gap as b_side_subtotal_aed above."""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    hours = hypercare_hours_for_n(n)
    return round(hours * pol["cost_to_serve"]["support_rate_aed"])


def internal_consultant_cost_aed_hr(policy=None):
    """Single source of truth for the internal delivery cost floor
    (AED/hr) — policy.yaml: cost_to_serve.internal_consultant_cost_aed_hr
    must equal this function's output; test_pricing_engine.py asserts it
    (drift guard). Owner-stated cost-basis inputs
    (policy.yaml: internal_cost_basis), UNVERIFIED against real payroll
    records — see HANDOVER.md decision #12.

    There is exactly one delivery role (owner/founder); callers/SDRs are
    fixed overhead, not a per-role delivery cost — see
    internal_cost_basis.role_structure. Do not derive a per-role cost
    table from this function's inputs; there is only one delivery role
    to cost."""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    basis = pol["internal_cost_basis"]
    ops = basis["monthly_operating_basis_aed"]
    cash_out_monthly = (
        ops["licence_annual_aed"] / 12
        + ops["staff_salaries_monthly_aed"]
        + ops["office_monthly_aed"]
        + ops["phones_monthly_aed"]
        + ops["hosting_ai_monthly_aed"]
        + ops["other_monthly_aed"]
    )
    total_requirement_monthly = cash_out_monthly + ops["owner_salary_monthly_aed"]
    hrs = basis["delivery_hours_basis"]
    delivery_hours_per_month = (
        hrs["gross_hours_monthly"]
        - hrs["less_caller_mgmt_hours"]
        - hrs["less_marketing_hours"]
        - hrs["less_training_hours"]
        - hrs["less_admin_accounts_hours"]
        - hrs["less_sales_hours"]
    )
    return round(total_requirement_monthly / delivery_hours_per_month, 2)


def billing_floor_aed_hr(policy=None):
    """Commission-adjusted billing floor (AED/hr) -- ADDED v4 (2026-08-16),
    HANDOVER.md decision #14. This is the actual quoting gate;

    internal_consultant_cost_aed_hr() (aka "cost_floor_per_hour") only
    recovers SGC's operating cost -- it says nothing about commission.
    Commission (internal_cost_basis.commission.combined_pct, 14%) is paid
    OUT OF REVENUE on top of that cost, on every closed deal. A deal billed
    at exactly cost_floor_per_hour therefore never actually clears the
    floor once commission is paid out of it -- 14% of revenue billed at
    cost recovers less than 100% of cost. This function computes the
    higher, correct number: cost_floor_per_hour / (1 - commission_total).

    Two floors, two jobs, do not conflate them:
      internal_consultant_cost_aed_hr() -- cost recovery only, reported as
        a separate metric and used as the WARN threshold.
      billing_floor_aed_hr() (this function) -- cost recovery AND
        commission paid -- this is what BLOCK actually gates on.
    A rate between the two floors "recovers cost, does not pay the
    owner" -- WARN, not PASS. See rate_guard_verdict()."""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    cost_floor = internal_consultant_cost_aed_hr(pol)
    commission_total = pol["internal_cost_basis"]["commission"]["combined_pct"]
    return round(cost_floor / (1 - commission_total), 2)


def rate_guard_verdict(rate_aed_hr, policy=None):
    """BLOCK / WARN / PASS for a single hourly rate against the two floors
    (see billing_floor_aed_hr() docstring for why there are two).
      rate < internal_consultant_cost_aed_hr()           -> BLOCK
      internal_consultant_cost_aed_hr() <= rate < billing_floor_aed_hr() -> WARN
      rate >= billing_floor_aed_hr()                      -> PASS"""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    cost_floor = internal_consultant_cost_aed_hr(pol)
    billing_floor = billing_floor_aed_hr(pol)
    if rate_aed_hr < cost_floor:
        return "BLOCK"
    if rate_aed_hr < billing_floor:
        return "WARN"
    return "PASS"


def breakeven_hours(net_revenue_aed, policy=None):
    """Hours at which net revenue (after commission) exactly recovers cost
    -- net_revenue_aed / internal_consultant_cost_aed_hr(). Uses the COST
    floor, not the billing floor: this answers "how many hours before we
    lose money outright," a different question from the PASS/WARN/BLOCK
    effective-rate gate in deal_guard_verdict(), which uses the billing
    floor. Risk-adjusted hours above this number BLOCK (see T22)."""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    cost_floor = internal_consultant_cost_aed_hr(pol)
    return round(net_revenue_aed / cost_floor, 2)


def deal_guard_verdict(net_revenue_aed, risk_adjusted_hours, policy=None):
    """Whole-deal BLOCK/WARN/PASS: effective net rate = net_revenue_aed /
    risk_adjusted_hours, checked against rate_guard_verdict(). Must be
    called with RISK-ADJUSTED hours (class-b-task-inventory.yaml /
    contingency-schedule terms), never raw estimated hours -- quoting on
    raw hours is the exact failure mode this guards against (see Part 3,
    HANDOVER.md decision #16)."""
    pol = policy or _load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    effective_rate = round(net_revenue_aed / risk_adjusted_hours, 2)
    return effective_rate, rate_guard_verdict(effective_rate, pol)


def class_d_hours_or_cost(edition):
    """Class D structural guarantee: zero for Community by construction."""
    if edition == "community":
        return 0
    raise NotImplementedError(
        "Enterprise Class D pricing not modeled in this engine yet — see "
        "editions.yaml:36 / saas-modules.yaml for the per-user licence "
        "figures; no corpus client currently uses Enterprise."
    )


# ===========================================================================
# Pricing v4 — template-catalogue.yaml (product-plus-services model)
# ADDED 2026-08-16, HANDOVER.md decisions #14-#17. See
# 00-knowledge/pricing/template-catalogue.yaml for the full model and
# every figure's provenance.
# ===========================================================================

def platform_fee_aed(catalogue=None):
    """Fixed platform fee. Deliberately takes NO hours argument at all --
    that is the mechanism, not a convention, that makes it structurally
    impossible to derive this figure from an hour count (see T24, which
    mutates hour inputs elsewhere in the engine and asserts this value is
    unaffected -- it can't be affected, this function never reads one)."""
    cat = catalogue or load_template_catalogue()
    return cat["platform_fee"]["amount_aed"]


def modules_subtotal_aed(module_names=None, catalogue=None):
    """Sum of named modules' fixed prices. module_names=None sums ALL
    five catalogue modules (the reference-quote case); pass an explicit
    subset for a partial quote (e.g. F2's platform + lead_capture only)."""
    cat = catalogue or load_template_catalogue()
    names = module_names if module_names is not None else list(cat["modules"].keys())
    return sum(cat["modules"][m]["amount_aed"] for m in names)


def migration_band_for_records(record_count, catalogue=None):
    """Returns (band_name, amount_aed). Above the highest band, returns
    ("above_band_3", None) -- UNPRICED, routed to Commercial Desk. Never
    extrapolates a number past the governed bands (T16/T26)."""
    cat = catalogue or load_template_catalogue()
    bands = cat["migration_bands"]
    for band_name in ("band_1", "band_2", "band_3"):
        band = bands[band_name]
        if record_count <= band["to_records"]:
            return band_name, band["amount_aed"]
    return "above_band_3", None


def reference_quote_total_aed(catalogue=None):
    """Platform + all 5 modules + migration band_2 -- the 35,000
    reference figure, computed from catalogue line items every call, not
    read from a stored total."""
    cat = catalogue or load_template_catalogue()
    return (platform_fee_aed(cat)
            + modules_subtotal_aed(catalogue=cat)
            + cat["migration_bands"]["band_2"]["amount_aed"])


def discount_gate_verdict(quoted_total_aed, catalogue=None, undiscounted_total_aed=None):
    """COMMERCIAL_DESK_APPROVAL_REQUIRED when quoted_total_aed is a
    DISCOUNT below 90% of what the SAME scope would otherwise cost
    (undiscounted_total_aed), OK otherwise. A real gate, called by the
    render path -- not a comment SDRs are trusted to read.

    BUG FOUND AND FIXED while wiring the Part 5 render path (2026-08-16):
    the first version of this function compared every quote against the
    fixed reference-quote floor (31,500, 90% of the 35,000 5-module
    reference deal) regardless of what was actually being quoted. That is
    correct for T23's own case (discounting the reference quote itself,
    35,000 -> 30,000) but wrong in general: a genuinely SMALLER-SCOPE
    quote (e.g. platform + one module only, F2's fixture, 19,500) is not
    a discount at all, and was incorrectly triggering
    COMMERCIAL_DESK_APPROVAL_REQUIRED just for being a smaller number
    than the unrelated 5-module reference floor. Fixed by comparing
    quoted_total_aed against 90% of ITS OWN scope's undiscounted total,
    not a fixed constant. undiscounted_total_aed defaults to
    reference_quote_total_aed(cat) only to preserve T23's exact existing
    call signature (discount_gate_verdict(30000, cat)) -- every other
    caller (the render path) must pass its own fixture's actual
    undiscounted total explicitly."""
    cat = catalogue or load_template_catalogue()
    basis = undiscounted_total_aed if undiscounted_total_aed is not None else reference_quote_total_aed(cat)
    floor = round(basis * 0.90)
    if quoted_total_aed < floor:
        return "COMMERCIAL_DESK_APPROVAL_REQUIRED"
    return "OK"


def contingency_pct_for(categories, policy=None):
    """categories: a category name (str) or iterable of category names
    from policy.yaml: contingency_schedule. Returns the single applicable
    pct -- the MAX across all supplied categories (combination_rule,
    "worst-risk-governs"), never a sum. INTERNAL ONLY -- never surface
    this percentage on a client-facing document (Part 5.4)."""
    pol = policy or load_policy()
    schedule = pol["contingency_schedule"]
    if isinstance(categories, str):
        categories = [categories]
    pcts = [schedule[c]["pct"] for c in categories]
    return max(pcts)


def risk_adjusted_hours(raw_hours, categories, policy=None):
    """raw_hours * (1 + contingency_pct_for(categories)). Returns
    (raw_hours, risk_adjusted_hours, pct_applied) -- callers must report
    BOTH raw and risk-adjusted in internal output (Part 3), and must use
    ONLY the risk-adjusted figure in any effective-rate/floor check
    (deal_guard_verdict, breakeven_hours) -- quoting on raw hours is the
    exact failure mode this function exists to prevent."""
    pol = policy or load_policy()
    pct = contingency_pct_for(categories, pol)
    adjusted = round(raw_hours * (1 + pct), 2)
    return raw_hours, adjusted, pct


def commission_release_aed(cash_collected_aed, policy=None):
    """Commission released against payments ACTUALLY RECEIVED, per
    internal_cost_basis.commission.release ("pro-rata against payments
    actually received, not on invoice/close"). = cash_collected_aed *
    commission_total. Deliberately takes cash COLLECTED, not contract
    value -- the two produce very different numbers (a small collected
    amount against a large contract releases a small commission), and
    conflating them is the exact failure mode this function's signature
    guards against structurally: there is no contract_value parameter to
    accidentally pass instead."""
    pol = policy or load_policy()
    commission_total = pol["internal_cost_basis"]["commission"]["combined_pct"]
    return round(cash_collected_aed * commission_total, 2)


def enhancement_net_aed_hr(catalogue=None, policy=None):
    """Enhancement rate net of commission -- 550 * (1 - commission_total).
    Computed, not the catalogue's stored net_after_commission_aed_hr
    (that field is documentation; this function is the checked source)."""
    cat = catalogue or load_template_catalogue()
    pol = policy or load_policy()
    commission_total = pol["internal_cost_basis"]["commission"]["combined_pct"]
    return round(cat["enhancement"]["rate_aed_hr"] * (1 - commission_total), 2)


if __name__ == "__main__":
    print("This module is imported by validate.py and test_pricing_engine.py.")
    print("Run 'python 05-ops/test_pricing_engine.py' to exercise it directly.")
    inv = load_inventory()
    for n in (1, 5, 20, 40, 51, 75, 150, 400):
        r = b_hours_pert(n, inv)
        print(f"N={n:>4}  B_hours O/M/P/mean = {r['o']:.2f}/{r['m']:.2f}/{r['p']:.2f}/{r['mean']:.2f}")
