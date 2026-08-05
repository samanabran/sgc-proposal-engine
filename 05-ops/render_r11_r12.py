#!/usr/bin/env python3
"""
R11/R12 renderer -- standalone quotation (R11) and one-page commercial
summary (R12), per the spec approved 2026-08-06 (CHANGELOG.md pricing
v3.1 addenda).

Scoped to MRD-meridianview-realty ONLY, per explicit instruction -- the
sole client currently clean on both T10 (stored-vs-derived) and T12
(input-layer provenance). ALLOWED_CLIENTS below is the single point of
enforcement; do not widen it without separate authorization.

Design:
  - Every rendered figure is read from a loaded worksheet/policy dict via
    pricing_engine._load() -- FIELD_SOURCE_MAP is the only place a field
    path is named. No literal AED/hour figure appears in the template
    strings themselves.
  - Pre-render gate: refuses to render for any client that is not clean
    on BOTH T10 and T12 (reuses test_pricing_engine.py's own check
    functions -- no separate, divergent gate logic).
  - Post-render drift check (T11): re-extracts every numeral that looks
    like a rendered AED/hour figure from the output text and confirms it
    traces to a value FIELD_SOURCE_MAP actually emitted. Fails the build,
    writes nothing, on any figure that doesn't trace.
  - Output is Markdown only. No PDF generation, no HTML in this pass.

Usage:
    python render_r11_r12.py <client-dir-name>
Exits non-zero (no files written) if the client is refused or the drift
check fails.
"""
import os
import re
import sys
import io
import contextlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "05-ops"))
import pricing_engine as pe  # noqa: E402
import test_pricing_engine as tpe  # noqa: E402  -- reused for the pre-render gate only

ALLOWED_CLIENTS = ["MRD-meridianview-realty"]


# ---------------------------------------------------------------------
# Pre-render gate: T10 AND T12 clean, reusing the real check functions.
# ---------------------------------------------------------------------
def pre_render_gate(client):
    # Always run the real T10/T12 checks, even for a scope-refused client --
    # so the refusal shows both reasons (explicit scope AND, independently,
    # whether the client would even clear the gate on its own merits).
    tpe.FAILURES.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        tpe.t10_client_facing_money_figure_guard()
        tpe.t12_input_provenance_guard()
    client_failures = [f for f in tpe.FAILURES if client in f]

    reasons = []
    if client not in ALLOWED_CLIENTS:
        reasons.append(f"{client} is not in ALLOWED_CLIENTS -- R11/R12 is scoped to "
                        "MRD-meridianview-realty only per the 2026-08-06 approval; no other "
                        "client may render this pass, independent of the check results below.")
    reasons.extend(client_failures)
    return (len(reasons) == 0), reasons


# ---------------------------------------------------------------------
# Field-to-source map. Every entry is (label, extractor(ws, policy) -> value).
# The render functions below build their content ONLY from calling these
# extractors -- no other numeral may appear in a template.
# ---------------------------------------------------------------------
def _fmt_aed(n):
    return f"{n:,.0f}" if isinstance(n, (int, float)) and float(n).is_integer() else f"{n:,}"


FIELD_SOURCE_MAP = {
    "client_legal_name":      ("client-brief.yaml: client.legal_name", lambda ws, brief, pol: brief["client"]["legal_name"]),
    "decision_maker":         ("client-brief.yaml: client.decision_maker", lambda ws, brief, pol: brief["client"]["decision_maker"]),
    "term_months":            ("pricing-worksheet.yaml: inputs.term_months", lambda ws, brief, pol: ws["inputs"]["term_months"]),
    "edition":                ("pricing-worksheet.yaml: inputs.edition", lambda ws, brief, pol: ws["inputs"]["edition"]),
    "work_packages":          ("pricing-worksheet.yaml: number_2_build.delivery_hours[*].package",
                                lambda ws, brief, pol: [e["package"] for e in ws["number_2_build"]["delivery_hours"]]),
    "build_value_aed":        ("pricing-worksheet.yaml: number_2_build.build_value_aed", lambda ws, brief, pol: ws["number_2_build"]["build_value_aed"]),
    "mobilisation_fee_aed":   ("pricing-worksheet.yaml: number_3_financing.mobilisation_aed", lambda ws, brief, pol: ws["number_3_financing"]["mobilisation_aed"]),
    "financed_remainder_aed": ("pricing-worksheet.yaml: number_3_financing.deferred_aed", lambda ws, brief, pol: ws["number_3_financing"]["deferred_aed"]),
    "uplift_pct":             ("pricing-worksheet.yaml: number_3_financing.uplift_pct", lambda ws, brief, pol: ws["number_3_financing"]["uplift_pct"]),
    "recovery_monthly_aed":   ("pricing-worksheet.yaml: number_3_financing.recovery_monthly_aed", lambda ws, brief, pol: ws["number_3_financing"]["recovery_monthly_aed"]),
    "subscription_fee_aed_mo":("pricing-worksheet.yaml: assembly.option_a.subscription_aed", lambda ws, brief, pol: ws["assembly"]["option_a"]["subscription_aed"]),
    "payment_cadence":        ("pricing-worksheet.yaml: payment_cadence", lambda ws, brief, pol: ws["payment_cadence"]),
    "year1_total_aed":        ("pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed", lambda ws, brief, pol: ws["assembly"]["option_a"]["year1_client_cost_aed"]),
    "vat_registered":         ("policy.yaml: vat.registered", lambda ws, brief, pol: pol["vat"]["registered"]),
    "charge_vat":             ("policy.yaml: vat.charge_vat", lambda ws, brief, pol: pol["vat"]["charge_vat"]),
}

# monthly_billing_deviation withheld per the approved spec until its
# surcharge_pct is cited to a policy field -- deliberately NOT in the map
# above. If a future pass adds it, it must land here with its own
# extractor, never as a bare literal in a template string.
WITHHELD = ["monthly_billing_deviation.surcharge_pct -- uncited to any policy.yaml field, "
            "per the approved R11/R12 spec's withhold rule (CHANGELOG.md pricing v3.1 addenda)"]


def load_context(client):
    client_dir = os.path.join(REPO_ROOT, "02-clients", client)
    ws = pe._load(os.path.join(client_dir, "02-calc", "pricing-worksheet.yaml"))
    brief = pe._load(os.path.join(client_dir, "00-intake", "client-brief.yaml"))
    pol = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    values = {}
    emitted = []  # (label, value, source_path) -- feeds the drift check
    for label, (source_path, extractor) in FIELD_SOURCE_MAP.items():
        v = extractor(ws, brief, pol)
        values[label] = v
        emitted.append((label, v, source_path))
    return values, emitted


# ---------------------------------------------------------------------
# T11 -- post-render drift check. Extracts every AED-shaped numeral from
# the rendered text and confirms it equals one of the values this build
# actually emitted from FIELD_SOURCE_MAP. Anything else is a literal that
# didn't come from a source field, which is exactly the defect class this
# whole build exists to prevent.
# ---------------------------------------------------------------------
def drift_check(rendered_text, emitted):
    emitted_numeric_strings = set()
    for label, v, _src in emitted:
        if isinstance(v, (int, float)):
            emitted_numeric_strings.add(_fmt_aed(v))
            emitted_numeric_strings.add(str(v))
            emitted_numeric_strings.add(str(round(v)))
        elif isinstance(v, list):
            continue

    found_numerals = re.findall(r"AED\s*([\d,]+(?:\.\d+)?)", rendered_text)
    undriftable = []
    for raw in found_numerals:
        if raw not in emitted_numeric_strings:
            undriftable.append(raw)
    return undriftable


def render_r11(client, values):
    packages = "\n".join(f"- {p}" for p in values["work_packages"])
    vat_line = ("SGC TECH AI is not currently registered for UAE VAT, and no VAT is charged on this proposal."
                if values["charge_vat"] is False else
                "VAT is charged at the prevailing rate on this proposal.")
    text = f"""# Standalone Quotation

**Client:** {values['client_legal_name']}
**Attention:** {values['decision_maker']}

## Scope
{packages}

## Term & Edition
- Term: {values['term_months']} months
- Edition: {values['edition']}

## Commercial Terms
- Implementation Value: AED {_fmt_aed(values['build_value_aed'])}
- Mobilisation Fee (due at kickoff): AED {_fmt_aed(values['mobilisation_fee_aed'])}
- Financed Remainder: AED {_fmt_aed(values['financed_remainder_aed'])}
- Financing Uplift: {values['uplift_pct']*100:.0f}%
- Recovery (monthly, over the term): AED {_fmt_aed(values['recovery_monthly_aed'])}
- Subscription Fee: AED {_fmt_aed(values['subscription_fee_aed_mo'])} / month
- Payment Cadence: {values['payment_cadence']}
- Year-1 Total: AED {_fmt_aed(values['year1_total_aed'])}

## VAT
{vat_line}

## Withheld pending resolution
{chr(10).join('- ' + w for w in WITHHELD)}
"""
    return text


def render_r12(client, values):
    packages = ", ".join(values["work_packages"])
    text = f"""# Commercial Summary — {values['client_legal_name']}

| | |
|---|---|
| Edition | {values['edition']} |
| Term | {values['term_months']} months |
| Scope | {packages} |
| Implementation Value | AED {_fmt_aed(values['build_value_aed'])} |
| Mobilisation Fee | AED {_fmt_aed(values['mobilisation_fee_aed'])} |
| Subscription Fee | AED {_fmt_aed(values['subscription_fee_aed_mo'])} / month |
| Payment Cadence | {values['payment_cadence']} |
| Year-1 Total | AED {_fmt_aed(values['year1_total_aed'])} |
"""
    return text


def build(client, write=True):
    ok, reasons = pre_render_gate(client)
    if not ok:
        print(f"=== REFUSED: {client} ===")
        for r in reasons:
            print(f"  {r}")
        return 1

    values, emitted = load_context(client)
    r11 = render_r11(client, values)
    r12 = render_r12(client, values)

    drift_r11 = drift_check(r11, emitted)
    drift_r12 = drift_check(r12, emitted)
    if drift_r11 or drift_r12:
        print(f"=== BUILD FAILED (T11 drift check): {client} ===")
        print(f"  R11 undriftable figures: {drift_r11}")
        print(f"  R12 undriftable figures: {drift_r12}")
        return 1

    print(f"=== BUILD OK: {client} (T10, T12, T11 all clean) ===")
    if write:
        out_dir = os.path.join(REPO_ROOT, "02-clients", client, "04-draft")
        os.makedirs(out_dir, exist_ok=True)
        r11_path = os.path.join(out_dir, "MRD-2026-SUB-01_Rev3_Quotation.md")
        r12_path = os.path.join(out_dir, "MRD-2026-SUB-01_Rev3_Summary.md")
        with open(r11_path, "w", encoding="utf-8") as fh:
            fh.write(r11)
        with open(r12_path, "w", encoding="utf-8") as fh:
            fh.write(r12)
        print(f"  wrote {r11_path}")
        print(f"  wrote {r12_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2:
        sys.exit(build(sys.argv[1]))
    # No arg: demonstrate the gate against the full corpus.
    exit_code = 0
    for client in tpe.CLIENT_WORKSHEETS:
        rc = build(client, write=(client in ALLOWED_CLIENTS))
        exit_code = exit_code or rc
        print()
    sys.exit(exit_code)
