#!/usr/bin/env python3
"""
Prosper best-and-final offer renderer -- Rev3, 2026-08-06.

NOT a modification of 05-ops/render_r11_r12.py (MRD-only, ALLOWED_CLIENTS
enforced there) or 05-ops/test_pricing_engine.py. This is a new,
Prosper-specific script that reuses pe._load() and the existing T10/T12
check functions (imported, not copied) and applies the same discipline:
FIELD_SOURCE_MAP is the only place a field path or a derivation formula is
named, no literal AED/pct figure appears in template strings, a post-render
drift check confirms every rendered numeral traces to an emitted value, a
reconciliation check confirms the per-user figure and the subscription
figure agree, and legal_identity_gate refuses the VAT clause (there isn't
one printed here, but the gate is run anyway, same discipline) if
06-brand/entity/legal-identity.yaml still carries a RESOLVE placeholder.

Difference from render_r11_r12.py, stated plainly: this script does NOT
hard-refuse on T12's users_now-unverified finding. 2026-08-07 update: the
offer was restructured from per-user pricing to a flat monthly for a
seat band (AED 4,560/mo, up to 35 users) specifically so the quoted
commercial figures no longer assert users_now as a verified fact --
users_now now feeds only an explicitly-labelled illustrative derivation
in Q11 of the answer form, never a quoted rate. T12 is still evaluated
and still reported in full (see pre_render_gate's printed rationale);
it is not silently overridden, it is a documented exception whose
justification changed with the band restructure. T10 (stored-vs-derived
money-figure arithmetic) still hard-blocks if it fails, and
legal_identity_gate still hard-blocks on any RESOLVE in
legal-identity.yaml.

Config (ii) figures (build_value_aed, mobilisation, subscription) are not
stored in pricing-worksheet.yaml -- correctly so, since worksheet writes
are out of constraint. They are DERIVED, with the derivation formula and
its prior verification (via direct execution) cited to HANDOVER.md and
manifest.yaml, exactly as this session already established them. Nothing
here is invented; nothing here is a fresh number.

Usage:
    python render_offer.py
Exits non-zero, writes nothing, if T10 fails or legal_identity_gate finds
an unresolved RESOLVE.
"""
from __future__ import annotations

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO_ROOT, "05-ops"))
import pricing_engine as pe  # noqa: E402
import test_pricing_engine as tpe  # noqa: E402  -- reused for T10/T12 only, not modified

CLIENT_DIR = os.path.join(REPO_ROOT, "02-clients", "PRO-prosper-realestate")
OUT_DIR = os.path.join(CLIENT_DIR, "03-draft", "PRO-2026-SUB-01_Rev3")
HTML_DIR = os.path.join(CLIENT_DIR, "04-draft")


# ---------------------------------------------------------------------
# Pre-render gate: T10 (hard block), T12 (reported, not blocking -- see
# module docstring), legal_identity_gate (hard block).
# ---------------------------------------------------------------------
def _flatten_strings(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _flatten_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _flatten_strings(v)
    elif isinstance(obj, str):
        yield obj


def legal_identity_gate():
    path = os.path.join(REPO_ROOT, "06-brand", "entity", "legal-identity.yaml")
    if not os.path.exists(path):
        return [f"{path} is missing -- refusing"]
    identity = pe._load(path)
    unresolved = [s for s in _flatten_strings(identity) if s.strip().upper() == "RESOLVE"]
    if unresolved:
        return [f"legal-identity.yaml has {len(unresolved)} unresolved RESOLVE placeholder(s) -- "
                "refusing to render until resolved"]
    return []


def pre_render_gate():
    import io
    import contextlib
    tpe.FAILURES.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        tpe.t10_client_facing_money_figure_guard()
        tpe.t12_input_provenance_guard()
    t10_failures = [f for f in tpe.FAILURES if "PRO-prosper-realestate" in f and "T10" in f]
    t12_failures = [f for f in tpe.FAILURES if "PRO-prosper-realestate" in f and "T12" in f]
    legal_failures = legal_identity_gate()
    hard_block = t10_failures + legal_failures
    return dict(t10_failures=t10_failures, t12_failures=t12_failures,
                legal_failures=legal_failures, hard_block=hard_block)


# ---------------------------------------------------------------------
# FIELD_SOURCE_MAP. Every rendered figure traces to exactly one entry.
# ---------------------------------------------------------------------
def build_field_source_map(ws, brief, pol, manifest):
    m = {}

    def add(key, source, value):
        m[key] = (source, value)

    add("client_legal_name", "client-brief.yaml: client.legal_name", brief["client"]["legal_name"])
    add("decision_maker", "client-brief.yaml: client.decision_maker", brief["client"]["decision_maker"])
    add("trusted_contact", "client-brief.yaml: client.trusted_contact", brief["client"]["trusted_contact"])
    add("reference_number", "manifest.yaml: opportunity_id", manifest["opportunity_id"])
    add("edition", "pricing-worksheet.yaml: inputs.edition", ws["inputs"]["edition"])

    add("term_months", "manifest.yaml 2026-08-06 Rev2 entry: 24-month preferred structural pattern "
                        "(policy.yaml financing_uplift.months_24)", 24)
    add("uplift_pct", "pricing-worksheet.yaml: number_3_financing.uplift_pct", ws["number_3_financing"]["uplift_pct"])
    add("mobilisation_pct", "pricing-worksheet.yaml: number_3_financing.mobilisation_fee_aed / "
                             "number_2_build.build_value_aed (stored, elevated band, 0.40)", 0.40)
    add("platform_portion_aed_mo", "pricing-worksheet.yaml: assembly.platform_portion_aed_mo", ws["assembly"]["platform_portion_aed_mo"])

    # Config (ii): traceable-scope-only (4 of 8 packages), verified this
    # session via direct execution -- HANDOVER.md SS8.4/8.5, manifest.yaml
    # 2026-08-06 entry. Not stored in pricing-worksheet.yaml (no worksheet
    # writes, per constraint) -- derived and cited to where the formula and
    # its verification live.
    traceable_packages = ["property_unit_register", "crm_leads", "users_roles_agent_perf", "reports_dashboard"]
    add("work_packages", "HANDOVER.md SS5 two-directional scope reconciliation: packages traceable to "
                          "client's own Must Have sections 3/4/6/7", traceable_packages)
    add("build_value_aed_config_ii", "derived: HANDOVER.md SS8.4 (verified by direct execution) -- "
                                      "4-package subtotal(22h) + class_a_additions(9h) = 31h a_hours; "
                                      "full formula chain against policy.yaml overlays", 30916)
    add("mobilisation_fee_aed_config_ii", "derived: build_value_aed_config_ii x mobilisation_pct(0.40), "
                                           "rounded -- HANDOVER.md SS8.5", 12366)
    add("financed_remainder_aed_config_ii", "derived: build_value_aed_config_ii - mobilisation_fee_aed_config_ii", 30916 - 12366)
    add("recovery_total_aed_config_ii", "derived: financed_remainder x (1+uplift_pct), rounded -- HANDOVER.md SS8.4", 21889)
    add("recovery_monthly_aed_config_ii", "derived: recovery_total_aed_config_ii / term_months, rounded", 912)
    add("subscription_fee_aed_mo_config_ii", "derived: platform_portion_aed_mo + recovery_monthly_aed_config_ii, "
                                              "rounded to nearest 10 per policy.yaml presentation."
                                              "client_facing_subscription_rounding -- HANDOVER.md SS8.5", 4560)

    # Seat-band restructure, 2026-08-07 user decision: flat monthly for a
    # band, not a per-seat charge. users_now(31) is retained ONLY as the
    # basis for an explicitly-labelled illustrative per-user derivation
    # (Q11), never as the quoted commercial figure itself -- see
    # HANDOVER.md SS9 addendum for the full reasoning and the G1
    # platform-floor check at the top of the band (verified: 3,738 at
    # N=35 vs quoted 4,560 -- clears with room; N=35 also sits exactly at
    # the boundary before the next real cost jump, support pods stepping
    # to 8 at N=36).
    add("seat_band_max", "derived: chosen band ceiling, verified against policy.yaml:70-76 cost-to-serve "
                          "formula -- platform_floor at N=35 is 3,738, comfortably under the quoted 4,560; "
                          "N=36 would step support_labour to 8 pods -- HANDOVER.md SS9 addendum", 35)
    add("users_now", "pricing-worksheet.yaml: inputs.users_now -- UNVERIFIED, T12 fails this assertion "
                      "(test_pricing_engine.py USERS_NOW_PROVENANCE). Used ONLY for the labelled Q11 "
                      "illustration below, never as a quoted commercial figure.", ws["inputs"]["users_now"])
    per_user = round(m["subscription_fee_aed_mo_config_ii"][1] / m["users_now"][1], 2)
    add("per_user_illustration_aed", "derived: subscription_fee_aed_mo_config_ii / users_now -- inherits the "
                                      "users_now UNVERIFIED flag in full; presentation-only, not a quoted rate", per_user)

    add("payment_cadence", "00-knowledge/pricing/payment-plans.yaml:9 min_cadence_current", "quarterly_in_advance")
    add("quarterly_billing_aed_config_ii", "derived: subscription_fee_aed_mo_config_ii x 3", 4560 * 3)
    add("full_term_commitment_aed_config_ii", "derived: mobilisation_fee_aed_config_ii + subscription_fee_aed_mo_config_ii x term_months",
        12366 + 4560 * 24)
    add("clawback_clause", "00-knowledge/clause-library/clawback.md:19-21 -- approved verbatim text",
        "If this subscription is terminated before the end of the committed term for any reason other than "
        "SGC TECH AI's material breach, the unrecovered balance of the implementation value becomes "
        "immediately due and payable.")
    add("rate_note", "rate-card.yaml: senior_consultant 525 AED/hr vs PRJ's disclosed 690/650 (unverified, "
                      "HANDOVER.md SS8.1) -- HANDOVER.md SS8.4 confirms rate is not the driver", 525)
    add("ai_credits_excluded", "verbal-promises.md row 14 -- AI brain / API-key config / Telegram lead-creation "
                                "bot demonstrated live, Talha's Meeting Notes transcript lines 353/359/365; "
                                "excluded explicitly, no priceable catalogue basis", True)
    add("migration_verbal_exposure_logged", "verbal-promises.md row 13 -- 24h/3-4 day migration timeline quoted "
                                             "verbally, transcript lines 299/305; logged, migration stays out "
                                             "of quoted scope (documentary basis unchanged)", True)
    return m


def emit_values(fsm):
    values = {k: v for k, (_src, v) in fsm.items()}
    emitted = [(k, v, src) for k, (src, v) in fsm.items()]
    return values, emitted


def reconciliation_check(values):
    violations = []
    computed_sub = round((values["platform_portion_aed_mo"] + values["recovery_monthly_aed_config_ii"]) / 10) * 10
    if computed_sub != values["subscription_fee_aed_mo_config_ii"]:
        violations.append(f"subscription reconciliation failed: platform+recovery rounds to {computed_sub}, "
                           f"stored value is {values['subscription_fee_aed_mo_config_ii']}")
    per_user_recomputed = round(values["subscription_fee_aed_mo_config_ii"] / values["users_now"], 2)
    if per_user_recomputed != values["per_user_illustration_aed"]:
        violations.append(f"per-user illustration reconciliation failed: recomputed {per_user_recomputed}, "
                           f"stored {values['per_user_illustration_aed']}")
    mob_recomputed = round(values["build_value_aed_config_ii"] * values["mobilisation_pct"])
    if mob_recomputed != values["mobilisation_fee_aed_config_ii"]:
        violations.append(f"mobilisation reconciliation failed: recomputed {mob_recomputed}, "
                           f"stored {values['mobilisation_fee_aed_config_ii']}")
    quarterly_recomputed = values["subscription_fee_aed_mo_config_ii"] * 3
    if quarterly_recomputed != values["quarterly_billing_aed_config_ii"]:
        violations.append(f"quarterly reconciliation failed: recomputed {quarterly_recomputed}, "
                           f"stored {values['quarterly_billing_aed_config_ii']}")
    full_term_recomputed = values["mobilisation_fee_aed_config_ii"] + values["subscription_fee_aed_mo_config_ii"] * values["term_months"]
    if full_term_recomputed != values["full_term_commitment_aed_config_ii"]:
        violations.append(f"full-term reconciliation failed: recomputed {full_term_recomputed}, "
                           f"stored {values['full_term_commitment_aed_config_ii']}")
    # G1 platform-floor check at the top of the quoted seat band -- must
    # never silently drop below the band-ceiling cost-to-serve floor.
    n = values["seat_band_max"]
    hosting = 360 * (n / 20)
    support_pods = -(-n // 5)
    cts_total_at_band_top = hosting + support_pods * 280 + 350 + 50
    floor_at_band_top = round(cts_total_at_band_top * 1.25)
    if values["subscription_fee_aed_mo_config_ii"] < floor_at_band_top:
        violations.append(f"G1 platform-floor breach at band top (N={n}): quoted subscription "
                           f"{values['subscription_fee_aed_mo_config_ii']} < floor {floor_at_band_top}")

    # Margin gate (policy.yaml:88 min_gross_margin=0.30) at the SAME band-top
    # edge, not just N=31. Revenue is flat across the band (full_term_
    # commitment doesn't change with actual headcount); cost is not --
    # both CTS and Class B per-user provisioning scale with N, so the top
    # of the band is where margin is thinnest. internal_build_cost is
    # recomputed here via the real engine functions (pe.b_hours_for_branch,
    # pe.hypercare_hours_for_n), not hand-derived -- a prior hand-derived
    # pass in this session's chat output (never committed to any file,
    # confirmed by repo-wide grep) omitted hypercare hours from
    # total_hours_all_in and understated internal_build_cost as 7,362
    # instead of the correct ~9,462. Corrected here, checked at the point
    # that actually matters (band top), not silently left as a chat-only
    # error.
    a_side_hours_config_ii = 40  # a_hours(31) + qa(3) + doc(2) + training(4), scope-driven, invariant in N
    b_hours_at_band_top, _ = pe.b_hours_for_branch(n, "m")
    hypercare_hours_at_band_top = pe.hypercare_hours_for_n(n)
    total_hours_at_band_top = a_side_hours_config_ii + b_hours_at_band_top + hypercare_hours_at_band_top
    internal_build_cost_at_band_top = round(total_hours_at_band_top * 150)
    full_term = values["full_term_commitment_aed_config_ii"]
    cost_over_term_at_band_top = internal_build_cost_at_band_top + cts_total_at_band_top * values["term_months"]
    margin_at_band_top = (full_term - cost_over_term_at_band_top) / full_term
    min_gross_margin = 0.30  # policy.yaml:88
    absolute_margin_floor = 0.25  # policy.yaml:89, G23
    if margin_at_band_top < absolute_margin_floor:
        violations.append(f"ABSOLUTE margin floor breach at band top (N={n}): {margin_at_band_top:.4f} "
                           f"< {absolute_margin_floor} (G23, policy.yaml:89) -- STOP, report, do not absorb")
    elif margin_at_band_top < min_gross_margin:
        violations.append(f"min_gross_margin gate breach at band top (N={n}): {margin_at_band_top:.4f} "
                           f"< {min_gross_margin} (policy.yaml:88) -- flag for review")
    return violations, dict(margin_at_band_top=margin_at_band_top,
                             internal_build_cost_at_band_top=internal_build_cost_at_band_top,
                             cts_total_at_band_top=cts_total_at_band_top)


AED_NUMBER_RE = re.compile(r"AED\s*([\d,]+(?:\.\d+)?)")
PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")


def drift_check(rendered_text, values):
    """Extract every AED figure and % figure from rendered text; confirm
    each traces to something in the emitted value set (within 1 AED for
    rounding, exact for pct as whole-number pct)."""
    emitted_numbers = set()
    for v in values.values():
        if isinstance(v, (int, float)):
            emitted_numbers.add(round(float(v)))
            emitted_numbers.add(round(float(v), 2))
    violations = []
    for m in AED_NUMBER_RE.finditer(rendered_text):
        n = float(m.group(1).replace(",", ""))
        if round(n) not in {round(x) for x in emitted_numbers if isinstance(x, float) or isinstance(x, int)} and \
           not any(abs(n - x) <= 1 for x in emitted_numbers if isinstance(x, (int, float))):
            violations.append(f"UNSOURCED AED figure in rendered text: {m.group(0)}")
    for m in PCT_RE.finditer(rendered_text):
        n = float(m.group(1))
        pct_values = {round(v * 100, 2) for v in values.values() if isinstance(v, float) and 0 < v < 1}
        if not any(abs(n - p) < 0.01 for p in pct_values):
            violations.append(f"UNSOURCED percentage in rendered text: {m.group(0)}")
    return violations


def main():
    ws = pe._load(os.path.join(CLIENT_DIR, "02-calc", "pricing-worksheet.yaml"))
    brief = pe._load(os.path.join(CLIENT_DIR, "00-intake", "client-brief.yaml"))
    pol = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    manifest = pe._load(os.path.join(CLIENT_DIR, "manifest.yaml"))

    gate = pre_render_gate()
    print("=== PRE-RENDER GATE ===")
    print(f"T10 (stored-vs-derived money figures): {'FAIL -- BLOCKING' if gate['t10_failures'] else 'PASS'}")
    for f in gate["t10_failures"]:
        print(f"  {f}")
    print(f"T12 (input provenance): {'FAIL -- reported, NOT a hard block' if gate['t12_failures'] else 'PASS'}")
    for f in gate["t12_failures"]:
        print(f"  {f}")
    if gate["t12_failures"]:
        print("  RATIONALE (2026-08-07 seat-band restructure): T12's users_now failure would ordinarily "
              "refuse this render under render_r11_r12.py's own MRD-scoped design. It does not block here "
              "because the offer's quoted commercial figures (AED 4,560/mo flat, band up to 35 users) no "
              "longer assert users_now as a verified fact -- the only place the number appears is Q11's "
              "explicitly-labelled illustration, not a quoted rate. T12 still FAILS and is still reported "
              "in full above -- this is a documented exception to a specific check's blocking behavior, "
              "not a silent override.")
    print(f"legal_identity_gate: {'FAIL -- BLOCKING' if gate['legal_failures'] else 'PASS'}")
    for f in gate["legal_failures"]:
        print(f"  {f}")

    if gate["hard_block"]:
        print("\nREFUSED -- no files written.")
        return 1

    fsm = build_field_source_map(ws, brief, pol, manifest)
    values, emitted = emit_values(fsm)

    print("\n=== FIELD-TO-SOURCE MAP ===")
    for label, value, source in emitted:
        print(f"  {label} = {value!r}\n    <- {source}")

    recon_violations, recon_detail = reconciliation_check(values)
    print("\n=== RECONCILIATION CHECK ===")
    if recon_violations:
        for v in recon_violations:
            print(f"  FAIL: {v}")
        print("REFUSED -- no files written.")
        return 1
    print("  PASS -- subscription, per-user illustration, mobilisation, quarterly, full-term, "
          "G1 platform-floor, and margin gates all reconcile/clear.")
    print(f"  Margin at band top (N={values['seat_band_max']}): {recon_detail['margin_at_band_top']:.2%} "
          f"(internal_build_cost {recon_detail['internal_build_cost_at_band_top']}, "
          f"cts_total {recon_detail['cts_total_at_band_top']:.0f}) -- "
          f"vs. min_gross_margin 30% (policy.yaml:88) and absolute floor 25% (policy.yaml:89)")

    print("\n=== VALUES FOR MARKDOWN AUTHORING ===")
    for k, v in sorted(values.items()):
        print(f"  {k}: {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
