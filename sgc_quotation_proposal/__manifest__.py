# -*- coding: utf-8 -*-
# SGC Quotation Proposal — pricing v4 QWeb report templates only, no models.
# STAGED, NOT INSTALLED. HANDOVER.md decision #18/#20. This module's
# content was ORIGINALLY a structural mirror of 05-ops/render_proposal_v4.py
# (same 10 sections, same field names, same content rules) -- see
# 00-intake/proposal-engine-v4-test-2026-08-16.md §6.3 for that original
# parity check.
#
# THAT PARITY IS NOW KNOWN STALE (2026-08-16, post-origin-merge renderer
# rebuild). reports/proposal_template.xml still reflects the PRE-rebuild
# schema: no recurring/platform_portion_aed_mo section, no 12/24/36-month
# horizons, doc.excluded_capabilities bound to a catalogue key that has
# never existed (renders an empty table), and a Scope & Acceptance table
# hardcoded to five fixed capability claims regardless of what was
# actually quoted -- the exact defect fixed in the Python generator on
# this date (known-defects.md #27). This module MUST NOT be installed
# until reports/proposal_template.xml is rebuilt to match
# RENDERER_SCHEMA_VERSION below.
#
# GUARD: 'installable' is False, not just documented as staged. Odoo's
# addon loader skips a module with installable=False outright -- a
# stronger guarantee than a hook or a comment, since there is no code
# path that can install this by accident. 05-ops/test_pricing_engine.py:
# check_qweb_schema_parity() additionally fails the standard test suite
# if this file is ever flipped back to installable=True without the pin
# below being updated to match 05-ops/render_proposal_v4.py's current
# RENDERER_SCHEMA_VERSION -- see that check for what "reconciled" means
# concretely. Flip installable back to True only after doing that work,
# not as part of unrelated cleanup.
#
# LAST RECONCILED AGAINST RENDERER SCHEMA VERSION: "v4.0-pre-recurring"
# (i.e. never reconciled against the current one, "v4.1-recurring" --
# see 05-ops/render_proposal_v4.py). This pin exists so the parity check
# has a concrete, machine-comparable target instead of relying on someone
# noticing the drift by reading prose.

{
    'name': 'SGC Quotation Proposal (Pricing v4)',
    'version': '19.0.1.0.0',
    'summary': 'Pricing v4 client-facing proposal report templates (QWeb) — report templates only, no models, no business logic.',
    'description': """
QWeb report templates mirroring 05-ops/render_proposal_v4.py's standalone
HTML generator: cover, understanding of requirement, capability summary,
scope + acceptance criteria, exclusions + alternatives, commercial
summary, payment terms, timeline, dependencies/assumptions, change
control + signature. All commercial figures are expected to be passed in
via the rendering context (docs) computed by 05-ops/pricing_engine.py --
this module defines NO models and computes NO prices itself; it is
presentation only.

STAGED 2026-08-16, NOT INSTALLABLE -- two independent reasons, either one
sufficient on its own: (1) the database freeze on sgc_staging (production
Postgres) forbids any -u/-i this session; (2) as of the same date this
module's QWeb template is a known schema mismatch against the
standalone generator it is supposed to mirror (see comment above
RENDERER_SCHEMA_VERSION_PINNED). Re-enable only after both are resolved.
""",
    'author': 'SGC TECH AI / Scholarix Global Consultants IFZA',
    'website': 'https://sgctech.ai',
    'license': 'LGPL-3',
    'category': 'Sales/CRM',
    'depends': ['base', 'web'],
    'data': [
        'reports/proposal_template.xml',
    ],
    'installable': False,  # see guard comment above -- do not flip without reconciling proposal_template.xml first
    'application': False,
    # Machine-readable pin read by check_qweb_schema_parity() in
    # 05-ops/test_pricing_engine.py -- update this alongside actually
    # reconciling reports/proposal_template.xml, not before.
    'RENDERER_SCHEMA_VERSION_PINNED': 'v4.0-pre-recurring',
}
