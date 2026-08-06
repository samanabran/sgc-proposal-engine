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
    functions -- no separate, divergent gate logic), AND on spec_binding
    (FIELD_SOURCE_MAP itself matches a frozen, independently-written
    expected-source table -- catches a swapped MAP entry, which
    label_binding_check below cannot, since that only inspects rendered
    text), AND on legal_identity_gate (06-brand/entity/legal-identity.yaml
    has no unresolved RESOLVE placeholder -- refuses before printing any
    VAT clause otherwise, per 2026-08-06 review).
  - Post-render drift check (T11): re-extracts every numeral that looks
    like a rendered AED/hour figure from the output text and confirms it
    traces to a value FIELD_SOURCE_MAP actually emitted. Fails the build,
    writes nothing, on any figure that doesn't trace.
  - Post-render label-binding check (T11): pins each rendered label to
    the one FIELD_SOURCE_MAP key it may read from; catches a figure
    swapped between two labels, which drift_check alone cannot (both
    values remain in the emitted set either way).
  - Post-render reconciliation check (T11): asserts
    mobilisation_fee_aed + subscription_fee_aed_mo*12 == year1_total_aed
    on the actual emitted values -- not printed as a decorative line
    unless it's true.
  - Post-render display-name check (T11): the Scope section shows
    human-readable package names (PACKAGE_DISPLAY_NAMES, presentation
    only); this check re-maps the displayed names back to package ids
    and confirms the resulting set equals values['work_packages']
    one-to-one -- no package silently dropped, added, or duplicated by
    the display-name substitution.
  - Client-facing output never names a YAML field path, a commit hash, a
    check name (T10/T12/T11), or a policy filename. Anything internal
    (e.g. the withheld-figure note) goes to a separate, clearly-marked
    non-client file: 04-draft/_INTERNAL_render-log.md.
  - Output is Markdown only. No PDF generation, no HTML in this pass.

Usage:
    python render_r11_r12.py <client-dir-name>
Exits non-zero (no files written) if the client is refused or any T11
post-render check fails.
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

    spec_violations = spec_binding_check()
    if spec_violations:
        reasons.extend(f"FIELD_SOURCE_MAP spec-binding violation: {v}" for v in spec_violations)

    legal_reasons = legal_identity_gate()
    reasons.extend(legal_reasons)

    return (len(reasons) == 0), reasons


# ---------------------------------------------------------------------
# Field-to-source map. Every entry is (label, extractor(ws, policy) -> value).
# The render functions below build their content ONLY from calling these
# extractors -- no other numeral may appear in a template.
# ---------------------------------------------------------------------
def _fmt_aed(n):
    return f"{n:,.0f}" if isinstance(n, (int, float)) and float(n).is_integer() else f"{n:,}"


FIELD_SOURCE_MAP = {
    "client_legal_name":      ("client-brief.yaml: client.legal_name", lambda ws, brief, pol, manifest: brief["client"]["legal_name"]),
    "decision_maker":         ("client-brief.yaml: client.decision_maker", lambda ws, brief, pol, manifest: brief["client"]["decision_maker"]),
    "term_months":            ("pricing-worksheet.yaml: inputs.term_months", lambda ws, brief, pol, manifest: ws["inputs"]["term_months"]),
    "edition":                ("pricing-worksheet.yaml: inputs.edition", lambda ws, brief, pol, manifest: ws["inputs"]["edition"]),
    "work_packages":          ("pricing-worksheet.yaml: number_2_build.delivery_hours[*].package",
                                lambda ws, brief, pol, manifest: [e["package"] for e in ws["number_2_build"]["delivery_hours"]]),
    "build_value_aed":        ("pricing-worksheet.yaml: number_2_build.build_value_aed", lambda ws, brief, pol, manifest: ws["number_2_build"]["build_value_aed"]),
    "mobilisation_fee_aed":   ("pricing-worksheet.yaml: number_3_financing.mobilisation_aed", lambda ws, brief, pol, manifest: ws["number_3_financing"]["mobilisation_aed"]),
    "financed_remainder_aed": ("pricing-worksheet.yaml: number_3_financing.deferred_aed", lambda ws, brief, pol, manifest: ws["number_3_financing"]["deferred_aed"]),
    "uplift_pct":             ("pricing-worksheet.yaml: number_3_financing.uplift_pct", lambda ws, brief, pol, manifest: ws["number_3_financing"]["uplift_pct"]),
    "recovery_monthly_aed":   ("pricing-worksheet.yaml: number_3_financing.recovery_monthly_aed", lambda ws, brief, pol, manifest: ws["number_3_financing"]["recovery_monthly_aed"]),
    "platform_portion_aed":   ("pricing-worksheet.yaml: assembly.option_a.platform_portion_aed", lambda ws, brief, pol, manifest: ws["assembly"]["option_a"]["platform_portion_aed"]),
    "subscription_fee_aed_mo":("pricing-worksheet.yaml: assembly.option_a.subscription_aed", lambda ws, brief, pol, manifest: ws["assembly"]["option_a"]["subscription_aed"]),
    "payment_cadence":        ("pricing-worksheet.yaml: payment_cadence", lambda ws, brief, pol, manifest: ws["payment_cadence"]),
    "year1_total_aed":        ("pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed", lambda ws, brief, pol, manifest: ws["assembly"]["option_a"]["year1_client_cost_aed"]),
    "vat_registered":         ("policy.yaml: vat.registered", lambda ws, brief, pol, manifest: pol["vat"]["registered"]),
    "charge_vat":             ("policy.yaml: vat.charge_vat", lambda ws, brief, pol, manifest: pol["vat"]["charge_vat"]),
    "reference_number":       ("manifest.yaml: opportunity_id", lambda ws, brief, pol, manifest: manifest["opportunity_id"]),
}

# monthly_billing_deviation withheld per the approved spec until its
# surcharge_pct is cited to a policy field -- deliberately NOT in the map
# above. If a future pass adds it, it must land here with its own
# extractor, never as a bare literal in a template string. INTERNAL ONLY:
# never printed in client-facing R11/R12 output (2026-08-06 review) --
# written to _INTERNAL_render-log.md by build() instead. See withheld
# note text below for the field path/policy citation; that citation
# itself is exactly the kind of internal vocabulary that must not reach
# a client.
WITHHELD = ["monthly_billing_deviation.surcharge_pct -- uncited to any policy.yaml field, "
            "per the approved R11/R12 spec's withhold rule (CHANGELOG.md pricing v3.1 addenda)"]


# ---------------------------------------------------------------------
# Spec-binding check (T11, 2026-08-06). label_binding_check further down
# proves rendered TEXT matches FIELD_SOURCE_MAP -- it says nothing about
# whether FIELD_SOURCE_MAP itself still says what it's supposed to.
# Swapping two entries' (source_path, extractor) pairs in the map would
# pass drift_check (values still trace to something emitted) AND
# label_binding_check (the swapped map is now internally self-consistent
# -- the label reads whatever the swapped extractor returns and reports
# it correctly). Only a comparison against a source EXTERNAL to
# FIELD_SOURCE_MAP can catch that. EXPECTED_FIELD_SOURCES is that
# external source: written independently, by hand, not derived from the
# map it checks.
#
# RECONCILED 2026-08-06 (corrected same day -- see below): the flatter
# paths ("assembly.subscription_fee_aed_mo", "assembly.year1_total_aed")
# are NOT fictional. They are exactly what Kallat's, Prosper's, and VGE's
# worksheets actually use -- a flat `assembly:` block
# (pricing-worksheet.yaml e.g. KP-kallat-properties:129-137). MRD alone
# wraps the same fields in an `assembly.option_a:` block
# (pricing-worksheet.yaml:97-119) -- a vestige of a planned `option_b`
# (zero-mobilisation) alternative that was later withdrawn (see MRD
# pricing-worksheet.yaml:120, "option_b ... is WITHDRAWN"); Kallat/
# Prosper/VGE never had an option_b concept, so their schema stayed flat.
# This divergence is real and, as far as this repo's own files show,
# undocumented (no CHANGELOG.md entry explains it). Since
# render_r11_r12.py is scoped to MRD only (ALLOWED_CLIENTS), the paths
# below are correct for the one client this renderer is authorized to
# read -- but this table would need a second, client-specific branch
# before ALLOWED_CLIENTS could ever be widened; flagged, not fixed here,
# since widening scope is explicitly out of bounds this pass.
EXPECTED_FIELD_SOURCES = {
    "client_legal_name":       "client-brief.yaml: client.legal_name",
    "decision_maker":          "client-brief.yaml: client.decision_maker",
    "term_months":              "pricing-worksheet.yaml: inputs.term_months",
    "edition":                  "pricing-worksheet.yaml: inputs.edition",
    "work_packages":            "pricing-worksheet.yaml: number_2_build.delivery_hours[*].package",
    "build_value_aed":          "pricing-worksheet.yaml: number_2_build.build_value_aed",
    "mobilisation_fee_aed":     "pricing-worksheet.yaml: number_3_financing.mobilisation_aed",
    "financed_remainder_aed":   "pricing-worksheet.yaml: number_3_financing.deferred_aed",
    "uplift_pct":               "pricing-worksheet.yaml: number_3_financing.uplift_pct",
    "recovery_monthly_aed":     "pricing-worksheet.yaml: number_3_financing.recovery_monthly_aed",
    "platform_portion_aed":     "pricing-worksheet.yaml: assembly.option_a.platform_portion_aed",
    "subscription_fee_aed_mo":  "pricing-worksheet.yaml: assembly.option_a.subscription_aed",
    "payment_cadence":          "pricing-worksheet.yaml: payment_cadence",
    "year1_total_aed":          "pricing-worksheet.yaml: assembly.option_a.year1_client_cost_aed",
    "vat_registered":           "policy.yaml: vat.registered",
    "charge_vat":               "policy.yaml: vat.charge_vat",
    "reference_number":         "manifest.yaml: opportunity_id",
}


def spec_binding_check():
    """Field-by-field comparison of FIELD_SOURCE_MAP's declared source path
    against EXPECTED_FIELD_SOURCES, independent of any rendered text.
    Returns a list of violation strings (empty = clean)."""
    violations = []
    for field, expected_source in EXPECTED_FIELD_SOURCES.items():
        entry = FIELD_SOURCE_MAP.get(field)
        if entry is None:
            violations.append(f"'{field}' expected in FIELD_SOURCE_MAP (source: {expected_source}) but missing")
            continue
        actual_source, _extractor = entry
        if actual_source != expected_source:
            violations.append(f"'{field}' expected source '{expected_source}', "
                               f"FIELD_SOURCE_MAP declares '{actual_source}'")
    extra = set(FIELD_SOURCE_MAP) - set(EXPECTED_FIELD_SOURCES)
    for field in sorted(extra):
        violations.append(f"'{field}' present in FIELD_SOURCE_MAP but not in EXPECTED_FIELD_SOURCES -- "
                           "add it to the frozen table before it can ship")
    return violations


# ---------------------------------------------------------------------
# Display-name mapping (2026-08-06). Presentation only -- must never
# change which packages render, only how their id is shown. Scoped to
# the package ids that actually appear in MRD's own worksheet (no work
# on any other client's catalogue this pass). Deliberately a plain dict
# indexed with [] (not .get()): an unmapped package id must raise, never
# silently fall back to showing the raw identifier -- that fallback is
# exactly the defect this mapping exists to close.
# ---------------------------------------------------------------------
PACKAGE_DISPLAY_NAMES = {
    "discovery": "Discovery & Requirements",
    "property_unit_register": "Property & Unit Register",
    "tenancies_contracts_reminders": "Tenancies, Contracts & Reminders",
    "invoicing_trn": "Invoicing (TRN-ready)",
    "maintenance_invoice_from_request": "Maintenance-to-Invoice Workflow",
    "crm_leads": "CRM & Lead Management",
    "reports_dashboard": "Reporting Dashboard",
}


def display_name_check(rendered_scope_names, source_package_ids):
    """T11: confirms the displayed name list maps back to source_package_ids
    one-to-one -- no package silently dropped, added, or duplicated by the
    display-name substitution. Returns a list of violation strings."""
    reverse = {v: k for k, v in PACKAGE_DISPLAY_NAMES.items()}
    violations = []
    if len(reverse) != len(PACKAGE_DISPLAY_NAMES):
        violations.append("PACKAGE_DISPLAY_NAMES has duplicate display names -- reverse mapping is not 1:1")
    recovered_ids = []
    for name in rendered_scope_names:
        if name not in reverse:
            violations.append(f"displayed name '{name}' does not map back to any known package id")
            continue
        recovered_ids.append(reverse[name])
    if sorted(recovered_ids) != sorted(source_package_ids):
        violations.append(f"recovered id set {sorted(recovered_ids)} != source id set {sorted(source_package_ids)}")
    return violations


# ---------------------------------------------------------------------
# Legal-identity gate (2026-08-06). The VAT sentence asserts a legal fact
# about the entity (registered/not registered for UAE VAT). If
# legal-identity.yaml still carries an unresolved RESOLVE placeholder --
# the file's own documented failure mode, see its header comment -- that
# fact is unverified and must not be printed. Checked as part of the
# pre-render gate, not a template-level omission, so a bad legal-identity
# file refuses the whole build rather than silently shipping a
# VAT-clause-shaped hole.
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
        return [f"06-brand/entity/legal-identity.yaml is missing -- cannot verify any legal fact, "
                "including the VAT clause; refusing"]
    identity = pe._load(path)
    unresolved = [s for s in _flatten_strings(identity) if s.strip().upper() == "RESOLVE"]
    if unresolved:
        return [f"06-brand/entity/legal-identity.yaml still has {len(unresolved)} unresolved RESOLVE "
                "placeholder(s) -- refusing to emit the VAT clause (or the rest of this build) until "
                "resolved, per the file's own documented failure mode"]
    return []


def load_context(client):
    client_dir = os.path.join(REPO_ROOT, "02-clients", client)
    ws = pe._load(os.path.join(client_dir, "02-calc", "pricing-worksheet.yaml"))
    brief = pe._load(os.path.join(client_dir, "00-intake", "client-brief.yaml"))
    pol = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    manifest = pe._load(os.path.join(client_dir, "manifest.yaml"))
    values = {}
    emitted = []  # (label, value, source_path) -- feeds the drift check
    for label, (source_path, extractor) in FIELD_SOURCE_MAP.items():
        v = extractor(ws, brief, pol, manifest)
        values[label] = v
        emitted.append((label, v, source_path))

    # Derived, disclosed intermediate (2026-08-06): platform_portion_aed +
    # recovery_monthly_aed, BEFORE the nearest-10 rounding that produces
    # subscription_fee_aed_mo. Rendered so the subscription's components
    # visibly sum to something (1,677), with the rounding step shown
    # explicitly, rather than three numbers that don't sum on the page.
    # Declared here -- not a bare template literal -- so drift_check can
    # trace it like every other rendered figure.
    values["subscription_raw_sum_aed"] = values["platform_portion_aed"] + values["recovery_monthly_aed"]
    emitted.append(("subscription_raw_sum_aed", values["subscription_raw_sum_aed"],
                     "derived: platform_portion_aed + recovery_monthly_aed, pre-rounding"))

    # Derived, disclosed (2026-08-06): full-term (24-month) contract value --
    # mobilisation + subscription*term_months. Year-1 alone understates what
    # a 24-month term actually commits the client to. Declared here, not a
    # template literal, same discipline as subscription_raw_sum_aed above.
    values["full_term_commitment_aed"] = (values["mobilisation_fee_aed"]
                                           + values["subscription_fee_aed_mo"] * values["term_months"])
    emitted.append(("full_term_commitment_aed", values["full_term_commitment_aed"],
                     "derived: mobilisation_fee_aed + subscription_fee_aed_mo * term_months"))
    return values, emitted


def reconciliation_check(values):
    """T11: mobilisation_fee_aed + subscription_fee_aed_mo*12 must equal
    year1_total_aed, AND mobilisation_fee_aed + subscription_fee_aed_mo*
    term_months must equal full_term_commitment_aed (the second is a
    self-consistency check, not a cross-check against a separate stored
    field -- MRD's worksheet schema has no full-term figure of its own to
    compare against, unlike Kallat/Prosper/VGE's flat assembly block which
    does; see the EXPECTED_FIELD_SOURCES note on the schema divergence).
    Returns (ok, computed_year1, computed_full_term)."""
    computed_year1 = values["mobilisation_fee_aed"] + values["subscription_fee_aed_mo"] * 12
    computed_full_term = (values["mobilisation_fee_aed"]
                           + values["subscription_fee_aed_mo"] * values["term_months"])
    ok = (computed_year1 == values["year1_total_aed"]
          and computed_full_term == values["full_term_commitment_aed"])
    return ok, computed_year1, computed_full_term


def _extract_r11_scope_names(rendered_text):
    m = re.search(r"## Scope\n(.*?)\n##", rendered_text, re.S)
    if not m:
        return []
    return [line[2:] for line in m.group(1).splitlines() if line.startswith("- ")]


def _extract_r12_scope_names(rendered_text):
    # "; " (not ",") -- at least one display name (tenancies_contracts_reminders)
    # legitimately contains a comma, so comma-splitting would corrupt it.
    m = re.search(r"\|\s*Scope\s*\|\s*(.*?)\s*\|\s*\n", rendered_text)
    if not m:
        return []
    return [s.strip() for s in m.group(1).split(";")]


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


# ---------------------------------------------------------------------
# Label-binding check. drift_check above only proves a rendered number
# traces to SOME value this build emitted -- it says nothing about
# whether it's the RIGHT value for the label it's printed under. A
# figure swapped between two labels (e.g. Mobilisation Fee's value
# printed next to "Subscription Fee") still passes drift_check, because
# both numbers are still in the emitted set. LABEL_FIELD_BINDING pins
# each rendered label to the one FIELD_SOURCE_MAP key it is allowed to
# read from; label_binding_check re-parses the rendered text and fails
# on any mismatch, independent of drift_check.
# ---------------------------------------------------------------------
LABEL_FIELD_BINDING = {
    "Implementation Value": "build_value_aed",
    "Mobilisation Fee": "mobilisation_fee_aed",
    "Financed Remainder": "financed_remainder_aed",
    "Platform Portion": "platform_portion_aed",
    "Recovery (monthly, over the term)": "recovery_monthly_aed",
    "Subscription Fee": "subscription_fee_aed_mo",
    "Year-1 Total": "year1_total_aed",
    "Total 24-Month Contract Value": "full_term_commitment_aed",
}


def label_binding_check(rendered_text, values):
    violations = []
    for label, field_key in LABEL_FIELD_BINDING.items():
        pattern = re.compile(re.escape(label) + r"[^\n]*?AED\s*([\d,]+(?:\.\d+)?)")
        m = pattern.search(rendered_text)
        if not m:
            continue  # this label doesn't appear in this particular rendered doc
        found = m.group(1).replace(",", "")
        expected = values.get(field_key)
        expected_str = _fmt_aed(expected).replace(",", "") if isinstance(expected, (int, float)) else str(expected)
        if found != expected_str:
            violations.append(
                f"label '{label}' is bound to values['{field_key}']={expected} "
                f"but the rendered text shows AED {found} next to it"
            )
    return violations


def render_r11(client, values):
    packages = "\n".join(f"- {PACKAGE_DISPLAY_NAMES[p]}" for p in values["work_packages"])
    vat_line = ("SGC TECH AI is not currently registered for UAE VAT, and no VAT is charged on this proposal."
                if values["charge_vat"] is False else
                "VAT is charged at the prevailing rate on this proposal.")
    year1_check_aed = values["mobilisation_fee_aed"] + values["subscription_fee_aed_mo"] * 12
    full_term_check_aed = values["mobilisation_fee_aed"] + values["subscription_fee_aed_mo"] * values["term_months"]
    text = f"""# Standalone Quotation

**Reference:** {values['reference_number']}
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
- Subscription Fee: AED {_fmt_aed(values['subscription_fee_aed_mo'])} / month
    - Platform Portion: AED {_fmt_aed(values['platform_portion_aed'])}
    - Recovery (monthly, over the term): AED {_fmt_aed(values['recovery_monthly_aed'])}
    - Subtotal: AED {_fmt_aed(values['subscription_raw_sum_aed'])} -- rounded to the nearest 10 = AED {_fmt_aed(values['subscription_fee_aed_mo'])}
- Payment Cadence: {values['payment_cadence']}
- Year-1 Total: AED {_fmt_aed(values['year1_total_aed'])}
- Total {values['term_months']}-Month Contract Value: AED {_fmt_aed(values['full_term_commitment_aed'])}

## Reconciliation
- Mobilisation (AED {_fmt_aed(values['mobilisation_fee_aed'])}) + Subscription (AED {_fmt_aed(values['subscription_fee_aed_mo'])}) x 12 months = AED {_fmt_aed(year1_check_aed)} = Year-1 Total
- Mobilisation (AED {_fmt_aed(values['mobilisation_fee_aed'])}) + Subscription (AED {_fmt_aed(values['subscription_fee_aed_mo'])}) x {values['term_months']} months = AED {_fmt_aed(full_term_check_aed)} = Total {values['term_months']}-Month Contract Value

The AED {_fmt_aed(values['recovery_monthly_aed'])}/month recovery portion of the Subscription Fee runs for the full {values['term_months']}-month term and is fully collected by the end of month {values['term_months']} — it does not extend beyond the term. The Subscription Fee itself does not reduce at that point: it continues at the same AED {_fmt_aed(values['subscription_fee_aed_mo'])}/month rate, month-to-month, after the initial term.

## VAT
{vat_line}
"""
    return text


def render_r12(client, values):
    # "; " not ", " -- tenancies_contracts_reminders's display name itself
    # contains a comma; a comma-joined list would be ambiguous to re-parse.
    packages = "; ".join(PACKAGE_DISPLAY_NAMES[p] for p in values["work_packages"])
    text = f"""# Commercial Summary — {values['client_legal_name']}

| | |
|---|---|
| Reference | {values['reference_number']} |
| Edition | {values['edition']} |
| Term | {values['term_months']} months |
| Scope | {packages} |
| Implementation Value | AED {_fmt_aed(values['build_value_aed'])} |
| Mobilisation Fee | AED {_fmt_aed(values['mobilisation_fee_aed'])} |
| Subscription Fee | AED {_fmt_aed(values['subscription_fee_aed_mo'])} / month |
| Payment Cadence | {values['payment_cadence']} |
| Year-1 Total | AED {_fmt_aed(values['year1_total_aed'])} |
| Total 24-Month Contract Value | AED {_fmt_aed(values['full_term_commitment_aed'])} |
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

    label_r11 = label_binding_check(r11, values)
    label_r12 = label_binding_check(r12, values)
    if label_r11 or label_r12:
        print(f"=== BUILD FAILED (T11 label-binding check): {client} ===")
        for v in label_r11:
            print(f"  R11: {v}")
        for v in label_r12:
            print(f"  R12: {v}")
        return 1

    reconciled, computed_year1, computed_full_term = reconciliation_check(values)
    if not reconciled:
        print(f"=== BUILD FAILED (T11 reconciliation check): {client} ===")
        print(f"  mobilisation({values['mobilisation_fee_aed']}) + subscription({values['subscription_fee_aed_mo']})*12 "
              f"= {computed_year1} (year1_total_aed={values['year1_total_aed']})")
        print(f"  mobilisation({values['mobilisation_fee_aed']}) + subscription({values['subscription_fee_aed_mo']})*"
              f"{values['term_months']} = {computed_full_term} (full_term_commitment_aed={values['full_term_commitment_aed']})")
        return 1

    display_r11 = display_name_check(_extract_r11_scope_names(r11), values["work_packages"])
    display_r12 = display_name_check(_extract_r12_scope_names(r12), values["work_packages"])
    if display_r11 or display_r12:
        print(f"=== BUILD FAILED (T11 display-name check): {client} ===")
        for v in display_r11:
            print(f"  R11: {v}")
        for v in display_r12:
            print(f"  R12: {v}")
        return 1

    print(f"=== BUILD OK: {client} (T10, T12, spec-binding, legal-identity, T11 drift + "
          f"label-binding + reconciliation + display-name all clean) ===")
    if write:
        out_dir = os.path.join(REPO_ROOT, "02-clients", client, "04-draft")
        os.makedirs(out_dir, exist_ok=True)
        r11_path = os.path.join(out_dir, "MRD-2026-SUB-01_Rev3_Quotation.md")
        r12_path = os.path.join(out_dir, "MRD-2026-SUB-01_Rev3_Summary.md")
        # 2026-08-06: moved OUT of 04-draft/ (the client deliverable folder) into
        # 02-calc/, which is already the established internal-only working area
        # (worksheet, gate-report, risk-assessment all live there and are never
        # sent). A "do not forward" header next to the deliverables is still a
        # forwarding risk if someone drags the whole draft folder into an email --
        # this closes that regardless of what the header says. No packaging/send
        # script exists yet in this repo to "confirm excludes underscore files"
        # against, so moving the file is the only concrete guarantee available now.
        calc_dir = os.path.join(REPO_ROOT, "02-clients", client, "02-calc")
        log_path = os.path.join(calc_dir, "_internal-render-log.md")
        with open(r11_path, "w", encoding="utf-8") as fh:
            fh.write(r11)
        with open(r12_path, "w", encoding="utf-8") as fh:
            fh.write(r12)
        with open(log_path, "w", encoding="utf-8") as fh:
            fh.write(
                "# INTERNAL render log -- NOT client-facing. Do not attach, forward, or send.\n"
                f"# Client: {client}  Build: MRD-2026-SUB-01_Rev3\n\n"
                "## Withheld figures (omitted from client output, not just relabeled)\n"
                + "\n".join("- " + w for w in WITHHELD) + "\n\n"
                "## Gate results\n"
                f"- spec_binding_check: clean ({len(EXPECTED_FIELD_SOURCES)} fields checked)\n"
                f"- legal_identity_gate: clean\n"
                f"- reconciliation_check (year-1): {values['mobilisation_fee_aed']} + "
                f"{values['subscription_fee_aed_mo']}*12 = {computed_year1} == "
                f"{values['year1_total_aed']}\n"
                f"- reconciliation_check (full term): {values['mobilisation_fee_aed']} + "
                f"{values['subscription_fee_aed_mo']}*{values['term_months']} = {computed_full_term} == "
                f"{values['full_term_commitment_aed']}\n"
            )
        print(f"  wrote {r11_path}")
        print(f"  wrote {r12_path}")
        print(f"  wrote {log_path} (internal only, outside the deliverable folder)")
    return 0


# ---------------------------------------------------------------------
# Issue-promotion gate (2026-08-06, PROPOSED -- not wired into build()
# above and not invoked by anything yet; no 04-draft -> 05-issued
# promotion script exists in this repo for it to gate. Defined here, in
# the one file that currently understands both the worksheet and the
# manifest, so whichever script eventually does the copy/move can import
# and call it first. Read-only: never writes, never moves a file itself.
# ---------------------------------------------------------------------
def issue_promotion_gate(client):
    """Refuses promotion of `client`'s current revision from 04-draft to
    05-issued while manifest.yaml's issued_date is empty OR the current
    revision's 13-next-steps.md signature block still contains a RESOLVE
    placeholder. Returns a list of blocking reasons (empty = clear to
    issue)."""
    client_dir = os.path.join(REPO_ROOT, "02-clients", client)
    manifest = pe._load(os.path.join(client_dir, "manifest.yaml"))
    current_revision = manifest.get("current_revision")
    reasons = []

    revisions = {r["ref"]: r for r in manifest.get("revisions", [])}
    rev = revisions.get(current_revision)
    if rev is None:
        return [f"manifest.yaml current_revision '{current_revision}' not found in revisions[] -- cannot verify issued_date"]
    if not (rev.get("issued_date") or "").strip():
        reasons.append(f"manifest.yaml revisions[{current_revision}].issued_date is empty -- "
                        "not yet issued, refusing promotion to 05-issued")

    next_steps_path = os.path.join(client_dir, "03-draft", current_revision, "13-next-steps.md")
    if not os.path.exists(next_steps_path):
        reasons.append(f"{next_steps_path} not found -- cannot verify the signature block")
    else:
        with open(next_steps_path, "r", encoding="utf-8") as fh:
            next_steps_text = fh.read()
        m = re.search(r"## Signature block(.*)", next_steps_text, re.S)
        signature_section = m.group(1) if m else next_steps_text
        if "RESOLVE" in signature_section:
            reasons.append(f"{next_steps_path}'s signature block still contains a RESOLVE placeholder -- "
                            "refusing promotion to 05-issued")
    return reasons


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
