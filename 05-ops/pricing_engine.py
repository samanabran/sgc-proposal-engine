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


def class_d_hours_or_cost(edition):
    """Class D structural guarantee: zero for Community by construction."""
    if edition == "community":
        return 0
    raise NotImplementedError(
        "Enterprise Class D pricing not modeled in this engine yet — see "
        "editions.yaml:36 / saas-modules.yaml for the per-user licence "
        "figures; no corpus client currently uses Enterprise."
    )


if __name__ == "__main__":
    print("This module is imported by validate.py and test_pricing_engine.py.")
    print("Run 'python 05-ops/test_pricing_engine.py' to exercise it directly.")
    inv = load_inventory()
    for n in (1, 5, 20, 40, 51, 75, 150, 400):
        r = b_hours_pert(n, inv)
        print(f"N={n:>4}  B_hours O/M/P/mean = {r['o']:.2f}/{r['m']:.2f}/{r['p']:.2f}/{r['mean']:.2f}")
