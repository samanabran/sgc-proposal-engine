#!/usr/bin/env python3
"""
Proposal-document generator -- standalone, offline, no Odoo/DB.

REBUILT 2026-08-16 after the origin/main merge (see HANDOVER.md, and the
capability-inventory discussion in this session's conversation). The
previous version of this file called a self-built, since-retired parallel
pricing engine (platform_fee_aed()/modules_subtotal_aed()/
discount_gate_verdict(), reading a template-catalogue.yaml schema that no
longer exists). Origin/main's implementation won that merge wholesale --
see 05-ops/pricing_engine.py: four_component_build(), business_cost_floor(),
hour_rate_floor_test(), platform_portion_aed_mo().

STRICT RULE, the reason this file was rebuilt rather than patched: THIS
FILE COMPUTES NO AED FIGURE OF ITS OWN, EVER. It calls
four_component_build(), platform_portion_aed_mo(), hour_rate_floor_test(),
risk_adjusted_hours() and prints what they return. The only arithmetic
performed directly in this file is PRESENTATIONAL aggregation of
already-computed figures (e.g. recurring_aed_mo * 12 for a horizon total)
-- never a floor, a rate, or a commission calculation. If a commercial
figure appears in a rendered document that does not trace to a specific
pe.* function call, that is a defect in this file, not a acceptable
shortcut. Two vocabularies for the same number is exactly how this
session's merge conflict happened in the first place.

Design spec (Prosper's real conventions), unchanged from the prior
version -- see 02-clients/PRO-prosper-realestate/04-draft/render_brand.py,
06-brand/tokens/color.yaml, 06-brand/entity/legal-identity.yaml. Two
disclosed deviations also unchanged: no watermark rotation wired
(disproportionate to this pass); VAT/registration status always printed
on the commercial-summary page (supersedes AGENTS.md's older conditional
rule for v4 documents specifically).

RECURRING MODEL, new in this rebuild: a real deal (see
02-clients/RVN-realestate-leads/) carries a recurring subscription fee
(platform_portion_aed_mo, computed by pricing_engine.py:
platform_portion_aed_mo() from users_now -- the SAME formula every
client worksheet in this repo has hand-computed since before pricing v4
existed) alongside any one-time four-component build. This renderer
prints BOTH: a one-time section and a recurring section, with horizon
totals at 12/24/36 months, each labelled separately -- NO cross-horizon
comparison, per the explicit instruction that produced this rebuild
(a "which term is the better deal" framing has already been a defect in
this repo once, see known-defects.md #16).

SECTIONS NEVER DISAPPEAR: this generator enforces a hard 10-page budget
by reflowing content across pages, never by dropping a required section
because it has little content. A minimal deal must still show all ten
sections -- assert_required_sections() below is the actual gate, run on
every fixture, not a styling convention. Exclusions, change control, and
acceptance are exactly the sections a small deal would be tempted to
compress away, and they are the three sections that protect the seller
in a dispute.

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

REQUIRED_SECTIONS = [
    "cover", "understanding", "capability", "scope", "exclusions",
    "commercial-summary", "payment-terms", "timeline", "dependencies",
    "change-control",
]


class BlocksIssue(Exception):
    """Raised when a required field cannot be resolved -- the document
    must render as [BLOCKS ISSUE] and the generator must exit non-zero,
    never guess a plausible value."""


def _deciding_human():
    contact = LEGAL.get("contact", {})
    signer = contact.get("actual_signer")
    if not signer:
        raise BlocksIssue("legal-identity.yaml: contact.actual_signer is empty")
    return signer, contact.get("named_approver"), contact.get("signer_authority")


def _warrant_tier_lint(html_text):
    """Refuse to print a T1 ("proven in production") phrasing anywhere in
    this generator's output -- every capability priced here is T2
    (deploys from repository, real client evidence, not yet re-verified
    on a clean install)."""
    t1_phrases = [r"\bproven in production\b", r"\bproduction[- ]proven\b", r"\balready proven\b"]
    hits = []
    for pat in t1_phrases:
        for m in re.finditer(pat, html_text, re.IGNORECASE):
            hits.append((pat, html_text[max(0, m.start() - 40):m.end() + 40]))
    return hits


def assert_required_sections(html_text, section_ids=REQUIRED_SECTIONS):
    """THE section-presence gate, not a convention. Every fixture, at any
    page count, must carry all ten <div id="section-..."> markers below --
    a page-count fix that drops a section instead of reflowing it is the
    defect this function exists to catch. Raises AssertionError (loud,
    not a silent False) naming exactly which section is missing."""
    missing = [s for s in section_ids if f'id="section-{s}"' not in html_text]
    if missing:
        raise AssertionError(f"Required section(s) missing from rendered output: {missing}")
    return True


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
  font-size: 14.5px;
  line-height: 1.65;
  color: var(--charcoal);
  background: var(--ivory);
  margin: 0;
  padding: 0;
}

.page-section { max-width: 170mm; margin: 0 auto; padding: 6mm 0; }
.page-break { page-break-after: always; }

.masthead { margin-bottom: 10mm; }
.masthead .prepared-for { font-family: "Inter", sans-serif; font-size: 13px; color: var(--slate); }
.masthead .reference { font-family: "Inter", sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gold); }

h1.cover-title, h1.section {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  color: var(--navy);
  letter-spacing: -0.5px;
  margin-top: 0;
  margin-bottom: 3mm;
  border-bottom: 1.5px solid var(--gold);
  padding-bottom: 2mm;
}
h1.cover-title { font-size: 32px; }
h1.section { font-size: 22px; }

h2.subsection { font-family: "Inter", sans-serif; font-size: 15px; font-weight: 600; color: var(--gold); margin-top: 4mm; margin-bottom: 2mm; }
h3 { font-family: "Inter", sans-serif; font-size: 13px; font-weight: 600; color: var(--navy); }

p { margin: 0 0 0.7em 0; }
strong { color: var(--navy); }

table { border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 12.5px; }
th {
  background: var(--navy); color: var(--ivory);
  font-family: "Inter", sans-serif; font-size: 10px; text-transform: uppercase;
  letter-spacing: 0.04em; text-align: left; padding: 4px 8px;
}
td { border: 1px solid var(--champagne); padding: 4px 8px; }

blockquote {
  font-family: "Inter", sans-serif; font-style: italic;
  border-left: 3px solid var(--gold); background: var(--parchment);
  margin: 3mm 0; padding: 3mm 4mm; color: var(--navy);
}

hr { border: none; border-top: 1px solid var(--champagne); margin: 4mm 0; }

.caption, .footnote {
  font-family: "Inter", sans-serif; font-size: 10px; text-transform: uppercase;
  letter-spacing: 0.04em; color: var(--slate);
}

.open-flag { color: #A24949; font-weight: 700; }  /* wine -- status signalling only, per palette usage_notes */
.horizon-block { border: 1px solid var(--champagne); padding: 3mm 4mm; margin: 2mm 0; display: inline-block; width: 30%; vertical-align: top; margin-right: 1.5%; }

ul, ol { padding-left: 1.2em; }
li { margin-bottom: 0.3em; }

.sig-block { margin-top: 6mm; }
.sig-line { border-top: 1px solid var(--charcoal); width: 70mm; margin-top: 8mm; padding-top: 2mm; font-size: 11px; }
"""


def build_quote(module_names, maturity, migration_band, users_now, enhancement_hours=0.0, policy=None):
    """Every commercial figure computed here traces to a pe.* function
    call -- see the module docstring's strict-consumer rule. Returns the
    raw dicts from each function, undecorated, so the render functions
    below can quote them directly rather than re-deriving anything."""
    cat = pe.load_template_catalogue()
    pol = policy or pe.load_policy()
    basis = pe.business_cost_floor()

    one_time = pe.four_component_build(
        modules_selected=module_names, maturity=maturity, migration_band=migration_band,
        enhancement_hours=enhancement_hours, catalogue=cat, cost_basis=basis,
    )
    recurring = pe.platform_portion_aed_mo(users_now, pol)

    floor_test = None
    if not one_time["migration"]["unpriced"]:
        floor_test = pe.hour_rate_floor_test(
            price_ex_vat_aed=one_time["price_ex_vat_aed"], hours_total=one_time["hours_total"], cost_basis=basis,
        )

    # PRESENTATIONAL aggregation only (horizon totals) -- not a pricing
    # decision, just multiplying two already-computed figures by a month
    # count. See module docstring.
    recurring_aed_mo = recurring["platform_portion_aed_mo"]
    horizons = {}
    if not one_time["migration"]["unpriced"]:
        for months in (12, 24, 36):
            horizons[months] = {
                "months": months,
                "one_time_aed": one_time["price_ex_vat_aed"],
                "recurring_total_aed": round(recurring_aed_mo * months, 2),
                "total_aed": round(one_time["price_ex_vat_aed"] + recurring_aed_mo * months, 2),
            }

    return {
        "one_time": one_time,
        "recurring": recurring,
        "floor_test": floor_test,
        "horizons": horizons,
        "unpriced": one_time["migration"]["unpriced"],
        "excluded_capabilities": cat.get("excluded_capabilities", {}),
        "enhancement_rate_aed_hr": cat["enhancement"]["default_rate_aed_hr"],
    }


def render_client_html(quote, client_name, reference):
    """Client-facing document. Content rules enforced by construction:
    this function receives already-computed dicts from build_quote() and
    only formats/labels them -- it performs no pe.* calls and no pricing
    arithmetic itself."""
    signer, approver, authority = _deciding_human()
    vat_registered = LEGAL["vat_registered"]
    trn = LEGAL.get("trn")
    today = datetime.date(2026, 8, 16)
    ot = quote["one_time"]

    sections = []

    sections.append(f"""
<div id="section-cover" class="page-section page-break">
  <div class="masthead">
    <div class="prepared-for">Prepared for {client_name}</div>
    <div class="reference">Reference: {reference}</div>
  </div>
  <h1 class="cover-title">{LEGAL['trading_as']}</h1>
  <p style="font-family:'Playfair Display',serif;font-size:18px;color:var(--navy);">Real Estate Growth Platform &mdash; Proposal</p>
  <p class="caption">{today.strftime('%d %B %Y')}</p>
</div>""")

    sections.append("""
<div id="section-understanding" class="page-section">
  <h1 class="section">Understanding Your Requirement</h1>
  <p>This proposal separates what you pay once (platform template, selected
  modules, data migration, any bespoke enhancement) from what you pay
  every month (the platform's ongoing hosting, support, and account
  management, sized to your team). Every figure on the following pages
  traces to a single governed calculation &mdash; nothing here is a
  placeholder or a hand-typed number.</p>
</div>""")

    module_rows = "".join(
        f"<tr><td>{m['name'].replace('_',' ').title()}</td><td>AED {_fmt_aed(m['price_aed'])}</td></tr>"
        for m in ot["modules"]["rows"]
    )
    sections.append(f"""
<div id="section-capability" class="page-section">
  <h1 class="section">What This Delivers</h1>
  <table><tr><th>Capability</th><th>One-Time Price</th></tr>
  <tr><td>Platform template</td><td>AED {_fmt_aed(ot['template']['price_aed'])}</td></tr>
  {module_rows}
  </table>
  <p class="caption">Odoo 19 Community &mdash; version lock. A different Odoo version is a separate engagement.</p>
</div>""")

    sections.append("""
<div id="section-scope" class="page-section">
  <h1 class="section">Scope &amp; Acceptance</h1>
  <table><tr><th>Requirement</th><th>Acceptance Criterion</th></tr>
  <tr><td>Lead capture</td><td>Inbound lead creates a CRM record within the platform, visible to an assigned user.</td></tr>
  <tr><td>Property/listing management</td><td>A property record can be created, listed, and its status updated by an authorised user.</td></tr>
  <tr><td>Commission &amp; deals</td><td>A closed deal computes commission per the configured scheme and is visible on the deal record.</td></tr>
  <tr><td>Multi-agent access control</td><td>Agent A cannot view Agent B's commission or deal records; record-rule enforced, not UI-hidden only.</td></tr>
  <tr><td>Reporting &amp; dashboards</td><td>Configured reports return live data from the modules above.</td></tr>
  </table>
</div>""")

    excl_rows = ""
    for key, row in quote["excluded_capabilities"].items():
        name = key.replace("_", " ").title()
        excl_rows += f"<tr><td>{name}</td><td>Not included</td><td>{row.get('alternative_offered','See scoping call.')}</td></tr>"
    sections.append(f"""
<div id="section-exclusions" class="page-section">
  <h1 class="section">What Is Not Included &mdash; Named Directly</h1>
  <p>Not "coming soon," not bundled under a different name. Each has a stated alternative.</p>
  <table><tr><th>Capability</th><th>Status</th><th>Alternative Offered</th></tr>
  {excl_rows}
  </table>
</div>""")

    vat_line = ("VAT: not currently registered &mdash; no VAT charged"
                if vat_registered is False else
                f"VAT: registered, TRN {trn}, 5% exclusive of the totals below" if vat_registered else "[OPEN]")

    if quote["unpriced"]:
        commercial_body = f"""
  <table>
  <tr><td>Platform template</td><td>AED {_fmt_aed(ot['template']['price_aed'])}</td></tr>
  <tr><td>Modules ({len(ot['modules']['rows'])})</td><td>AED {_fmt_aed(ot['modules']['price_aed'])}</td></tr>
  <tr><td>Migration</td><td class="open-flag">UNPRICED &mdash; routed to Commercial Desk</td></tr>
  <tr><td><strong>One-time total</strong></td><td class="open-flag"><strong>[OPEN &mdash; migration UNPRICED]</strong></td></tr>
  </table>
  <p>Recurring platform fee (once migration is priced and scope is confirmed): AED {_fmt_aed(quote['recurring']['platform_portion_aed_mo'])}/month.</p>"""
    else:
        horizon_blocks = ""
        for months in (12, 24, 36):
            h = quote["horizons"][months]
            horizon_blocks += f"""<div class="horizon-block">
  <h3>{months}-month horizon</h3>
  <p>One-time: AED {_fmt_aed(h['one_time_aed'])}<br/>
  Recurring ({months} &times; AED {_fmt_aed(quote['recurring']['platform_portion_aed_mo'])}/mo): AED {_fmt_aed(h['recurring_total_aed'])}<br/>
  <strong>Total: AED {_fmt_aed(h['total_aed'])}</strong></p>
  </div>"""
        commercial_body = f"""
  <h2 class="subsection">One-time (due at kickoff)</h2>
  <table>
  <tr><td>Platform template</td><td>AED {_fmt_aed(ot['template']['price_aed'])}</td></tr>
  <tr><td>Modules ({len(ot['modules']['rows'])})</td><td>AED {_fmt_aed(ot['modules']['price_aed'])}</td></tr>
  <tr><td>Migration ({ot['migration']['band']})</td><td>AED {_fmt_aed(ot['migration']['price_aed'])}</td></tr>
  <tr><td><strong>One-time total</strong></td><td><strong>AED {_fmt_aed(ot['price_ex_vat_aed'])}</strong></td></tr>
  </table>
  <h2 class="subsection">Recurring (monthly, ongoing)</h2>
  <p>Platform hosting, support, and account management, sized to your team: <strong>AED {_fmt_aed(quote['recurring']['platform_portion_aed_mo'])}/month</strong>.</p>
  <h2 class="subsection">Commitment horizons &mdash; each stated independently, not a comparison</h2>
  {horizon_blocks}
  <p class="caption">Security deposit (refundable instrument, not a fee): one month's recurring fee, AED {_fmt_aed(quote['recurring']['platform_portion_aed_mo'])}, held per the term selected and returned per the governing agreement &mdash; not itself part of any horizon total above.</p>"""

    sections.append(f"""
<div id="section-commercial-summary" class="page-section">
  <h1 class="section">Commercial Summary</h1>
  {commercial_body}
  <p class="caption">All figures AED, exclusive of VAT (5% standard rate where applicable). {vat_line}.</p>
  <p class="caption">Enhancement hours (out-of-scope requests beyond the above): AED {quote['enhancement_rate_aed_hr']}/hr, quoted per request &mdash; not a basis for pricing a whole deal.</p>
  <p class="caption">Quotation validity: [OPEN &mdash; no policy.yaml value exists for a standard validity period; see internal worksheet.]</p>
</div>""")

    sections.append("""
<div id="section-payment-terms" class="page-section">
  <h1 class="section">Payment Terms</h1>
  <p>One-time total due at kickoff. Recurring fee billed monthly in advance
  from the go-live date. Enhancement hours invoiced per completed request.</p>
</div>""")

    sections.append("""
<div id="section-timeline" class="page-section">
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

    sections.append("""
<div id="section-dependencies" class="page-section">
  <h1 class="section">Client Dependencies &amp; Assumptions</h1>
  <ul>
  <li>[PRV] Source data for migration is clean and exported in a supported format by the data-quality sign-off date.</li>
  <li>[PRV] A named client contact is available for discovery and UAT.</li>
  <li>[PRV] Client holds any third-party accounts required for integrations in scope.</li>
  </ul>
</div>""")

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
<div id="section-change-control" class="page-section">
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


def render_internal_worksheet(quote, client_name, reference, fixture_name, module_names):
    """INTERNAL ONLY -- the floor guard, gross break-even metric,
    contingency-adjusted hours all live here, never on the client
    document above."""
    pol = pe.load_policy()
    ot = quote["one_time"]
    lines = [f"# INTERNAL WORKSHEET — {fixture_name} — {reference} — {client_name}", ""]
    lines.append("**NOT FOR CLIENT TRANSMISSION.**")
    lines.append("")
    lines.append("## One-time build (pe.four_component_build())")
    lines.append(f"- template: {ot['template']}")
    lines.append(f"- modules: {ot['modules']}")
    lines.append(f"- migration: {ot['migration']}")
    lines.append(f"- price_ex_vat_aed: {ot['price_ex_vat_aed']}, hours_total: {ot['hours_total']}")
    lines.append("")
    lines.append("## Recurring (pe.platform_portion_aed_mo())")
    lines.append(f"{quote['recurring']}")
    lines.append("")
    if quote["floor_test"]:
        ft = quote["floor_test"]
        lines.append("## Quote-time floor test (pe.hour_rate_floor_test())")
        for k, v in ft.items():
            lines.append(f"- {k}: {v}")
        lines.append(f"- NOTE: gross_break_even_aed_hr ({ft['gross_break_even_aed_hr']}) is a REPORTED METRIC, "
                      f"not a threshold -- a quote billed at exactly that gross rate earns zero cushion. "
                      f"The verdict above (BLOCK/WARN/PASS) is the actual gate.")
    else:
        lines.append("## Quote-time floor test: not computed -- migration UNPRICED, no total to test.")
    lines.append("")
    lines.append("## Risk-adjusted hours (contingency schedule, policy.yaml -- local-only addition, survives merge unmodified)")
    cat = pe.load_template_catalogue()
    for m in module_names:
        mod = cat["modules"][m]
        raw_h = mod.get("hours", 0)
        # Modules ported from this repo's own git history are git-tracked-
        # and-deployed-before by construction; multi_agent_access_control
        # explicitly is (see its own catalogue comment) -- others are
        # origin's own catalogue rows, same category by default absent
        # evidence otherwise.
        try:
            _, adjusted, pct = pe.risk_adjusted_hours(raw_h, "git_tracked_deployed_before", pol)
            lines.append(f"- {m}: raw={raw_h}h, risk_adjusted={adjusted}h (contingency {pct*100:.0f}%)")
        except KeyError:
            lines.append(f"- {m}: raw={raw_h}h (contingency_schedule not available -- policy.yaml may not carry it in this context)")
    lines.append("")
    lines.append("- quotation_validity: NO policy.yaml value exists for a standard validity period as of this pass — printed as [OPEN] on the client document, not a plausible-but-invented date.")
    return "\n".join(lines)


FIXTURES = {
    "F1": {
        "client_name": "ZZZ SYNTHETIC TEST FIXTURE (not a real client)",
        "reference": "ZZZFIXTURE-2026-V4-01",
        "module_names": pe.RVN_MATURE_MODULES + ["multi_agent_access_control", "property_portal_feed"],
        "maturity": "mature",
        "migration_band": "from_1000_to_5000",
        "users_now": 25,
    },
    "F2": {
        "client_name": "ZZZ MINIMAL SYNTHETIC FIXTURE (not a real client)",
        "reference": "ZZZFIXTURE-2026-V4-02",
        "module_names": ["lead_capture_meta_google_ads"],
        "maturity": "first_build",
        "migration_band": "up_to_1000",
        "users_now": 5,
    },
    "F3": {
        "client_name": "ZZZ OVER-CAPACITY SYNTHETIC FIXTURE (not a real client)",
        "reference": "ZZZFIXTURE-2026-V4-03",
        "module_names": pe.RVN_MATURE_MODULES + ["multi_agent_access_control", "property_portal_feed"],
        "maturity": "mature",
        "migration_band": "over_20000",
        "users_now": 25,
    },
}


def run_fixture(name):
    fx = FIXTURES[name]
    quote = build_quote(
        module_names=fx["module_names"], maturity=fx["maturity"],
        migration_band=fx["migration_band"], users_now=fx["users_now"],
    )

    client_html = render_client_html(quote, fx["client_name"], fx["reference"])

    lint_hits = _warrant_tier_lint(client_html)
    if lint_hits:
        raise SystemExit(f"{name}: warrant-tier lint FAILED: {lint_hits}")

    assert_required_sections(client_html)  # raises loudly if any of the 10 sections is missing

    internal_md = render_internal_worksheet(quote, fx["client_name"], fx["reference"], name, fx["module_names"])

    os.makedirs(OUT_DIR, exist_ok=True)
    html_path = os.path.join(OUT_DIR, f"{name}_{fx['reference']}_client.html")
    worksheet_path = os.path.join(OUT_DIR, f"{name}_{fx['reference']}_INTERNAL_worksheet.md")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(client_html)
    with open(worksheet_path, "w", encoding="utf-8") as fh:
        fh.write(internal_md)

    if quote["unpriced"]:
        print(f"{name}: UNPRICED (migration band {fx['migration_band']}) -- routed to Commercial Desk")
    else:
        h24 = quote["horizons"][24]
        verdict = quote["floor_test"]["verdict"] if quote["floor_test"] else None
        print(f"{name}: one_time={quote['one_time']['price_ex_vat_aed']} "
              f"recurring_mo={quote['recurring']['platform_portion_aed_mo']} "
              f"24mo_total={h24['total_aed']} floor_verdict={verdict}")
    print(f"  client HTML: {html_path}")
    print(f"  internal worksheet: {worksheet_path}")
    return html_path, worksheet_path, quote


if __name__ == "__main__":
    targets = sys.argv[1:] or list(FIXTURES.keys())
    for t in targets:
        run_fixture(t)
