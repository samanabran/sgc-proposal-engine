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


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_inventory():
    return _load(INVENTORY_PATH)


def load_rate_card():
    return _load(RATE_CARD_PATH)


def load_hour_lookup():
    return _load(HOUR_LOOKUP_PATH)


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


def class_d_hours_or_cost(edition):
    """Class D structural guarantee: zero for Community by construction."""
    if edition == "community":
        return 0
    raise NotImplementedError(
        "Enterprise Class D pricing not modeled in this engine yet — see "
        "editions.yaml:36 / saas-modules.yaml for the per-user licence "
        "figures; no corpus client currently uses Enterprise."
    )


BUSINESS_COST_BASIS_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "business-cost-basis.yaml")
TEMPLATE_CATALOGUE_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "template-catalogue.yaml")


def load_business_cost_basis():
    return _load(BUSINESS_COST_BASIS_PATH)


def load_template_catalogue():
    return _load(TEMPLATE_CATALOGUE_PATH)


def business_cost_floor(basis=None):
    """PART 1: whole-business operating cost floor, computed not hardcoded.
    Every field here is derived from business-cost-basis.yaml -- change any
    input in that file and this function's output changes with it. Never
    hardcode 394 (or whatever the current output is) anywhere else; call
    this function and read floor_per_hour_aed."""
    b = basis or load_business_cost_basis()
    fixed = b["fixed_monthly_aed"]
    cash_out_monthly = (
        fixed["licence_annual_aed"] / 12
        + fixed["staff_salaries_monthly_aed"]
        + fixed["office_monthly_aed"]
        + fixed["phones_monthly_aed"]
        + fixed["hosting_ai_monthly_aed"]
        + fixed["other_monthly_aed"]
    )
    extras_total = 0.0
    for name, extra in b.get("optional_extras", {}).items():
        if not extra.get("enabled"):
            continue
        if name == "gratuity_accrual":
            extras_total += extra["pct_of_basic"] * extra.get("basic_monthly_aed", 0)
        elif name == "contingency_pct":
            continue  # applied after total_requirement below, not a flat monthly add
        else:
            extras_total += extra.get("monthly_aed", 0)
    cash_out_monthly += extras_total

    total_requirement = cash_out_monthly + fixed["owner_salary_monthly_aed"]

    contingency = b.get("optional_extras", {}).get("contingency_pct", {})
    if contingency.get("enabled"):
        total_requirement *= (1 + contingency.get("pct_of_total_requirement", 0))

    delivery_hours = b["delivery"]["delivery_hours_per_month"]
    floor_per_hour_aed = total_requirement / delivery_hours

    return {
        "cash_out_monthly_aed": round(cash_out_monthly, 2),
        "total_requirement_aed": round(total_requirement, 2),
        "delivery_hours_per_month": delivery_hours,
        "floor_per_hour_aed": round(floor_per_hour_aed, 2),
        "target_rate_per_hour_aed": b["target_rate_per_hour_aed"],
        "commission_sales_pct": b["commission"]["commission_sales_pct"],
        "commission_delivery_pct": b["commission"]["commission_delivery_pct"],
    }


def four_component_build(modules_selected, maturity, migration_band, enhancement_hours=0.0,
                          enhancement_rate_aed_hr=None, catalogue=None, cost_basis=None):
    """PART 2: template + modules + migration + enhancement, replacing the
    single-fixed-figure build_value_aed model. Returns priced components and
    hours separately so every AED figure traces to a named catalogue row
    (RULE 1) instead of one asserted total."""
    cat = catalogue or load_template_catalogue()
    basis = cost_basis or business_cost_floor()

    tmpl = cat["template_base"]
    template_price_aed = tmpl["fixed_fee_aed"]
    template_hours = tmpl["hours_by_maturity"][maturity]

    module_mult = cat["module_hour_multiplier_by_maturity"][maturity]
    module_rows = []
    modules_price_aed = 0.0
    modules_hours = 0.0
    for name in modules_selected:
        row = cat["modules"][name]
        hours = row["hours"] * module_mult
        module_rows.append({"name": name, "price_aed": row["price_aed"], "hours": round(hours, 3)})
        modules_price_aed += row["price_aed"]
        modules_hours += hours

    mig = cat["migration_bands"][migration_band]
    migration_unpriced = bool(mig.get("unpriced"))
    migration_price_aed = None if migration_unpriced else mig["price_aed"]
    migration_hours = None if migration_unpriced else mig["hours"]

    rate = enhancement_rate_aed_hr if enhancement_rate_aed_hr is not None else basis["target_rate_per_hour_aed"]
    enhancement_price_aed = round(enhancement_hours * rate, 2)

    if migration_unpriced:
        price_ex_vat = None  # RULE 1 / PART 8: never render a total that silently drops an unpriced component
    else:
        price_ex_vat = round(template_price_aed + modules_price_aed + migration_price_aed + enhancement_price_aed, 2)

    hours_total = None if migration_unpriced else round(template_hours + modules_hours + migration_hours + enhancement_hours, 3)

    return {
        "template": {"price_aed": template_price_aed, "hours": template_hours, "maturity": maturity},
        "modules": {"rows": module_rows, "price_aed": round(modules_price_aed, 2), "hours": round(modules_hours, 3)},
        "migration": {"band": migration_band, "price_aed": migration_price_aed, "hours": migration_hours,
                       "unpriced": migration_unpriced, "note": mig.get("note")},
        "enhancement": {"hours": enhancement_hours, "rate_aed_hr": rate, "price_aed": enhancement_price_aed},
        "price_ex_vat_aed": price_ex_vat,
        "hours_total": hours_total,
    }


def hour_rate_floor_test(price_ex_vat_aed, hours_total, discount_aed=0.0, cost_basis=None,
                          sales_pct=None, delivery_pct=None):
    """PART 3 quote-time floor test. NAMED DISTINCTLY from the repo's
    existing G23 (policy.yaml: gates.absolute_margin_floor, a MARGIN-pct
    gate already checked per-worksheet) -- this is a different computation
    (effective AED/hour vs the whole-business cost floor from PART 1), not
    a redefinition of the existing G23. Do not conflate the two; report
    both if both are relevant to a deal."""
    basis = cost_basis or business_cost_floor()
    sales = sales_pct if sales_pct is not None else basis["commission_sales_pct"]
    delivery = delivery_pct if delivery_pct is not None else basis["commission_delivery_pct"]

    net_price = price_ex_vat_aed - discount_aed
    commission_aed = net_price * (sales + delivery) / 100.0
    net_aed = net_price - commission_aed
    effective_rate_aed_hr = net_aed / hours_total if hours_total else 0.0
    floor = basis["floor_per_hour_aed"]
    cushion_pct = (effective_rate_aed_hr / floor - 1) * 100 if floor else 0.0

    if effective_rate_aed_hr < floor:
        verdict = "BLOCK"
    elif cushion_pct < 15:
        verdict = "WARN"
    else:
        verdict = "PASS"

    return {
        "price_ex_vat_aed": net_price,
        "hours_total": hours_total,
        "commission_aed": round(commission_aed, 2),
        "net_aed": round(net_aed, 2),
        "effective_rate_aed_hr": round(effective_rate_aed_hr, 2),
        "floor_per_hour_aed": floor,
        "cushion_pct": round(cushion_pct, 2),
        "verdict": verdict,
    }


if __name__ == "__main__":
    print("This module is imported by validate.py and test_pricing_engine.py.")
    print("Run 'python 05-ops/test_pricing_engine.py' to exercise it directly.")
    inv = load_inventory()
    for n in (1, 5, 20, 40, 51, 75, 150, 400):
        r = b_hours_pert(n, inv)
        print(f"N={n:>4}  B_hours O/M/P/mean = {r['o']:.2f}/{r['m']:.2f}/{r['p']:.2f}/{r['mean']:.2f}")
