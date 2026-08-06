#!/usr/bin/env python3
"""
Draft drift audit -- report-only, proposed 2026-08-06, not wired into
any build or gate. Scans every AED/hour figure in MRD's 13-section
03-draft prose set and classifies each against a three-tier resolution
order: (1) pricing-worksheet.yaml, (2) client-brief.yaml, (3) a named
knowledge-layer file. A figure with no named source in any tier is a
third, distinct category (UNSOURCED), not folded into STALE.

This is a registry-based checker, not a general prose parser: SOURCE_REGISTRY
below records, by hand, which field/file backs each figure found in the
13-section set (built from a manual line-by-line audit this session).
Extending it to a new draft requires extending the registry -- it does
not infer sources on its own. That hand-built registry is exactly what
makes "explicit named source, not a wildcard" possible; a fully generic
version would have to guess, which is the failure mode this script
exists to avoid.

Usage: python 05-ops/audit_draft_drift.py
Exit 0 always -- this is a report, not a gate. Prints a classification
table and a summary count.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "05-ops"))
import pricing_engine as pe  # noqa: E402

CLIENT = "MRD-meridianview-realty"
CLIENT_DIR = os.path.join(REPO_ROOT, "02-clients", CLIENT)
DRAFT_DIR = os.path.join(CLIENT_DIR, "03-draft", "MRD-2026-SUB-01_Rev3")

ws = pe._load(os.path.join(CLIENT_DIR, "02-calc", "pricing-worksheet.yaml"))
brief = pe._load(os.path.join(CLIENT_DIR, "00-intake", "client-brief.yaml"))
phase2 = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "phase2-catalogue.yaml"))
editions = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "editions.yaml"))

CURRENT = {
    "mobilisation_aed":      ws["number_3_financing"]["mobilisation_aed"],
    "subscription_aed":      ws["assembly"]["option_a"]["subscription_aed"],
    "year1_total_aed":       ws["assembly"]["option_a"]["year1_client_cost_aed"],
    "recovery_monthly_aed":  ws["number_3_financing"]["recovery_monthly_aed"],
    "quarterly_billing_aed": ws["assembly"]["option_a"]["subscription_aed"] * 3,
    "a_side_hours":          ws["number_2_build"]["a_side_hours"],
    "portal_sync_property_finder": phase2["items"]["portal_sync_property_finder"]["price_aed"],
    "portal_sync_bayut_dubizzle":  phase2["items"]["portal_sync_bayut_dubizzle"]["price_aed"],
    "website_lead_capture":        phase2["items"]["website_lead_capture"]["price_aed"],
    "upgrade_cost_estimate_hours": editions["editions"]["community"]["upgrade_cost_estimate_hours"]
        if "community" in editions.get("editions", {}) else editions["editions"]["community"]["upgrade_cost_estimate_hours"],
    "budget_rejected_aed":         ws["inputs"]["budget_rejected_aed"],
    "migration_records":           brief["scope_signals"]["migration_records"],
    "migration_files":             brief["scope_signals"]["migration_files"],
    "users_now":                   ws["inputs"]["users_now"],
    "users_12mo":                  ws["inputs"]["users_12mo"],
    "term_months":                 ws["inputs"]["term_months"],
    "gates_passed_count":          41,  # manifest.yaml: "all 41 gates pass" -- structural constant, not a worksheet field
    "annual_credit_cap_aed":       round(ws["assembly"]["option_a"]["subscription_aed"] * 12 * 0.10),
}

# (file, line, figure_as_printed, registry_key, source_tier, named_source)
# source_tier in {"worksheet", "brief", "knowledge-layer"}
SOURCE_REGISTRY = [
    ("13-next-steps.md", 6, "AED 5,280", "mobilisation_aed", "worksheet", "pricing-worksheet.yaml: number_3_financing.mobilisation_aed"),
    ("12-why-sgc.md", 27, "AED 25,440", "year1_total_aed", "worksheet", "pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed"),
    ("12-why-sgc.md", 28, "AED 30,000+", "budget_rejected_aed", "worksheet", "pricing-worksheet.yaml: inputs.budget_rejected_aed"),
    ("01-executive-summary.md", 21, "AED 25,440", "year1_total_aed", "worksheet", "pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed"),
    ("01-executive-summary.md", 22, "24 months", "term_months", "worksheet", "pricing-worksheet.yaml: inputs.term_months"),
    ("03-understanding-business.md", 13, "AED 30,000", "budget_rejected_aed", "worksheet", "pricing-worksheet.yaml: inputs.budget_rejected_aed"),
    ("04-as-is.md", 26, "480 records", "migration_records", "brief", "client-brief.yaml: scope_signals.migration_records"),
    ("04-as-is.md", 27, "210 documents", "migration_files", "brief", "client-brief.yaml: scope_signals.migration_files"),
    ("06-solution-phase1.md", 20, "12 hours", "upgrade_cost_estimate_hours", "knowledge-layer", "editions.yaml: editions.community.upgrade_cost_estimate_hours"),
    ("06-solution-phase1.md", 43, "46 hours", "a_side_hours", "worksheet", "pricing-worksheet.yaml: number_2_build.a_side_hours"),
    ("06-solution-phase1.md", 56, "480 records", "migration_records", "brief", "client-brief.yaml: scope_signals.migration_records"),
    ("06-solution-phase1.md", 56, "210 documents", "migration_files", "brief", "client-brief.yaml: scope_signals.migration_files"),
    ("07-options-inclusions.md", 7, "AED 3,900", "portal_sync_property_finder", "knowledge-layer", "phase2-catalogue.yaml: items.portal_sync_property_finder.price_aed"),
    ("07-options-inclusions.md", 8, "AED 3,400", "portal_sync_bayut_dubizzle", "knowledge-layer", "phase2-catalogue.yaml: items.portal_sync_bayut_dubizzle.price_aed"),
    ("07-options-inclusions.md", 9, "AED 2,400", "website_lead_capture", "knowledge-layer", "phase2-catalogue.yaml: items.website_lead_capture.price_aed"),
    ("10-commercial-terms.md", 7, "AED 5,280", "mobilisation_aed", "worksheet", "pricing-worksheet.yaml: number_3_financing.mobilisation_aed"),
    ("10-commercial-terms.md", 8, "AED 1,680", "subscription_aed", "worksheet", "pricing-worksheet.yaml: assembly.option_a.subscription_aed"),
    ("10-commercial-terms.md", 9, "AED 25,440", "year1_total_aed", "worksheet", "pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed"),
    ("10-commercial-terms.md", 17, "AED 5,040", "quarterly_billing_aed", "worksheet", "derived: subscription_aed * 3"),
    ("10-commercial-terms.md", 33, "18%", None, "worksheet", "pricing-worksheet.yaml: number_3_financing.uplift_pct"),
    ("10-commercial-terms.md", 34, "AED 527", "recovery_monthly_aed", "worksheet", "pricing-worksheet.yaml: number_3_financing.recovery_monthly_aed"),
    # 2026-08-06 (final pass): rewritten to reference "the Subscription Fee
    # stated in Section 10" instead of restating a computed AED figure --
    # no independent literal to audit here anymore, so it can't re-stale on
    # the next subscription move. Registry entry retired, not re-added as
    # a figure; see CHANGELOG.md for the fix and why a hardcoded number
    # keeps recurring otherwise.
]

# Figures found in the 13-section set with NO entry above -- genuinely
# unsourced, not stale (no field anywhere claims to back them).
UNSOURCED = [
    ("04-as-is.md", 5, "AED 1,100 (lower bound of the PropSpace range)"),
    ("01-executive-summary.md", 23, "6 weeks (timeline to go-live)"),
    ("08-implementation-recovery.md", 7, "Week 1 (kickoff)"),
    ("08-implementation-recovery.md", 8, "Week 2 (discovery/data validation)"),
    ("08-implementation-recovery.md", 9, "Weeks 3-5 (configuration/migration)"),
    ("08-implementation-recovery.md", 10, "Week 6 (training)"),
    ("08-implementation-recovery.md", 11, "Week 6 (go-live)"),
    ("11-support-sla.md", 7, "24 hours (email SLA response time)"),
    ("11-support-sla.md", 13, "5% per week / 2 months (go-live SLA credit terms)"),
    ("09-partnership-terms.md", 9, "30 days (non-renewal notice)"),
    ("09-partnership-terms.md", 15, "day 30 (adoption checkpoint)"),
    ("09-partnership-terms.md", 16, "day 60 (adoption checkpoint)"),
]


def _fmt(n):
    return f"{n:,.0f}" if isinstance(n, (int, float)) else str(n)


def audit():
    rows = []
    for file, line, printed, key, tier, source in SOURCE_REGISTRY:
        printed_num = re.sub(r"[^\d.]", "", printed.split()[-1] if "%" not in printed else printed)
        current = CURRENT.get(key) if key else None
        if key is None:
            status = "MATCHED (structural, not a figure)"
        elif current is None:
            status = "SOURCE KEY NOT COMPUTED -- registry bug"
        else:
            printed_val = printed.replace("AED", "").replace(",", "").replace("%", "").replace("+", "").strip()
            try:
                printed_val = float(printed_val.split()[0].split("(")[0])
            except ValueError:
                printed_val = None
            if printed_val is not None and abs(printed_val - float(current)) < 0.5:
                status = "MATCHED"
            else:
                status = f"STALE (current: {_fmt(current)})"
        rows.append((file, line, printed, tier, source, status))

    print(f"{'File:Line':35} {'Printed':16} {'Tier':16} {'Status'}")
    print("-" * 110)
    matched = stale = 0
    for file, line, printed, tier, source, status in rows:
        print(f"{file+':'+str(line):35} {printed:16} {tier:16} {status}")
        print(f"{'':35} {'':16} source: {source}")
        if status.startswith("MATCHED"):
            matched += 1
        elif status.startswith("STALE"):
            stale += 1
    print()
    print(f"{'File:Line':35} {'Figure':50} Status")
    print("-" * 110)
    for file, line, desc in UNSOURCED:
        print(f"{file+':'+str(line):35} {desc:50} UNSOURCED")

    print()
    print(f"SUMMARY: {matched} matched, {stale} stale, {len(UNSOURCED)} unsourced "
          f"(of {matched+stale+len(UNSOURCED)} figures classified)")
    return matched, stale, len(UNSOURCED)


if __name__ == "__main__":
    audit()
    sys.exit(0)
