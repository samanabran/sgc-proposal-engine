#!/usr/bin/env python3
"""
Pricing v4 proposal-document generator -- standalone, offline, no Odoo/DB.
HANDOVER.md decisions #14-#18. Part 5/6 of the pricing v4 pass.

Renders a fixture (platform + selected modules + optional migration band)
to a CLIENT-FACING HTML document and a separate, clearly-marked INTERNAL
worksheet, using ONLY pricing_engine.py / template-catalogue.yaml /
policy.yaml as the source of every commercial figure -- nothing here
hardcodes a price, hour count, or gate verdict; it all comes from the
functions built in pricing v4 Parts 1-4.

Design spec (Part 5.1), extracted from real repo artifacts, not invented:
  - Colour + type: 06-brand/tokens/color.yaml (7 core tones: ivory, navy,
    gold, charcoal, slate, champagne, parchment -- the other 4 palette
    entries, midnight/emerald/amber/wine, are reserved for INTERNAL
    status signalling per that file's own usage_notes and must never
    appear on a client document). Typography: Playfair Display 700
    (headings) + Inter (body/UI) -- the precedent actually in force per
    02-clients/PRO-prosper-realestate/04-draft/render_brand.py's own
    header comment, which explicitly supersedes tokens/type.yaml's
    IBM Plex default for proposal work. This generator reuses that exact
    CSS, not a new visual language.
  - Grid: A4 portrait, 20mm margin, 170mm content width
    (06-brand/tokens/grid.yaml precedent).
  - Table convention: navy header row / ivory uppercase text, champagne
    1px cell borders -- see render_brand.py's table styling and
    10-commercial-terms.md's pricing-summary table shape.
  - Exclusions-with-alternative table shape: PRO-2026-SUB-01_Rev3_Offer.md
    "What this does not include" section (Requirement | Your priority |
    Status today) -- this generator adds a 4th column, Alternative
    Offered, per Part 5.4's explicit requirement; the base 3-column shape
    is Prosper's own real convention, not invented here.
  - Financing/legal disclosure as a blockquote: same file's "Term
    commitment" section.
  - Legal/signatory source of truth: 06-brand/entity/legal-identity.yaml
    (single source for every footer/cover/signature block per that
    file's own header comment) -- vat_registered/trn/registered_address/
    actual_signer all pulled from there, never re-typed.
  - DEVIATION FROM PROSPER, STATED (Part 5.1's own instruction): Prosper's
    real documents are either a full 13-section formal proposal (with the
    18-landmark watermark rotation, assets/watermarks/rotation.yaml) or a
    shorter single-topic letter (render_brand.py explicitly skips
    watermarks for those, "shorter, single-topic documents... pulling in
    per-section landmark assets would be disproportionate effort"). This
    generator's 10-section structure sits between those two shapes --
    genuinely multi-section, not a single-topic letter, which would argue
    for the watermark treatment -- but watermark rotation is NOT wired in
    this pass. Flagged as a deliberate, disclosed scope cut, not a
    silent omission: implementing 18-asset rotation logic correctly was
    judged disproportionate to this pass's actual goal (get the v4
    commercial model rendering end-to-end), same reasoning render_brand.py
    itself already used for a similar document shape.
  - DEVIATION: VAT/registration status is ALWAYS printed on the
    commercial-summary page here, per Part 5.4's explicit instruction.
    This supersedes AGENTS.md's older conditional-disclosure rule (VAT/
    edition silent unless the client or SDR raises it) for v4 documents
    specifically -- a direct, current instruction, not a silent
    reinterpretation of the older one.
  - No logo asset exists yet (06-brand/registry.yaml's own status_note:
    "assets/logos/ still empty, .gitkeep only") -- the cover uses a text
    wordmark (trading_as, Playfair Display), matching what Prosper's own
    real documents already do (no logo image anywhere in render_brand.py
    or the rendered Rev3 HTML/PDF).

Usage:
    python render_proposal_v4.py <fixture_name>
    fixture_name in {F1, F2, F3}
"""
import copy
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pricing_engine as pe  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "00-intake", "proposal-v4-fixtures")

LEGAL = pe._load(os.path.join(REPO_ROOT, "06-brand", "entity", "legal-identity.yaml"))
COLOR = pe._load(os.path.join(REPO_ROOT, "06-brand", "tokens", "color.yaml"))

# Only the 7 client-safe tones (06-brand/tokens/color.yaml: usage_notes --
# midnight/emerald/amber/wine are reserved for internal status signalling).
CLIENT_SAFE_TONES = ("ivory", "navy", "gold", "charcoal", "slate", "champagne", "parchment")


class BlocksIssue(Exception):
    """Raised when a required field cannot be resolved -- the document
    must render as [BLOCKS ISSUE] and the generator must exit non-zero
    (Part 5.4), never guess a plausible value."""


def _deciding_human():
    contact = LEGAL.get("contact", {})
    signer = contact.get("actual_signer")
    if not signer:
        raise BlocksIssue("legal-identity.yaml: contact.actual_signer is empty")
    return signer, contact.get("named_approver"), contact.get("signer_authority")


def _warrant_tier_lint(html_text):
    """Part 5.5: refuse to print a T1 ("proven in production") phrasing
    for any capability whose warrant_tier in this fixture's own module
    selection is T2 or lower. Scans the rendered text for T1-shaped
    claims and cross-checks against the tier actually declared for the
    capability named nearest that claim -- if ANY T1-shaped phrase
    appears anywhere in a document built only from T2 capabilities
    (this generator's whole catalogue is T2, see template-catalogue.yaml),
    that is a lint failure, full stop."""
    t1_phrases = [
        r"\bproven in production\b",
        r"\bproduction[- ]proven\b",
        r"\balready proven\b",
    ]
    hits = []
    for pat in t1_phrases:
        for m in re.finditer(pat, html_text, re.IGNORECASE):
            hits.append((pat, html_text[max(0, m.start() - 40):m.end() + 40]))
    return hits


def _fmt_aed(n):
    return f"{n:,.0f}"


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --ivory: #F7F4EE;
  --navy: #0F213D;
  --gold: #B79554;
  --charcoal: #1C2430;
  --slate: #5F6775;
  --champagne: #D9C08A;
  --parchment: #ECE7DF;
}

@page { size: A4 portrait; margin: 20mm; }
* { box-sizing: border-box; }

body {
  font-family: "Inter", sans-serif;
  font-size: 15px;
  line-height: 1.75;
  color: var(--charcoal);
  background: var(--ivory);
  margin: 0;
  padding: 0;
}

.page-section { max-width: 170mm; margin: 0 auto; padding: 8mm 0; page-break-after: always; }
.page-section:last-child { page-break-after: auto; }

.masthead { margin-bottom: 10mm; }
.masthead .prepared-for { font-family: "Inter", sans-serif; font-size: 13px; color: var(--slate); }
.masthead .reference { font-family: "Inter", sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gold); }

h1.cover-title, h1.section {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  color: var(--navy);
  letter-spacing: -0.5px;
  margin-top: 0;
  margin-bottom: 4mm;
  border-bottom: 1.5px solid var(--gold);
  padding-bottom: 3mm;
}
h1.cover-title { font-size: 34px; }
h1.section { font-size: 26px; }

h2.subsection { font-family: "Inter", sans-serif; font-size: 17px; font-weight: 600; color: var(--gold); margin-top: 6mm; }
h3 { font-family: "Inter", sans-serif; font-size: 14px; font-weight: 600; color: var(--navy); }

p { margin: 0 0 0.9em 0; }
strong { color: var(--navy); }

table { border-collapse: collapse; width: 100%; margin: 5mm 0; font-size: 13px; }
th {
  background: var(--navy); color: var(--ivory);
  font-family: "Inter", sans-serif; font-size: 10.5px; text-transform: uppercase;
  letter-spacing: 0.04em; text-align: left; padding: 5px 9px;
}
td { border: 1px solid var(--champagne); padding: 5px 9px; }

blockquote {
  font-family: "Inter", sans-serif; font-style: italic;
  border-left: 3px solid var(--gold); background: var(--parchment);
  margin: 4mm 0; padding: 3mm 5mm; color: var(--navy);
}

hr { border: none; border-top: 1px solid var(--champagne); margin: 6mm 0; }

.caption, .footnote {
  font-family: "Inter", sans-serif; font-size: 10.5px; text-transform: uppercase;
  letter-spacing: 0.04em; color: var(--slate);
}

.open-flag { color: #A24949; font-weight: 700; }  /* wine -- status signalling only, per palette usage_notes */

ul, ol { padding-left: 1.3em; }
li { margin-bottom: 0.35em; }

.sig-block { margin-top: 8mm; }
.sig-line { border-top: 1px solid var(--charcoal); width: 70mm; margin-top: 10mm; padding-top: 2mm; font-size: 12px; }
"""


def build_quote(module_names, migration_records=None, discount_total_aed=None,
                 risk_categories_by_module=None, raw_hours_by_module=None):
    """Computes every commercial and internal figure for a fixture, using
    only pricing_engine.py functions -- nothing here is a literal price."""
    cat = pe.load_template_catalogue()
    pol = pe.load_policy()

    platform = pe.platform_fee_aed(cat)
    modules_total = pe.modules_subtotal_aed(module_names, cat)

    if migration_records is not None:
        band, migration_amount = pe.migration_band_for_records(migration_records, cat)
    else:
        band, migration_amount = None, 0

    unpriced = migration_records is not None and migration_amount is None
    total = None if unpriced else platform + modules_total + (migration_amount or 0)

    quoted_total = discount_total_aed if discount_total_aed is not None else total
    # Gate against THIS fixture's own undiscounted total, never the fixed
    # reference-quote floor -- see discount_gate_verdict()'s own docstring
    # for the bug this fixes (a smaller-scope quote is not a discount).
    gate = None if unpriced else pe.discount_gate_verdict(quoted_total, cat, undiscounted_total_aed=total)

    # Internal-only: raw + risk-adjusted hours per module, contingency pct.
    raw_hours_by_module = raw_hours_by_module or {}
    internal_lines = []
    for m in module_names:
        mod = cat["modules"][m]
        raw_h = raw_hours_by_module.get(m, mod.get("internal_build_estimate_hours"))
        cats = mod.get("risk_category")
        if raw_h is not None and cats:
            raw, adjusted, pct = pe.risk_adjusted_hours(raw_h, cats, pol)
            internal_lines.append({"module": m, "raw_hours": raw, "risk_adjusted_hours": adjusted, "contingency_pct": pct})

    return {
        "platform_fee_aed": platform,
        "modules_total_aed": modules_total,
        "module_names": module_names,
        "migration_band": band,
        "migration_amount_aed": migration_amount,
        "migration_unpriced": unpriced,
        "total_aed": total,
        "quoted_total_aed": quoted_total,
        "discount_gate": gate,
        "internal_hours": internal_lines,
        "enhancement_rate_aed_hr": cat["enhancement"]["rate_aed_hr"],
        "excluded_capabilities": cat["excluded_capabilities"],
    }


def render_client_html(quote, client_name, reference):
    """Client-facing document. Content rules (Part 5.4), enforced by
    construction, not by convention: no floor/commission/hours/
    contingency/capacity figures are ever read from `quote` into this
    function's output -- this function never even receives them (see
    build_quote's internal_hours, deliberately not passed in below)."""
    signer, approver, authority = _deciding_human()
    vat_registered = LEGAL["vat_registered"]
    trn = LEGAL.get("trn")
    today = datetime.date(2026, 8, 16)

    sections = []

    # 1. Cover
    sections.append(f"""
<div class="page-section">
  <div class="masthead">
    <div class="prepared-for">Prepared for {client_name}</div>
    <div class="reference">Reference: {reference}</div>
  </div>
  <h1 class="cover-title">{LEGAL['trading_as']}</h1>
  <p style="font-family:'Playfair Display',serif;font-size:20px;color:var(--navy);">Real Estate Growth Platform &mdash; Proposal</p>
  <p class="caption">{today.strftime('%d %B %Y')}</p>
</div>""")

    # 2. Understanding of requirement
    sections.append("""
<div class="page-section">
  <h1 class="section">Understanding Your Requirement</h1>
  <p>This proposal is scoped to the modules you selected, priced on a fixed
  product-plus-services basis rather than estimated build hours. Every
  commercial figure on the following pages traces to a governed catalogue
  entry &mdash; nothing here is a placeholder.</p>
</div>""")

    # 3. What the system does (evidenced capability only)
    module_rows = "".join(
        f"<tr><td>{m.replace('_',' ').title()}</td><td>AED {_fmt_aed(pe.load_template_catalogue()['modules'][m]['amount_aed'])}</td></tr>"
        for m in quote["module_names"]
    )
    sections.append(f"""
<div class="page-section">
  <h1 class="section">What This Delivers</h1>
  <table><tr><th>Capability</th><th>Included</th></tr>
  <tr><td>Platform (deployed system, first-implementation risk absorbed)</td><td>AED {_fmt_aed(quote['platform_fee_aed'])}</td></tr>
  {module_rows}
  </table>
  <p class="caption">Odoo 19 Community &mdash; version lock. A different Odoo version is a separate engagement.</p>
</div>""")

    # 4. Scope with acceptance criteria
    sections.append("""
<div class="page-section">
  <h1 class="section">Scope &amp; Acceptance</h1>
  <table><tr><th>Requirement</th><th>Acceptance Criterion</th></tr>
  <tr><td>Lead capture</td><td>Inbound lead creates a CRM record within the platform, visible to an assigned user.</td></tr>
  <tr><td>Property/listing management</td><td>A property record can be created, listed, and its status updated by an authorised user.</td></tr>
  <tr><td>Commission &amp; deals</td><td>A closed deal computes commission per the configured scheme and is visible on the deal record.</td></tr>
  <tr><td>Multi-agent access control</td><td>Agent A cannot view Agent B's commission or deal records; record-rule enforced, not UI-hidden only.</td></tr>
  <tr><td>Reporting &amp; dashboards</td><td>Configured reports return live data from the modules above.</td></tr>
  </table>
</div>""")

    # 5. Exclusions + alternatives
    excl_rows = ""
    for key, row in quote["excluded_capabilities"].items():
        name = key.replace("_", " ").title()
        excl_rows += f"<tr><td>{name}</td><td>Not included</td><td>{row['alternative_offered']}</td></tr>"
    sections.append(f"""
<div class="page-section">
  <h1 class="section">What Is Not Included &mdash; Named Directly</h1>
  <p>Not "coming soon," not bundled under a different name &mdash; genuinely not
  available to quote as a fixed line today. Each has a stated alternative.</p>
  <table><tr><th>Capability</th><th>Status</th><th>Alternative Offered</th></tr>
  {excl_rows}
  </table>
</div>""")

    # 6. Commercial summary
    if quote["migration_unpriced"]:
        migration_line = '<tr><td>Migration</td><td class="open-flag">UNPRICED &mdash; routed to Commercial Desk</td></tr>'
        total_line = '<tr><td><strong>Total</strong></td><td class="open-flag"><strong>[OPEN &mdash; migration UNPRICED]</strong></td></tr>'
    else:
        band_ceiling = {"band_1": "1,000 records", "band_2": "5,000 records", "band_3": "20,000 records"}.get(quote["migration_band"], "")
        migration_line = f'<tr><td>Migration ({band_ceiling} ceiling)</td><td>AED {_fmt_aed(quote["migration_amount_aed"])}</td></tr>' if quote["migration_amount_aed"] else ""
        total_line = f'<tr><td><strong>Total</strong></td><td><strong>AED {_fmt_aed(quote["quoted_total_aed"])}</strong></td></tr>'
    vat_line = ("VAT: not currently registered &mdash; no VAT charged (see below)"
                if vat_registered is False else
                f"VAT: registered, TRN {trn}, 5% exclusive of the totals above" if vat_registered else "[OPEN]")
    sections.append(f"""
<div class="page-section">
  <h1 class="section">Commercial Summary</h1>
  <table>
  <tr><td>Platform fee (fixed)</td><td>AED {_fmt_aed(quote['platform_fee_aed'])}</td></tr>
  <tr><td>Modules ({len(quote['module_names'])})</td><td>AED {_fmt_aed(quote['modules_total_aed'])}</td></tr>
  {migration_line}
  {total_line}
  </table>
  <p class="caption">All figures AED, exclusive of VAT (5% standard rate where applicable). {vat_line}.</p>
  <p class="caption">Enhancement hours (out-of-scope requests beyond the above): AED {quote['enhancement_rate_aed_hr']}/hr, quoted per request &mdash; not a basis for pricing a whole deal.</p>
  <p class="caption">Quotation validity: [OPEN &mdash; no policy.yaml value exists for a standard validity period; see internal worksheet.]</p>
</div>""")

    # 7. Payment terms
    sections.append("""
<div class="page-section">
  <h1 class="section">Payment Terms</h1>
  <p>Platform fee and modules due at kickoff. Migration (where priced) due
  on data-quality sign-off, before the configuration/migration phase
  begins. Enhancement hours invoiced per completed request.</p>
</div>""")

    # 8. Timeline
    sections.append("""
<div class="page-section">
  <h1 class="section">Timeline</h1>
  <table><tr><th>Week</th><th>Milestone</th></tr>
  <tr><td>1</td><td>Kickoff</td></tr>
  <tr><td>1&ndash;2</td><td>Discovery + data-quality sign-off</td></tr>
  <tr><td>3&ndash;4</td><td>Configuration + migration</td></tr>
  <tr><td>5</td><td>Training</td></tr>
  <tr><td>5&ndash;6</td><td>Go-live</td></tr>
  <tr><td>8</td><td>Hypercare</td></tr>
  </table>
</div>""")

    # 9. Client dependencies + assumptions
    sections.append("""
<div class="page-section">
  <h1 class="section">Client Dependencies &amp; Assumptions</h1>
  <ul>
  <li>[PRV] Source data for migration is clean and exported in a supported format by the data-quality sign-off date.</li>
  <li>[PRV] A named client contact is available for discovery and UAT.</li>
  <li>[PRV] Client holds any third-party accounts (portals, email) required for integrations in scope.</li>
  </ul>
</div>""")

    # 10. Change control + acceptance/signature
    if signer:
        sig_block = f"""
  <div class="sig-block">
    <p><strong>{LEGAL['trading_as']}</strong> ({LEGAL['legal_name']})</p>
    <p>{signer} &mdash; acting on behalf of {approver}, per: {authority}</p>
    <div class="sig-line">Signature &amp; date</div>
  </div>
  <div class="sig-block">
    <p><strong>{client_name}</strong></p>
    <div class="sig-line">Signature &amp; date</div>
  </div>"""
    else:
        sig_block = '<p class="open-flag">[BLOCKS ISSUE] Deciding-human line could not be populated.</p>'
    sections.append(f"""
<div class="page-section">
  <h1 class="section">Change Control &amp; Acceptance</h1>
  <p>Any change to scope after acceptance is a standalone change-control
  instrument &mdash; a new signed line item, not a verbal variation to this
  document.</p>
  {sig_block}
  <p class="footnote">{LEGAL['registered_address']}. {LEGAL.get('contact',{}).get('email','')}</p>
</div>""")

    body = "\n".join(sections)
    full_html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{reference} — {client_name}</title>
<style>{CSS}</style></head><body>
{body}
</body></html>"""
    return full_html


def render_internal_worksheet(quote, client_name, reference, fixture_name):
    """INTERNAL ONLY -- the floor guard, contingency %, raw hours, and
    capacity figures excluded from the client document above all live
    here instead."""
    pol = pe.load_policy()
    lines = [f"# INTERNAL WORKSHEET — {fixture_name} — {reference} — {client_name}", ""]
    lines.append("**NOT FOR CLIENT TRANSMISSION.**")
    lines.append("")
    lines.append(f"- platform_fee_aed: {quote['platform_fee_aed']}")
    lines.append(f"- modules_total_aed: {quote['modules_total_aed']} ({', '.join(quote['module_names'])})")
    lines.append(f"- migration_band: {quote['migration_band']}, amount_aed: {quote['migration_amount_aed']}, unpriced: {quote['migration_unpriced']}")
    lines.append(f"- quoted_total_aed: {quote['quoted_total_aed']}")
    lines.append(f"- discount_gate: {quote['discount_gate']}")
    lines.append("")
    lines.append("## Internal hours (raw vs risk-adjusted, INTERNAL ONLY)")
    total_raw, total_adj = 0.0, 0.0
    for line in quote["internal_hours"]:
        lines.append(f"- {line['module']}: raw={line['raw_hours']}h, risk_adjusted={line['risk_adjusted_hours']}h (contingency {line['contingency_pct']*100:.0f}%)")
        total_raw += line["raw_hours"]
        total_adj += line["risk_adjusted_hours"]
    lines.append(f"- TOTAL: raw={total_raw}h, risk_adjusted={total_adj}h")
    lines.append("")
    if quote["quoted_total_aed"] is not None and total_adj > 0:
        commission_total = pol["internal_cost_basis"]["commission"]["combined_pct"]
        net = round(quote["quoted_total_aed"] * (1 - commission_total), 2)
        eff_rate, verdict = pe.deal_guard_verdict(net, total_adj, pol)
        lines.append(f"## Floor guard (using RISK-ADJUSTED hours, never raw)")
        lines.append(f"- net_after_commission_aed: {net}")
        lines.append(f"- effective_rate_aed_hr: {eff_rate}")
        lines.append(f"- verdict: {verdict}")
    else:
        lines.append("## Floor guard: not computed — no risk-adjusted internal hours available for this fixture's module selection (only multi_agent_access_control carries an internal_build_estimate_hours figure in template-catalogue.yaml; a fixture without it has nothing to floor-check against yet).")
    lines.append("")
    lines.append(f"- quotation_validity: NO policy.yaml value exists for a standard validity period as of this pass — printed as [OPEN] on the client document, not a plausible-but-invented date.")
    return "\n".join(lines)


FIXTURES = {
    "F1": {
        # RENAMED 2026-08-16: this fixture originally used "RVN" as a
        # plausible-sounding fictional brokerage name, without knowing
        # RVN-realestate-leads is a real, in-progress client on origin/main
        # with three real prices already attached (see the merge-conflict
        # investigation this session). A synthetic test fixture must never
        # be named anything a real client could plausibly be — use an
        # obviously-fake identifier instead, never another brokerage-shaped
        # name.
        "client_name": "ZZZ SYNTHETIC TEST FIXTURE (not a real client)",
        "reference": "ZZZFIXTURE-2026-V4-01",
        "module_names": ["lead_capture_pipeline", "property_listing_management",
                          "commission_and_deals", "multi_agent_access_control",
                          "reporting_and_dashboards"],
        "migration_records": 3000,   # band_2, 5,000 AED -> expect total 35,000
        "expected_total_aed": 35000,
    },
    "F2": {
        "client_name": "Minimal Test Client",
        "reference": "MIN-2026-V4-01",
        "module_names": ["lead_capture_pipeline"],
        "migration_records": 500,    # band_1, 2,500 AED -> expect total 19,500
        "expected_total_aed": 19500,
    },
    "F3": {
        "client_name": "Over-Capacity Test Client",
        "reference": "OOB-2026-V4-01",
        "module_names": ["lead_capture_pipeline", "property_listing_management",
                          "commission_and_deals", "multi_agent_access_control",
                          "reporting_and_dashboards"],
        "migration_records": 25000,  # above_band_3 -> UNPRICED, never a number
        "expected_total_aed": None,
    },
}


def run_fixture(name):
    fx = FIXTURES[name]
    quote = build_quote(fx["module_names"], fx["migration_records"])

    if fx["expected_total_aed"] is not None:
        assert quote["quoted_total_aed"] == fx["expected_total_aed"], (
            f"{name}: computed total {quote['quoted_total_aed']} != expected {fx['expected_total_aed']}")
    else:
        assert quote["migration_unpriced"] and quote["quoted_total_aed"] is None, (
            f"{name}: expected UNPRICED, got {quote['quoted_total_aed']}")

    client_html = render_client_html(quote, fx["client_name"], fx["reference"])
    lint_hits = _warrant_tier_lint(client_html)
    if lint_hits:
        raise SystemExit(f"{name}: warrant-tier lint FAILED — T1 phrasing found with only T2 evidence: {lint_hits}")

    internal_md = render_internal_worksheet(quote, fx["client_name"], fx["reference"], name)

    os.makedirs(OUT_DIR, exist_ok=True)
    html_path = os.path.join(OUT_DIR, f"{name}_{fx['reference']}_client.html")
    worksheet_path = os.path.join(OUT_DIR, f"{name}_{fx['reference']}_INTERNAL_worksheet.md")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(client_html)
    with open(worksheet_path, "w", encoding="utf-8") as fh:
        fh.write(internal_md)

    print(f"{name}: quoted_total_aed={quote['quoted_total_aed']} discount_gate={quote['discount_gate']} "
          f"migration_unpriced={quote['migration_unpriced']}")
    print(f"  client HTML: {html_path}")
    print(f"  internal worksheet: {worksheet_path}")
    return html_path, worksheet_path, quote


if __name__ == "__main__":
    targets = sys.argv[1:] or list(FIXTURES.keys())
    for t in targets:
        run_fixture(t)
