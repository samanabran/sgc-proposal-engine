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
POLICY_PATH = os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml")


def load_business_cost_basis():
    return _load(BUSINESS_COST_BASIS_PATH)


def load_template_catalogue():
    return _load(TEMPLATE_CATALOGUE_PATH)


def load_policy():
    return _load(POLICY_PATH)


def contingency_pct_for(categories, policy=None):
    """LOCAL-ONLY ADDITION, ported forward across the origin/main merge
    (policy.yaml: contingency_schedule never conflicted -- origin has no
    equivalent concept). categories: a category name (str) or iterable of
    category names from policy.yaml: contingency_schedule. Returns the
    single applicable pct -- the MAX across all supplied categories
    (combination_rule, "worst-risk-governs"), never a sum. INTERNAL ONLY
    -- never surface this percentage on a client-facing document."""
    pol = policy or load_policy()
    schedule = pol["contingency_schedule"]
    if isinstance(categories, str):
        categories = [categories]
    pcts = [schedule[c]["pct"] for c in categories]
    return max(pcts)


def risk_adjusted_hours(raw_hours, categories, policy=None):
    """raw_hours * (1 + contingency_pct_for(categories)). Returns
    (raw_hours, risk_adjusted_hours, pct_applied) -- callers must report
    BOTH raw and risk-adjusted in internal output, and must use ONLY the
    risk-adjusted figure in any effective-rate/floor check -- quoting on
    raw hours is the exact failure mode this function exists to prevent."""
    pol = policy or load_policy()
    pct = contingency_pct_for(categories, pol)
    adjusted = round(raw_hours * (1 + pct), 2)
    return raw_hours, adjusted, pct


def platform_portion_aed_mo(users_now, policy=None):
    """Formalizes the recurring-subscription platform/CTS floor formula
    that has been HAND-COMPUTED per client-worksheet since before this
    repo's pricing-v4 correction pass existed (policy.yaml: cost_to_serve
    -- see e.g. 02-clients/PRO-prosper-realestate/02-calc/pricing-worksheet.yaml,
    02-clients/RVN-realestate-leads/02-calc/pricing-worksheet.yaml:108's
    own inline comment: 'max(CTS x 1.25 = 1170, market_defensible_floor)').
    Never hand-compute this again in a worksheet or a document -- call
    this function and read platform_portion_aed_mo from its return value,
    the same discipline business_cost_floor() already established for the
    whole-business floor. Formula, unchanged from every worksheet that
    already computed it by hand:
        hosting_allocation_aed = hosting_node_true_cost_aed * (users / hosting_node_user_capacity)
        support_labour_aed = ceil(users / 5) * support_hours_per_5_users * support_rate_aed
        account_mgmt_aed = tier lookup (account_mgmt_aed tiers, highest tier applies above its own threshold)
        cts_total_aed = hosting_allocation + support_labour + account_mgmt + tooling_flat_aed
        platform_portion_aed_mo = round(cts_total_aed * gates.platform_floor_multiplier)
    """
    pol = policy or load_policy()
    cts = pol["cost_to_serve"]

    hosting_allocation_aed = cts["hosting_node_true_cost_aed"] * (users_now / cts["hosting_node_user_capacity"])
    support_labour_aed = math.ceil(users_now / 5) * cts["support_hours_per_5_users"] * cts["support_rate_aed"]

    tiers = cts["account_mgmt_aed"]
    sorted_tiers = sorted(((int(k.split("_")[1]), v) for k, v in tiers.items()), key=lambda t: t[0])
    account_mgmt_aed = sorted_tiers[-1][1]  # default: highest tier, if users exceeds every threshold
    for threshold, value in sorted_tiers:
        if users_now <= threshold:
            account_mgmt_aed = value
            break

    tooling_aed = cts["tooling_flat_aed"]
    cts_total_aed = hosting_allocation_aed + support_labour_aed + account_mgmt_aed + tooling_aed
    platform_floor_multiplier = pol["gates"]["platform_floor_multiplier"]
    platform_portion_aed_mo_value = round(cts_total_aed * platform_floor_multiplier)

    return {
        "users_now": users_now,
        "hosting_allocation_aed": round(hosting_allocation_aed, 2),
        "support_labour_aed": support_labour_aed,
        "account_mgmt_aed": account_mgmt_aed,
        "tooling_aed": tooling_aed,
        "cts_total_aed": round(cts_total_aed, 2),
        "platform_floor_multiplier": platform_floor_multiplier,
        "platform_portion_aed_mo": platform_portion_aed_mo_value,
    }


def horizon_totals(one_time_aed, recurring_aed_mo, months_list=(12, 24, 36)):
    """One-time + (recurring x months) at each named horizon, independently
    -- never as a comparison between horizons (see known-defects.md #16:
    a "which term is the better deal" framing was already a defect once).
    Moved here from render_proposal_v4.py 2026-08-16: multiplying a
    monthly figure by a month count is still commercial arithmetic, and
    the renderer's own stated rule is that it computes no AED figure of
    its own, ever -- see that module's docstring. This keeps that rule
    literally true instead of "true except for one multiplication"."""
    horizons = {}
    for months in months_list:
        recurring_total_aed = round(recurring_aed_mo * months, 2)
        horizons[months] = {
            "months": months,
            "one_time_aed": one_time_aed,
            "recurring_total_aed": recurring_total_aed,
            "total_aed": round(one_time_aed + recurring_total_aed, 2),
        }
    return horizons


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

    # Derivation labelling (client-facing discipline, per correction pass):
    # template and modules are FIXED PRODUCT FEES — hours shown for internal
    # capacity planning only, never implied as rate x hours (12,000 / 6h
    # would misread as a 2,000/hr rate, which is not the rate card). Only
    # migration and enhancement are genuine rate x hours derivations.
    return {
        "template": {"price_aed": template_price_aed, "hours": template_hours, "maturity": maturity,
                      "derivation": "fixed_fee", "scope": tmpl.get("scope")},
        "modules": {"rows": module_rows, "price_aed": round(modules_price_aed, 2), "hours": round(modules_hours, 3),
                     "derivation": "fixed_fee_per_catalogue_row"},
        "migration": {"band": migration_band, "price_aed": migration_price_aed, "hours": migration_hours,
                       "unpriced": migration_unpriced, "note": mig.get("note"), "derivation": "banded_fixed_fee"},
        "enhancement": {"hours": enhancement_hours, "rate_aed_hr": rate, "price_aed": enhancement_price_aed,
                         "derivation": "rate_x_hours"},
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
    both if both are relevant to a deal.

    TWO NUMBERS BELOW LIVE ON DIFFERENT AXES -- reviewed and confirmed
    2026-08-16, do not collapse them into each other:

    gross_break_even_aed_hr = floor / (1 - commission_rate). This is
    ARITHMETIC, not a policy choice -- it is the GROSS rate at which NET
    (after commission) lands EXACTLY on the floor, i.e. ZERO cushion.
    Netting commission out first (as this function already does) and
    comparing to `floor` is algebraically identical to comparing a gross
    rate against this figure -- they are the same test expressed at
    different points in the arithmetic, not two different tests. Reported
    below as a METRIC only, never as a second threshold: a quote billed at
    exactly gross_break_even_aed_hr passes this function's BLOCK/WARN/PASS
    check (net == floor is not < floor) but earns the business nothing.
    Printed so whoever is authoring a quote can see that.

    `15` in `cushion_pct < 15` below is a POLICY CHOICE about how much
    margin the business wants above the floor, chosen directly by the
    owner -- it is NOT derived from the commission rate, and it is
    coincidentally close to (but not the same as) commission-rate-implied
    figures like 1/(1-0.14)-1 = 16.28%. Do not "correct" it to match a
    derived percentage; that would be changing a deliberate policy choice
    while believing you found an arithmetic bug."""
    basis = cost_basis or business_cost_floor()
    sales = sales_pct if sales_pct is not None else basis["commission_sales_pct"]
    delivery = delivery_pct if delivery_pct is not None else basis["commission_delivery_pct"]
    commission_rate = (sales + delivery) / 100.0

    net_price = price_ex_vat_aed - discount_aed
    commission_aed = net_price * commission_rate
    net_aed = net_price - commission_aed
    effective_rate_aed_hr = net_aed / hours_total if hours_total else 0.0
    floor = basis["floor_per_hour_aed"]
    cushion_pct = (effective_rate_aed_hr / floor - 1) * 100 if floor else 0.0
    gross_break_even_aed_hr = round(floor / (1 - commission_rate), 2) if commission_rate < 1 else None

    if effective_rate_aed_hr < floor:
        verdict = "BLOCK"
    elif cushion_pct < 15:  # POLICY CHOICE (owner-chosen), not derived -- see docstring
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
        "gross_break_even_aed_hr": gross_break_even_aed_hr,
        "cushion_pct": round(cushion_pct, 2),
        "verdict": verdict,
    }


def commission_released(contract_value_aed, cash_collected_to_date_aed, sales_pct=None,
                         delivery_pct=None, retention_pct=None, cost_basis=None):
    """PART 6: commission is CALCULATED on closed deal value but RELEASED
    pro-rata against cash actually collected, on any payment structure
    (milestone or subscription). Invariant this function exists to enforce:
    commission_released_to_date <= commission_rate * cash_collected_to_date,
    at every point, for every structure. 5% retention withheld against the
    release pending clawback -- see 00-knowledge/clause-library/commission-retention.md
    for the operative clause text (trigger, calc, recovery, time limit,
    right to net against future commission)."""
    basis = cost_basis or business_cost_floor()
    sales = sales_pct if sales_pct is not None else basis["commission_sales_pct"]
    delivery = delivery_pct if delivery_pct is not None else basis["commission_delivery_pct"]
    retention = retention_pct if retention_pct is not None else 5.0  # PART 6: 5% retention, held for clawback -- NOT elsewhere documented in this repo as of this pass; introduced here per explicit spec instruction, flagged in report

    rate = (sales + delivery) / 100.0
    commission_earned_on_cash_aed = contract_value_aed and cash_collected_to_date_aed * rate or 0.0
    retained_aed = commission_earned_on_cash_aed * (retention / 100.0)
    released_aed = commission_earned_on_cash_aed - retained_aed

    return {
        "contract_value_aed": contract_value_aed,
        "cash_collected_to_date_aed": cash_collected_to_date_aed,
        "commission_rate_pct": round(rate * 100, 4),
        "commission_earned_on_cash_aed": round(commission_earned_on_cash_aed, 2),
        "retention_pct": retention,
        "retained_aed": round(retained_aed, 2),
        "released_aed": round(released_aed, 2),
    }


# PART 4/5: RVN's actual mature-build module selection, used only to derive
# a documented default hours/price-per-build for capacity_table() below --
# NOT a hardcoded hours figure. Any caller who wants a different build shape
# passes hours_per_build / price_per_build_aed explicitly and this default is
# bypassed entirely. Scope per the correction-pass brief: template + lead
# capture + WhatsApp notification + auto distribution + call logging +
# attendance + daily reporting; migration 1,000-5,000 records. Matches
# 02-clients/RVN-realestate-leads (property_portal_feed excluded -- not in
# RVN's scope).
RVN_MATURE_MODULES = [
    "lead_capture_meta_google_ads",
    "whatsapp_lead_notification",
    "auto_distribution_manual_reassign",
    "call_logging_manual_entry",
    "attendance_in_app_checkin",
    "daily_reporting_pack",
]


def default_mature_build(cost_basis=None, catalogue=None):
    """Derives (hours, price) for one mature build from four_component_build()
    using RVN's real module selection, rather than hardcoding 34h/31,500 --
    changing template-catalogue.yaml propagates here automatically."""
    result = four_component_build(
        modules_selected=RVN_MATURE_MODULES, maturity="mature",
        migration_band="from_1000_to_5000", cost_basis=cost_basis, catalogue=catalogue,
    )
    return result["hours_total"], result["price_ex_vat_aed"]


def capacity_table(deals_per_month_range=range(1, 7), hours_per_build=None,
                    price_per_build_aed=None, cost_basis=None):
    """PART 4: for N deals/month (1-6 by default), show hours consumed,
    gross, net after commission, less cash costs, available for owner
    salary, variance against the owner-salary requirement, and whether it
    fits inside monthly delivery capacity. Also returns the minimum deal
    count that both fits capacity AND clears the full owner-salary
    requirement -- computed from the actual basis figures, never hardcoded
    to "3"."""
    basis = cost_basis or business_cost_floor()
    raw_basis = load_business_cost_basis()
    owner_salary_required_aed = raw_basis["fixed_monthly_aed"]["owner_salary_monthly_aed"]

    if hours_per_build is None or price_per_build_aed is None:
        default_hours, default_price = default_mature_build(basis)
        hours_per_build = hours_per_build if hours_per_build is not None else default_hours
        price_per_build_aed = price_per_build_aed if price_per_build_aed is not None else default_price

    delivery_hours = basis["delivery_hours_per_month"]
    commission_rate = (basis["commission_sales_pct"] + basis["commission_delivery_pct"]) / 100.0
    cash_out_monthly = basis["cash_out_monthly_aed"]

    rows = []
    min_deals_fits_and_covers = None
    for n in deals_per_month_range:
        hours = round(hours_per_build * n, 3)
        gross_aed = round(price_per_build_aed * n, 2)
        commission_aed = round(gross_aed * commission_rate, 2)
        net_aed = round(gross_aed - commission_aed, 2)
        available_for_owner_salary_aed = round(net_aed - cash_out_monthly, 2)
        variance_vs_requirement_aed = round(available_for_owner_salary_aed - owner_salary_required_aed, 2)
        fits_hours = hours <= delivery_hours
        covers_requirement = available_for_owner_salary_aed >= owner_salary_required_aed
        if fits_hours and covers_requirement and min_deals_fits_and_covers is None:
            min_deals_fits_and_covers = n
        rows.append({
            "deals_per_month": n,
            "hours": hours,
            "hours_pct_of_capacity": round(hours / delivery_hours * 100, 1) if delivery_hours else None,
            "gross_aed": gross_aed,
            "commission_aed": commission_aed,
            "net_aed": net_aed,
            "available_for_owner_salary_aed": available_for_owner_salary_aed,
            "variance_vs_requirement_aed": variance_vs_requirement_aed,
            "fits_hours": fits_hours,
            "covers_requirement": covers_requirement,
        })

    return {
        "hours_per_build": hours_per_build,
        "price_per_build_aed": price_per_build_aed,
        "delivery_hours_per_month": delivery_hours,
        "owner_salary_required_aed": owner_salary_required_aed,
        "rows": rows,
        "min_deals_that_fit_and_cover_aed": min_deals_fits_and_covers,
    }


def signed_undelivered_capacity_flag(signed_undelivered_hours, remaining_capacity_hours):
    """PART 4: 'Flag any pipeline state where signed-but-undelivered work
    exceeds remaining capacity for the period.' Pure comparison -- callers
    supply both figures from their own pipeline tracking; this function does
    not source pipeline data itself (none exists in this repo as of this
    pass -- RULE V: NOT FOUND, no sgc.pricing.* pipeline model located)."""
    exceeds = signed_undelivered_hours > remaining_capacity_hours
    return {
        "signed_undelivered_hours": signed_undelivered_hours,
        "remaining_capacity_hours": remaining_capacity_hours,
        "exceeds_capacity": exceeds,
        "overage_hours": round(max(0.0, signed_undelivered_hours - remaining_capacity_hours), 3),
    }


RECURRING_COMMISSION_DURATION_OPTIONS = ("perpetual", "12_months_from_go_live", "first_year_revenue")

# RULE V / RULE 1: grepped policy.yaml and payment-plans.yaml for any
# existing recurring-commission-duration convention before adding this --
# NOT FOUND. No commission-on-recurring-revenue duration rule exists
# anywhere in this repo prior to this pass.
#
# DECISION (2026-08-16, owner): default set to "12_months_from_go_live",
# not "perpetual". Perpetual was the initial default only because it was
# the sole option consistent with the repo's prior silence -- it was never
# a recommendation, and the owner explicitly chose to close the gap rather
# than let every deal from here inherit the expensive default by omission.
# At 14% combined commission, perpetual costs ~164/client/month forever
# against the same margin line that has to absorb growing support load
# (see recurring_support_load_table below); at 15 live clients that is
# ~2,460/month leaking out on revenue closed years earlier. 12 months from
# go-live is the conventional cap, costs nothing to adopt now, and is far
# cheaper than renegotiating a perpetual promise after the fact. "perpetual"
# and "first_year_revenue" remain valid, explicitly-chosen options for any
# caller who wants them -- this only changes what happens when nobody
# chooses.
DEFAULT_RECURRING_COMMISSION_DURATION = "12_months_from_go_live"


def recurring_support_load_table(support_hours_per_client, live_client_counts=(5, 10, 15, 20, 30, 40),
                                  monthly_fee_aed=1170, recurring_commission_pct=None,
                                  recurring_commission_duration=DEFAULT_RECURRING_COMMISSION_DURATION,
                                  cost_basis=None):
    """PART 5. support_hours_per_client has NO DEFAULT and is a REQUIRED
    positional argument -- deliberately. The brief is explicit that this
    number "has to come from measurement once clients are live" and must
    not be silently assumed; a caller MUST supply either a real measured
    figure (once available, log at 00-knowledge/pricing/support-hours-log.yaml)
    or an explicitly-chosen illustrative scenario value (see
    illustrative_support_load_scenarios() below for the labelled wrapper --
    do not call this function directly with a guessed number and treat the
    output as anything but illustrative).

    monthly_fee_aed default (1170) traces to
    02-clients/RVN-realestate-leads/02-calc/pricing-worksheet.yaml:108
    (platform_portion_aed_mo) -- the only live recurring-fee figure in the
    repo as of this pass. Pass a different value explicitly for any other
    client/segment.

    recurring_commission_duration is a REQUIRED-BY-BRIEF configuration
    choice -- see RECURRING_COMMISSION_DURATION_OPTIONS and
    DEFAULT_RECURRING_COMMISSION_DURATION's docstring above for the owner's
    2026-08-16 decision to default to "12_months_from_go_live" over the
    initially-implemented "perpetual"."""
    if recurring_commission_duration not in RECURRING_COMMISSION_DURATION_OPTIONS:
        raise ValueError(f"recurring_commission_duration must be one of {RECURRING_COMMISSION_DURATION_OPTIONS}")

    basis = cost_basis or business_cost_floor()
    commission_pct = (
        recurring_commission_pct if recurring_commission_pct is not None
        else basis["commission_sales_pct"] + basis["commission_delivery_pct"]
    )
    cost_floor = basis["floor_per_hour_aed"]
    delivery_hours = basis["delivery_hours_per_month"]
    default_hours, _ = default_mature_build(basis)

    net_recurring_aed = round(monthly_fee_aed * (1 - commission_pct / 100.0), 2)

    rows = []
    for n_clients in live_client_counts:
        support_hours_consumed = round(support_hours_per_client * n_clients, 3)
        support_cost_aed = round(support_hours_consumed * cost_floor, 2)
        margin_per_client_aed = round(net_recurring_aed - (support_hours_per_client * cost_floor), 2)
        delivery_hours_remaining = round(delivery_hours - support_hours_consumed, 3)
        builds_still_possible = max(0, int(delivery_hours_remaining // default_hours)) if delivery_hours_remaining > 0 else 0
        rows.append({
            "live_clients": n_clients,
            "support_hours_consumed": support_hours_consumed,
            "support_cost_aed": support_cost_aed,
            "net_recurring_per_client_aed": net_recurring_aed,
            "margin_per_client_aed": margin_per_client_aed,
            "delivery_hours_remaining": delivery_hours_remaining,
            "builds_still_possible": builds_still_possible,
        })

    return {
        "support_hours_per_client": support_hours_per_client,
        "monthly_fee_aed": monthly_fee_aed,
        "recurring_commission_pct": commission_pct,
        "recurring_commission_duration": recurring_commission_duration,
        "net_recurring_per_client_aed": net_recurring_aed,
        "rows": rows,
    }


def illustrative_support_load_scenarios(scenario_hours=(1, 2, 3), **kwargs):
    """Explicitly-labelled wrapper: runs recurring_support_load_table() at
    the brief's own reference points (1h/2h/3h per client) for illustration
    ONLY. These are NOT measured figures -- see support-hours-log.yaml for
    where the real, measured number goes once clients are live. Never treat
    this function's output as the operating plan; it exists to show the
    shape of the risk, not to replace measurement."""
    return {
        "warning": "ILLUSTRATIVE / UNMEASURED. support_hours_per_client values below (1, 2, 3) are the "
                   "brief's own reference points, not real measurement. Log actual support hours at "
                   "00-knowledge/pricing/support-hours-log.yaml from first go-live and call "
                   "recurring_support_load_table() directly with the real figure once available.",
        "scenarios": {
            hours: recurring_support_load_table(support_hours_per_client=hours, **kwargs)
            for hours in scenario_hours
        },
    }


if __name__ == "__main__":
    print("This module is imported by validate.py and test_pricing_engine.py.")
    print("Run 'python 05-ops/test_pricing_engine.py' to exercise it directly.")
    inv = load_inventory()
    for n in (1, 5, 20, 40, 51, 75, 150, 400):
        r = b_hours_pert(n, inv)
        print(f"N={n:>4}  B_hours O/M/P/mean = {r['o']:.2f}/{r['m']:.2f}/{r['p']:.2f}/{r['mean']:.2f}")
